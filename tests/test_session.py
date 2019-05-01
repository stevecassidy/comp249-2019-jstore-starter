import unittest
from bottle import request

import session
import dbschema

class MockBeakerSession(dict):
    """A Mock version of a beaker session, just a dictionary
    with a 'save' method that does nothing"""

    def save(self):
        pass


class SessionTests(unittest.TestCase):

    def setUp(self):

        # init an in-memory database
        self.db = dbschema.connect(':memory:')
        dbschema.create_tables(self.db)
        self.products = dbschema.sample_data(self.db)
        if 'beaker.session' in request.environ:
            del request.environ['beaker.session']


    def test_get_cart(self):
        """Can get the contents of the cart"""

        request.environ['beaker.session'] = MockBeakerSession({'cart': []})
        self.assertEqual([], session.get_cart_contents())

        cart = [{'id': 1, 'quantity': 3, 'name': 'test', 'cost': 123.45}]
        request.environ['beaker.session'] = {'cart': cart}
        self.assertEqual(cart, session.get_cart_contents())

    def test_cart(self):
        """We can add items to the shopping cart
        and retrieve them"""

        cart = []
        request.environ['beaker.session'] = MockBeakerSession({'cart': cart})
        self.assertEqual([], session.get_cart_contents())

        # now add something to the cart
        for pname in ['Yellow Wool Jumper', 'Ocean Blue Shirt']:
            product =  self.products[pname]
            session.update_cart(self.db, product['id'], 1, False)

        cart = session.get_cart_contents()
        self.assertEqual(2, len(cart))

        # check that all required fields are in the every cart entry
        for entry in cart:
            self.assertIn('id', entry)
            self.assertIn('name', entry)
            self.assertIn('quantity', entry)
            self.assertIn('cost', entry)



if __name__=='__main__':
    unittest.main()


