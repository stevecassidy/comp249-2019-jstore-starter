import unittest
import os
from bottle.ext import sqlite, beaker
import bottle
import html
from webtest import TestApp
import dbschema
import main
import session
import urllib

DATABASE_NAME = "test.db"
# initialise the sqlite plugin for bottle
main.app.install(sqlite.Plugin(dbfile=DATABASE_NAME))
bottle.debug()

# make sure bottle looks for templates in the main directory, not this one
bottle.TEMPLATE_PATH = [os.path.join(os.path.dirname(__file__), p) for p in ['../', '../views/']]


class FunctionalTests(unittest.TestCase):

    def setUp(self):

        session_opts = {
            'session.type': 'memory',
        }
        beaker_app = beaker.middleware.SessionMiddleware(main.app, session_opts)

        self.app = TestApp(beaker_app)
        self.db = dbschema.connect(DATABASE_NAME)
        dbschema.create_tables(self.db)
        self.products = dbschema.sample_data(self.db)

    def tearDown(self):
        self.db.close()
        os.unlink(DATABASE_NAME)

    def test_home_page_html(self):
        """Home page should be an HTML page
        """

        response = self.app.get('/')

        # just test that we can get the HTML content - only works if result is HTML
        self.assertIsNotNone(response.html())

    def test_product(self):
        """/products returns JSON"""

        response = self.app.get('/products')
        self.assertIn('products', response.json)

    def test_add_to_cart_works(self):
        """If I click on the add to cart button my product
        is added to the shopping cart"""

        product = self.products['Yellow Wool Jumper']
        quantity = 3

        response = self.app.post('/cart', {'productid': product['id'], 'quantity': quantity})

        self.assertEqual(302, response.status_code)

        # now get the cart, should have our product in it
        response = self.app.get('/cart')

        self.assertIn('cart', response.json)
        self.assertEqual(1, len(response.json['cart']))
        self.assertEqual(product['id'], response.json['cart'][0]['id'])
        self.assertEqual(quantity, response.json['cart'][0]['quantity'])

    def test_add_cart_increments(self):
        """adding the same thing twice increments the quantity"""

        product = self.products['Yellow Wool Jumper']
        quantity = 3

        response = self.app.post('/cart', {'productid': product['id'], 'quantity': quantity})
        response = self.app.post('/cart', {'productid': product['id'], 'quantity': quantity})
        response = self.app.get('/cart')
        self.assertEqual(1, len(response.json['cart']))
        self.assertEqual(product['id'], response.json['cart'][0]['id'])
        self.assertEqual(quantity*2, response.json['cart'][0]['quantity'])

    def test_add_cart_new_item(self):
        """ adding another product makes the cart longer"""

        product = self.products['Yellow Wool Jumper']
        product2 = self.products['Dark Denim Top']
        quantity = 3

        self.app.post('/cart', {'productid': product['id'], 'quantity': quantity})
        self.app.post('/cart', {'productid': product2['id'], 'quantity': quantity})

        response = self.app.get('/cart')
        self.assertEqual(2, len(response.json['cart']))
        self.assertEqual(product2['id'], response.json['cart'][1]['id'])
        self.assertEqual(quantity, response.json['cart'][1]['quantity'])

    def test_add_cart_resets(self):
        """adding the same thing twice with the update flag resets the quantity"""

        product = self.products['Yellow Wool Jumper']
        quantity = 3

        self.app.post('/cart', {'productid': product['id'], 'quantity': quantity})
        self.app.post('/cart', {'productid': product['id'], 'quantity': quantity,
                                           'update': '1'})
        response = self.app.get('/cart')
        self.assertEqual(1, len(response.json['cart']))
        self.assertEqual(product['id'], response.json['cart'][0]['id'])
        self.assertEqual(quantity, response.json['cart'][0]['quantity'])

    def test_add_cart_delete(self):
        """adding something with quantity=0 removes it from the cart if the update flag is set"""

        product = self.products['Yellow Wool Jumper']
        quantity = 3

        self.app.post('/cart', {'productid': product['id'], 'quantity': quantity})
        self.app.post('/cart', {'productid': product['id'], 'quantity': 0,
                                           'update': '1'})
        response = self.app.get('/cart')
        self.assertEqual([], response.json['cart'])

    def test_cart_page(self):
        """The page at /cart should show the current contents of the
        shopping cart"""

        response = self.app.get('/cart')

        self.assertIn('cart', response.json)



if __name__=='__main__':

    unittest.main()
