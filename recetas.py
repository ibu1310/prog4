
import sqlite3

def connect_db():
    """Connect to SQLite database or create one if it doesn't exist."""
    conn = sqlite3.connect("recipe_book.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            steps TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn

def add_recipe(conn):
    """Add a new recipe to the database."""
    name = input("Enter the recipe name: ")
    ingredients = input("Enter the ingredients (separated by commas): ")
    steps = input("Enter the steps: ")

    cursor = conn.cursor()
    cursor.execute("INSERT INTO recipes (name, ingredients, steps) VALUES (?, ?, ?)",
                   (name, ingredients, steps))
    conn.commit()
    print("Recipe added successfully!")

def update_recipe(conn):
    """Update an existing recipe."""
    list_recipes(conn)
    recipe_id = input("Enter the ID of the recipe to update: ")

    name = input("Enter the new recipe name: ")
    ingredients = input("Enter the new ingredients (separated by commas): ")
    steps = input("Enter the new steps: ")

    cursor = conn.cursor()
    cursor.execute("UPDATE recipes SET name = ?, ingredients = ?, steps = ? WHERE id = ?",
                   (name, ingredients, steps, recipe_id))
    conn.commit()
    print("Recipe updated successfully!")

def delete_recipe(conn):
    """Delete a recipe from the database."""
    list_recipes(conn)
    recipe_id = input("Enter the ID of the recipe to delete: ")

    cursor = conn.cursor()
    cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    conn.commit()
    print("Recipe deleted successfully!")

def list_recipes(conn):
    """List all recipes in the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM recipes")
    recipes = cursor.fetchall()

    if recipes:
        print("\nRecipes:")
        for recipe in recipes:
            print(f"{recipe[0]}: {recipe[1]}")
    else:
        print("No recipes found.")

def search_recipe(conn):
    """Search for a recipe's ingredients and steps."""
    recipe_name = input("Enter the name of the recipe to search for: ")

    cursor = conn.cursor()
    cursor.execute("SELECT ingredients, steps FROM recipes WHERE name LIKE ?", (f"%{recipe_name}%",))
    result = cursor.fetchone()

    if result:
        print("\nIngredients:")
        print(result[0])
        print("\nSteps:")
        print(result[1])
    else:
        print("Recipe not found.")

def main():
    """Main function to run the application."""
    conn = connect_db()

    while True:
        print("\nRecipe Book")
        print("1. Add a new recipe")
        print("2. Update an existing recipe")
        print("3. Delete a recipe")
        print("4. List all recipes")
        print("5. Search for ingredients and steps")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_recipe(conn)
        elif choice == "2":
            update_recipe(conn)
        elif choice == "3":
            delete_recipe(conn)
        elif choice == "4":
            list_recipes(conn)
        elif choice == "5":
            search_recipe(conn)
        elif choice == "6":
            print("Goodbye!")
            conn.close()
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()