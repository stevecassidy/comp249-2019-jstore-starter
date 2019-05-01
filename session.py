"""
Code for handling sessions in our web application
"""

from bottle import request

import model


def update_cart(db, itemid, quantity, update=False):
    """Update or add an item to the shopping cart.

    If the item is already present in the cart and update=False, the
    quantity of the item will be incremented, if
    update=True then the quantity will be reset. If
    update=True and quantity=0, the item will be removed
    from the cart"""

    session = request.environ.get('beaker.session')

    product = model.product_get(db, itemid)
    newitem = {
        'id': itemid,
        'quantity': quantity,
        'name': product['name'],
        'cost': quantity * product['unit_cost']
    }
    cart = session.get('cart', [])
    newcart = []
    found = False
    for item in cart:
        if item['id'] == itemid:
            # update the quantity
            if update:
                item['quantity'] = quantity
            else:
                item['quantity'] += quantity
            item['cost'] = round(item['quantity'] * product['unit_cost'], 2)
            if not (quantity == 0 and update):
                newcart.append(item)
            found = True
        else:
            # carry over existing item
            newcart.append(item)
    # only add if we didn't find the product in the cart already
    if not found and quantity > 0:
        newcart.append(newitem)

    session['cart'] = newcart
    session.save()


def get_cart_contents():
    """Return the contents of the shopping cart as
    a list of dictionaries:
    [{'id': <id>, 'quantity': <qty>, 'name': <name>, 'cost': <cost>}, ...]
    """
    session = request.environ.get('beaker.session')
    return session.get('cart', [])
