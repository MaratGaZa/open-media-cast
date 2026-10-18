# Очередь execution tasks

Draft 0.1 · 2026-10-18. Сейчас разрешена подготовка документации. Реализация не начата. [SDD runbook](../runbooks/SDD_AND_AGENTS.md) задаёт порядок выполнения.

Перед стартом дополнить карточку target, версиями и scope поручения. E00.5 — исследовательский smoke готовыми утилитами: он не требует принятия всей SPEC или выбора стека. Для реализации последующих задач нужна принятая часть SPEC. Локальные task IDs достаточны без GitHub issues.

| ID | Задача и зависимости | Критерий завершения / проверки | Риск и stop condition |
|---|---|---|---|
| E00 | Принять baseline документов; сейчас | Владелец определил scope, требования, первый исследовательский этап; спорные пункты записаны | Нельзя принять стек по умолчанию только из-за наличия Draft |
| E00.5 | Короткий smoke Apple TV 3 и Sony готовыми утилитами; до E00–E02 | pyatv/go2tv, совместимый синтетический MP4; отдельно start/video/audio/pause/seek/stop, версии и cleanup; [процедура](../runbooks/RECEIVER_SPIKES.md) | Cast недоступен по ответу владельца; утилиты и устройства требуют готовности. Не писать собственный сервер или GUI ради smoke |
| E01 | Инвентарь стенда; E00 | Model/firmware/OS, topology без секретов, версии инструментов, доступ к Cast; TEST-RX prerequisites | Нет доступа к устройству — оставить его blocked; не сканировать посторонние сети |
| E02 | Синтетическое медиа и сервер законченного файла; E01 | Клип + checksum + probe; корректные HEAD/Range/206/416 и закрытие сервера; TEST-HTTP-01/02 | Произвольный доступ к файлам или неверный Range — stop перед реальным видео |
| E03 | AirPlay spike на Apple TV 3; E02 | Pairing/start/pause/seek/stop, реальные наблюдения, точная версия pyatv; TEST-RX-01 | Нуждается в ослаблении auth либо нет видео — зафиксировать, не обходить защиту |
| E04 | DLNA spike на Sony; E02 | SSDP + service description, SetURI/play/pause/seek/stop в доступном API; TEST-RX-03 | DMR не обнаружен или action unsupported — не подменять тест просмотром медиатеки |
| E05 | Cast spike; E02 и hardware access | Discovery/load/status/control, local URL, TEST-RX-02 | Нет Cast-приёмника — unverified, emulator не закрывает критерий |
| E06 | Сравнить delivery и принять ADR-002; E03–E05 (или явно признанные blockers) | direct/remux/transcode, seek, dependency/license inventory, решение Python/Rust и ограниченный Android feasibility | Нельзя обещать Android, если нужный runtime не имеет проверенного пути упаковки |
| E07 | Core и контрактные тесты; E06 | Session IDs, cancellation, typed errors, stale-event tests; TEST-SESSION-01 | UI/протоколы протекли в domain — исправить границу до расширения |
| E08 | macOS direct-play UI и адаптеры; E07 | Один согласованный поток end-to-end, все три протокола отдельно, доступность UI; TEST-UI-01 | Успешная команда без видео не считается playback |
| E09 | Media planner и подготовка; E08 | Выбор direct/remux/audio/full transcode, progress/cancel/cache limits; TEST-MEDIA-01/02 | На тестовом profile не хватает ресурсов — явный отказ/подготовка, не бесконечный loading |
| E10 | Согласованный scope tracks/subtitles/queue; E09, после M1 | TEST-MEDIA-03, native/WebVTT или burn-in по профилю, seek после преобразования | Audio-only/RAOP и очередь требуют отдельных решений по scope |
| E11 | Recovery, privacy и квалификация macOS; E10 | Сеть, disk-full, restart, cleanup; TEST-SESSION-02 и TEST-SEC-01; отдельная macOS 14 | Если нет минимальной ОС — minimum runtime остаётся unverified |
| E12 | macOS package/release candidate; E11 | Чистая установка без dev environment, checksum/notices, review; TEST-PKG-01 | Нет подписи/решения distribution — локальный candidate, не публичный release |
| E13 | Fedora Xfce port; E12 + версия/архитектура Linux | Нативный UI, discovery, media backend, три RX, установка package; TEST-PORT-01 | Контейнерный успех не равен Xfce runtime; SELinux/firewall не отключать |
| E14 | Windows 10/11 port; E13 + стенды | Обе ОС, пути Unicode, cancel дерева процессов, firewall prompt, package | WSL не заменяет Windows native evidence |
| E15 | Android sender; E14 + устройства/SDK decision | Documents URI, lifecycle, permissions, MediaCodec/backend, три RX; 2 семейства смартфонов | Закрытие экрана/энергосбережение теряет сессию — не объявлять background ready |

## Карточка для запуска

Заполнить: ID; цель пользователя; scope/non-goals; REQ IDs; зависимости и их evidence; исходный SHA или точный snapshot; target OS/receiver; допустимые каталоги; изменения SPEC/ADR; ожидаемые tests; риски; stop condition; rollback; фактический итог. Отдельно указать, нужны ли установка, hardware access, commit/push или публикация и есть ли уже разрешение.

## Definition of Done задачи

Требования выполнены в разрешённом объёме; применимые проверки прошли; незакрытое помечено явно; нет секретов/личного медиа; изменения просмотрены; docs/traceability обновлены. Для hardware-задачи нужен реальный receiver record с версией сборки. Для doc-only задачи не нужны product tests. Blocked-задача может иметь полезный отчёт, но не статус completed acceptance.

## Откат

Работать в отдельной ветке `codex/<task>` после появления принятого baseline. Сохранять пользовательские изменения. Откат кода — revert конкретной задачи после согласования затрагиваемых изменений; без reset чужой работы. Runtime rollback — stop, закрытие локального сервера, завершение созданных процессов и очистка собственного cache. Настройки устройств не менять необратимо.
