# Стратегия проверок и evidence

Draft 0.1 · 2026-10-18. Все продуктовые tests ниже запланированы, но не реализованы и не выполнены.

## Уровни

E0 — источник/гипотеза; E1 — unit/contract с контролируемыми данными; E2 — интеграция процессов/HTTP на host; E3 — реальный receiver; E4 — готовый пакет в целевой среде. Уровни не заменяют друг друга: E4 без receiver run не доказывает E3. `supported` требует указанного сценария/версии/устройства, не общей метки технологии.

Статусы: planned, running, passed, failed, blocked, unverified, not-applicable. `blocked` указывает конкретную недоступную предпосылку. Неизвестное не становится passed после повторения формулировки в README.

## Набор проверок

| ID | Сценарий | Содержательный oracle | Уровень |
|---|---|---|---|
| TEST-MEDIA-01 | Probe/выбор источника | Синтетические файлы с заранее известными потоками; cancel выбора, unreadable/corrupt file, Unicode path | E1/E2 |
| TEST-MEDIA-02 | Media planning | Совместимый profile → direct; несовместимый audio → audio transcode; неподдержанный codec → контролируемый план/отказ; реальный output перепроверен probe | E1/E2 |
| TEST-MEDIA-03 | Subtitles/tracks/seek | Видимый текст/правильный язык на RX, синхронность после seek, cleanup burn-in job; fixture с видимыми time markers | E2/E3 |
| TEST-HTTP-01 | Законченный файл | HEAD/GET, первый/последний/suffix range, 206/416, корректные длины и байты, досрочное закрытие клиента | E2 |
| TEST-HTTP-02 | Изоляция URL | Чужой/просроченный token, traversal/encoded traversal, другой путь и session mismatch не раскрывают файл; revoke завершает доступ | E1/E2 |
| TEST-RX-01 | Apple TV 3 | Discovery, auth, first frame+audio, pause/resume/seek/stop, повторное подключение; фактическое наблюдение | E3 |
| TEST-RX-02 | Google Cast | Реальный video receiver, load/status/control, доступ к LAN URL, error/cancel | E3 |
| TEST-RX-03 | Sony DLNA | Реальный DMR/services, URI/play/pause/seek/stop, отдельный результат каждого действия | E3 |
| TEST-SESSION-01 | Race/cancel | Событие старого session ID не меняет новый; cancel во время probe/prepare/connect; bounded retry | E1/E2 |
| TEST-SESSION-02 | Recovery/resources | Потеря сети, sleep/wake, receiver restart, disk-full, app restart; нет оставшихся owned process/socket/cache вне политики | E2/E3 |
| TEST-SEC-01 | Диагностика/границы | Синтетические секреты и пути отсутствуют в обычных логах, args не интерпретируются shell, нет выдачи произвольного файла | E1/E2 |
| TEST-PKG-01 | Установка | Готовый artifact на чистой целевой ОС без dev tools, архитектура, запуск и удаление | E4 |
| TEST-UI-01 | Управление UI | Keyboard/touch, доступные подписи, состояния pending/error, повторные команды не создают дубликаты | E1/E3 |
| TEST-PORT-01 | Порт | Все обязательные сценарии на данной ОС плюс специфичные permissions/lifecycle/backend | E2/E3/E4 |

## Media corpus

Создать небольшой набор синтетических клипов с цветом, временем кадра и test tone. Начальный baseline: 720p H.264/AAC. Затем менять одну характеристику: container, audio codec, video codec/pixel format, fps, subtitles. Для каждого сохранить checksum, способ генерации, tool versions и ffprobe-описание. Реальные фильмы/персональные файлы не нужны в Git.

Перекодированный результат должен иметь ожидаемые параметры и воспроизводиться на receiver. Успешный exit FFmpeg не доказывает ни качество, ни синхронность. Для визуального наблюдения использовать marker на изображении и слышимый сигнал в известные моменты.

## Hardware evidence

Указывать source SHA либо точный experimental snapshot, build checksum, toolchain, OS, устройство/прошивку, fixture, сеть без реальных адресов, режим auth, start/stop timestamps и результаты. Пользователь может подтвердить изображение/звук; агент не должен объявлять их увиденными, если доступна только телеметрия.

Минимальные ожидания v1 берутся из [SPEC](../specs/PRODUCT_SPEC.md). Если обязательный seek не работает, профиль не квалифицирован полностью: изменить реализацию или получить решение по scope. Сообщить в UI `unsupported` полезно, но это не закрывает обязательную функцию.

## Документация и skills

Проверки initial package: существование локальных ссылок, согласованность REQ/TEST IDs, два Git root, отсутствие source в внешнем индексе, schema/frontmatter skills, отсутствие ложных completed claims. Не создавать unit-тесты, которые лишь ищут заголовки документа или повторяют его текст. Независимая поведенческая проверка skills остаётся отдельным возможным этапом.
