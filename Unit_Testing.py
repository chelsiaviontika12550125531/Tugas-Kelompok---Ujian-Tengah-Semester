import unittest
from Main_data import Groceries, Food, Beverages, HouseholdItems, Transaction, Store


# =========================
# TEST PRODUCT (ALL TYPES)
# =========================
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
            old_stock = p.get_stock()
            result = p.add_stock(5)
            self.assertTrue(result)
            self.assertEqual(p.get_stock(), old_stock + 5)

    def test_add_stock_invalid(self):
        for p in self.products:
            result = p.add_stock(-5)
            self.assertFalse(result)

    def test_reduce_stock(self):
        for p in self.products:
            old_stock = p.get_stock()
            result = p.reduce_stock(2)
            self.assertTrue(result)
            self.assertEqual(p.get_stock(), old_stock - 2)

    def test_reduce_stock_fail(self):
        for p in self.products:
            result = p.reduce_stock(999)
            self.assertFalse(result)

    def test_item_info(self):
        expected_prefix = ["[GROCERY]", "[FOOD]", "[DRINK]", "[HOUSEHOLD]"]

        for p, prefix in zip(self.products, expected_prefix):
            info = p.item_info()
            self.assertTrue(info.startswith(prefix))
            self.assertIn(p.name, info)

    def test_polymorphism(self):
        for p in self.products:
            self.assertTrue(hasattr(p, "item_info"))


# =========================
# TEST MIXIN
# =========================
class TestMixin(unittest.TestCase):

    def test_timestamp_update(self):
        product = Food("Roti", 5000, 10, 3000)
        before = product.get_timestamp()["updated_at"]

        product.add_stock(5)

        after = product.get_timestamp()["updated_at"]
        self.assertNotEqual(before, after)


# =========================
# TEST TRANSACTION
# =========================
class TestTransaction(unittest.TestCase):

    def setUp(self):
        self.product = Beverages("Teh Botol", 4000, 10, 2500)
        self.transaction = Transaction()

    def test_add_to_cart_success(self):
        result = self.transaction.add_to_cart(self.product, 2)
        self.assertTrue(result)
        self.assertEqual(self.transaction.total, 8000)
        self.assertEqual(len(self.transaction.cart), 1)

    def test_add_to_cart_fail(self):
        result = self.transaction.add_to_cart(self.product, 20)
        self.assertFalse(result)
        self.assertEqual(self.transaction.total, 0)
        self.assertEqual(len(self.transaction.cart), 0)

    def test_receipt_data(self):
        self.transaction.add_to_cart(self.product, 1)
        cart, total = self.transaction.get_receipt_data()
        self.assertEqual(total, 4000)
        self.assertEqual(cart[0]["name"], "Teh Botol")

    def test_cart_content(self):
        self.transaction.add_to_cart(self.product, 2)
        item = self.transaction.cart[0]

        self.assertEqual(item["name"], "Teh Botol")
        self.assertEqual(item["amount"], 2)
        self.assertEqual(item["subtotal"], 8000)

    def test_stock_reduced_after_transaction(self):
        old_stock = self.product.get_stock()
        self.transaction.add_to_cart(self.product, 2)

        self.assertEqual(self.product.get_stock(), old_stock - 2)


# =========================
# TEST STORE
# =========================
class TestStore(unittest.TestCase):

    def setUp(self):
        self.store = Store("Toko ABC")
        self.product1 = Groceries("Beras", 10000, 50, 8000)
        self.product2 = HouseholdItems("Sabun", 5000, 20, 3000)

    def test_add_product(self):
        self.store.add_product(self.product1)
        self.assertEqual(len(self.store.products), 1)

    def test_multiple_products(self):
        self.store.add_product(self.product1)
        self.store.add_product(self.product2)
        self.assertEqual(len(self.store.products), 2)

    def test_get_products(self):
        self.store.add_product(self.product1)
        products = self.store.get_products()
        self.assertTrue(len(products) > 0)

    def test_new_transaction(self):
        t = self.store.new_transaction()
        self.assertEqual(len(self.store.transactions), 1)
        self.assertIsInstance(t, Transaction)

    def test_stock_report(self):
        self.store.add_product(self.product1)
        report = self.store.get_stock_report()
        self.assertEqual(report["Beras"], 50)

    def test_transaction_report(self):
        self.store.add_product(self.product1)
        t = self.store.new_transaction()
        t.add_to_cart(self.product1, 2)

        report = self.store.get_transaction_report()
        self.assertEqual(len(report), 1)



if __name__ == "__main__":
    unittest.main()