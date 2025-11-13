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


# November 2024 Recipes (Protein-optimiert, Meal-Prep-kompatibel)
def create_apfel_zimt_overnight_oats_protein() -> MealieRecipe:
    """Create Apfel-Zimt Overnight Oats (Protein-optimiert) recipe."""
    ingredients = [
        MealieIngredient(title="Haferflocken", quantity=30, unit="g"),
        MealieIngredient(title="Hafermilch", quantity=150, unit="ml", note="ungesüßt"),
        MealieIngredient(title="Chiasamen", quantity=1, unit="EL"),
        MealieIngredient(title="Leinsamen", quantity=1, unit="EL", note="gemahlen"),
        MealieIngredient(title="Erbsenprotein-Pulver", quantity=20, unit="g", note="pur, ohne Zusätze"),
        MealieIngredient(title="Mandelmus", quantity=1, unit="EL"),
        MealieIngredient(title="Apfel", quantity=1, unit="Stück", note="morgens frisch schneiden"),
        MealieIngredient(title="Walnüsse", quantity=15, unit="g", note="gehackt"),
        MealieIngredient(title="Zimt", quantity=0.5, unit="TL")
    ]

    instructions = [
        create_instruction_step(
            "Haferflocken, Hafermilch, Chiasamen, Leinsamen, Erbsenprotein-Pulver, Mandelmus und Zimt in einem Schraubglas (400ml) gut vermischen.",
            1
        ),
        create_instruction_step(
            "Glas verschließen und über Nacht (mind. 6 Stunden) im Kühlschrank ziehen lassen.",
            2
        ),
        create_instruction_step(
            "Am Morgen: Apfel in kleine Würfel schneiden und zusammen mit gehackten Walnüssen auf die Overnight Oats geben.",
            3
        ),
        create_instruction_step(
            "Optional: Mit etwas zusätzlichem Zimt bestreuen und genießen.",
            4
        )
    ]

    nutrition = MealieNutrition(
        calories="390 kcal",
        protein="28g",
        carbohydrate="50g",
        fat="10g",
        fiber="11g"
    )

    return MealieRecipe(
        name="Apfel-Zimt Overnight Oats (Protein-optimiert)",
        description="Protein-reiches Frühstück mit 28g Protein pro Portion. Über Nacht vorbereitet, morgens nur noch Toppings hinzufügen. Perfekt für Meal Prep (bis zu 3 Tage haltbar).",
        recipe_yield="1 Portion",
        prep_time="PT5M",
        total_time="PT6H5M",
        ingredients=ingredients,
        instructions=instructions,
        nutrition=nutrition,
        tags=["Whole Food Challenge", "Frühstück", "Vegan", "Meal Prep", "High Protein"],
        categories=["Frühstück"]
    )


def create_kichererbsen_buddha_bowl_rohkost() -> MealieRecipe:
    """Create Kichererbsen-Buddha-Bowl mit Karotten-Gurken-Rohkost recipe."""
    ingredients = [
        MealieIngredient(title="Kichererbsen", quantity=120, unit="g", note="gekocht, geröstet"),
        MealieIngredient(title="Quinoa", quantity=80, unit="g", note="gekocht"),
        MealieIngredient(title="Brokkoli", quantity=80, unit="g", note="gedämpft"),
        MealieIngredient(title="Karotten", quantity=80, unit="g", note="in Julienne-Streifen, roh"),
        MealieIngredient(title="Gurke", quantity=50, unit="g", note="in Streifen, roh"),
        MealieIngredient(title="Avocado", quantity=0.25, unit="Stück"),
        MealieIngredient(title="Tahini-Dressing", quantity=2, unit="EL"),
        MealieIngredient(title="Kürbiskerne", quantity=1, unit="EL"),
        MealieIngredient(title="Petersilie", note="frisch, zum Garnieren")
    ]

    instructions = [
        create_instruction_step(
            "Quinoa kochen: 80g Quinoa mit 160ml Wasser 15 Min köcheln, 5 Min ruhen lassen.",
            1
        ),
        create_instruction_step(
            "Kichererbsen rösten: Mit 1 TL Kreuzkümmel, 1 TL Paprikapulver, 1 TL Knoblauchpulver würzen. Bei 200°C für 25 Min rösten bis knusprig.",
            2
        ),
        create_instruction_step(
            "Brokkoli dämpfen: In Röschen schneiden, 8 Min dämpfen, kalt abschrecken.",
            3
        ),
        create_instruction_step(
            "Rohkost vorbereiten: Karotten mit Gemüseschäler in dünne Julienne-Streifen schneiden. Gurke in Streifen schneiden.",
            4
        ),
        create_instruction_step(
            "Bowl zusammenstellen: Quinoa als Basis, alle Komponenten arrangieren (Kichererbsen, Brokkoli, Karotten-Julienne, Gurkenstreifen, Avocado).",
            5
        ),
        create_instruction_step(
            "Mit Tahini-Dressing beträufeln, Kürbiskerne darüberstreuen, mit Petersilie garnieren.",
            6
        )
    ]

    nutrition = MealieNutrition(
        calories="400 kcal",
        protein="24g",
        carbohydrate="54g",
        fat="16g",
        fiber="14g"
    )

    return MealieRecipe(
        name="Kichererbsen-Buddha-Bowl mit Karotten-Gurken-Rohkost",
        description="Meal-Prep-optimierte Buddha-Bowl mit rohem Gemüse statt geröstetem. Rohkost bleibt 4-5 Tage knackig! Perfekt für die Wochenvorbereitung.",
        recipe_yield="1 Portion",
        prep_time="PT10M",
        perform_time="PT25M",
        total_time="PT35M",
        ingredients=ingredients,
        instructions=instructions,
        nutrition=nutrition,
        tags=["Whole Food Challenge", "Lunch", "Vegan", "Meal Prep", "Bowl", "Rohkost"],
        categories=["Mittagessen"]
    )


def create_rotkohl_curry_tofu() -> MealieRecipe:
    """Create Rotkohl-Curry mit Kichererbsen und Tofu recipe."""
    ingredients = [
        MealieIngredient(title="Rotkohl", quantity=150, unit="g", note="fein geschnitten"),
        MealieIngredient(title="Kichererbsen", quantity=150, unit="g", note="gekocht"),
        MealieIngredient(title="Tofu", quantity=120, unit="g", note="gewürfelt"),
        MealieIngredient(title="Zwiebel", quantity=50, unit="g", note="gewürfelt"),
        MealieIngredient(title="Knoblauch", quantity=2, unit="Zehen", note="gehackt"),
        MealieIngredient(title="Currypaste", quantity=1.5, unit="EL", note="z.B. rote Currypaste"),
        MealieIngredient(title="Ingwer", quantity=1, unit="TL", note="frisch, gerieben"),
        MealieIngredient(title="Kokosmilch", quantity=100, unit="ml"),
        MealieIngredient(title="Gemüsebrühe", quantity=50, unit="ml"),
        MealieIngredient(title="Kurkuma", quantity=1, unit="TL"),
        MealieIngredient(title="Kreuzkümmel", quantity=0.5, unit="TL"),
        MealieIngredient(title="Kokosöl", quantity=1, unit="EL"),
        MealieIngredient(title="Quinoa", quantity=80, unit="g", note="gekocht, zum Servieren")
    ]

    instructions = [
        create_instruction_step(
            "Tofu würfeln und in 1 TL Kokosöl kräftig anbraten (5 Min), aus der Pfanne nehmen.",
            1
        ),
        create_instruction_step(
            "Zwiebel und Knoblauch im restlichen Öl glasig anbraten.",
            2
        ),
        create_instruction_step(
            "Currypaste, Ingwer, Kurkuma und Kreuzkümmel hinzufügen, 1 Min unter Rühren anbraten.",
            3
        ),
        create_instruction_step(
            "Rotkohl hinzugeben, 3 Min anbraten bis er etwas zusammenfällt.",
            4
        ),
        create_instruction_step(
            "Kichererbsen, Kokosmilch und Gemüsebrühe hinzufügen. 10 Min köcheln lassen.",
            5
        ),
        create_instruction_step(
            "Gebratenen Tofu zurück in die Pfanne geben, 2 Min mitköcheln. Mit Salz und Pfeffer abschmecken.",
            6
        ),
        create_instruction_step(
            "Über gekochte Quinoa servieren.",
            7
        )
    ]

    nutrition = MealieNutrition(
        calories="506 kcal",
        protein="42g",
        carbohydrate="52g",
        fat="18g",
        fiber="12g"
    )

    return MealieRecipe(
        name="Rotkohl-Curry mit Kichererbsen und Tofu (Protein-optimiert)",
        description="Protein-reiches Curry mit 42g Protein. Tofu wird separat angebraten für beste Textur. Schmeckt aufgewärmt noch besser - ideal für Meal Prep!",
        recipe_yield="1 Portion",
        prep_time="PT10M",
        perform_time="PT20M",
        total_time="PT30M",
        ingredients=ingredients,
        instructions=instructions,
        nutrition=nutrition,
        tags=["Whole Food Challenge", "Curry", "Vegan", "Meal Prep", "High Protein"],
        categories=["Mittagessen"]
    )


def create_buddha_bowl_linsen_tofu_rohkost() -> MealieRecipe:
    """Create Buddha-Bowl mit Linsen, Tofu und buntem Rohkost-Gemüse recipe."""
    ingredients = [
        MealieIngredient(title="Braune Linsen", quantity=120, unit="g", note="gekocht"),
        MealieIngredient(title="Tofu", quantity=120, unit="g", note="mariniert und angebraten"),
        MealieIngredient(title="Quinoa", quantity=80, unit="g", note="gekocht"),
        MealieIngredient(title="Karotten", quantity=100, unit="g", note="in Julienne-Streifen, roh"),
        MealieIngredient(title="Rote Bete", quantity=80, unit="g", note="gekocht, gewürfelt"),
        MealieIngredient(title="Rotkohl", quantity=80, unit="g", note="fein gehobelt, roh"),
        MealieIngredient(title="Tahini-Dressing", quantity=2, unit="EL"),
        MealieIngredient(title="Hanfsamen", quantity=1, unit="EL"),
        MealieIngredient(title="Kürbiskerne", quantity=1, unit="EL"),
        MealieIngredient(title="Petersilie", note="frisch, zum Garnieren"),
        MealieIngredient(title="Sojasauce", quantity=1, unit="EL", note="für Tofu-Marinade"),
        MealieIngredient(title="Ingwer", quantity=0.5, unit="TL", note="gerieben, für Marinade")
    ]

    instructions = [
        create_instruction_step(
            "Tofu-Marinade: Tofu in 2x2cm Würfel schneiden. Mit 1 EL Sojasauce und 0.5 TL Ingwer marinieren (mind. 30 Min).",
            1
        ),
        create_instruction_step(
            "Linsen kochen: 120g braune Linsen mit 300ml Wasser 20-25 Min köcheln bis bissfest.",
            2
        ),
        create_instruction_step(
            "Quinoa kochen: 80g Quinoa mit 160ml Wasser 15 Min köcheln, 5 Min ruhen lassen.",
            3
        ),
        create_instruction_step(
            "Rote Bete kochen: Würfeln, in Wasser 30 Min kochen bis weich (Handschuhe tragen!).",
            4
        ),
        create_instruction_step(
            "Rohkost vorbereiten: Karotten in Julienne-Streifen schneiden. Rotkohl fein hobeln. In luftdichten Containern lagern (hält 5 Tage!).",
            5
        ),
        create_instruction_step(
            "Tofu anbraten: Marinierten Tofu in heißer Pfanne 5-7 Min von allen Seiten goldbraun braten.",
            6
        ),
        create_instruction_step(
            "Bowl zusammenstellen: Quinoa als Basis, alle Komponenten arrangieren. Mit Tahini-Dressing beträufeln, Hanfsamen und Kürbiskerne darüberstreuen.",
            7
        )
    ]

    nutrition = MealieNutrition(
        calories="455 kcal",
        protein="36g",
        carbohydrate="58g",
        fat="16g",
        fiber="16g"
    )

    return MealieRecipe(
        name="Buddha-Bowl mit Linsen, Tofu und buntem Rohkost-Gemüse",
        description="Meal-Prep-freundliche Bowl mit Rohkost statt geröstetem Gemüse. Rohkost bleibt 4-5 Tage knackig! 36g Protein pro Portion.",
        recipe_yield="1 Portion",
        prep_time="PT15M",
        perform_time="PT30M",
        total_time="PT45M",
        ingredients=ingredients,
        instructions=instructions,
        nutrition=nutrition,
        tags=["Whole Food Challenge", "Dinner", "Vegan", "Meal Prep", "Bowl", "High Protein", "Rohkost"],
        categories=["Abendessen"]
    )


def create_linsen_feldsalat_rohkost() -> MealieRecipe:
    """Create Linsen-Feldsalat mit buntem Rohkost-Gemüse recipe."""
    ingredients = [
        MealieIngredient(title="Grüne Linsen", quantity=180, unit="g", note="gekocht"),
        MealieIngredient(title="Karotten", quantity=80, unit="g", note="in Julienne-Streifen, roh"),
        MealieIngredient(title="Gurke", quantity=60, unit="g", note="in Streifen, roh"),
        MealieIngredient(title="Feldsalat", quantity=80, unit="g", note="gewaschen"),
        MealieIngredient(title="Apfel", quantity=1, unit="Stück", note="dünn geschnitten"),
        MealieIngredient(title="Walnüsse", quantity=20, unit="g", note="gehackt"),
        MealieIngredient(title="Quinoa", quantity=80, unit="g", note="gekocht"),
        MealieIngredient(title="Apfel-Balsamico-Vinaigrette", quantity=2, unit="EL"),
        MealieIngredient(title="Apfelessig", quantity=1.5, unit="EL", note="für Dressing"),
        MealieIngredient(title="Balsamico", quantity=1, unit="EL", note="für Dressing"),
        MealieIngredient(title="Ahornsirup", quantity=0.5, unit="EL", note="für Dressing"),
        MealieIngredient(title="Dijon-Senf", quantity=0.5, unit="TL", note="für Dressing"),
        MealieIngredient(title="Olivenöl", quantity=0.5, unit="EL", note="für Dressing")
    ]

    instructions = [
        create_instruction_step(
            "Grüne Linsen kochen: 180g Linsen mit 450ml Wasser 25 Min köcheln bis bissfest. Abgießen, abkühlen lassen.",
            1
        ),
        create_instruction_step(
            "Quinoa kochen: 80g Quinoa mit 160ml Wasser 15 Min köcheln, 5 Min ruhen lassen.",
            2
        ),
        create_instruction_step(
            "Apfel-Balsamico-Vinaigrette: 1.5 EL Apfelessig, 1 EL Balsamico, 0.5 EL Ahornsirup, 0.5 TL Senf und 0.5 EL Olivenöl in Schraubglas schütteln.",
            3
        ),
        create_instruction_step(
            "Rohkost vorbereiten: Karotten in Julienne-Streifen schneiden. Gurke in Streifen schneiden. Feldsalat waschen.",
            4
        ),
        create_instruction_step(
            "Am Servieren: Apfel dünn schneiden, Walnüsse hacken.",
            5
        ),
        create_instruction_step(
            "Salat zusammenstellen: Quinoa und Linsen als Basis, Rohkost-Gemüse, Feldsalat, Apfel und Walnüsse hinzufügen. Mit Vinaigrette beträufeln.",
            6
        )
    ]

    nutrition = MealieNutrition(
        calories="420 kcal",
        protein="31g",
        carbohydrate="60g",
        fat="12g",
        fiber="18g"
    )

    return MealieRecipe(
        name="Linsen-Feldsalat mit buntem Rohkost-Gemüse (Protein-optimiert)",
        description="Leichter, protein-reicher Salat mit 31g Protein und 18g Ballaststoffen. Rohkost-Gemüse für optimale Meal-Prep-Haltbarkeit (4-5 Tage). Apfel und Walnüsse am besten frisch hinzufügen.",
        recipe_yield="1 Portion",
        prep_time="PT15M",
        perform_time="PT25M",
        total_time="PT40M",
        ingredients=ingredients,
        instructions=instructions,
        nutrition=nutrition,
        tags=["Whole Food Challenge", "Dinner", "Vegan", "Meal Prep", "Salat", "High Protein", "High Fiber", "Rohkost"],
        categories=["Abendessen"]
    )


# Example usage
if __name__ == "__main__":
    # Create November 2024 recipes (Protein-optimiert, Meal-Prep-kompatibel)
    recipes = [
        create_apfel_zimt_overnight_oats_protein(),
        create_kichererbsen_buddha_bowl_rohkost(),
        create_rotkohl_curry_tofu(),
        create_buddha_bowl_linsen_tofu_rohkost(),
        create_linsen_feldsalat_rohkost()
    ]

    # Export to files
    export_recipes_batch(recipes, output_dir="mealie_exports")

    print("\n📦 All recipes exported to mealie_exports/")
    print("📝 Import these JSON files directly into Mealie")
    print("\n🌟 November 2024 Recipes - Protein-optimiert & Meal-Prep-kompatibel:")
    print("   • Apfel-Zimt Overnight Oats (28g Protein)")
    print("   • Kichererbsen-Buddha-Bowl mit Rohkost (24g Protein)")
    print("   • Rotkohl-Curry mit Tofu (42g Protein)")
    print("   • Buddha-Bowl mit Linsen, Tofu und Rohkost (36g Protein)")
    print("   • Linsen-Feldsalat mit Rohkost (31g Protein)")
    print("\n✨ Alle Rezepte mit Rohkost für 4-5 Tage Meal-Prep-Haltbarkeit!")
