
from bottle import Bottle, template, static_file, request, redirect, response, run
import os

import model
import session


app = Bottle()

@app.route('/')
def index():
    """Deliver the index page. Really just a
    static file but for convenience we do this through
    the template"""

    # an awful hack since static_file doesn't use the global response
    # object in bottle so the cookie we want to set will be ignored
    # we copy the global response object here for safe keeping
    # replace it with the result of static_file
    # then call our cookie setting function which will add a cookie
    # to the response
    # then we restore the global response object
    # and finally return the one we've made with the cookie set
    #
    global response

    global_response = response

    response = static_file("index.html", root=os.path.join(os.path.dirname(__file__), "views"))

    local_response = response
    response = global_response

    return local_response



@app.route('/cart')
def cart_contents():

    cart = session.get_cart_contents()
    return {'cart': cart}

@app.post('/cart')
def add_to_cart(db):

    productid = request.forms.get('productid', type=int)
    quantity = request.forms.get('quantity', type=int)
    update = request.forms.get('update')
    session.update_cart(db, productid, quantity, update=='1')

    return redirect('/cart')



@app.route('/products')
def products(db):

    return {'products': model.product_list(db)}


@app.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')


if __name__ == '__main__':

    from bottle.ext import sqlite, beaker

    from dbschema import DATABASE_NAME
    # install the database plugin
    app.install(sqlite.Plugin(dbfile=DATABASE_NAME))

    session_opts = {
        'session.type': 'memory',
    }

    beaker_app = beaker.middleware.SessionMiddleware(app, session_opts)

    run(app=beaker_app, debug=True, port=8010)
