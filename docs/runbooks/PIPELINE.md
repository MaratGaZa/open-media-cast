# Runbook: разработка, CI и выпуск

Редакция 2026-10-19. Цикл изменения задан владельцем; автоматический pipeline ещё не установлен. Manifests и CI YAML пока отсутствуют; продуктовые команды ниже запускаются только после появления соответствующего проекта.

## Сейчас: документация

Проверить локальные ссылки, таблицу требований/тестов, Draft/Accepted и наличие всех упомянутых файлов. Проверить независимость Git-корней и исключение `project/` из капсулы. Skills проверяются bundled `quick_validate.py`, если доступен, плюс чтением сценариев их применения. Структурный validator не доказывает поведение агента.

## Подготовка инструментов после принятия стека

Записать точные версии Rust, Node/package manager, Tauri, SDK/Xcode, Python для lab, FFmpeg и OS. Закрепить toolchain, lockfiles и CI actions; непинованные `latest` не использовать как доказательство воспроизводимости. Не устанавливать весь стек заранее только из-за упоминания в исследовании.

Source размещён в публичном [MaratGaZa/open-media-cast](https://github.com/MaratGaZa/open-media-cast); капсула остаётся локальной. Для main активен ruleset require PR, formal approvals=0, без bypass. Комментарий REVIEW и соответствие head SHA проверяются по SDD, а не этим ruleset. Actions и required checks ещё не настроены: отдельная [задача #2](https://github.com/MaratGaZa/open-media-cast/issues/2) после подготовки правил и README.

## Проверки по типу изменения

Порядок работы, полномочия и merge gate заданы только в [SDD](SDD_AND_AGENTS.md#цикл-изменения--каноническое-правило). Ниже перечислены области проверок, а не отдельный цикл PR.

1. **Docs/contracts:** ссылки, traceability, проверка схем и совместимости изменений.
2. **Core:** форматирование, lint, unit/property/contract tests, обработка отмены и stale events.
3. **UI:** typecheck, lint, тесты действий и состояний; проверка доступности основных controls.
4. **Media/HTTP integration:** законченные fixtures, Range, неправильные запросы, cleanup, controlled failures. Аппаратный encoder проверяется отдельно от software fallback.
5. **Platform build:** только заявленные target OS/архитектуры; артефакт содержит manifest версий.
6. **Hardware qualification:** локальный доверенный стенд в LAN, конкретный receiver и фиксированный artifact. Обычный облачный runner не видит домашний телевизор.
7. **Review и release readiness:** сравнить actual evidence с заявляемыми возможностями. Изменение после hardware test требует повторной оценки затронутых проверок.

После создания Rust workspace базовые команды из `project/`:

```sh
cargo fmt --all -- --check
cargo clippy --workspace --all-targets --locked -- -D warnings
cargo test --workspace --all-targets --locked
git diff --check
```

Их применимость нужно уточнить, если platform crates не собираются на текущем host; не скрывать исключённые packages. UI script names устанавливаются в manifest при scaffolding: пока не существует `npm test` или другого обещанного script. Для unit/HTTP tests не нужны живые домашние устройства.

## Матрица окружений

| Цель | Автоматизация | Обязательная дополнительная проверка |
|---|---|---|
| macOS ARM64 | Нативная сборка, core/UI/media tests | Минимальная 14 и текущая поддерживаемая ОС; установка готового пакета; receiver tests |
| Fedora Xfce | Build/test на выбранной Fedora | Настоящая desktop-сессия, сеть, codecs и пакет; container не заменяет GUI |
| Windows 10/11 | Windows build/tests | Отдельный native smoke на 10 и 11; paths/process cleanup |
| Android | Gradle/NDK build, unit/emulator | Реальные телефоны, разрешения, screen-off/background, сеть и кодеки |

Не обещать наличие подходящего CI runner до проверки предложения hosting. Наличие x86_64 runner не закрывает ARM64; deployment target не закрывает runtime на минимальной ОС.

## Безопасное выполнение hardware tests

Запускать на доверенном локальном стенде, вручную разрешённом владельцем. Не выполнять код недоверенного PR на домашнем runner с доступом к устройствам и credentials. Для synthetic fixture определить duration и stop timeout; при сбое остановить только процессы/сервер данного теста. Сохранять sanitized result, а не полный сетевой дамп.

## Release candidate

Пакет содержит source SHA, dirty=false (или явно назван experimental snapshot), toolchain/dependency manifest, checksum, notices/SBOM и сведения о проверенных OS/receivers. Секреты signing и pairing не помещать в артефакт.

Порядок: собрать → установить в чистой целевой среде → проверить заявляемые сценарии → review → получить разрешение на публикацию → подписать/нотарифицировать по выбранному каналу → проверить опубликованный checksum и установку. Конкретный порядок signing/notarization зависит от формата: final distribution artifact должен проходить установочную проверку, а не только предварительная unsigned-сборка.

Mac: channel/signing ADR до публичного выпуска. Linux: выбранный формат и dependencies. Windows: installer/signing strategy. Android: signed package, test track/side-load policy. Эти действия не выполнялись.

## Отказ и откат

При красной проверке сохранять диагностический результат и исправлять причину в той же задаче. Не делать зелёным pipeline исключением проблемного receiver или отключением проверки без изменения scope владельцем. Невозможный hardware test — unverified/blocked, не pass.

Для локального теста: cancel session → terminate owned media processes → revoke URL → close sockets → cleanup owned cache. Для выпуска: остановить дальнейшую публикацию, сохранить предыдущий artifact, отозвать ошибочную версию/обновление только по разрешению, выпустить исправление с проверенным rollback path. Автообновления первого релиза пока не специфицированы.
