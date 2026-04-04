import pandas as pd
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


class BaseProduct(ABC, TimestampMixin):
    def __init__(self, name, price, stock, category, capital_price):
        super().__init__()
        self.name = name
        self._price = price
        self._stock = stock
        self.category = category
        self.__capital_price = capital_price

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

    # SETTER
    def reduce_stock(self, amount):
        if amount > 0 and amount <= self._stock:
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
    
    def set_stock(self, stock):
        if stock >= 0:
            self._stock = stock
            self.touch()
            return True
        return False


class Groceries(BaseProduct):
    def __init__(self, name, price, stock, capital_price):
        super().__init__(name, price, stock, "Kebutuhan Pokok", capital_price)

    def item_info(self):
        return f"[GROCERY] {self.name} - Rp{self._price} (Stock: {self._stock})"


class Food(BaseProduct):
    def __init__(self, name, price, stock, capital_price):
        super().__init__(name, price, stock, "Makanan", capital_price)

    def item_info(self):
        return f"[FOOD] {self.name} - Rp{self._price} (Stock: {self._stock})"


class Beverages(BaseProduct):
    def __init__(self, name, price, stock, capital_price):
        super().__init__(name, price, stock, "Minuman", capital_price)

    def item_info(self):
        return f"[DRINK] {self.name} - Rp{self._price} (Stock: {self._stock})"


class HouseholdItems(BaseProduct):
    def __init__(self, name, price, stock, capital_price):
        super().__init__(name, price, stock, "Kebutuhan Rumah Tangga", capital_price)

    def item_info(self):
        return f"[HOUSEHOLD] {self.name} - Rp{self._price} (Stock: {self._stock})"

class Transaction:
    _id_counter = 1  # auto increment ID

    def __init__(self, customer_name):
        self.id = Transaction._id_counter
        Transaction._id_counter += 1

        self.customer_name = customer_name
        self.cart = []
        self.total = 0
        self.date = datetime.now()

    def add_to_cart(self, product, amount):
        if product.reduce_stock(amount):
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

    def new_transaction(self, customer_name):
        new_transac  = Transaction(customer_name)
        self.transactions.append(new_transac)
        return new_transac

    def get_stock_report(self):
        return {new_product.name: new_product.get_stock() for new_product in self.products}

    def get_transaction_report(self):
        return [new_transac.get_receipt_data() for new_transac in self.transactions]

    # ===================== PANDAS =====================
    def get_stock_report_df(self):
        data = {
            "Product"   : [new_product.name for new_product in self.products],
            "Category"  : [new_product.category for new_product in self.products],
            "Stock"     : [new_product.get_stock() for new_product in self.products],
            "Price"     : [new_product.get_price() for new_product in self.products]
        }
        return pd.DataFrame(data)

    
    def get_transaction_report_df(self):
        data = []
        for new_transac in self.transactions:
            for item in new_transac.cart:
                data.append({
                    "Transaction ID": new_transac.id,
                    "Customer": new_transac.customer_name,
                    "Product": item["name"],
                    "Amount": item["amount"],
                    "Subtotal": item["subtotal"],
                    "Total": new_transac.total,
                    "Date": new_transac.date.strftime("%Y-%m-%d %H:%M")
                })
        return pd.DataFrame(data)
