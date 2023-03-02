import dataclasses
import datetime
import decimal
import enum
from typing import Any

JSON = dict[str, Any]


class OrderStatus(enum.Enum):
    placed = "placed"
    in_progress = "in_progress"
    shipped = "shipped"
    cancelled = "cancelled"


@dataclasses.dataclass()
class Order(object):
    order_id: int
    order_placed: datetime.date
    product_name: str
    price: decimal.Decimal
    first_name: str
    last_name: str
    address: str
    email: str
    order_status: OrderStatus

    @classmethod
    def from_json(cls, order_json: JSON) -> "Order":
        return Order(
            order_id=order_json["order_id"],
            order_placed=datetime.date.fromisoformat(order_json["order_placed"]),
            product_name=order_json["product_name"],
            price=decimal.Decimal.from_float(order_json["price"]),
            first_name=order_json["first_name"],
            last_name=order_json["last_name"],
            address=order_json["address"],
            email=order_json["email"],
            order_status=OrderStatus(order_json["order_status"]),
        )

    def to_json(self) -> JSON:
        return dict(
            order_id=self.order_id,
            order_placed=self.order_placed.isoformat(),
            product_name=self.product_name,
            price=self.price_formatted,
            first_name=self.first_name,
            last_name=self.last_name,
            address=self.address,
            email=self.email,
            order_status=self.order_status.value,
        )

    @property
    def price_formatted(self) -> str:
        return f"{self.price:.2f}"


@dataclasses.dataclass()
class AggregateStats(object):
    total_orders: int
    total_orders_this_month: int
    orders_in_progress: int
    total_revenue: decimal.Decimal
    recent_orders: list[Order]

    def to_json(self) -> JSON:
        return dict(
            total_orders=self.total_orders,
            total_orders_this_month=self.total_orders_this_month,
            orders_in_progress=self.orders_in_progress,
            total_revenue=self.total_revenue_formatted,
            recent_orders=[o.to_json() for o in self.recent_orders],
        )

    @property
    def total_revenue_formatted(self) -> str:
        return f"{self.total_revenue:.2f}"
