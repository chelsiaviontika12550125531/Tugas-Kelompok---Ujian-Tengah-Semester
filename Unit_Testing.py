import unittest
from Main_data import Groceries, Food, Beverages, HouseholdItems, Transaction, Store


class TestAllProductTypes(unittest.TestCase):
    def setUp(self):
        self.products = [
            Groceries("Beras", 10000, 50, 8000),
            Food("Mie Instan", 3000, 20, 2000),
            Beverages("Teh Botol", 4000, 10, 2500),
            HouseholdItems("Sabun", 5000, 15, 3000)
        ]

    def test_get_price(self):
        for p in self.products:
            self.assertIsInstance(p.get_price(), int)

    def test_get_stock(self):
        for p in self.products:
            self.assertIsInstance(p.get_stock(), int)

    def test_capital_price(self):
        for p in self.products:
            self.assertIsInstance(p.get_capital_price(), int)

    def test_add_stock(self):
        for p in self.products:
            old = p.get_stock()
            result = p.add_stock(5)
            self.assertTrue(result)
            self.assertEqual(p.get_stock(), old + 5)

    def test_reduce_stock(self):
        for p in self.products:
            old = p.get_stock()
            result = p.reduce_stock(2)
            self.assertTrue(result)
            self.assertEqual(p.get_stock(), old - 2)

    def test_item_info(self):
        for p in self.products:
            info = p.item_info()
            self.assertIn(p.name, info)


class TestMixin(unittest.TestCase):
    def test_timestamp_update(self):
        product = Food("Roti", 5000, 10, 3000)
        before = product.get_timestamp()["updated_at"]

        product.add_stock(5)

        after = product.get_timestamp()["updated_at"]
        self.assertNotEqual(before, after)


class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.product = Beverages("Teh Botol", 4000, 10, 2500)
        self.transaction = Transaction("Chelsia")

    def test_add_to_cart_success(self):
        result = self.transaction.add_to_cart(self.product, 2)
        self.assertTrue(result)
        self.assertEqual(self.transaction.total, 8000)
        self.assertEqual(len(self.transaction.cart), 1)

    def test_add_to_cart_fail(self):
        result = self.transaction.add_to_cart(self.product, 20)
        self.assertFalse(result)

    def test_receipt_data(self):
        self.transaction.add_to_cart(self.product, 1)
        cart, total = self.transaction.get_receipt_data()

        self.assertEqual(total, 4000)
        self.assertEqual(cart[0]["name"], "Teh Botol")


class TestStore(unittest.TestCase):
    def setUp(self):
        self.store = Store("Toko ABC")
        self.product = Groceries("Beras", 10000, 50, 8000)

    def test_add_product(self):
        self.store.add_product(self.product)
        self.assertEqual(len(self.store.products), 1)

    def test_new_transaction(self):
        t = self.store.new_transaction("Chelsia")
        self.assertEqual(len(self.store.transactions), 1)
        self.assertIsInstance(t, Transaction)

    def test_stock_report(self):
        self.store.add_product(self.product)
        report = self.store.get_stock_report()

        self.assertEqual(report["Beras"], 50)

    def test_transaction_report(self):
        self.store.add_product(self.product)
        t = self.store.new_transaction("Chelsia")
        t.add_to_cart(self.product, 2)

        report = self.store.get_transaction_report()
        self.assertEqual(len(report), 1)


if __name__ == "__main__":
    unittest.main()