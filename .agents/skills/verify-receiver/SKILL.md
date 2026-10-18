---
name: verify-receiver
description: Проверить конкретный AirPlay, Google Cast или DLNA-приёмник Open Media Cast на реальном устройстве и оформить воспроизводимый результат. Использовать для receiver spike или диагностики совместимости; не для обычной правки документации.
metadata:
  version: 0.1.1
---

# Проверка приёмника

Статус поведенческой проверки: untested. Полномочия — [AGENTS](../../../AGENTS.md); процедура и команды — [receiver runbook](../../../docs/runbooks/RECEIVER_SPIKES.md).

1. Установи scope (E00.5 или квалификация), target, модель/прошивку, OS, версии инструментов и доступность приёмника. Прочитай относящиеся REQ в [SPEC](../../../docs/specs/PRODUCT_SPEC.md).
2. Подготовь синтетический fixture с видимым временем, checksum/probe. Проверь путь выдачи и Range с другого LAN-хоста, если диагностируешь delivery/seek.
3. Выполни discovery и штатное pairing при необходимости. Apple TV legacy: video/DMAP отдельно от RAOP/mirroring; DLNA: MediaRenderer отдельно от MediaServer; Cast: реальный receiver и условия доступа в интернет. Для .app на macOS 15+ учти Local Network.
4. Проверь start, изображение/звук, pause/resume, seek и stop по отдельности. `command accepted`, `playing reported`, `video observed` — разные поля. Защиту устройства ради результата не ослабляй.
5. Ограничь попытку по времени, заверши принадлежащие ей процессы/сервер и запиши cleanup. При недоступном receiver локальная часть может продолжаться, а E3 остаётся blocked/unverified.
6. Обнови [матрицу](../../../docs/testing/DEVICE_MATRIX.md) по фактическому результату. Особенность модели добавляй в соответствующий раздел runbook с firmware и ссылкой на опыт; здесь сохраняй краткий маршрут к этим знаниям.

## Шаблон отчёта

```text
test_id; date; sender_os_arch; receiver_model_firmware; source_revision;
library_versions; fixture_checksum; auth_mode; transport;
command; expected; observed; latency; cleanup; status; limitations
```

Для E00.5 укажи, что проверена сторонняя утилита. Для готового binary добавь artifact checksum. Реальные IP, pairing keys и токены в отчёт не включай. Успех одного профиля не переносится на другие форматы или устройства.
