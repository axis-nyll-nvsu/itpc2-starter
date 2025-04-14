import requests

# API Configuration
BASE_URL = "http://localhost:5000/api/"


def display_menu():
    """Display the main menu"""
    print("\n" + "=" * 50)
    print("PRODUCT MANAGEMENT SYSTEM".center(50))
    print("=" * 50)
    print("1. List All Products")
    print("2. View Product Details")
    print("3. Add New Product")
    print("4. Update Product")
    print("5. Delete Product")
    print("6. Exit")
    print("=" * 50)


def list_products():
    """List all products"""
    try:
        response = requests.get(f"{BASE_URL}/products")
        if response.status_code == 200:
            products = response.json()
            if not products:
                print("\nNo products found!")
                return

            print("\n" + "-" * 70)
            print(f"{'ID':<5}{'Name':<30}{'Price':<15}{'Description':<20}")
            print("-" * 70)
            for product in products:
                print(
                    f"{product['id']:<5}{product['name']:<30}${float(product['price']):<14.2f}{product.get('description', '')[:20]:<20}")
            print("-" * 70)
        else:
            print(f"\nError fetching products: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")


def view_product():
    """View details of a specific product"""
    product_id = input("\nEnter product ID: ")
    try:
        response = requests.get(f"{BASE_URL}/products/{product_id}")
        if response.status_code == 200:
            product = response.json()
            print("\n" + "-" * 50)
            print("PRODUCT DETAILS".center(50))
            print("-" * 50)
            print(f"ID: {product['id']}")
            print(f"Name: {product['name']}")
            print(f"Price: ${float(product['price']):.2f}")
            print(f"Description: {product.get('description', 'N/A')}")
            print("-" * 50)
        elif response.status_code == 404:
            print("\nProduct not found!")
        else:
            print(f"\nError: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")


def add_product():
    """Add a new product"""
    print("\nEnter product details:")
    name = input("Name: ")
    price = input("Price: ")
    description = input("Description (optional): ")

    if not name or not price:
        print("\nName and price are required!")
        return

    try:
        price = float(price)
    except ValueError:
        print("\nPrice must be a number!")
        return

    product_data = {
        "name": name,
        "price": price,
        "description": description if description else ''
    }

    try:
        response = requests.post(f"{BASE_URL}/products", json=product_data)
        if response.status_code == 201:
            print("\nProduct added successfully!")
            new_product = response.json()
            print(f"New Product ID: {new_product['id']}")
        else:
            print(f"\nError adding product: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")


def update_product():
    """Update an existing product"""
    product_id = input("\nEnter product ID to update: ")

    # First get the current product details
    try:
        response = requests.get(f"{BASE_URL}/products/{product_id}")
        if response.status_code != 200:
            print(f"\nError: {response.text if response.status_code != 404 else 'Product not found!'}")
            return

        current_product = response.json()
        print("\nCurrent product details:")
        print(f"1. Name: {current_product['name']}")
        print(f"2. Price: ${current_product['price']:.2f}")
        print(f"3. Description: {current_product.get('description', 'N/A')}")

        print("\nEnter new values (leave blank to keep current):")
        updates = {}

        name = input("New name: ")
        if name: updates["name"] = name

        price = input("New price: ")
        if price:
            try:
                updates["price"] = float(price)
            except ValueError:
                print("Price must be a number!")
                return

        description = input("New description: ")
        if description: updates["description"] = description

        if not updates:
            print("\nNo changes made!")
            return

        try:
            response = requests.put(f"{BASE_URL}/products/{product_id}", json=updates)
            if response.status_code == 200:
                print("\nProduct updated successfully!")
            else:
                print(f"\nError updating product: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"\nConnection error: {e}")

    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")


def delete_product():
    """Delete a product"""
    product_id = input("\nEnter product ID to delete: ")
    confirm = input(f"Are you sure you want to delete product {product_id}? (y/n): ")

    if confirm.lower() != 'y':
        print("Deletion cancelled.")
        return

    try:
        response = requests.delete(f"{BASE_URL}/products/{product_id}")
        if response.status_code == 200:
            print("\nProduct deleted successfully!")
        else:
            print(f"\nError deleting product: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")


def main():
    """Main program loop"""
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ")

        if choice == '1':
            list_products()
        elif choice == '2':
            view_product()
        elif choice == '3':
            add_product()
        elif choice == '4':
            update_product()
        elif choice == '5':
            delete_product()
        elif choice == '6':
            print("\nExiting program. Goodbye!")
            break
        else:
            print("\nInvalid choice! Please enter a number between 1-6.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()