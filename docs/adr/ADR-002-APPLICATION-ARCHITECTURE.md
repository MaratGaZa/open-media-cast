# ADR-002: переносимое ядро и адаптеры

Статус: **Proposed** · 2026-10-18. Требуется экспериментальная проверка перед принятием.

## Предлагаемое решение

Ведущий кандидат: Rust/Tokio для orchestration, Tauri 2 + TypeScript/Svelte для оболочки; платформенные интеграции Android — Kotlin, Apple API — тонкий Swift/Objective-C слой при необходимости. Python нужен сначала для протокольных экспериментов. Его поставка в готовом desktop-приложении — отдельное решение, а не скрытая постоянная зависимость.

Альтернативы: Flutter/Dart + Rust, Python/PySide6, SwiftUI + Rust. Выбор интерфейса не заменяет решение о реализации AirPlay, Cast и DLNA. Универсальная рабочая Rust-библиотека для всех нужных вариантов AirPlay пока не установлена.

## Три независимые оси

1. **Продукт:** очередь, состояния сессии, отмена, retry policy, выбор способа подготовки медиа.
2. **Протокол:** AirPlay, Google Cast, DLNA. Это тип приёмника, а не ОС отправителя.
3. **Платформа:** файлы и разрешения, discovery API, защищённое хранилище, кодеки, background lifecycle, packaging.

Например, `plan_media(source, receiverCapabilities)` — общая логика. `prepare_media(plan)` выбирает platform backend. AirPlay-адаптер формирует команды для приёмника. UI не запускает произвольные shell-строки и не владеет токенами pairing.

## Предлагаемая карта исходников — пока не создана

```text
project/
  apps/desktop/          # Tauri UI + thin host, если Tauri принят
  apps/android/          # Android host/integration, UI-reuse уточняется spike
  crates/core/           # session, queue, domain errors, media planning
  crates/media/          # probe, preparation jobs, bounded cache
  crates/media-http/     # selected-file delivery
  crates/receivers/      # initially modules airplay/cast/dlna, split when useful
  crates/platform/       # platform adapter contracts and implementations
  tools/protocol-lab/    # Python comparison experiments
  tests/fixtures/        # synthetic media descriptors and sanitized protocols
```

Это предложение для отдельного согласования каталогов после выбора стека. Не создавать пустые crates ради диаграммы. Если одна библиотека с модулями проще для первой итерации, сохранить эти границы внутри неё. Android-host должен проверять жизнеспособность общего core до окончательной фиксации ABI; production Android делается четвёртой платформой.

## Контракты

- `ReceiverAdapter`: discover, pair (если нужно), capabilities, load, play/pause/seek/stop, события.
- `MediaBackend`: probe, prepare, progress, cancel, cleanup. Указание поддержки codec не равно успешному runtime encode.
- `FileAccess`: пользовательский выбор, чтение/seek потока; Android URI не превращается автоматически в обычный путь.
- `CredentialStore`: хранение и удаление pairing-данных.
- `SessionController`: согласует UI-команды, медиа и приёмник; игнорирует события старой сессии после смены receiver.

Каждая команда имеет request/session ID, timeout и результат. Capabilities допускают supported/unsupported/unknown. Недоступные операции объясняются пользователю. Статус UI учитывает наблюдения приёмника; отправка команды не считается подтверждением её выполнения.

## Media delivery

FFmpeg/ffprobe на desktop — отдельный контролируемый процесс с массивом аргументов, без shell и без пользовательских дополнительных опций. Его stderr очищается, cancel завершает дерево процессов. Сначала поддержать законченный MP4 с Range. Для streaming transcode отдельно проверить контейнер/seek/доступность будущих фрагментов. На Android сравнить Media3/MediaCodec и сборку native media library; desktop sidecar не считать переносимым по умолчанию.

HTTP-сервер доступен выбранному приёмнику по LAN, поэтому loopback-only bind не подходит. Выбранный интерфейс, непредсказуемый session URL и сроки доступа ограничивают выдачу файла. Это не обеспечивает шифрование старого DLNA/HTTP; модель доверия — согласованная домашняя сеть. Никакой публичной раздачи через UPnP port mapping.

## Условия принятия

Три протокольных отчёта (или явно признанный blocker недоступного устройства), проверка AirPlay auth/control, выбор стратегии Python/Rust, media-delivery эксперимент, минимальная оценка Android integration, лицензионный перечень. При отсутствии реального Cast результат исследования может быть принят частично, но Cast-поддержка приложения остаётся unverified.

Откат: сохранить prototyping results и контрактные тесты, поменять UI/adapter за интерфейсом; не переписывать подтверждённые требования под удобства случайной библиотеки.
