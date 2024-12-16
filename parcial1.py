import sqlite3

class BudgetSystem:
    def __init__(self):
        self.conn = sqlite3.connect("budget.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL
            )
        """)
        self.conn.commit()

    def register_item(self):
        name = input("Enter the item name: ")
        category = input("Enter the item category: ")
        amount = float(input("Enter the amount: "))

        self.cursor.execute(
            (name, category, amount)
        )
        self.conn.commit()
        print("Item registered successfully!")

    def search_item(self):
        name = input("Enter the item name to search: ")
        self.cursor.execute("SELECT * FROM items WHERE name LIKE ?", (f"%{name}%",))
        results = self.cursor.fetchall()

        if results:
            print("\nSearch Results:")
            for item in results:
                print(f"ID: {item[0]}, Name: {item[1]}, Category: {item[2]}, Amount: {item[3]}")
        else:
            print("No items found.")

    def edit_item(self):
        self.list_items()
        item_id = int(input("Enter the ID of the item to edit: "))

        self.cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        item = self.cursor.fetchone()

        if item:
            name = input(f"Enter new name (current: {item[1]}): ") or item[1]
            category = input(f"Enter new category (current: {item[2]}): ") or item[2]
            amount = input(f"Enter new amount (current: {item[3]}): ")
            amount = float(amount) if amount else item[3]

            self.cursor.execute(
                (name, category, amount, item_id)
            )
            self.conn.commit()
            print("Item updated successfully!")
        else:
            print("Item not found.")

    def delete_item(self):
        self.list_items()
        item_id = int(input("Enter the ID of the item to delete: "))

        self.cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        self.conn.commit()
        if self.cursor.rowcount > 0:
            print("Item deleted successfully!")
        else:
            print("Item not found.")

    def list_items(self):
        self.cursor.execute("SELECT * FROM items")
        items = self.cursor.fetchall()

        if items:
            print("\nRegistered Items:")
            for item in items:
                print(f"ID: {item[0]}, Name: {item[1]}, Category: {item[2]}, Amount: {item[3]}")
        else:
            print("No items found.")

    def close(self):
        self.conn.close()

def main():
    budget_system = BudgetSystem()

    while True:
        print("\nBudget Management System")
        print("1. Register a new item")
        print("2. Search for an item")
        print("3. Edit an item")
        print("4. Delete an item")
        print("5. List all items")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            budget_system.register_item()
        elif choice == "2":
            budget_system.search_item()
        elif choice == "3":
            budget_system.edit_item()
        elif choice == "4":
            budget_system.delete_item()
        elif choice == "5":
            budget_system.list_items()
        elif choice == "6":
            print("Goodbye!")
            budget_system.close()
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()