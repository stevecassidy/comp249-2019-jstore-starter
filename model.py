"""
Database model for Online Store

Provides functions to access the database
"""


def product_get(db, id):
    """Return the product with the given id or None if
    it can't be found.
    Returns a sqlite3.Row object"""

    sql = """SELECT id, name, description, category, image_url, unit_cost, inventory FROM products WHERE id=?"""
    cur = db.cursor()
    cur.execute(sql, (id,))

    return dict(cur.fetchone())


def product_list(db, category=None):
    """Return a list of products, if category is not None, return products from
    that category. Results are returned in no particular order.
    Returns a list of dictionaries"""

    cur = db.cursor()

    if category:
        sql = """SELECT id, name, description, category, image_url, unit_cost, inventory 
        FROM products WHERE category = ?
        """
        cur.execute(sql, (category,))
    else:
        sql = 'SELECT id, name, description, category, image_url, unit_cost, inventory FROM products'
        cur.execute(sql)

    return [dict(r) for r in cur.fetchall()]
