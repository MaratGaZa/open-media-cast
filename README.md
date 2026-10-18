# Open Media Cast

Draft 0.1 · 2026-10-18. Пока только документация; исполняемого приложения и продуктовых тестов нет.

Приложение для локальных видео: macOS ≥14 ARM64 → Fedora Xfce → Windows 10/11 → Android. Приёмники первого релиза: Apple TV, Google Cast, DLNA MediaRenderer, с явной матрицей проверенных моделей.

Ориентир владельца — [Beamer 4](https://softorino.com/beamer): создать собственное приложение с сопоставимым удобством передачи видео, используя AI-agents. Мотивация и соответствие основных сценариев этапам разработки зафиксированы в SPEC.

## Источники истины

- [Спецификация](docs/specs/PRODUCT_SPEC.md) — предлагаемое поведение и критерии приёмки.
- [Архитектура](docs/adr/ADR-002-APPLICATION-ARCHITECTURE.md) — общее ядро и адаптеры, статус Proposed.
- [Два репозитория](docs/adr/ADR-001-REPOSITORY-BOUNDARIES.md) — Accepted владельцем 2026-10-18.
- [Roadmap](docs/plans/ROADMAP.md) и [execution tasks](docs/plans/IMPLEMENTATION_PLAN.md).
- [SDD и работа агентов](docs/runbooks/SDD_AND_AGENTS.md), [CI и выпуск](docs/runbooks/PIPELINE.md), [эксперименты](docs/runbooks/RECEIVER_SPIKES.md).
- [Стратегия тестирования](docs/testing/TEST_STRATEGY.md), [матрица](docs/testing/DEVICE_MATRIX.md).
- [Правила](docs/rules/ENGINEERING_RULES.md), [AGENTS.md](AGENTS.md).

Код платформ будет жить в этом репозитории. Отдельные исходные каталоги и manifests появятся после принятия стека. Сейчас не требуется устанавливать Rust, Node, Python или FFmpeg, чтобы читать пакет.

Учебный курс и исследование хранятся во внешней капсуле, в соседних с `project/` каталогах. Они не нужны для корректного чтения канонической SPEC этого репозитория. Remote и публичная лицензия пока не выбраны.
