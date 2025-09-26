"""
Orders (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from db import get_sqlalchemy_session, get_redis_conn
from sqlalchemy import desc
from models.order import Order

def get_order_by_id(order_id):
    """Get order by ID from Redis"""
    r = get_redis_conn()
    return r.hgetall(order_id)

def get_orders_from_mysql(limit=9999):
    """Get last X orders"""
    session = get_sqlalchemy_session()
    return session.query(Order).order_by(desc(Order.id)).limit(limit).all()

def get_orders_from_redis(limit=9999):
    """Get last X orders"""
    r = get_redis_conn()

    order_keys = r.keys("order:*")

    order_keys = [k for k in order_keys if ':item:' not in k]

    def extract_id(key):
        try:
            return int(key.split(":")[1])
        except Exception:
            return 0
    order_keys = sorted(order_keys, key=extract_id, reverse=True)[:limit]
    orders = []
    for key in order_keys:
        order_data = r.hgetall(key)

        order_data['id'] = int(order_data.get('order_id', 0))
        order_data['user_id'] = int(order_data.get('user_id', 0))
        order_data['total_amount'] = float(order_data.get('total_amount', 0))
        orders.append(order_data)
    return orders

def get_highest_spending_users():
    """Get top 10 users who spent the most (from Redis)"""
    from collections import defaultdict
    r = get_redis_conn()
    order_keys = r.keys("order:*")
    order_keys = [k for k in order_keys if ':item:' not in k]
    expenses_by_user = defaultdict(float)
    for key in order_keys:
        order = r.hgetall(key)
        user_id = int(order.get('user_id', 0))
        total = float(order.get('total_amount', 0))
        expenses_by_user[user_id] += total
    highest_spending_users = sorted(expenses_by_user.items(), key=lambda item: item[1], reverse=True)[:10]

    return highest_spending_users

def get_best_selling_products(top_n=10):
    """Get top N best selling products (by quantity sold) from Redis"""
    r = get_redis_conn()
    product_keys = r.keys("product:*")
    sales = []
    for key in product_keys:
        try:
            product_id = int(key.split(":")[1])
            quantity = int(r.get(key) or 0)
            sales.append((product_id, quantity))
        except Exception:
            continue
    best_sellers = sorted(sales, key=lambda x: x[1], reverse=True)[:top_n]
    return best_sellers