import redis
import json

class RecipeBook:
    def __init__(self):
        self.client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

    def add_recipe(self):
        name = input("Enter the recipe name: ")
        ingredients = input("Enter the ingredients (separated by commas): ")
        steps = input("Enter the steps: ")

        recipe = {
            "ingredients": ingredients,
            "steps": steps
        }
        self.client.set(name, json.dumps(recipe))
        print("Recipe added successfully!")

    def update_recipe(self):
        self.list_recipes()
        name = input("Enter the name of the recipe to update: ")

        if self.client.exists(name):
            ingredients = input("Enter the new ingredients (separated by commas): ")
            steps = input("Enter the new steps: ")

            recipe = {
                "ingredients": ingredients,
                "steps": steps
            }
            self.client.set(name, json.dumps(recipe))
            print("Recipe updated successfully!")
        else:
            print("Recipe not found.")

    def delete_recipe(self):
        self.list_recipes()
        name = input("Enter the name of the recipe to delete: ")

        if self.client.delete(name):
            print("Recipe deleted successfully!")
        else:
            print("Recipe not found.")

    def list_recipes(self):
        keys = self.client.keys()

        if keys:
            print("\nRecipes:")
            for key in keys:
                print(f"- {key}")
        else:
            print("No recipes found.")

    def search_recipe(self):
        name = input("Enter the name of the recipe to search for: ")

        recipe = self.client.get(name)
        if recipe:
            recipe_data = json.loads(recipe)
            print("\nIngredients:")
            print(recipe_data["ingredients"])
            print("\nSteps:")
            print(recipe_data["steps"])
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
