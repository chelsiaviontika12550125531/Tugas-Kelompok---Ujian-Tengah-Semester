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
        TimestampMixin.__init__(self)
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

    
    
    #pandas
    def get_stock_report_df(self):
        data = {
            "Product": [p.name for p in self.products],
            "Category": [p.category for p in self.products],
            "Stock": [p.get_stock() for p in self.products],
            "Price": [p.get_price() for p in self.products]
        }
        return pd.DataFrame(data)

    def get_transaction_report_df(self):
        data = []
        for t in self.transactions:
            cart, total = t.get_receipt_data()
            for item in cart:
                data.append({
                    "Product": item["name"],
                    "Amount": item["amount"],
                    "Subtotal": item["subtotal"],
                    "Total Transaction": total
                })
        return pd.DataFrame(data)





if __name__ == "__main__":
    store = Store("Toko Kelompok 6")

    p1 = Groceries("Beras", 10000, 50, 8000)
    p2 = Food("Mie Instan", 3000, 20, 2000)
    p3 = Beverages("Teh Botol", 5000, 30, 3500)
    p4 = HouseholdItems("Sabun Cuci", 7000, 25, 5000)
    p5 = Food("Roti", 8000, 15, 6000)
    p6 = Groceries("Gula", 12000, 40, 9000)
    
    store.add_product(p1)
    store.add_product(p2)
    store.add_product(p3)
    store.add_product(p4)
    store.add_product(p5)
    store.add_product(p6)

    t = store.new_transaction()
    t.add_to_cart(p1, 2)
    t.add_to_cart(p2, 3)
    t.add_to_cart(p3, 2)
    t.add_to_cart(p4, 1)

    print("=" * 40)
    print(f"{store.name:^40}")
    print("=" * 40)

    print("\n LIST PRODUK")
    print("-" * 80)
    print(f"{'Class':<15} | {'Nama':<15} | {'Kategori':<25} | {'Harga':<10} | Stock")
    print("-" * 80)

    for p in store.products:
        class_name = type(p).__name__
        print(f"{class_name:<15} | {p.name:<15} | {p.category:<25} | Rp{p.get_price():>6} | {p.get_stock()}")

    print("\n STOCK REPORT")
    print("-" * 40)
    stock = store.get_stock_report()
    for name, qty in stock.items():
        print(f"{name:<15} : {qty}")

    print("\n STOCK REPORT (TABLE)")
    print("-" * 40)
    df_stock = store.get_stock_report_df()
    print(df_stock.to_string(index=False))

    print("\n TRANSACTION DETAIL")
    print("-" * 40)
    cart, total = t.get_receipt_data()
    for item in cart:
        print(f"{item['name']:<15} x{item['amount']} = Rp{item['subtotal']}")

    print("-" * 40)
    print(f"{'TOTAL':<15} = Rp{total}")

    print("\n TRANSACTION REPORT (TABLE)")
    print("-" * 40)
    df_trans = store.get_transaction_report_df()
    print(df_trans.to_string(index=False))

    print("\n" + "=" * 40)
    print("TERIMA KASIH 🙏".center(40))
    print("=" * 40)