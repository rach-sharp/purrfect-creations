import datetime
import decimal

from flask import render_template

from purrfect_creations import core_types
from purrfect_creations.app import app


def test_dashboard_render():
    now = datetime.datetime(year=2020, month=1, day=1)

    stats = core_types.AggregateStats(
        total_orders=123456,
        total_orders_this_month=54321,
        orders_in_progress=2468,
        total_revenue=decimal.Decimal("0.99"),
        recent_orders=[],
    )

    with app.app_context():
        html_output = render_template("dashboard.html", aggregate_stats=stats, now=now)

    # check some magic strings are contained within the html output for convenience
    # very high chance of incorrectly passing if any change made to code
    # but just for saving time in tech test
    assert str(stats.total_orders) in html_output
    assert str(stats.total_orders_this_month) in html_output
    assert str(stats.orders_in_progress) in html_output
    assert str(stats.total_revenue) in html_output


def test_dashboard_render_revenue_to_2dp():
    now = datetime.datetime(year=2020, month=1, day=1)

    stats = core_types.AggregateStats(
        total_orders=123456,
        total_orders_this_month=54321,
        orders_in_progress=2468,
        total_revenue=decimal.Decimal("0.9999"),
        recent_orders=[],
    )

    with app.app_context():
        html_output = render_template("dashboard.html", aggregate_stats=stats, now=now)

    assert str(stats.total_orders) in html_output
    assert str(stats.total_orders_this_month) in html_output
    assert str(stats.orders_in_progress) in html_output
    assert "1.00" in html_output


def test_dashboard_render_orders():
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
        ),
        core_types.Order(
            order_id=2,
            order_placed=now,
            product_name="cat mittens",
            price=decimal.Decimal("123.23"),
            first_name="Kit",
            last_name="Ten",
            address="123 Cat Street",
            email="catheart@gmail.com",
            order_status=core_types.OrderStatus.in_progress,
        ),

    ]

    stats = core_types.AggregateStats(
        total_orders=0,
        total_orders_this_month=0,
        orders_in_progress=0,
        total_revenue=decimal.Decimal("0"),
        recent_orders=orders,
    )

    with app.app_context():
        html_output = render_template("dashboard.html", aggregate_stats=stats, now=now)

    assert all(o.product_name in html_output for o in orders)
