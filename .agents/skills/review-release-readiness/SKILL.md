---
name: review-release-readiness
description: Проверить готовность конкретного release candidate Open Media Cast по артефактам сборки, совместимости устройств и установке. Использовать перед заявлением о готовности выпуска; не для автоматической публикации или обычного code review.
metadata:
  version: 0.1.0
---

# Готовность выпуска

Определи заявляемые OS/архитектуры, receivers и функции. Прочитай [SPEC](../../../docs/specs/PRODUCT_SPEC.md), [pipeline](../../../docs/runbooks/PIPELINE.md), [матрицу](../../../docs/testing/DEVICE_MATRIX.md) и [rules](../../../docs/rules/ENGINEERING_RULES.md).

Проверь конкретный source SHA/snapshot и checksum кандидата, version manifest, notices/SBOM и канал распространения. Сопоставь каждое обещание с evidence: unit, integration, hardware, installation. Отдельно проверь минимальную ОС, ARM64, все заявленные протоколы, cleanup и установку без developer tools.

Если нет реального Cast, теста macOS 14 или подписанного final package, перечисли именно отсутствующее доказательство. Нельзя переносить успешный тест на другой binary после изменения dependencies или encoder. Повторные проверки назначай по затронутому поведению, а не механически.

Выдай verdict `ready`, `ready for limited experiment` либо `not ready`, перечисли findings по влиянию, evidence и действия для закрытия. Ограниченный эксперимент должен иметь явно разрешённый scope; это не обход требований полного v1.

Review не публикует, не подписывает, не создаёт release и не выполняет merge. Не запрашивай разрешение повторно, если нужное действие уже отдельно поручено, но проверь, что оно относится к данному кандидату.
