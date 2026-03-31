from Main_data import Groceries, Food, Beverages, HouseholdItems, Transaction, Store
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
    print("TERIMA KASIH ".center(40))
    print("=" * 40)
