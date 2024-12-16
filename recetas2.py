from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    ingredients = Column(String, nullable=False)
    steps = Column(String, nullable=False)

def connect_db():
    engine = create_engine('mysql+pymysql://user:password@localhost/recipe_book')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def add_recipe(session):
    name = input("Enter the recipe name: ")
    ingredients = input("Enter the ingredients (separated by commas): ")
    steps = input("Enter the steps: ")

    recipe = Recipe(name=name, ingredients=ingredients, steps=steps)
    session.add(recipe)
    session.commit()
    print("Recipe added successfully!")

def update_recipe(session):
    list_recipes(session)
    recipe_id = int(input("Enter the ID of the recipe to update: "))

    recipe = session.query(Recipe).get(recipe_id)
    if recipe:
        recipe.name = input("Enter the new recipe name: ")
        recipe.ingredients = input("Enter the new ingredients (separated by commas): ")
        recipe.steps = input("Enter the new steps: ")

        session.commit()
        print("Recipe updated successfully!")
    else:
        print("Recipe not found.")

def delete_recipe(session):
    list_recipes(session)
    recipe_id = int(input("Enter the ID of the recipe to delete: "))

    recipe = session.query(Recipe).get(recipe_id)
    if recipe:
        session.delete(recipe)
        session.commit()
        print("Recipe deleted successfully!")
    else:
        print("Recipe not found.")

def list_recipes(session):
    recipes = session.query(Recipe).all()

    if recipes:
        print("\nRecipes:")
        for recipe in recipes:
            print(f"{recipe.id}: {recipe.name}")
    else:
        print("No recipes found.")

def search_recipe(session):
    recipe_name = input("Enter the name of the recipe to search for: ")

    recipe = session.query(Recipe).filter(Recipe.name.like(f"%{recipe_name}%")).first()

    if recipe:
        print("\nIngredients:")
        print(recipe.ingredients)
        print("\nSteps:")
        print(recipe.steps)
    else:
        print("Recipe not found.")

def main():
    session = connect_db()

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
            add_recipe(session)
        elif choice == "2":
            update_recipe(session)
        elif choice == "3":
            delete_recipe(session)
        elif choice == "4":
            list_recipes(session)
        elif choice == "5":
            search_recipe(session)
        elif choice == "6":
            print("Goodbye!")
            session.close()
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
