import datetime
import decimal

from purrfect_creations import core, core_types


def test_derive_aggregate_stats_from_no_orders():
    now = datetime.datetime(year=2020, month=1, day=1)

    aggregate_stats = core.derive_aggregate_stats_from_orders(orders=[], now=now)

    assert aggregate_stats == core_types.AggregateStats(
        total_orders=0,
        total_orders_this_month=0,
        orders_in_progress=0,
        total_revenue=decimal.Decimal("0"),
        recent_orders=[],
    )


def test_derive_aggregate_stats_one_order_success():
    now = datetime.datetime(year=2020, month=1, day=1)

    orders = [
        core_types.Order(
            order_id=1,
            order_placed=now,
            product_name="cat tiara",
            price=decimal.Decimal("123.23"),
            first_name="Kit",
            last_name="Ten",
            address="123 Cat Street",
            email="catheart@gmail.com",
            order_status=core_types.OrderStatus.in_progress,
        )
    ]

    aggregate_stats = core.derive_aggregate_stats_from_orders(orders=orders, now=now)

    assert aggregate_stats == core_types.AggregateStats(
        total_orders=1,
        total_orders_this_month=1,
        orders_in_progress=1,
        total_revenue=decimal.Decimal("123.23"),
        recent_orders=[
            orders[0],
        ],
    )


def test_derive_aggregate_stats_multi_order_success():
    # one of each Order Status
    # two submitted now, two submitted months ago

    now = datetime.datetime(year=2020, month=1, day=1)
    months_ago = datetime.datetime(year=2019, month=10, day=1)

    orders = [
        core_types.Order(
            order_id=1,
            order_placed=now,
            product_name="cat tiara",
            price=decimal.Decimal("123.23"),
            first_name="Kit",
            last_name="Ten",
            address="123 Cat Street",
            email="catheart@gmail.com",
            order_status=core_types.OrderStatus.in_progress,
        ),
        core_types.Order(
            order_id=2,
            order_placed=now,
            product_name="cat tiara",
            price=decimal.Decimal("123.23"),
            first_name="Kit",
            last_name="Ten",
            address="123 Cat Street",
            email="catheart@gmail.com",
            order_status=core_types.OrderStatus.placed,
        ),
        core_types.Order(
            order_id=2,
            order_placed=months_ago,
            product_name="cat tiara",
            price=decimal.Decimal("123.23"),
            first_name="Kit",
            last_name="Ten",
            address="123 Cat Street",
            email="catheart@gmail.com",
            order_status=core_types.OrderStatus.shipped,
        ),
        core_types.Order(
            order_id=2,
            order_placed=months_ago,
            product_name="cat tiara",
            price=decimal.Decimal("123.23"),
            first_name="Kit",
            last_name="Ten",
            address="123 Cat Street",
            email="catheart@gmail.com",
            order_status=core_types.OrderStatus.cancelled,
        ),
    ]

    aggregate_stats = core.derive_aggregate_stats_from_orders(orders=orders, now=now)

    assert aggregate_stats == core_types.AggregateStats(
        total_orders=4,
        total_orders_this_month=2,
        orders_in_progress=1,
        total_revenue=decimal.Decimal("123.23") * 3,  # not counting cancelled
        recent_orders=[
            orders[0],
            orders[1],
            orders[2],
            orders[3],
        ],
    )


def test_derive_aggregate_stats_limit_recent_orders():
    now = datetime.datetime(year=2020, month=1, day=1)

    orders = [
        core_types.Order(
            order_id=1,
            order_placed=now,
            product_name="cat tiara",
            price=decimal.Decimal("123.23"),
            first_name="Kit",
            last_name="Ten",
            address="123 Cat Street",
            email="catheart@gmail.com",
            order_status=core_types.OrderStatus.in_progress,
        )
    ] * 20

    aggregate_stats = core.derive_aggregate_stats_from_orders(orders=orders, now=now)

    assert aggregate_stats == core_types.AggregateStats(
        total_orders=20,
        total_orders_this_month=20,
        orders_in_progress=20,
        total_revenue=decimal.Decimal("123.23") * 20,  # not counting cancelled
        recent_orders=orders[:10],
    )
