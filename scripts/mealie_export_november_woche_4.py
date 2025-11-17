#!/usr/bin/env python3
"""
Mealie Recipe Export für November Woche 4 (24.-28. November 2025)
Alle 15 Rezepte mit HYBRID-REDUKTION und korrekten Nährwerten
"""

import json
import os
from typing import List, Dict


def create_recipe(
    name: str,
    description: str,
    prep_time: str,
    cook_time: str = None,
    ingredients: List[str] = None,
    instructions: str = "",
    meal_type: str = "Mittagessen",
    calories: str = None,
    protein: str = None,
    carbs: str = None,
    fat: str = None,
    fiber: str = None
) -> Dict:
    """Create a Mealie-compatible recipe in schema.org format."""
    recipe = {
        "@context": "https://schema.org",
        "@type": "Recipe",
        "name": name,
        "description": description,
        "prepTime": prep_time,
        "recipeIngredient": ingredients or [],
        "recipeInstructions": instructions,
        "keywords": f"whole food,WFC,November 2025,HYBRID-Reduktion,{meal_type}"
    }

    if cook_time:
        recipe["performTime"] = cook_time

    nutrition = {}
    if calories:
        nutrition["calories"] = calories
    if protein:
        nutrition["proteinContent"] = protein
    if carbs:
        nutrition["carbohydrateContent"] = carbs
    if fat:
        nutrition["fatContent"] = fat
    if fiber:
        nutrition["fiberContent"] = fiber

    if nutrition:
        recipe["nutrition"] = nutrition

    return recipe


def save_recipe(recipe: Dict, filename: str, output_dir: str = "mealie_exports"):
    """Save recipe to JSON file."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(recipe, f, indent=2, ensure_ascii=False)

    print(f"✅ {filename}")


# ============================================================================
# FRÜHSTÜCKE (REDUZIERT)
# ============================================================================

recipes = []

# 1. Apfel-Zimt Overnight Oats
recipes.append(create_recipe(
    name="Apfel-Zimt Overnight Oats (REDUZIERT)",
    description="Halbe Portionen, keine Nüsse/Samen. Über Nacht vorbereiten, morgens genießen.",
    prep_time="PT5M",
    meal_type="Frühstück",
    calories="205",
    protein="12g",
    carbs="30g",
    fat="5g",
    fiber="4g",
    ingredients=[
        "15g Haferflocken",
        "75ml Hafermilch (ungesüßt)",
        "0.5 EL Mandelmus (7.5g)",
        "10g Erbsenprotein-Pulver",
        "0.5 mittelgroßer Apfel (75g), gewürfelt",
        "1 TL Zimt",
        "Prise Salz"
    ],
    instructions="Abends: Alle Zutaten in Schraubglas mischen, über Nacht kühl stellen.\nMorgens: Kurz umrühren und genießen!"
))

# 2. Haferbrei mit Beeren
recipes.append(create_recipe(
    name="Haferbrei mit Beeren (REDUZIERT)",
    description="Ersetzt Chia Pudding. Warm oder kalt genießbar.",
    prep_time="PT5M",
    cook_time="PT2M",
    meal_type="Frühstück",
    calories="204",
    protein="12g",
    carbs="26g",
    fat="5g",
    fiber="3g",
    ingredients=[
        "15g Haferflocken",
        "100ml Hafermilch",
        "0.5 EL Cashewmus (7.5g)",
        "10g Erbsenprotein-Pulver",
        "50g gemischte Beeren (TK)",
        "1/2 TL Vanillepulver",
        "Prise Salz"
    ],
    instructions="Variante 1 (kalt): Alle Zutaten außer Beeren in Glas mischen, über Nacht kühl stellen, morgens mit Beeren toppen.\nVariante 2 (warm): Haferflocken mit Hafermilch 2 Min kochen, Proteinpulver einrühren (nicht kochen!), mit TK-Beeren toppen."
))

# 3. Protein-Boost Oats
recipes.append(create_recipe(
    name="Overnight Oats Protein-Boost (REDUZIERT)",
    description="Minimalistisch! Alle Samen entfernt, maximale Kalorienreduktion.",
    prep_time="PT5M",
    meal_type="Frühstück",
    calories="189",
    protein="12g",
    carbs="23g",
    fat="5g",
    fiber="3g",
    ingredients=[
        "15g Haferflocken",
        "100ml Hafermilch",
        "0.5 EL Mandelmus (7.5g)",
        "10g Erbsenprotein-Pulver",
        "25g Beeren",
        "Prise Salz"
    ],
    instructions="Abends: Alle Zutaten gründlich vermischen.\nÜber Nacht im Kühlschrank quellen lassen.\nMorgens: Mit Beeren toppen und genießen!"
))

# 4. Quinoa-Frühstücksbowl
recipes.append(create_recipe(
    name="Quinoa-Frühstücksbowl (REDUZIERT)",
    description="Herzhaftes warmes Frühstück. Quinoa vorkochen für schnelle Zubereitung.",
    prep_time="PT5M",
    cook_time="PT3M",
    meal_type="Frühstück",
    calories="290",
    protein="16g",
    carbs="44g",
    fat="6g",
    fiber="5g",
    ingredients=[
        "30g Quinoa (roh) → 90g gekocht",
        "100ml Hafermilch",
        "12.5g Erbsenprotein-Pulver",
        "60g Apfel, gewürfelt",
        "1 TL Zimt",
        "0.5 EL getrocknete Cranberries (7.5g)",
        "0.5 EL Mandelmus (7.5g)",
        "Prise Salz"
    ],
    instructions="Meal Prep: Quinoa vorkochen, portionieren (5 Tage haltbar).\nMorgens: Quinoa mit Hafermilch und Proteinpulver 2-3 Min aufwärmen (nicht kochen!).\nApfel würfeln, mit Zimt, Cranberries und Mandelmus toppen."
))

# 5. Beeren-Power Oats
recipes.append(create_recipe(
    name="Beeren-Power Overnight Oats (REDUZIERT)",
    description="Alle Samen entfernt. Reich an Antioxidantien aus Beeren.",
    prep_time="PT5M",
    meal_type="Frühstück",
    calories="204",
    protein="14g",
    carbs="25g",
    fat="5g",
    fiber="3g",
    ingredients=[
        "15g Haferflocken",
        "75ml Hafermilch",
        "0.5 EL Mandelmus (7.5g)",
        "12.5g Erbsenprotein-Pulver",
        "50g gemischte Beeren",
        "Prise Zimt"
    ],
    instructions="Abends: Haferflocken, Hafermilch, Mandelmus, Proteinpulver und Zimt gründlich vermischen.\nGlas verschließen, über Nacht kühl stellen.\nMorgens: Mit Beeren toppen!"
))

# ============================================================================
# MITTAGESSEN (HYBRID-REDUKTION)
# ============================================================================

# 6. Kichererbsen-Buddha-Bowl
recipes.append(create_recipe(
    name="Kichererbsen-Buddha-Bowl mit Rote Bete",
    description="Farbenfroh, sättigend, meal-prep perfekt. Rote Bete ist saisonal!",
    prep_time="PT10M",
    cook_time="PT20M",
    meal_type="Mittagessen",
    calories="660",
    protein="35g",
    carbs="71g",
    fat="25g",
    fiber="20g",
    ingredients=[
        "130g Kichererbsen (gekocht)",
        "80g Quinoa (gekocht)",
        "100g Rote Bete (gekocht, gewürfelt)",
        "120g Tofu (gewürfelt, angebraten)",
        "50g Karotten (julienne, roh)",
        "1 TL Kreuzkümmel",
        "1 TL Paprikapulver",
        "1/2 TL Knoblauchpulver",
        "1.5 EL Tahini-Dressing (23g)",
        "1 EL Kürbiskerne",
        "Frische Petersilie",
        "Salz, Pfeffer"
    ],
    instructions="Meal Prep (Sonntag):\n1. Kichererbsen mit Gewürzen rösten (200°C, 20 Min)\n2. Quinoa kochen\n3. Rote Bete kochen/würfeln\n4. Tofu würfeln und anbraten\n5. Tahini-Dressing: Tahini + Zitronensaft + Wasser + Knoblauch\n\nTäglich: Quinoa aufwärmen, alle Komponenten in Bowl arrangieren, Dressing drüber, Kürbiskerne toppen."
))

# 7. Linsen-Salat
recipes.append(create_recipe(
    name="Linsen-Salat mit Rote Bete und Walnüssen",
    description="Frisch, eisenreich, proteinreich. Perfekter kalter Salat.",
    prep_time="PT10M",
    meal_type="Mittagessen",
    calories="462",
    protein="28g",
    carbs="54g",
    fat="15g",
    fiber="18g",
    ingredients=[
        "160g grüne Linsen (gekocht)",
        "120g Tofu (gewürfelt, angebraten)",
        "100g Rote Bete (gekocht, gewürfelt)",
        "50g Gurke (gewürfelt)",
        "30g Feldsalat",
        "12g Walnüsse (gehackt)",
        "Saft 1/2 Zitrone",
        "1 TL Olivenöl",
        "Salz, Pfeffer"
    ],
    instructions="Meal Prep: Linsen kochen, Tofu braten, Rote Bete kochen.\nTäglich: Alle Zutaten in Schüssel geben, mit Zitronensaft, Olivenöl, Salz und Pfeffer würzen, gut vermengen, Walnüsse toppen."
))

# 8. Kichererbsen-Curry
recipes.append(create_recipe(
    name="Kichererbsen-Curry mit Spinat und Tofu",
    description="Cremig-würzig, leicht reduzierte Kokosmilch. Wärmend und sättigend.",
    prep_time="PT10M",
    cook_time="PT15M",
    meal_type="Mittagessen",
    calories="690",
    protein="35g",
    carbs="65g",
    fat="32g",
    fiber="19g",
    ingredients=[
        "140g Kichererbsen (gekocht)",
        "120g Tofu (gewürfelt)",
        "80g Spinat (frisch)",
        "100g Champignons (geschnitten)",
        "1 TL Currypaste",
        "50ml Kokosmilch",
        "1 TL Ingwer (gerieben)",
        "Kurkuma, Kreuzkümmel",
        "80g Quinoa (gekocht)",
        "1 EL Kürbiskerne",
        "1 EL Kokosöl"
    ],
    instructions="Meal Prep: Kichererbsen + Quinoa vorkochen.\nTäglich: Kokosöl erhitzen, Tofu anbraten, Champignons + Currypaste + Gewürze anrösten, Kichererbsen + Kokosmilch + Spinat hinzufügen, 10 Min köcheln, über Quinoa servieren, Kürbiskerne toppen."
))

# 9. Rotkohl-Curry
recipes.append(create_recipe(
    name="Rotkohl-Curry mit Kichererbsen und Tofu",
    description="Violett-farbenfroh! Rotkohl hat November-Saison. Cremig-würzig.",
    prep_time="PT10M",
    cook_time="PT15M",
    meal_type="Mittagessen",
    calories="646",
    protein="30g",
    carbs="68g",
    fat="29g",
    fiber="18g",
    ingredients=[
        "150g Rotkohl (fein geschnitten)",
        "110g Kichererbsen (gekocht)",
        "120g Tofu (gewürfelt)",
        "1 TL Currypaste",
        "50ml Kokosmilch",
        "1 TL Ingwer (gerieben)",
        "Kurkuma, Kreuzkümmel",
        "80g Quinoa (gekocht)",
        "1 EL Hanfsamen",
        "1 EL Kokosöl"
    ],
    instructions="Kokosöl erhitzen, Tofu anbraten, Rotkohl + Currypaste + Gewürze anrösten, Kichererbsen + Kokosmilch hinzufügen, 10-12 Min köcheln bis Rotkohl weich, über Quinoa servieren, Hanfsamen toppen."
))

# 10. Pilz-Lauch-Pfanne
recipes.append(create_recipe(
    name="Pilz-Lauch-Pfanne mit Tofu und Quinoa",
    description="Umami-reich! Pilz-Nuss-Füllung vorkochen spart Zeit.",
    prep_time="PT10M",
    cook_time="PT15M",
    meal_type="Mittagessen",
    calories="471",
    protein="27g",
    carbs="45g",
    fat="20g",
    fiber="10g",
    ingredients=[
        "140g Pilze (Champignons + Shiitake)",
        "9g Walnüsse",
        "6g Cashews",
        "100g Lauch (in Ringen)",
        "150g Tofu (angebraten)",
        "60g Quinoa (gekocht)",
        "2 EL Sojasauce",
        "1 TL Olivenöl",
        "Paprika geräuchert, Thymian",
        "5g Hanfsamen"
    ],
    instructions="Meal Prep: Pilz-Füllung vorkochen (Pilze + Nüsse + Sojasauce + Gewürze braten, 5 Tage haltbar).\nTäglich: Pilz-Füllung mit Lauch in Pfanne aufwärmen, Tofu separat braten, über Quinoa servieren, Hanfsamen toppen."
))

# ============================================================================
# ABENDESSEN (HYBRID-REDUKTION)
# ============================================================================

# 11. Lauch-Miso-Suppe
recipes.append(create_recipe(
    name="Lauch-Miso-Suppe mit Tofu und Pilzen",
    description="Schnell, leicht, wärmend. Miso ist probiotisch (nicht kochen!).",
    prep_time="PT5M",
    cook_time="PT10M",
    meal_type="Abendessen",
    calories="327",
    protein="21g",
    carbs="36g",
    fat="11g",
    fiber="7g",
    ingredients=[
        "150g Lauch (in Ringen)",
        "130g Tofu (gewürfelt)",
        "100g Shiitake-Pilze",
        "1 EL Miso-Paste",
        "400ml Gemüsebrühe",
        "1 TL Ingwer (gerieben)",
        "2 Frühlingszwiebeln",
        "0.5 TL Sesamöl",
        "0.5 EL Hanfsamen (5g)",
        "Wakame (optional)"
    ],
    instructions="Gemüsebrühe erhitzen, Lauch + Pilze 5 Min köcheln, vom Herd nehmen, Miso-Paste einrühren (nicht kochen!), Tofu + Sesamöl hinzufügen, mit Frühlingszwiebeln + Hanfsamen + Wakame toppen."
))

# 12. Rotkohl-Salat Cannellini
recipes.append(create_recipe(
    name="Gerösteter Rotkohl-Salat mit Cannellini",
    description="Knuspriger gerösteter Rotkohl! Süß-herzhaft, saisonal.",
    prep_time="PT10M",
    cook_time="PT20M",
    meal_type="Abendessen",
    calories="562",
    protein="29g",
    carbs="60g",
    fat="23g",
    fiber="16g",
    ingredients=[
        "150g Rotkohl-Wedges",
        "140g Cannellini-Bohnen (gekocht)",
        "80g Tofu (gewürfelt)",
        "20g Walnüsse",
        "30g Rucola",
        "1 EL Kürbiskerne",
        "Ahornsirup, Balsamico",
        "Salz, Pfeffer"
    ],
    instructions="Meal Prep: Rotkohl in Wedges schneiden, mit Ahornsirup + Salz beträufeln, bei 200°C 20 Min rösten.\nTäglich: Gerösteten Rotkohl kurz aufwärmen, über Rucola servieren, mit Bohnen + Tofu + Walnüssen + Kürbiskernen toppen."
))

# 13. Pilz-Nuss-Bowl
recipes.append(create_recipe(
    name="Pilz-Nuss-Bowl mit Rote Bete und Quinoa",
    description="Umami-Bombe! Pilz-Füllung vorkochen für schnelles Abendessen.",
    prep_time="PT10M",
    cook_time="PT15M",
    meal_type="Abendessen",
    calories="444",
    protein="21g",
    carbs="47g",
    fat="19g",
    fiber="10g",
    ingredients=[
        "160g Pilze (Champignons, Shiitake)",
        "12g Walnüsse",
        "8g Cashews",
        "80g Quinoa (gekocht)",
        "80g Rote Bete (geröstet)",
        "50g Tofu",
        "5g Kürbiskerne",
        "2 EL Sojasauce",
        "Paprika, Thymian",
        "1 TL Olivenöl",
        "Petersilie"
    ],
    instructions="Meal Prep: Pilz-Nuss-Füllung vorkochen (Pilze + Nüsse braten, mit Sojasauce + Gewürzen abschmecken).\nTäglich: Füllung mit Quinoa + Rote Bete aufwärmen, Kürbiskerne + Petersilie toppen."
))

# 14. Linsen-Buddha-Bowl
recipes.append(create_recipe(
    name="Linsen-Buddha-Bowl mit Karotten und Tofu",
    description="Proteinreich! Roh + gekocht Mix, farbenfroh.",
    prep_time="PT10M",
    meal_type="Abendessen",
    calories="587",
    protein="34g",
    carbs="66g",
    fat="20g",
    fiber="20g",
    ingredients=[
        "140g grüne Linsen (gekocht)",
        "100g Tofu (mariniert, angebraten)",
        "70g Quinoa (gekocht)",
        "80g Karotten (julienne, roh)",
        "50g Kirschtomaten (halbiert)",
        "1.5 EL Tahini-Dressing (23g)",
        "1 EL Kürbiskerne",
        "5g Hanfsamen",
        "Petersilie"
    ],
    instructions="Alle Komponenten in Bowl arrangieren, Tahini-Dressing drüber, mit Kürbiskernen + Hanfsamen + Petersilie toppen."
))

# 15. Rotkohl-Apfel-Salat
recipes.append(create_recipe(
    name="Rotkohl-Apfel-Salat mit Cannellini",
    description="Frisch & knackig! Süß-sauer, saisonal (Rotkohl + Äpfel).",
    prep_time="PT15M",
    meal_type="Abendessen",
    calories="586",
    protein="25g",
    carbs="62g",
    fat="27g",
    fiber="16g",
    ingredients=[
        "120g Rotkohl (fein gehobelt)",
        "80g Apfel (dünn geschnitten)",
        "150g Cannellini-Bohnen (gekocht)",
        "80g Tofu (gewürfelt)",
        "15g Walnüsse (gehackt)",
        "2 EL Apfelessig",
        "1 EL Balsamico",
        "2 TL Ahornsirup",
        "1 TL Dijon-Senf",
        "2 TL Olivenöl"
    ],
    instructions="Rotkohl fein hobeln, mit Apfelessig marinieren (10 Min).\nVinaigrette: Balsamico + Ahornsirup + Senf + Olivenöl mixen.\nRotkohl mit Apfel + Bohnen + Tofu mischen, Vinaigrette drüber, Walnüsse toppen."
))

# ============================================================================
# EXPORT ALL RECIPES
# ============================================================================

if __name__ == "__main__":
    print("🚀 Exportiere November Woche 4 Rezepte für Mealie...\n")

    for i, recipe in enumerate(recipes, 1):
        filename = f"november-woche-4-{i:02d}-{recipe['name'].lower().replace(' ', '-').replace('ü', 'ue').replace('ö', 'oe').replace('ä', 'ae')}.json"
        save_recipe(recipe, filename)

    print(f"\n✅ Alle {len(recipes)} Rezepte exportiert nach mealie_exports/")
    print("📁 Import in Mealie: Settings → Importers → JSON → Upload Files")
