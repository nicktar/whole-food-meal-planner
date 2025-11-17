#!/usr/bin/env python3
"""
Mealie Export für korrigierten Wochenplan 15.-19. Dezember 2024
"""

import json
import re
from pathlib import Path
from typing import List, Dict

def extract_nutrition_values(nutrition_line: str) -> Dict[str, str]:
    """Extrahiert Nährwerte aus einer Zeile wie '470 kcal, 30.75g Protein, ...'"""
    nutrition = {}

    # Kalorien
    cal_match = re.search(r'(\d+)\s*kcal', nutrition_line)
    if cal_match:
        nutrition['calories'] = cal_match.group(1)

    # Protein
    prot_match = re.search(r'([\d.]+)g\s+Protein', nutrition_line)
    if prot_match:
        nutrition['proteinContent'] = prot_match.group(1)

    # Kohlenhydrate
    carb_match = re.search(r'([\d.]+)g\s+Kohlenhydrate', nutrition_line)
    if carb_match:
        nutrition['carbohydrateContent'] = carb_match.group(1)

    # Fett
    fat_match = re.search(r'([\d.]+)g\s+Fett', nutrition_line)
    if fat_match:
        nutrition['fatContent'] = fat_match.group(1)

    # Ballaststoffe
    fiber_match = re.search(r'([\d.]+)g\s+Ballaststoffe', nutrition_line)
    if fiber_match:
        nutrition['fiberContent'] = fiber_match.group(1)

    return nutrition

def parse_recipe_block(recipe_text: str, meal_type: str) -> Dict:
    """Parsed einen einzelnen Rezept-Block"""

    lines = recipe_text.split('\n')

    # Extrahiere Rezeptnamen aus der ersten Zeile
    name_match = re.search(r'###\s+(Frühstück|Mittagessen|Abendessen):\s+(.+?)(?:\s+\(|$)', lines[0])
    if not name_match:
        return None

    recipe_name = name_match.group(2).strip()

    # Finde Nährwerte
    nutrition_line = ""
    for line in lines:
        if line.startswith('**Nährwerte:**'):
            nutrition_line = line.replace('**Nährwerte:**', '').strip()
            break

    if not nutrition_line:
        return None

    nutrition = extract_nutrition_values(nutrition_line)

    # Extrahiere Zutaten
    ingredients = []
    in_ingredients = False
    for line in lines:
        if line.startswith('**Zutaten'):
            in_ingredients = True
            continue
        if in_ingredients:
            if line.startswith('**') or line.startswith('---'):
                break
            if line.strip().startswith('- '):
                ingredient = line.strip()[2:].strip()
                # Entferne Kommentare wie "← REDUZIERT!"
                ingredient = re.sub(r'\s*←.*$', '', ingredient)
                ingredient = re.sub(r'\s*\(.*?\)$', '', ingredient) # Entferne Kommentare in Klammern am Ende
                if ingredient and not ingredient.startswith('❌'):
                    ingredients.append(ingredient)

    # Extrahiere Zubereitungsanleitung
    instructions = []
    in_instructions = False
    for line in lines:
        if line.startswith('**Zubereitung'):
            in_instructions = True
            continue
        if in_instructions:
            if line.startswith('**') or line.startswith('---'):
                break
            if line.strip() and re.match(r'^\d+\.', line.strip()):
                instructions.append(line.strip())

    # Erstelle Mealie-kompatibles Rezept
    recipe = {
        "@context": "https://schema.org",
        "@type": "Recipe",
        "name": f"{recipe_name} - Korrigiert",
        "description": f"{meal_type} aus Wochenplan 15.-19. Dezember 2024 (korrigierte Nährwerte)",
        "recipeYield": "1 Portion",
        "recipeCategory": [meal_type, "Whole Food Challenge"],
        "keywords": ["whole food", "plant-based", "vollwertig", "pflanzlich"],
        "prepTime": "PT15M",
        "recipeIngredient": ingredients,
        "recipeInstructions": '\n'.join(instructions),
        "nutrition": {
            "@type": "NutritionInformation",
            **nutrition
        }
    }

    return recipe

def main():
    # Lese korrigierten Wochenplan
    plan_path = Path("meal-plans/wochenplan-2024-12-15-bis-19-KORRIGIERT.md")

    with open(plan_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Finde alle Rezept-Blöcke
    # Split nach TAG-Überschriften
    tag_blocks = re.split(r'## TAG \d+', content)

    recipes = []
    exported_names = set()  # Track welche Rezepte wir schon hatten

    for block in tag_blocks:
        # Finde alle Mahlzeiten in diesem Block
        for meal_type in ['Frühstück', 'Mittagessen', 'Abendessen']:
            # Finde Mahlzeit-Block
            pattern = f'### {meal_type}:.*?(?=### |## |$)'
            matches = re.finditer(pattern, block, re.DOTALL)

            for match in matches:
                recipe_text = match.group(0)

                # Überspringe, wenn es nur eine Referenz ist
                if '(siehe' in recipe_text.lower() or 'wiederholung' in recipe_text.lower():
                    continue

                recipe = parse_recipe_block(recipe_text, meal_type)

                if recipe and recipe['name'] not in exported_names:
                    recipes.append(recipe)
                    exported_names.add(recipe['name'])

    # Erstelle mealie_exports Verzeichnis falls nicht vorhanden
    export_dir = Path("mealie_exports")
    export_dir.mkdir(exist_ok=True)

    # Exportiere Rezepte
    print(f"\n📦 Exportiere {len(recipes)} Rezepte aus korrigiertem Wochenplan...")
    print("=" * 60)

    for recipe in recipes:
        # Erstelle sicheren Dateinamen
        safe_name = recipe['name'].lower()
        safe_name = re.sub(r'[^a-zäöüß0-9]+', '_', safe_name)
        safe_name = safe_name.strip('_')

        filename = export_dir / f"2024_12_15_{safe_name}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(recipe, f, indent=2, ensure_ascii=False)

        print(f"✅ {recipe['name']}")
        print(f"   → {filename}")

    print("=" * 60)
    print(f"✅ {len(recipes)} Rezepte erfolgreich exportiert!")
    print(f"📁 Ausgabeverzeichnis: {export_dir}/")
    print("\n💡 Import in Mealie:")
    print("   1. Gehe zu Recipes → Import")
    print("   2. Wähle 'JSON-LD' als Format")
    print("   3. Lade die JSON-Dateien hoch")

if __name__ == "__main__":
    main()
