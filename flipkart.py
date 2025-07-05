# flipkart.py
from models import view_products, place_order

class Product:
    def __init__(self, product_id, name, price, stock, description=""):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock
        self.description = description

class Store:
    def __init__(self):
        self.products = self.load_products()
        self.cart = []

    def load_products(self):
        db_products = view_products()
        products = []
        for row in db_products:
            pid, name, desc, price, stock = row
            products.append(Product(pid, name, price, stock, desc))
        return products

    def show_products(self):
        print("\n🛒 Available Products:")
        print("-" * 80)
        print(f"{'ID':<5}{'Name':<25}{'Price':<10}{'Stock':<10}Description")
        print("-" * 80)
        for p in self.products:
            print(f"{p.product_id:<5}{p.name:<25}₹{p.price:<10}{p.stock:<10}{p.description}")
        print("-" * 80)

    def add_to_cart(self, product_id, quantity):
        for product in self.products:
            if product.product_id == product_id:
                if quantity <= 0:
                    print("❌ Quantity must be at least 1.")
                    return
                if product.stock >= quantity:
                    self.cart.append((product, quantity))
                    product.stock -= quantity
                    print(f"✅ {quantity} x {product.name} added to cart.")
                    return
                else:
                    print("❌ Insufficient stock.")
                    return
        print("❌ Invalid product ID.")

    def view_cart(self):
        print("\n🛍️ Your Cart:")
        if not self.cart:
            print("🪹 Cart is empty.")
            return
        total = 0
        for item, quantity in self.cart:
            subtotal = item.price * quantity
            total += subtotal
            print(f"{item.name} x {quantity} = ₹{subtotal}")
        print(f"🧾 Total: ₹{total}")

    def checkout(self):
        if not self.cart:
            print("🪹 Your cart is empty.")
            return
        self.view_cart()
        try:
            customer_id_input = input("Enter your customer ID to place the order: ").strip()
            if not customer_id_input.isdigit():
                print("❌ Customer ID must be a number.")
                return
            customer_id = int(customer_id_input)

            items = [(item.product_id, quantity) for item, quantity in self.cart]
            order_id = place_order(customer_id, items)
            print(f"\n✅ Order placed successfully! Order ID: {order_id}")
            self.cart.clear()
        except Exception as e:
            print("❌ Failed to place order:", e)

def main():
    store = Store()
    while True:
        print("\n🧭 MENU:\n1. Show Products\n2. Add to Cart\n3. View Cart\n4. Checkout\n5. Exit")
        choice = input("Enter your choice: ").strip().lower()

        if choice in ['1', 'show products', 'show']:
            store.show_products()

        elif choice in ['2', 'add to cart', 'add']:
            try:
                pid_input = input("Enter product ID: ").strip()
                if not pid_input.isdigit():
                    print("❌ Product ID must be a number.")
                    continue
                pid = int(pid_input)

                qty_input = input("Enter quantity: ").strip()
                if not qty_input.isdigit():
                    print("❌ Quantity must be a number.")
                    continue
                qty = int(qty_input)

                store.add_to_cart(pid, qty)
            except Exception as e:
                print("⚠️ Unexpected error:", e)

        elif choice in ['3', 'view cart', 'cart']:
            store.view_cart()

        elif choice in ['4', 'checkout', 'check']:
            store.checkout()

        elif choice in ['5', 'exit', 'quit']:
            print("👋 Thank you for visiting! Have a great day.")
            break

        else:
            print("⚠️ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
