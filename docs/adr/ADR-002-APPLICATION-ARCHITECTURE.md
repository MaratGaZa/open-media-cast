# ADR-002: переносимое ядро и адаптеры

Статус: **Proposed** · 2026-10-18. Требуется экспериментальная проверка перед принятием.

## Предлагаемое решение

Ведущий кандидат: Rust/Tokio для orchestration, Tauri 2 + TypeScript/Svelte для оболочки; платформенные интеграции Android — Kotlin, Apple API — тонкий Swift/Objective-C слой при необходимости. Python нужен сначала для протокольных экспериментов. Его поставка в готовом desktop-приложении — отдельное решение, а не скрытая постоянная зависимость.

Альтернативы: Flutter/Dart + Rust, Python/PySide6, SwiftUI + Rust. Выбор интерфейса не заменяет решение о реализации AirPlay, Cast и DLNA. Универсальная рабочая Rust-библиотека для всех нужных вариантов AirPlay пока не установлена.

## Три независимые оси

1. **Продукт:** очередь, состояния сессии, отмена, retry policy, выбор способа подготовки медиа.
2. **Протокол:** AirPlay legacy, AirPlay 2, Google Cast, DLNA. Это возможности приёмника, а не ОС отправителя. Начать с legacy-видео Apple TV 3; современное pairing/control квалифицировать отдельно.
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
  crates/receivers/      # airplay_legacy/cast/dlna; airplay2 reserved, not scaffolded
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

Основная гипотеза E06: HLS с совместимыми H.264/AAC-сегментами для Apple TV 3/Cast, законченный файл для DLNA. Сравнить растущий EVENT, заранее подготовленный VOD и полный VOD-плейлист с генерацией сегментов по запросу. Последний вариант — отдельная гипотеза E06 на Apple TV 3: URI должен своевременно возвращать корректный сегмент, а не 404 или бесконечное ожидание. Само отсутствие готового файла на диске не исключает генерацию HTTP-ответа по запросу. Проверить холодный seek вперёд/назад, стабильность нумерации и временных меток, параллельные запросы, время генерации против timeout приёмника и ограничение ресурсов. Работоспособность этого варианта на нашем устройстве пока не установлена. [RFC 8216 §6.2.1](https://datatracker.ietf.org/doc/html/rfc8216#section-6.2.1).

DLNA progressive MPEG-TS с перезапуском encoder от позиции — запасная экспериментальная стратегия, не свойство DLNA Seek. Контракт допускает `native seek`, `prepare/reload at offset` и `unsupported`; общий UI показывает абсолютную позицию, а новое поколение подготовки отбрасывает старые события. Для законченного файла не нужен перезапуск FFmpeg при каждом seek.

HTTP-слой получает DLNA-профиль от адаптера: contentFeatures/transferMode и DIDL-Lite protocolInfo должны совпадать. `DLNA.ORG_OP=01` заявляет byte seek, `10` — time seek, `11` — оба; выставлять только реализованные операции. Flags/PN/CI зависят от ресурса и профиля, не копируются одной константой на все ответы. Начать с polling transport/position; GENA callback и дополнительный listener вводить только при реальной необходимости. [Реализация DLNA-профиля](https://github.com/StevenLooman/async_upnp_client/blob/master/async_upnp_client/profiles/dlna.py).

Собранный macOS .app: NSLocalNetworkUsageDescription, перечень используемых NSBonjourServices, диагностика отказа Local Network и отдельная проверка Application Firewall. Список служб выводится из используемого адаптера; RAOP не включается автоматически ради video-only. CLI из Terminal и .app имеют разные условия доступа. [Apple TN3179](https://developer.apple.com/documentation/technotes/tn3179-understanding-local-network-privacy).

HTTP-сервер доступен выбранному приёмнику по LAN, поэтому loopback-only bind не подходит. Выбранный интерфейс, непредсказуемый session URL и сроки доступа ограничивают выдачу файла. Это не обеспечивает шифрование старого DLNA/HTTP; модель доверия — согласованная домашняя сеть. Никакой публичной раздачи через UPnP port mapping.

## Условия принятия

Три протокольных отчёта (или явно признанный blocker недоступного устройства), проверка AirPlay auth/control, выбор стратегии Python/Rust, media-delivery эксперимент, минимальная оценка Android integration, лицензионный перечень. При отсутствии реального Cast результат исследования может быть принят частично, но Cast-поддержка приложения остаётся unverified.

Лицензирование и происхождение FFmpeg решаются в D2: кандидат для Mac — сборка без GPL-компонентов с VideoToolbox; использование этого encoder само по себе не меняет лицензию уже GPL-enabled бинарника. На Fedora проверить фактические encoders и доступность backend; выбор дополнительного репозитория или поставки собственного binary оформить до упаковки.

Откат: сохранить prototyping results и контрактные тесты, поменять UI/adapter за интерфейсом; не переписывать подтверждённые требования под удобства случайной библиотеки.
