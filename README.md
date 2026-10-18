# Open Media Cast

Проект приложения для передачи локального видео с компьютера на телевизор или
приставку. Целевые протоколы — AirPlay, DLNA/UPnP и Google Cast; ориентир по
удобству — Beamer 4. Требования и границы первого среза описаны в
[спецификации](docs/specs/PRODUCT_SPEC.md).

**Ранняя стадия:** готового приложения пока нет. В репозитории есть документация,
лабораторный HTTP-сервер и его контрактные тесты. Архитектура остаётся
[Proposed](docs/adr/ADR-002-APPLICATION-ARCHITECTURE.md); исходные каталоги
приложения и manifests появятся после принятия соответствующего решения.

## Цель первого MVP

Первый срез рассчитан на macOS 14+ ARM64: выбрать совместимый MP4 (H.264/AAC),
найти Apple TV 3 или Sony DLNA и управлять воспроизведением — запуском, паузой,
продолжением, перемоткой и остановкой. Это планируемое поведение, а не уже
доступные функции приложения.

Дальнейшие целевые платформы: Fedora Xfce, Windows 10/11 и Android. Google Cast
входит в цель полного v1; доступного Cast-стенда пока нет. Объём и порядок
развития задаются [roadmap](docs/plans/ROADMAP.md), а совместимость —
[матрицей устройств](docs/testing/DEVICE_MATRIX.md).

## Что проверено

- [E00.5](docs/testing/E00_5_2026-10-18.md): воспроизведение синтетического клипа
  и базовое управление на Apple TV 3 и Sony BRAVIA KDL-48W605B готовыми утилитами.
  Это исследовательский опыт, не квалификация будущего приложения.
- [T01](docs/testing/T01_2026-10-19.md): семь локальных тестов лабораторного
  HTTP-эталона проверяют ответы GET/HEAD, Range, доступ по токену и закрытие
  сервера. Проверки выполняются на loopback с синтетическими байтами; они не
  подтверждают кодеки или воспроизведение на телевизоре.

[GitHub Actions](.github/workflows/ci.yml) запускает T01 на PR и push в main.
Окружение и порядок проверки запусков описаны в [runbook CI](docs/runbooks/GITHUB_ACTIONS.md).

## Запуск тестов HTTP-эталона

Нужен установленный Python 3.13. Из корня этого репозитория:

```sh
python3.13 -m venv .venv
.venv/bin/python -m pip install -r tools/protocol-lab/requirements-tests.txt
.venv/bin/python -m unittest discover -s tools/protocol-lab -p test_media_server.py -v
```

Команды приведены для macOS/Linux. Тесты запускают собственный временный сервер;
телевизор и пользовательские медиафайлы не нужны. Контракт и ограничения — в
[TEST_FIRST](docs/runbooks/TEST_FIRST.md). Rust, Node и FFmpeg для этих тестов
не требуются.

## Работа над проектом

Для всех изменений, включая документацию, действует единый
[цикл изменения](docs/runbooks/SDD_AND_AGENTS.md#цикл-изменения--каноническое-правило).
Правила test-first находятся в [TEST_FIRST](docs/runbooks/TEST_FIRST.md),
проверки по типам изменений — в [PIPELINE](docs/runbooks/PIPELINE.md).
Агенты начинают с [AGENTS.md](AGENTS.md); задачи выбираются из
[плана реализации](docs/plans/IMPLEMENTATION_PLAN.md) в пределах принятого scope.

## Документация

| Документ | Назначение |
|---|---|
| [PRODUCT_SPEC](docs/specs/PRODUCT_SPEC.md) | Требования и критерии приёмки; статус Draft |
| [ADR-001](docs/adr/ADR-001-REPOSITORY-BOUNDARIES.md) | Принятые границы двух независимых репозиториев |
| [ADR-002](docs/adr/ADR-002-APPLICATION-ARCHITECTURE.md) | Предложение архитектуры и стека; статус Proposed |
| [TEST_STRATEGY](docs/testing/TEST_STRATEGY.md) | Уровни доказательств и сценарии проверки |
| [RECEIVER_SPIKES](docs/runbooks/RECEIVER_SPIKES.md) | Проведение опытов с приёмниками |
| [ENGINEERING_RULES](docs/rules/ENGINEERING_RULES.md) | Инженерные правила |

Публичный source-репозиторий содержит код, каноническую документацию и инструкции
агентам. Учебные материалы и рабочие заметки хранятся в отдельной локальной
капсуле и не нужны для чтения документации или запуска приведённых тестов.
Лицензия проекта пока не выбрана.
