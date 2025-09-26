"""
Report view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from views.template_view import get_template, get_param

def show_highest_spending_users():
    """ Show report of highest spending users """
    from queries.read_order import get_highest_spending_users
    from queries.read_user import get_user_by_id
    rows = []
    for user_id, total in get_highest_spending_users():
        user = get_user_by_id(user_id)
        name = user.get('name', f"Utilisateur {user_id}")
        rows.append(f"<tr><td>{name}</td><td>${total:.2f}</td></tr>")
    table = """
        <h2>Les plus gros acheteurs</h2>
        <table class='table'>
            <tr><th>Nom</th><th>Total dépensé</th></tr>
            {rows}
        </table>
    """.format(rows=''.join(rows))
    return get_template(table)

def show_best_sellers():
    """ Show report of best selling products """
    from queries.read_order import get_best_selling_products
    from queries.read_product import get_product_by_id
    rows = []
    for product_id, qty in get_best_selling_products():
        product = get_product_by_id(product_id)
        name = product.get('name', f"Produit {product_id}")
        rows.append(f"<tr><td>{name}</td><td>{qty}</td></tr>")
    table = """
        <h2>Les articles les plus vendus</h2>
        <table class='table'>
            <tr><th>Nom</th><th>Quantité vendue</th></tr>
            {rows}
        </table>
    """.format(rows=''.join(rows))
    return get_template(table)