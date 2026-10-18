# Проверяемые правила

Draft 0.1 · 2026-10-18. Эти правила описывают конкретные границы приложения; не требуют отдельного согласования для каждой обычной локальной правки.

| ID | Правило | Проверка |
|---|---|---|
| RULE-001 | Совместимость заявляется для конкретного OS/receiver/firmware/scenario | Claim связан с DEVICE_MATRIX и воспроизводимым E3/E4 evidence |
| RULE-002 | Media URL выдаёт только выбранный ресурс текущей сессии | TEST-HTTP-02; нет filesystem path routing, listing и публичного port mapping |
| RULE-003 | Media process вызывается массивом аргументов, без shell | Code review и malicious filename fixture; UI не передаёт произвольные FFmpeg options |
| RULE-004 | Cancellation владеет созданными ресурсами | TEST-SESSION-01/02; все owned children, sockets и cache освобождены |
| RULE-005 | Credentials и пользовательские данные не попадают в обычные логи/fixtures | TEST-SEC-01 и проверка export diagnostics |
| RULE-006 | Platform API не проникает в domain policy | Core/contract tests запускаются без UI SDK конкретной ОС |
| RULE-007 | Network input недоверенный | Limits/timeouts для XML, headers и responses; service/callback URLs проверяются; нет неограниченных redirects |
| RULE-008 | Метрики, hashes и package claims привязаны к проверенному snapshot | Изменение artifact не наследует старый release pass автоматически |
| RULE-009 | Обнаружение устройства не расширяет разрешённую сеть | Только выбранная пользователем LAN/target; не отключать firewall, SELinux, Gatekeeper или auth ради теста |

Session URL с токеном ограничивает доступ, но не делает HTTP шифрованным. Нельзя писать «безопасный канал» только на основании непредсказуемого имени. Конкретная схема авторизации/жизненного цикла должна быть проверена на старых приёмниках и не раскрывать control API в LAN.
