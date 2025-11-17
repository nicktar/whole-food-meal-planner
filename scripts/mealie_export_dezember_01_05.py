#!/usr/bin/env python3
"""
Mealie Recipe Export für Wochenplan Dezember 1-5, 2025
Generiert 14 Rezepte im schema.org Format für Mealie Import
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
    """Erstellt ein Mealie-kompatibles Rezept im schema.org Format."""
    recipe = {
        "@context": "https://schema.org",
        "@type": "Recipe",
        "name": name,
        "description": description,
        "prepTime": prep_time,
        "recipeIngredient": ingredients or [],
        "recipeInstructions": instructions,
        "keywords": f"whole food,Dezember 2025,meal prep,vegan,{meal_type},Woche 1-5"
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
    """Speichert Rezept als JSON Datei."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(recipe, f, indent=2, ensure_ascii=False)

    print(f"✅ Exportiert: {filepath}")


# ============================================================================
# FRÜHSTÜCK (4 Rezepte)
# ============================================================================

def create_overnight_oats_apfel_zimt():
    """Overnight Oats Apfel-Zimt (Mo, Fr)"""
    return create_recipe(
        name="Overnight Oats Apfel-Zimt",
        description="Protein-optimierte Overnight Oats mit Apfel und Zimt. Über Nacht vorbereiten, morgens genießen!",
        prep_time="PT2M",
        meal_type="Frühstück",
        ingredients=[
            "25g Haferflocken",
            "200ml Hafermilch (ungesüßt)",
            "1 EL gemahlene Leinsamen (10g)",
            "10g Mandelmus",
            "25g Erbsenprotein-Pulver (pur)",
            "150g Apfel, gewürfelt",
            "10g Walnüsse, gehackt",
            "1 TL Zimt",
            "Prise Salz"
        ],
        instructions="Am Vorabend alle Zutaten außer Walnüssen in ein Glas schichten.\nGut umrühren, verschließen, über Nacht im Kühlschrank quellen lassen.\nAm Morgen aus dem Kühlschrank nehmen, kurz umrühren, mit Walnüssen toppen, genießen!",
        calories="414 kcal",
        protein="30g",
        carbs="56g",
        fat="23g",
        fiber="10g"
    )


def create_overnight_oats_heidelbeeren():
    """Overnight Oats mit TK-Heidelbeeren (Mi)"""
    return create_recipe(
        name="Overnight Oats mit TK-Heidelbeeren",
        description="Protein-optimierte Overnight Oats mit TK-Heidelbeeren. Die Beeren tauen über Nacht auf und geben einen leckeren Geschmack!",
        prep_time="PT2M",
        meal_type="Frühstück",
        ingredients=[
            "25g Haferflocken",
            "200ml Hafermilch (ungesüßt)",
            "1 EL gemahlene Leinsamen (10g)",
            "10g Mandelmus",
            "25g Erbsenprotein-Pulver (pur)",
            "150g TK-Heidelbeeren",
            "10g Walnüsse, gehackt",
            "1 TL Zimt",
            "Prise Salz"
        ],
        instructions="Am Vorabend alle Zutaten außer Walnüssen in ein Glas schichten.\nGut umrühren, verschließen, über Nacht im Kühlschrank quellen lassen (TK-Beeren tauen auf).\nAm Morgen aus dem Kühlschrank nehmen, 5 Min antauen lassen, umrühren, mit Walnüssen toppen, genießen!",
        calories="422 kcal",
        protein="31g",
        carbs="56g",
        fat="22g",
        fiber="10g"
    )


def create_chia_pudding_tk_beeren():
    """Chia Pudding mit TK-Beeren (Di)"""
    return create_recipe(
        name="Chia Pudding mit TK-Beeren",
        description="Cremiger Chia Pudding mit gemischten TK-Beeren und Protein-Boost. Über Nacht vorbereiten!",
        prep_time="PT2M",
        meal_type="Frühstück",
        ingredients=[
            "2 EL Chiasamen (24g)",
            "250ml Hafermilch",
            "1/2 TL Vanilleextrakt",
            "25g Erbsenprotein-Pulver",
            "1 TL Zimt",
            "150g TK-Beeren gemischt (Heidelbeeren, Erdbeeren, Himbeeren)",
            "8g Walnüsse, gehackt",
            "5g Ahornsirup",
            "Prise Salz"
        ],
        instructions="Am Vorabend Chiasamen, Hafermilch, Vanilleextrakt, Erbsenprotein, Zimt und Salz in ein Glas geben.\nGut umrühren, verschließen, über Nacht im Kühlschrank quellen lassen.\nAm Morgen TK-Beeren leicht antauen lassen (5 Min), mit Ahornsirup und Walnüssen toppen, genießen!",
        calories="455 kcal",
        protein="28g",
        carbs="52g",
        fat="17g",
        fiber="12g"
    )


def create_chia_pudding_tk_kirschen():
    """Chia Pudding mit TK-Kirschen (Do)"""
    return create_recipe(
        name="Chia Pudding mit TK-Kirschen",
        description="Cremiger Chia Pudding mit TK-Kirschen und Protein-Boost. Die Kirschen geben eine herrlich fruchtige Note!",
        prep_time="PT2M",
        meal_type="Frühstück",
        ingredients=[
            "2 EL Chiasamen (24g)",
            "250ml Hafermilch",
            "1/2 TL Vanilleextrakt",
            "25g Erbsenprotein-Pulver",
            "1 TL Zimt",
            "150g TK-Kirschen (entsteint)",
            "8g Walnüsse, gehackt",
            "5g Ahornsirup",
            "Prise Salz"
        ],
        instructions="Am Vorabend Chiasamen, Hafermilch, Vanilleextrakt, Erbsenprotein, Zimt und Salz in ein Glas geben.\nGut umrühren, verschließen, über Nacht im Kühlschrank quellen lassen.\nAm Morgen TK-Kirschen leicht antauen lassen (5 Min), mit Ahornsirup und Walnüssen toppen, genießen!",
        calories="444 kcal",
        protein="28g",
        carbs="49g",
        fat="17g",
        fiber="12g"
    )


# ============================================================================
# MITTAGESSEN (5 Rezepte)
# ============================================================================

def create_linsen_curry_rotkohl_tofu():
    """Linsen-Curry mit Rotkohl und Tofu (Mo)"""
    return create_recipe(
        name="Linsen-Curry mit Rotkohl und Tofu",
        description="Wärmendes Curry mit grünen Linsen, Rotkohl und Tofu. Perfekt für kalte Dezembertage!",
        prep_time="PT15M",
        cook_time="PT15M",
        meal_type="Mittagessen",
        ingredients=[
            "150g Rotkohl, fein gehobelt",
            "160g gekochte grüne Linsen",
            "80g Tofu, gewürfelt",
            "1 TL Currypaste (10g)",
            "150ml Gemüsebrühe",
            "1 TL Ingwer, gerieben (5g)",
            "1 Knoblauchzehe, gehackt (3g)",
            "30g Zwiebel, gewürfelt",
            "1 TL Olivenöl",
            "1/2 TL Kurkuma, Kreuzkümmel",
            "Salz, Pfeffer"
        ],
        instructions="1. Olivenöl in Pfanne erhitzen, Zwiebel + Knoblauch 2 Min anbraten\n2. Currypaste, Ingwer, Gewürze dazugeben und kurz mitbraten\n3. Rotkohl + Tofu 3 Min anbraten\n4. Linsen + Gemüsebrühe hinzufügen, 10 Min köcheln lassen\n5. Mit Salz, Pfeffer abschmecken und servieren",
        calories="380 kcal",
        protein="24g",
        carbs="50g",
        fat="11g",
        fiber="18g"
    )


def create_kichererbsen_buddha_bowl_rotkohl():
    """Kichererbsen-Buddha-Bowl mit Rotkohl (Di)"""
    return create_recipe(
        name="Kichererbsen-Buddha-Bowl mit Rotkohl",
        description="Bunte Buddha Bowl mit gerösteten Kichererbsen, Quinoa, Brokkoli und mariniertem Rotkohl.",
        prep_time="PT5M",
        meal_type="Mittagessen",
        ingredients=[
            "100g Kichererbsen, geröstet mit Gewürzen (Kreuzkümmel, Paprika, Knoblauchpulver)",
            "80g Quinoa, gekocht",
            "80g Brokkoli, gedämpft",
            "50g Rotkohl, roh gehobelt und mariniert (Apfelessig, Zitrone)",
            "30g Tofu, gewürfelt",
            "8g Kürbiskerne",
            "Zitronen-Senf-Dressing:",
            "  - Saft 1/2 Zitrone",
            "  - 1 TL Olivenöl (5ml)",
            "  - 1 TL Dijon-Senf",
            "  - Salz, Pfeffer"
        ],
        instructions="Alle Komponenten in eine Bowl arrangieren.\nDressing aus Zitrone, Olivenöl, Senf, Salz und Pfeffer mischen.\nDressing über die Bowl träufeln.\nMit Kürbiskernen toppen und genießen!",
        calories="423 kcal",
        protein="20g",
        carbs="55g",
        fat="15g",
        fiber="14g"
    )


def create_geroesteter_rotkohl_linsen_tofu():
    """Gerösteter Rotkohl mit Linsen und Tofu (Mi)"""
    return create_recipe(
        name="Gerösteter Rotkohl mit Linsen und Tofu",
        description="Rotkohl-Wedges mit Ahornsirup-Glasur, dazu Linsen und Tofu auf Rucola. Einfach lecker!",
        prep_time="PT5M",
        meal_type="Mittagessen",
        ingredients=[
            "150g Rotkohl-Wedges, geröstet mit Ahornsirup-Glasur",
            "120g gekochte grüne Linsen",
            "90g Tofu, gewürfelt",
            "30g Rucola",
            "10g Walnüsse, geröstet",
            "Für den Rotkohl:",
            "  - 1 TL Olivenöl (Rösten)",
            "  - 5g Ahornsirup (Glasur)",
            "1/2 TL Balsamico-Essig",
            "Salz, Pfeffer"
        ],
        instructions="Rotkohl und Tofu kurz in der Pfanne oder im Ofen aufwärmen.\nMit gekochten Linsen und frischem Rucola auf einem Teller arrangieren.\nMit Balsamico beträufeln.\nMit gerösteten Walnüssen toppen und servieren.",
        calories="388 kcal",
        protein="22g",
        carbs="42g",
        fat="17g",
        fiber="15g"
    )


def create_pastinaken_karotten_curry_kichererbsen():
    """Pastinaken-Karotten-Curry mit Kichererbsen (Do)"""
    return create_recipe(
        name="Pastinaken-Karotten-Curry mit Kichererbsen",
        description="Winterliches Wurzelgemüse-Curry mit Pastinaken, Karotten, Kichererbsen und Tofu. Frisch gekocht am besten!",
        prep_time="PT15M",
        cook_time="PT15M",
        meal_type="Mittagessen",
        ingredients=[
            "120g Pastinaken, gewürfelt",
            "80g Karotten, gewürfelt",
            "110g Kichererbsen, gekocht",
            "80g Tofu, gewürfelt",
            "1 TL Currypaste (10g)",
            "150ml Gemüsebrühe",
            "1 TL Ingwer, gerieben",
            "1 Knoblauchzehe",
            "1/2 TL Kurkuma, Kreuzkümmel",
            "1 TL Olivenöl",
            "Frischer Koriander",
            "Salz, Pfeffer"
        ],
        instructions="1. Olivenöl in Pfanne erhitzen, Ingwer + Knoblauch anbraten\n2. Currypaste + Gewürze dazugeben und kurz mitbraten\n3. Pastinaken, Karotten und Tofu 5 Min anbraten\n4. Kichererbsen + Gemüsebrühe hinzufügen, 10 Min köcheln lassen\n5. Mit frischem Koriander garnieren und servieren",
        calories="439 kcal",
        protein="19g",
        carbs="57g",
        fat="14g",
        fiber="17g"
    )


def create_kichererbsen_bowl_rote_bete():
    """Kichererbsen-Bowl mit Rote Bete (Fr)"""
    return create_recipe(
        name="Kichererbsen-Bowl mit Rote Bete",
        description="Bunte Bowl mit gerösteten Kichererbsen, Rote Bete, Tofu und Tahini-Dressing.",
        prep_time="PT5M",
        meal_type="Mittagessen",
        ingredients=[
            "130g Kichererbsen, geröstet",
            "100g Rote Bete, gewürfelt",
            "80g Tofu, gewürfelt",
            "50g Karotten, roh gehobelt",
            "30g Feldsalat",
            "8g Kürbiskerne",
            "Zitronen-Tahini-Dressing (leicht):",
            "  - 1 TL Tahini (5g)",
            "  - Saft 1/2 Zitrone",
            "  - 2 EL Wasser",
            "  - Salz, Kreuzkümmel"
        ],
        instructions="Alle Komponenten in eine Bowl arrangieren.\nFür das Dressing Tahini, Zitronensaft, Wasser, Salz und Kreuzkümmel gut verrühren.\nDressing über die Bowl träufeln.\nMit Kürbiskernen toppen und genießen!",
        calories="421 kcal",
        protein="23g",
        carbs="54g",
        fat="14g",
        fiber="15g"
    )


# ============================================================================
# ABENDESSEN (5 Rezepte)
# ============================================================================

def create_rote_bete_salat_cannellini():
    """Rote-Bete-Salat mit Cannellini-Bohnen (Mo)"""
    return create_recipe(
        name="Rote-Bete-Salat mit Cannellini-Bohnen",
        description="Frischer Salat mit Rote Bete, Cannellini-Bohnen, Karotten und Walnüssen. Schnell zubereitet!",
        prep_time="PT5M",
        meal_type="Abendessen",
        ingredients=[
            "150g Rote Bete (vorgekocht), gewürfelt",
            "120g Cannellini-Bohnen, gekocht",
            "50g Karotten-Julienne (roh)",
            "40g Rucola",
            "40g Tofu, gewürfelt",
            "10g Walnüsse, gehackt",
            "Zitronen-Senf-Dressing:",
            "  - Saft 1/2 Zitrone",
            "  - 1 TL Olivenöl (5ml)",
            "  - 1 TL Dijon-Senf (5g)",
            "  - 1 TL Apfelessig",
            "  - Salz, Pfeffer, Kreuzkümmel"
        ],
        instructions="Alle Komponenten in eine große Bowl geben.\nFür das Dressing Zitronensaft, Olivenöl, Senf, Apfelessig und Gewürze gut verrühren.\nDressing über den Salat geben, gut vermischen.\nMit Walnüssen toppen und genießen!",
        calories="411 kcal",
        protein="20g",
        carbs="54g",
        fat="15g",
        fiber="14g"
    )


def create_linsen_feldsalat_apfel_tofu():
    """Linsen-Feldsalat mit Apfel und Tofu (Di)"""
    return create_recipe(
        name="Linsen-Feldsalat mit Apfel und Tofu",
        description="Frischer Salat mit grünen Linsen, Feldsalat, Apfel und Tofu. Perfekt für den Abend!",
        prep_time="PT5M",
        meal_type="Abendessen",
        ingredients=[
            "130g gekochte grüne Linsen",
            "50g Feldsalat",
            "80g Apfel, dünn geschnitten",
            "100g Kirschtomaten, halbiert",
            "50g Gurke, gewürfelt",
            "80g Tofu, gewürfelt",
            "10g Walnüsse, gehackt",
            "Apfelessig-Dressing:",
            "  - 2 EL Apfelessig",
            "  - 1 TL Olivenöl (5ml)",
            "  - 1 TL Dijon-Senf",
            "  - Salz, Pfeffer"
        ],
        instructions="Alle Komponenten in eine große Bowl geben.\nFür das Dressing Apfelessig, Olivenöl, Senf, Salz und Pfeffer gut verrühren.\nDressing über den Salat geben.\nMit Walnüssen toppen und genießen!",
        calories="401 kcal",
        protein="22g",
        carbs="46g",
        fat="17g",
        fiber="16g"
    )


def create_rote_bete_karotten_salat_cannellini():
    """Rote-Bete-Karotten-Salat mit Cannellini-Bohnen (Mi)"""
    return create_recipe(
        name="Rote-Bete-Karotten-Salat mit Cannellini-Bohnen",
        description="Bunter Wintersalat mit Rote Bete, gerösteten Karotten, Cannellini-Bohnen und Walnüssen.",
        prep_time="PT5M",
        meal_type="Abendessen",
        ingredients=[
            "120g Rote Bete, gewürfelt",
            "80g Karotten, geröstet",
            "110g Cannellini-Bohnen",
            "50g Tofu, gewürfelt",
            "40g Feldsalat",
            "10g Walnüsse, gehackt",
            "Für die Karotten:",
            "  - 1 TL Olivenöl (Karotten)",
            "Zitronen-Kreuzkümmel-Dressing:",
            "  - Saft 1/2 Zitrone",
            "  - 1 TL Olivenöl (5ml)",
            "  - 1/2 TL Kreuzkümmel",
            "  - Salz, Pfeffer"
        ],
        instructions="Alle Komponenten in eine große Bowl geben.\nFür das Dressing Zitronensaft, Olivenöl, Kreuzkümmel, Salz und Pfeffer gut verrühren.\nDressing über den Salat geben.\nMit Walnüssen toppen und genießen!",
        calories="439 kcal",
        protein="20g",
        carbs="50g",
        fat="19g",
        fiber="13g"
    )


def create_linsen_rucola_salat_rote_bete_tofu():
    """Linsen-Rucola-Salat mit Rote Bete und Tofu (Do)"""
    return create_recipe(
        name="Linsen-Rucola-Salat mit Rote Bete und Tofu",
        description="Proteinreicher Salat mit grünen Linsen, Rucola, Rote Bete, Tofu und Kirschtomaten.",
        prep_time="PT5M",
        meal_type="Abendessen",
        ingredients=[
            "145g gekochte grüne Linsen",
            "100g Rote Bete, gewürfelt",
            "40g Rucola",
            "80g Tofu, gewürfelt",
            "50g Kirschtomaten, halbiert",
            "10g Walnüsse, gehackt",
            "Zitronen-Dressing:",
            "  - Saft 1/2 Zitrone",
            "  - 1 TL Olivenöl (5ml)",
            "  - 1 TL Apfelessig",
            "  - Salz, Pfeffer"
        ],
        instructions="Alle Komponenten in eine große Bowl geben.\nFür das Dressing Zitronensaft, Olivenöl, Apfelessig, Salz und Pfeffer gut verrühren.\nDressing über den Salat geben.\nMit Walnüssen toppen und genießen!",
        calories="406 kcal",
        protein="24g",
        carbs="46g",
        fat="17g",
        fiber="16g"
    )


def create_cannellini_apfel_salat_haselnuesse():
    """Cannellini-Apfel-Salat mit Haselnüssen (Fr)"""
    return create_recipe(
        name="Cannellini-Apfel-Salat mit Haselnüssen",
        description="Herbstlicher Salat mit Cannellini-Bohnen, Apfel, Rote Bete und gerösteten Haselnüssen.",
        prep_time="PT5M",
        meal_type="Abendessen",
        ingredients=[
            "120g Cannellini-Bohnen",
            "100g Apfel, dünn geschnitten",
            "100g Rote Bete, gewürfelt",
            "40g Feldsalat",
            "50g Tofu, gewürfelt",
            "10g Haselnüsse, geröstet & gehackt",
            "Apfel-Balsamico-Dressing:",
            "  - 2 EL Apfelessig",
            "  - 1/2 TL Balsamico",
            "  - 1 TL Olivenöl (5ml)",
            "  - 5g Ahornsirup",
            "  - 1 TL Dijon-Senf",
            "  - Salz, Pfeffer"
        ],
        instructions="Alle Komponenten in eine große Bowl geben.\nFür das Dressing Apfelessig, Balsamico, Olivenöl, Ahornsirup, Senf, Salz und Pfeffer gut verrühren.\nDressing über den Salat geben.\nMit gerösteten Haselnüssen toppen und genießen!",
        calories="436 kcal",
        protein="20g",
        carbs="60g",
        fat="15g",
        fiber="14g"
    )


# ============================================================================
# MAIN EXPORT
# ============================================================================

if __name__ == "__main__":
    recipes = [
        # Frühstück
        ("2025_12_01_overnight_oats_apfel_zimt.json", create_overnight_oats_apfel_zimt()),
        ("2025_12_01_overnight_oats_heidelbeeren.json", create_overnight_oats_heidelbeeren()),
        ("2025_12_01_chia_pudding_tk_beeren.json", create_chia_pudding_tk_beeren()),
        ("2025_12_01_chia_pudding_tk_kirschen.json", create_chia_pudding_tk_kirschen()),

        # Mittagessen
        ("2025_12_01_linsen_curry_rotkohl_tofu.json", create_linsen_curry_rotkohl_tofu()),
        ("2025_12_01_kichererbsen_buddha_bowl_rotkohl.json", create_kichererbsen_buddha_bowl_rotkohl()),
        ("2025_12_01_geroesteter_rotkohl_linsen_tofu.json", create_geroesteter_rotkohl_linsen_tofu()),
        ("2025_12_01_pastinaken_karotten_curry_kichererbsen.json", create_pastinaken_karotten_curry_kichererbsen()),
        ("2025_12_01_kichererbsen_bowl_rote_bete.json", create_kichererbsen_bowl_rote_bete()),

        # Abendessen
        ("2025_12_01_rote_bete_salat_cannellini.json", create_rote_bete_salat_cannellini()),
        ("2025_12_01_linsen_feldsalat_apfel_tofu.json", create_linsen_feldsalat_apfel_tofu()),
        ("2025_12_01_rote_bete_karotten_salat_cannellini.json", create_rote_bete_karotten_salat_cannellini()),
        ("2025_12_01_linsen_rucola_salat_rote_bete_tofu.json", create_linsen_rucola_salat_rote_bete_tofu()),
        ("2025_12_01_cannellini_apfel_salat_haselnuesse.json", create_cannellini_apfel_salat_haselnuesse()),
    ]

    print("📦 Exportiere Dezember 1-5, 2025 Rezepte im schema.org Format...\n")

    for filename, recipe in recipes:
        save_recipe(recipe, filename)

    print("\n✅ Alle 14 Rezepte exportiert nach mealie_exports/")
    print("📝 Import diese JSON Files direkt in Mealie")
    print("\n🎯 Wochenplan Dezember 1-5, 2025 (14 Rezepte):")
    print("\n   FRÜHSTÜCK (4 Rezepte):")
    print("   • Overnight Oats Apfel-Zimt (414 kcal, 30g Protein)")
    print("   • Overnight Oats mit TK-Heidelbeeren (422 kcal, 31g Protein)")
    print("   • Chia Pudding mit TK-Beeren (455 kcal, 28g Protein)")
    print("   • Chia Pudding mit TK-Kirschen (444 kcal, 28g Protein)")
    print("\n   MITTAGESSEN (5 Rezepte):")
    print("   • Linsen-Curry mit Rotkohl und Tofu (380 kcal, 24g Protein)")
    print("   • Kichererbsen-Buddha-Bowl mit Rotkohl (423 kcal, 20g Protein)")
    print("   • Gerösteter Rotkohl mit Linsen und Tofu (388 kcal, 22g Protein)")
    print("   • Pastinaken-Karotten-Curry mit Kichererbsen (439 kcal, 19g Protein)")
    print("   • Kichererbsen-Bowl mit Rote Bete (421 kcal, 23g Protein)")
    print("\n   ABENDESSEN (5 Rezepte):")
    print("   • Rote-Bete-Salat mit Cannellini-Bohnen (411 kcal, 20g Protein)")
    print("   • Linsen-Feldsalat mit Apfel und Tofu (401 kcal, 22g Protein)")
    print("   • Rote-Bete-Karotten-Salat mit Cannellini-Bohnen (439 kcal, 20g Protein)")
    print("   • Linsen-Rucola-Salat mit Rote Bete und Tofu (406 kcal, 24g Protein)")
    print("   • Cannellini-Apfel-Salat mit Haselnüssen (436 kcal, 20g Protein)")
    print("\n✨ Alle im schema.org Format für Mealie Import!")
    print("🌟 Durchschnitt: 1259 kcal/Tag, 72g Protein/Tag")
