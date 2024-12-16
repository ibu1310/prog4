from pymongo import MongoClient

class RecipeBook:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["recipe_book"]
        self.collection = self.db["recipes"]

    def add_recipe(self):
        name = input("Enter the recipe name: ")
        ingredients = input("Enter the ingredients (separated by commas): ")
        steps = input("Enter the steps: ")

        recipe = {
            "name": name,
            "ingredients": ingredients,
            "steps": steps
        }
        self.collection.insert_one(recipe)
        print("Recipe added successfully!")

    def update_recipe(self):
        self.list_recipes()
        recipe_name = input("Enter the name of the recipe to update: ")

        recipe = self.collection.find_one({"name": recipe_name})
        if recipe:
            name = input("Enter the new recipe name: ")
            ingredients = input("Enter the new ingredients (separated by commas): ")
            steps = input("Enter the new steps: ")

            self.collection.update_one(
                {"_id": recipe["_id"]},
                {"$set": {"name": name, "ingredients": ingredients, "steps": steps}}
            )
            print("Recipe updated successfully!")
        else:
            print("Recipe not found.")

    def delete_recipe(self):
        self.list_recipes()
        recipe_name = input("Enter the name of the recipe to delete: ")

        result = self.collection.delete_one({"name": recipe_name})
        if result.deleted_count > 0:
            print("Recipe deleted successfully!")
        else:
            print("Recipe not found.")

    def list_recipes(self):
        recipes = self.collection.find()

        print("\nRecipes:")
        for recipe in recipes:
            print(f"- {recipe['name']}")

    def search_recipe(self):
        recipe_name = input("Enter the name of the recipe to search for: ")

        recipe = self.collection.find_one({"name": recipe_name})
        if recipe:
            print("\nIngredients:")
            print(recipe["ingredients"])
            print("\nSteps:")
            print(recipe["steps"])
        else:
            print("Recipe not found.")

def main():
    recipe_book = RecipeBook()

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
            recipe_book.add_recipe()
        elif choice == "2":
            recipe_book.update_recipe()
        elif choice == "3":
            recipe_book.delete_recipe()
        elif choice == "4":
            recipe_book.list_recipes()
        elif choice == "5":
            recipe_book.search_recipe()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
