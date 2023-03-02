import datetime
import decimal

from purrfect_creations import core_types
from purrfect_creations.api_clients.airtable_client import (
    PurrfectCreationsAirtableClient,
)
from purrfect_creations.core_types import AggregateStats


def get_aggregate_stats_from_airtable(
    airtable_client: PurrfectCreationsAirtableClient, now: datetime.datetime
) -> AggregateStats:
    orders = airtable_client.get_orders()
    aggregate_stats = derive_aggregate_stats_from_orders(orders=orders, now=now)
    return aggregate_stats


def _order_in_current_month(order: core_types.Order, today: datetime.date) -> bool:
    return (
        order.order_placed.year == today.year
        and order.order_placed.month == today.month
    )


def derive_aggregate_stats_from_orders(
    orders: list[core_types.Order], now: datetime.datetime
) -> AggregateStats:
    today = now.date()

    orders_in_month_count = 0
    orders_in_progress_count = 0
    total_revenue = decimal.Decimal("0")
    for order in orders:
        if _order_in_current_month(order=order, today=today):
            orders_in_month_count += 1
        if order.order_status == core_types.OrderStatus.in_progress:
            orders_in_progress_count += 1

        if order.order_status != core_types.OrderStatus.cancelled:
            total_revenue += order.price

    orders.sort(key=lambda o: o.order_placed, reverse=True)

    return AggregateStats(
        total_orders=len(orders),
        total_orders_this_month=orders_in_month_count,
        orders_in_progress=orders_in_progress_count,
        total_revenue=total_revenue,
        recent_orders=orders[:10],
    )
