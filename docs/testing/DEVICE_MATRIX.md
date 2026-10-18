# Матрица устройств

2026-10-18. Runtime Open Media Cast не запускался.

| Sender | Receiver | Проверяемая функция | Статус / evidence |
|---|---|---|---|
| Mac mini M4, macOS 15.7.9 (24G830) | Apple TV 3, firmware unknown | Системный AirPlay | Сообщение владельца об успехе; не тест нашего приложения |
| Mac mini M4 | Apple TV 3 | TEST-RX-01 | planned, нет результата |
| Mac mini M4 | Sony KDL-48W605B | TEST-RX-03 | planned; наличие Renderer документировано, runtime unverified |
| Mac mini M4 | Google Cast, модель не указана | TEST-RX-02 | blocked: владелец подтвердил отсутствие доступа 2026-10-18; ближайший smoke — Apple TV/Sony |
| macOS 14 ARM64 test host | Все RX | Минимальная ОС | unverified: host не определён |
| Fedora 44/45 Xfce (цель из review), установленная version/arch unknown | Все RX | TEST-PORT-01 Linux | planned |
| Windows 10 и 11, host unknown | Все RX | TEST-PORT-01 Windows | planned |
| Nothing Phone (1), Android unknown | Все RX | TEST-PORT-01 Android | planned |
| Xiaomi/Redmi/Poco, models unknown | Все RX | OEM lifecycle Android | planned |

Android-телефоны — будущие отправители, не квалифицированные Cast-приёмники. Один успешный приёмник не закрывает семейство или всю версию ОС. Изменение firmware, encoder build или delivery strategy требует оценки повторных тестов.

## Форма записи результата

`test_id; date; sender_os_arch; receiver_model_firmware; source_revision; artifact_checksum; library_versions; auth_mode; fixture_checksum; transport; command; expected; observed; latency; cleanup; status; limitations`.

Не хранить реальные IP, serial numbers, session tokens и pairing keys. Для нескольких ревизий добавлять новые строки/датированные отчёты; не заменять failed исторически на passed.
