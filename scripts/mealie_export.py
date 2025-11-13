#!/usr/bin/env python3
"""
Mealie Recipe Export Generator for Whole Food Challenge

Generates Mealie-compatible JSON recipe exports that can be imported
directly into Mealie for meal planning and tracking.
"""

import json
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class MealieIngredient:
    """Represents an ingredient in Mealie format."""
    title: str
    note: Optional[str] = None
    unit: Optional[str] = None
    quantity: Optional[float] = None
    original_text: Optional[str] = None
    
    def to_dict(self):
        """Convert to Mealie-compatible dictionary."""
        result = {"title": self.title}
        if self.note:
            result["note"] = self.note
        if self.unit:
            result["unit"] = {"name": self.unit}
        if self.quantity:
            result["quantity"] = self.quantity
        if self.original_text:
            result["originalText"] = self.original_text
        return result


@dataclass
class MealieNutrition:
    """Nutritional information in Mealie format."""
    calories: Optional[str] = None
    protein: Optional[str] = None
    carbohydrate: Optional[str] = None
    fat: Optional[str] = None
    fiber: Optional[str] = None
    
    def to_dict(self):
        """Convert to Mealie-compatible dictionary."""
        result = {}
        if self.calories:
            result["calories"] = self.calories
        if self.protein:
            result["protein"] = self.protein
        if self.carbohydrate:
            result["carbohydrateContent"] = self.carbohydrate
        if self.fat:
            result["fatContent"] = self.fat
        if self.fiber:
            result["fiberContent"] = self.fiber
        return result


@dataclass
class MealieRecipe:
    """Complete recipe in Mealie format."""
    name: str
    description: str
    recipe_yield: str  # e.g., "1 Portion"
    total_time: Optional[str] = None  # e.g., "PT15M" (15 minutes in ISO 8601)
    prep_time: Optional[str] = None
    perform_time: Optional[str] = None  # cooking/active time
    ingredients: List[MealieIngredient] = None
    instructions: List[Dict[str, str]] = None
    nutrition: Optional[MealieNutrition] = None
    tags: List[str] = None
    categories: List[str] = None
    
    def __post_init__(self):
        if self.ingredients is None:
            self.ingredients = []
        if self.instructions is None:
            self.instructions = []
        if self.tags is None:
            self.tags = ["Whole Food Challenge"]
        if self.categories is None:
            self.categories = []
    
    def to_dict(self):
        """Convert to Mealie-compatible dictionary."""
        result = {
            "name": self.name,
            "description": self.description,
            "recipeYield": self.recipe_yield,
            "recipeIngredient": [ing.to_dict() for ing in self.ingredients],
            "recipeInstructions": self.instructions,
            "tags": [{"name": tag} for tag in self.tags],
            "recipeCategory": [{"name": cat} for cat in self.categories]
        }
        
        if self.total_time:
            result["totalTime"] = self.total_time
        if self.prep_time:
            result["prepTime"] = self.prep_time
        if self.perform_time:
            result["performTime"] = self.perform_time
        if self.nutrition:
            result["nutrition"] = self.nutrition.to_dict()
        
        return result
    
    def to_json(self, indent=2):
        """Export as JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    def save_to_file(self, filename: str):
        """Save recipe to JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.to_json())


def minutes_to_iso8601(minutes: int) -> str:
    """Convert minutes to ISO 8601 duration format."""
    if minutes < 60:
        return f"PT{minutes}M"
    hours = minutes // 60
    remaining_minutes = minutes % 60
    if remaining_minutes:
        return f"PT{hours}H{remaining_minutes}M"
    return f"PT{hours}H"


def create_instruction_step(text: str, position: int) -> Dict[str, str]:
    """Create a single instruction step in Mealie format."""
    return {
        "text": text,
        "title": f"Schritt {position}"
    }


# Recipe Templates from Database
def create_overnight_oats() -> MealieRecipe:
    """Create Overnight Oats recipe."""
    ingredients = [
        MealieIngredient(title="Haferflocken", quantity=50, unit="g"),
        MealieIngredient(title="Hafermilch", quantity=150, unit="ml", note="ungesüßt"),
        MealieIngredient(title="Chiasamen", quantity=1, unit="EL"),
        MealieIngredient(title="Leinsamen", quantity=1, unit="EL", note="gemahlen"),
        MealieIngredient(title="Gemischte Beeren", quantity=100, unit="g", note="frisch oder TK"),
        MealieIngredient(title="Ahornsirup", quantity=1, unit="TL", note="optional"),
        MealieIngredient(title="Zimt", note="Prise")
    ]
    
    instructions = [
        create_instruction_step(
            "Haferflocken, Hafermilch, Chiasamen, Leinsamen und Zimt in einem Glas vermischen.",
            1
        ),
        create_instruction_step(
            "Über Nacht (mind. 6 Stunden) im Kühlschrank ziehen lassen.",
            2
        ),
        create_instruction_step(
            "Am Morgen mit gemischten Beeren toppen und optional mit Ahornsirup süßen.",
            3
        )
    ]
    
    nutrition = MealieNutrition(
        calories="320 kcal",
        protein="12g",
        carbohydrate="55g",
        fat="8g",
        fiber="10g"
    )
    
    return MealieRecipe(
        name="Overnight Oats mit Beeren",
        description="Einfaches, nährstoffreiches Frühstück für die Whole Food Challenge. Über Nacht vorbereitet, morgens sofort verzehrfertig.",
        recipe_yield="1 Portion",
        prep_time="PT5M",
        total_time="PT6H5M",  # includes overnight soaking
        ingredients=ingredients,
        instructions=instructions,
        nutrition=nutrition,
        tags=["Whole Food Challenge", "Frühstück", "Vegan", "Meal Prep"],
        categories=["Frühstück", "Overnight"]
    )


def create_buddha_bowl() -> MealieRecipe:
    """Create Kichererbsen-Buddha-Bowl recipe."""
    ingredients = [
        MealieIngredient(title="Kichererbsen", quantity=120, unit="g", note="gekocht"),
        MealieIngredient(title="Quinoa", quantity=80, unit="g", note="gekocht"),
        MealieIngredient(title="Brokkoli", quantity=80, unit="g", note="gedämpft"),
        MealieIngredient(title="Rotkohl", quantity=50, unit="g", note="roh, gehobelt"),
        MealieIngredient(title="Avocado", quantity=0.25, unit="Stück"),
        MealieIngredient(title="Kürbiskerne", quantity=1, unit="EL"),
        MealieIngredient(title="Tahini-Dressing", quantity=2, unit="EL")
    ]
    
    instructions = [
        create_instruction_step(
            "Kichererbsen auf einem Backblech mit Kreuzkümmel, Paprika und Knoblauchpulver würzen.",
            1
        ),
        create_instruction_step(
            "Bei 200°C ca. 20 Minuten rösten bis knusprig.",
            2
        ),
        create_instruction_step(
            "Quinoa als Basis in die Bowl geben.",
            3
        ),
        create_instruction_step(
            "Alle Komponenten (Kichererbsen, Brokkoli, Rotkohl, Avocado) arrangieren.",
            4
        ),
        create_instruction_step(
            "Mit Tahini-Dressing beträufeln und Kürbiskerne darüberstreuen.",
            5
        )
    ]
    
    nutrition = MealieNutrition(
        calories="420 kcal",
        protein="22g",
        carbohydrate="58g",
        fat="14g",
        fiber="15g"
    )
    
    return MealieRecipe(
        name="Kichererbsen-Buddha-Bowl",
        description="Ausgewogene Bowl mit gerösteten Kichererbsen, Quinoa und frischem Gemüse. Perfekt für Meal Prep.",
        recipe_yield="1 Portion",
        prep_time="PT10M",
        perform_time="PT20M",
        total_time="PT30M",
        ingredients=ingredients,
        instructions=instructions,
        nutrition=nutrition,
        tags=["Whole Food Challenge", "Lunch", "Vegan", "Meal Prep", "Bowl"],
        categories=["Mittagessen", "Bowl"]
    )


def create_rotkohl_curry() -> MealieRecipe:
    """Create Rotkohl-Curry-Mix recipe."""
    ingredients = [
        MealieIngredient(title="Rotkohl", quantity=150, unit="g", note="fein geschnitten"),
        MealieIngredient(title="Zwiebel", quantity=30, unit="g", note="gewürfelt"),
        MealieIngredient(title="Knoblauch", quantity=1, unit="Zehe", note="gehackt"),
        MealieIngredient(title="Currypaste", quantity=1, unit="TL"),
        MealieIngredient(title="Ingwer", quantity=0.5, unit="TL", note="frisch, gerieben"),
        MealieIngredient(title="Kokosmilch", quantity=75, unit="ml"),
        MealieIngredient(title="Gemüsebrühe", quantity=50, unit="ml"),
        MealieIngredient(title="Kurkuma", quantity=0.5, unit="TL"),
        MealieIngredient(title="Kreuzkümmel", quantity=0.25, unit="TL"),
        MealieIngredient(title="Kokosöl", quantity=1, unit="TL")
    ]
    
    instructions = [
        create_instruction_step(
            "Zwiebel und Knoblauch in Kokosöl glasig anbraten.",
            1
        ),
        create_instruction_step(
            "Currypaste, Ingwer, Kurkuma und Kreuzkümmel hinzufügen, kurz anbraten.",
            2
        ),
        create_instruction_step(
            "Rotkohl hinzugeben und 2-3 Minuten unter Rühren anbraten.",
            3
        ),
        create_instruction_step(
            "Kokosmilch und Gemüsebrühe hinzufügen.",
            4
        ),
        create_instruction_step(
            "15 Minuten köcheln lassen bis der Kohl weich ist. Mit Salz und Pfeffer abschmecken.",
            5
        )
    ]
    
    nutrition = MealieNutrition(
        calories="280 kcal",
        protein="8g",
        carbohydrate="25g",
        fat="18g",
        fiber="7g"
    )
    
    return MealieRecipe(
        name="Rotkohl-Curry-Mix",
        description="Würziges Rotkohl-Curry mit Kokosmilch. Ideal für Meal Prep, schmeckt aufgewärmt noch besser.",
        recipe_yield="1 Portion",
        prep_time="PT10M",
        perform_time="PT15M",
        total_time="PT25M",
        ingredients=ingredients,
        instructions=instructions,
        nutrition=nutrition,
        tags=["Whole Food Challenge", "Curry", "Vegan", "Meal Prep"],
        categories=["Abendessen", "Curry"]
    )


def export_recipes_batch(recipes: List[MealieRecipe], output_dir: str = "."):
    """
    Export multiple recipes to individual JSON files.
    
    Args:
        recipes: List of MealieRecipe objects
        output_dir: Directory to save files to
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    for recipe in recipes:
        # Create safe filename
        filename = recipe.name.lower().replace(" ", "_").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
        filename = f"{output_dir}/{filename}.json"
        recipe.save_to_file(filename)
        print(f"✅ Exported: {filename}")


# Example usage
if __name__ == "__main__":
    # Create example recipes
    recipes = [
        create_overnight_oats(),
        create_buddha_bowl(),
        create_rotkohl_curry()
    ]
    
    # Export to files
    export_recipes_batch(recipes, output_dir="mealie_exports")
    
    print("\n📦 All recipes exported to mealie_exports/")
    print("📝 Import these JSON files directly into Mealie")
