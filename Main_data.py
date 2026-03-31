from abc import ABC, abstractmethod
from datetime import datetime


class TimestampMixin:
    def __init__(self):
        self._created_at = datetime.now()
        self._updated_at = datetime.now()

    def touch(self):
        self._updated_at = datetime.now()

    def get_timestamp(self):
        return {
            "created_at": self._created_at,
            "updated_at": self._updated_at
        }


#abstract class
class BaseProduct(ABC, TimestampMixin):
    def __init__(self, name, price, stock, category, capital_price):
        TimestampMixin.__init__(self)
        self.name = name
        self._price = price              # enkapsulasi (protected)
        self._stock = stock              # enkapsulasi (protected)
        self.category = category
        self.__capital_price = capital_price  # enkapsulasi (private)

    #abstract method (fungsi)
    @abstractmethod
    def item_info(self):
        pass

    # GETTER
    def get_price(self):
        return self._price
    
    def get_stock(self):
        return self._stock
    
    def get_capital_price(self):
        return self.__capital_price

    # SETTER (dengan validasi)
    def reduce_stock(self, amount):
        if amount <= self._stock:
            self._stock -= amount
            self.touch()
            return True
        return False

    def add_stock(self, amount):
        if amount > 0:
            self._stock += amount
            self.touch()
            return True
        return False


#class turunan
class Groceries(BaseProduct):
    def __init__(self, name, price, stock, capital_price):
        super().__init__(name, price, stock, "Kebutuhan Pokok", capital_price)

    def item_info(self):
        return f"[GROCERY] {self.name} - {self._price} (Stock: {self._stock})"


class Food(BaseProduct):
    def __init__(self, name, price, stock, capital_price):
        super().__init__(name, price, stock, "Makanan", capital_price)

    def item_info(self):
        return f"[FOOD] {self.name} - {self._price} (Stock: {self._stock})"


class Beverages(BaseProduct):
    def __init__(self, name, price, stock, capital_price):
        super().__init__(name, price, stock, "Minuman", capital_price)

    def item_info(self):
        return f"[DRINK] {self.name} - {self._price} (Stock: {self._stock})"


class HouseholdItems(BaseProduct):
    def __init__(self, name, price, stock, capital_price):
        super().__init__(name, price, stock, "Kebutuhan Rumah Tangga", capital_price)

    def item_info(self):
        return f"[HOUSEHOLD] {self.name} - {self._price} (Stock: {self._stock})"





class Transaction:
    def __init__(self):
        self.cart = []
        self.total = 0

    def add_to_cart(self, product, amount):
        if product.get_stock() >= amount:
            product.reduce_stock(amount)
            subtotal = product.get_price() * amount
            self.cart.append({
                "name": product.name,
                "amount": amount,
                "subtotal": subtotal
            })
            self.total += subtotal
            return True
        return False

    def get_receipt_data(self):
        return self.cart, self.total




class Store:
    def __init__(self, name):
        self.name = name
        self.products = []
        self.transactions = []

    def add_product(self, product):
        self.products.append(product)

    def get_products(self):
        return [p.item_info() for p in self.products]

    def new_transaction(self):
        t = Transaction()
        self.transactions.append(t)
        return t

    def get_stock_report(self):
        return {p.name: p.get_stock() for p in self.products}

    def get_transaction_report(self):
        return [t.get_receipt_data() for t in self.transactions]