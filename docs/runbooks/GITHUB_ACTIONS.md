# GitHub Actions: T02

[Workflow](../../.github/workflows/ci.yml) запускает T01 на `pull_request` в main
(opened, synchronize, reopened, ready_for_review), на `push` в main после merge
и вручную через workflow_dispatch. Нет фильтра путей: документационные PR тоже
получают check. Для PR проверяется синтетический merge с base, для push — коммит
main. Ручной запуск становится доступен после появления workflow в main.

Один GitHub-hosted runner ubuntu-24.04, Python 3.13, timeout 10 минут. Actions
закреплены полными SHA, токен имеет только contents:read, credentials checkout
не сохраняются. Домашние устройства, пользовательское медиа и секреты не нужны.

Check: **HTTP contract tests (Python 3.13)**. Выполняются реальные тесты T01 на
loopback; отсутствие тестов или неуспешный тест завершает шаг ошибкой. Это E2
лабораторного HTTP-эталона. Rust/UI-код и аппаратная квалификация не проверяются.

## Зависимости

`tools/protocol-lab/requirements-tests.txt` задаёт прямую зависимость,
`requirements-ci.txt` закрепляет все девять пакетов текущего окружения. CI
устанавливает оба файла: несовместимое обновление прямой версии без обновления
фиксации завершится ошибкой resolver. Версии Python/pip/packages видны в логе;
Python закреплён на серии 3.13, patch и образ runner могут обновляться.

Для обновления фиксации из корня source (использован uv 0.12.13):

```sh
uv pip compile tools/protocol-lab/requirements-tests.txt --python-version 3.13 --no-header --no-annotate --output-file tools/protocol-lab/requirements-ci.txt
```

Обновление зависимостей — отдельный проверяемый PR, с локальным прогоном и CI.

## Приёмка и merge

После первого успешного PR-run добавить check в существующий ruleset main как
required status check с источником GitHub Actions и актуальным base. Сохранить
require PR, approvals=0 и отсутствие bypass. Проверить effective rules через API.
Проверки CI дополняют [независимый REVIEW](SDD_AND_AGENTS.md#формат-вердикта);
зелёный check не заменяет APPROVE на текущий head SHA.

После разрешённого merge проверить отдельный push-run на точный SHA main. До
merge этот пункт остаётся неподтверждённым. При красной проверке исправлять
причину отдельным изменением по SDD; не отключать gate для обхода ошибки.
