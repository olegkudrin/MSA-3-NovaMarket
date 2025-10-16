# Реестр событий Saga-хореографии оформления заказа

| Этап                             | Тип события  | Название               |
| -------------------------------- | ------------ | ---------------------- |
| Заказ создан                     | domain       | OrderCreated           |
| Заказ подтвержден                | domain       | OrderConfirmed         |
| Заказ отменен                    | compensation | OrderCancelled         |
| Товар зарезервирован             | domain       | StockReserved          |
| Ошибка при резервировании товара | failure      | StockReservationFailed |
| Товар разрезервирован            | compensation | StockReleased          |
| Платеж успешно обработан         | domain       | PaymentCompleted       |
| Ошибка при обработке платежа     | failure      | PaymentFailed          |
| Средства были возвращены         | compensation | RefundCompleted        |
| Заявка на доставку сформирована  | domain       | DeliveryRequested      |
| Заявка на доставку отвергунта    | failure      | DeliveryDeclined       |
| Заявка на доставку остановлена   | compensation | DeliveryStop           |
