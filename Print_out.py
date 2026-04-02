from Main_data import Groceries, Food, Beverages, HouseholdItems,Transaction, Store

users = [
    {"username": "admin", "password": "admin123", "role": "admin"},
    {"username": "kasir", "password": "123", "role": "kasir"}
]

def login():
    username = input("Username: ")
    password = input("Password: ")

    for user in users:
        if user["username"] == username and user["password"] == password:
            print(f"Login berhasil sebagai {user['role']}!\n")
            return user
    print("Login gagal!\n")
    return None


def admin_menu(store):
    while True:
        print("\n=== MENU ADMIN ===")
        print("1. Lihat Produk")
        print("2. Lihat Stock")
        print("3. Laporan Transaksi")
        print("0. Logout")

        pilih = input("Pilih: ")

        if pilih == "1":
            print("\n" + "=" * 50)
            print("DAFTAR PRODUK".center(50))
            print("=" * 50)
            print(f"{'No':<5} {'Nama':<20} {'Harga':<10} {'Stock':<10}")
            print("-" * 50)

            for i, p in enumerate(store.products):
                print(f"{i+1:<5} {p.name:<20} Rp{p.get_price():<8} {p.get_stock():<10}")

        elif pilih == "2":
            stock = store.get_stock_report()
            print("\n" + "=" * 40)
            print("STOCK REPORT".center(40))
            print("=" * 40)
            print(f"{'Produk':<20} {'Stock':<10}")
            print("-" * 40)

            for name, qty in stock.items():
                print(f"{name:<20} {qty:<10}")

        elif pilih == "3":
            df = store.get_transaction_report_df()

            if df.empty:
                print("\nBelum ada transaksi.")
            else:
                print("\n" + "=" * 60)
                print("LAPORAN TRANSAKSI".center(60))
                print("=" * 60)
                print(df.to_string(index=False))


        elif pilih == "0":
            break


def kasir_menu(store):
    while True:
        print("\n=== MENU KASIR ===")
        print("1. Transaksi Baru")
        print("0. Logout")

        pilih = input("Pilih: ")

        if pilih == "1":
            nama = input("Nama pelanggan: ")
            t = store.new_transaction(nama)

            while True:
                print("\nDaftar Produk:")
                print("-" * 50)

                for i, p in enumerate(store.products):
                    print(f"{i+1}. {p.name} - Rp{p.get_price()} (Stock: {p.get_stock()})")

                try:
                    pilih_produk = int(input("\nPilih produk (0 selesai): "))
                except:
                    print("Input harus angka!")
                    continue

                if pilih_produk == 0:
                    break

                jumlah = int(input("Jumlah: "))
                produk = store.products[pilih_produk - 1]

                if not t.add_to_cart(produk, jumlah):
                    print("Stock tidak cukup!")

            print("\n" + "=" * 50)
                        
            print("STRUK PEMBELIAN".center(50))
            print("=" * 50)
            print(f"Nama  : {nama}")
            print(f"ID    : {t.id}")
            print(f"Tgl   : {t.date.strftime('%Y-%m-%d %H:%M')}")
            print("-" * 50)

            print(f"{'Produk':<20} {'Qty':<5} {'Subtotal':<15}")
            print("-" * 50)

            cart, total = t.get_receipt_data()

            if not cart:
                print("Tidak ada pembelian.")
            else:
                for item in cart:
                    print(f"{item['name']:<20} {item['amount']:<5} Rp{item['subtotal']:<10}")

            print("-" * 50)
            print(f"{'TOTAL':<25} Rp{total}")
            print("=" * 50)
            print("Terima kasih!".center(50))
            print("=" * 50)

        elif pilih == "0" :
            break

if __name__ == "__main__":
    store = Store("Toko Kelompok 6")

    store.add_product(Groceries("Beras", 10000, 50, 8000))
    store.add_product(Food("Mie Instan", 3000, 20, 2000))
    store.add_product(Beverages("Teh Botol", 5000, 30, 3500))
    store.add_product(HouseholdItems("Sabun Cuci", 7000, 25, 5000))

    while True:
        print("\n=== MENU UTAMA ===")
        print("1. Login")
        print("0. Keluar")

        menu = input("Pilih: ")

        if menu == "1":
            user = login()
            if user:
                if user["role"] == "admin":
                    admin_menu(store)
                else:
                    kasir_menu(store)

        elif menu == "0":
            print("\nTerima Kasih sudah berbelanja di market kelompok 6\n")
            break