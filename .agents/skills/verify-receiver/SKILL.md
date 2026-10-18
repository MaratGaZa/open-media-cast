---
name: verify-receiver
description: Проверить конкретный AirPlay, Google Cast или DLNA-приёмник Open Media Cast на реальном устройстве и оформить воспроизводимый результат. Использовать для receiver spike или диагностики совместимости; не для обычной правки документации.
metadata:
  version: 0.1.0
---

# Проверка приёмника

Прочитай применимые REQ в [SPEC](../../../docs/specs/PRODUCT_SPEC.md), [receiver runbook](../../../docs/runbooks/RECEIVER_SPIKES.md) и [матрицу](../../../docs/testing/DEVICE_MATRIX.md).

Установи модель/прошивку, OS отправителя, разрешённый target и test scope. Используй synthetic fixture и фиксированную версию инструмента. Если фактическое устройство недоступно, можно проверить локальную часть, но receiver outcome остаётся unverified/blocked.

Разделяй discovery, pairing, команду load, реальное изображение/звук и control actions. Для Apple TV отличай mirroring, RAOP и video; для DLNA — MediaServer и MediaRenderer; для Cast — физический receiver и mock. Не менять auth/security ради успешного отчёта. Если нужен новый доступ или установка, проверь существующее разрешение и запроси только недостающее.

Выполни только разрешённые сценарии с ограниченным timeout; при сбое сначала штатно останови принадлежащие тесту процессы и сервер. Запиши test ID, source revision/snapshot, версии, fixture hash, expected/observed, limitations и cleanup. Включай только очищенные сетевые сведения.

Не подменяй наблюдения отсутствующей телеметрией: `command accepted`, `playing reported` и `video observed` — разные доказательства. Не распространяй успешный результат на другие модели, прошивки или форматы. Обнови матрицу только до фактически подтверждённого уровня.
