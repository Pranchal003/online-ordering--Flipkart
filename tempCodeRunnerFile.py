# flipkart.py
from models import view_products, place_order
class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"{self.product_id}. {self.name} - ₹{self.price} ({self.stock} left)"

class Store:
    def __init__(self):
        self.products = self.load_products()
        self.cart = []

    def load_products(self):
        db_products = view_products()
        products = []
        for row in db_products:
            pid, name, desc, price, stock = row
            products.append(Product(pid, name, price, stock))
        return products

    def show_products(self):
        print("\nAvailable Products:")
        for product in self.products:
            print(product)

    def add_to_cart(self, product_id, quantity):
        for product in self.products:
            if product.product_id == product_id:
                if product.stock >= quantity:
                    self.cart.append((product, quantity))
                    product.stock -= quantity  # Reduce in-memory stock
                    print(f"{quantity} x {product.name} added to cart.")
                    return
                else:
                    print("Insufficient stock.")
                    return
        print("Invalid product ID.")

    def view_cart(self):
        print("\nYour Cart:")
        if not self.cart:
            print("Cart is empty.")
            return
        total = 0
        for item, quantity in self.cart:
            subtotal = item.price * quantity
            total += subtotal
            print(f"{item.name} x {quantity} = ₹{subtotal}")
        print(f"Total: ₹{total}")

    def checkout(self):
        if not self.cart:
            print("Your cart is empty.")
            return
        self.view_cart()
        try:
            customer_id = int(input("Enter your customer ID to place the order: "))
            items = [(item.product_id, quantity) for item, quantity in self.cart]
            order_id = place_order(customer_id, items)
            print(f"\n✅ Order placed successfully! Order ID: {order_id}")
            self.cart.clear()
        except Exception as e:
            print("❌ Failed to place order:", e)

def main():
    store = Store()
    while True:
        print("\n1. Show Products\n2. Add to Cart\n3. View Cart\n4. Checkout\n5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            store.show_products()
        elif choice == '2':
            try:
                pid = int(input("Enter product ID: ").strip())
                qty = int(input("Enter quantity: ").strip())
                store.add_to_cart(pid, qty)
            except ValueError:
                print("Please enter valid numbers.")
        elif choice == '3':
            store.view_cart()
        elif choice == '4':
            store.checkout()
        elif choice == '5':
            print("Thank you for visiting!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
