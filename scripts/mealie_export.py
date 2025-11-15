#!/usr/bin/env python3
"""
Mealie Recipe Export Generator for Whole Food Challenge

Generates Mealie-compatible JSON recipe exports in schema.org format
that can be imported directly into Mealie for meal planning and tracking.
"""

import json
import os
from typing import List, Dict


def create_recipe(
    name: str,
    description: str,
    prep_time: str,  # ISO 8601 format like "PT15M"
    cook_time: str = None,
    ingredients: List[str] = None,
    instructions: str = "",  # Single string with \n line breaks
    meal_type: str = "Mittagessen",  # Frühstück, Mittagessen, oder Abendessen
    calories: str = None,
    protein: str = None,
    carbs: str = None,
    fat: str = None,
    fiber: str = None
) -> Dict:
    """
    Create a Mealie-compatible recipe in schema.org format.

    Args:
        name: Recipe name
        description: Recipe description
        prep_time: Preparation time in ISO 8601 format (e.g., "PT15M")
        cook_time: Cooking time in ISO 8601 format (optional)
        ingredients: List of ingredient strings (e.g., "50g Rote Linsen (ca. 100g gekocht)")
        instructions: Single string with \n line breaks
        meal_type: "Frühstück", "Mittagessen", or "Abendessen"
        calories, protein, carbs, fat, fiber: Nutrition info as strings

    Returns:
        Dictionary in schema.org format ready for JSON export
    """
    recipe = {
        "@context": "https://schema.org",
        "@type": "Recipe",
        "name": name,
        "description": description,
        "prepTime": prep_time,
        "recipeIngredient": ingredients or [],
        "recipeInstructions": instructions,
        "keywords": f"whole food,KI Rezepte,food prep,vegetarisch,vegan,{meal_type}"
    }

    if cook_time:
        recipe["performTime"] = cook_time

    # Add nutrition if provided
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

    print(f"✅ Exported: {filepath}")


# ============================================================================
# NOVEMBER 2024 RECIPES - Protein-optimiert & Meal-Prep-kompatibel
# ============================================================================

def create_apfel_zimt_overnight_oats_protein():
    """Apfel-Zimt Overnight Oats (Protein-optimiert)"""
    return create_recipe(
        name="Apfel-Zimt Overnight Oats (Protein-optimiert)",
        description="Protein-reiches Frühstück mit 28g Protein pro Portion. Über Nacht vorbereitet, morgens nur noch Toppings hinzufügen. Perfekt für Meal Prep (bis zu 3 Tage haltbar).",
        prep_time="PT5M",
        meal_type="Frühstück",
        ingredients=[
            "30g Haferflocken",
            "150ml Hafermilch (ungesüßt)",
            "1 EL Chiasamen",
            "1 EL Leinsamen (gemahlen)",
            "20g Erbsenprotein-Pulver (pur, ohne Zusätze)",
            "1 EL Mandelmus",
            "1 Apfel (morgens frisch schneiden)",
            "15g Walnüsse (gehackt)",
            "1/2 TL Zimt"
        ],
        instructions="""Haferflocken, Hafermilch, Chiasamen, Leinsamen, Erbsenprotein-Pulver, Mandelmus und Zimt in einem Schraubglas (400ml) gut vermischen.
Glas verschließen und über Nacht (mind. 6 Stunden) im Kühlschrank ziehen lassen.
Am Morgen: Apfel in kleine Würfel schneiden und zusammen mit gehackten Walnüssen auf die Overnight Oats geben.
Optional: Mit etwas zusätzlichem Zimt bestreuen und genießen.""",
        calories="390",
        protein="28g",
        carbs="50g",
        fat="10g",
        fiber="11g"
    )


def create_kichererbsen_buddha_bowl_rohkost():
    """Kichererbsen-Buddha-Bowl mit Karotten-Gurken-Rohkost"""
    return create_recipe(
        name="Kichererbsen-Buddha-Bowl mit Karotten-Gurken-Rohkost",
        description="Meal-Prep-optimierte Buddha-Bowl mit rohem Gemüse statt geröstetem. Rohkost bleibt 4-5 Tage knackig! Perfekt für die Wochenvorbereitung.",
        prep_time="PT10M",
        cook_time="PT25M",
        meal_type="Mittagessen",
        ingredients=[
            "40g Kichererbsen (ca. 120g gekocht, geröstet)",
            "30g Quinoa (ca. 80g gekocht)",
            "80g Brokkoli (gedämpft)",
            "80g Karotten (in Julienne-Streifen, roh)",
            "50g Gurke (in Streifen, roh)",
            "1/4 Avocado",
            "2 EL Tahini-Dressing",
            "1 EL Kürbiskerne",
            "Petersilie (frisch, zum Garnieren)"
        ],
        instructions="""Quinoa kochen: 30g Quinoa mit 60ml Wasser 15 Min köcheln, 5 Min ruhen lassen.
Kichererbsen rösten: Mit 1 TL Kreuzkümmel, 1 TL Paprikapulver, 1 TL Knoblauchpulver würzen. Bei 200°C für 25 Min rösten bis knusprig.
Brokkoli dämpfen: In Röschen schneiden, 8 Min dämpfen, kalt abschrecken.
Rohkost vorbereiten: Karotten mit Gemüseschäler in dünne Julienne-Streifen schneiden. Gurke in Streifen schneiden.
Bowl zusammenstellen: Quinoa als Basis, alle Komponenten arrangieren (Kichererbsen, Brokkoli, Karotten-Julienne, Gurkenstreifen, Avocado).
Mit Tahini-Dressing beträufeln, Kürbiskerne darüberstreuen, mit Petersilie garnieren.""",
        calories="400",
        protein="24g",
        carbs="54g",
        fat="16g",
        fiber="14g"
    )


def create_rotkohl_curry_tofu():
    """Rotkohl-Curry mit Kichererbsen und Tofu"""
    return create_recipe(
        name="Rotkohl-Curry mit Kichererbsen und Tofu (Protein-optimiert)",
        description="Protein-reiches Curry mit 42g Protein. Tofu wird separat angebraten für beste Textur. Schmeckt aufgewärmt noch besser - ideal für Meal Prep!",
        prep_time="PT10M",
        cook_time="PT20M",
        meal_type="Mittagessen",
        ingredients=[
            "150g Rotkohl (fein geschnitten)",
            "50g Kichererbsen (ca. 150g gekocht)",
            "120g Tofu (gewürfelt)",
            "50g Zwiebel (gewürfelt)",
            "2 Knoblauchzehen (gehackt)",
            "1,5 EL Currypaste (z.B. rote Currypaste)",
            "1 TL Ingwer (frisch, gerieben)",
            "100ml Kokosmilch",
            "50ml Gemüsebrühe",
            "1 TL Kurkuma",
            "1/2 TL Kreuzkümmel",
            "1 EL Kokosöl",
            "30g Quinoa (ca. 80g gekocht, zum Servieren)"
        ],
        instructions="""Tofu würfeln und in 1 TL Kokosöl kräftig anbraten (5 Min), aus der Pfanne nehmen.
Zwiebel und Knoblauch im restlichen Öl glasig anbraten.
Currypaste, Ingwer, Kurkuma und Kreuzkümmel hinzufügen, 1 Min unter Rühren anbraten.
Rotkohl hinzugeben, 3 Min anbraten bis er etwas zusammenfällt.
Kichererbsen, Kokosmilch und Gemüsebrühe hinzufügen. 10 Min köcheln lassen.
Gebratenen Tofu zurück in die Pfanne geben, 2 Min mitköcheln. Mit Salz und Pfeffer abschmecken.
Über gekochte Quinoa servieren.""",
        calories="506",
        protein="42g",
        carbs="52g",
        fat="18g",
        fiber="12g"
    )


def create_lauch_miso_suppe_tofu():
    """Lauch-Miso-Suppe mit Tofu und Pilzen"""
    return create_recipe(
        name="Lauch-Miso-Suppe mit Tofu und Pilzen",
        description="Leichte, aromatische Suppe mit 28g Protein. Miso-Paste erst am Ende hinzufügen (nicht kochen!). Frisch zubereiten für bestes Aroma - 15 Min am Morgen.",
        prep_time="PT10M",
        cook_time="PT10M",
        meal_type="Mittagessen",
        ingredients=[
            "150g Lauch/Porree (in Ringe geschnitten)",
            "150g Tofu (gewürfelt)",
            "100g Shiitake-Pilze (in Scheiben)",
            "2 EL Miso-Paste (helle oder dunkle)",
            "500ml Gemüsebrühe",
            "1 TL Ingwer (frisch, gerieben)",
            "2 Frühlingszwiebeln (in Ringe)",
            "1 EL Hanfsamen (zum Topping)",
            "1/2 TL Sesamöl (zum Verfeinern)"
        ],
        instructions="""Lauch in feine Ringe schneiden, gründlich waschen. Shiitake-Pilze in Scheiben schneiden.
Tofu in kleine Würfel schneiden.
Gemüsebrühe in Topf zum Kochen bringen. Ingwer hinzufügen.
Lauch und Pilze hinzugeben, 5 Min köcheln lassen.
Tofu-Würfel hinzufügen, weitere 3 Min köcheln.
Hitze ausschalten. Miso-Paste in etwas Brühe auflösen, dann in die Suppe einrühren (NICHT kochen, sonst verliert Miso Nährstoffe!).
Mit Frühlingszwiebeln, Hanfsamen und einem Tropfen Sesamöl servieren.""",
        calories="335",
        protein="28g",
        carbs="28g",
        fat="12g",
        fiber="9g"
    )


def create_vollkorn_wrap_pilz_nuss():
    """Vollkorn-Wrap mit Pilz-Nuss-Füllung und mariniertem Rotkohl"""
    return create_recipe(
        name="Vollkorn-Wrap mit Pilz-Nuss-Füllung und mariniertem Rotkohl",
        description="Herzhafter Wrap mit 28g Protein. Pilz-Nuss-Füllung hält 4-5 Tage, Wrap morgens frisch zusammenstellen. Marinierter Rotkohl gibt würzigen Kick!",
        prep_time="PT15M",
        cook_time="PT12M",
        meal_type="Mittagessen",
        ingredients=[
            "1 Vollkorn-Wrap (groß)",
            "150g gemischte Pilze (klein gehackt)",
            "20g Walnüsse (fein gehackt)",
            "15g Cashews (fein gehackt)",
            "60g Rotkohl (fein gehobelt, mariniert)",
            "50g Hummus",
            "20g Rucola (frisch)",
            "1 EL Tahini-Dressing",
            "1,5 EL Sojasauce (für Pilzfüllung)",
            "1/2 TL Ahornsirup (für Pilzfüllung)",
            "1/2 TL Paprika geräuchert (für Pilzfüllung)",
            "2 EL Apfelessig (für Rotkohl-Marinade)",
            "1/2 TL Kreuzkümmel (für Rotkohl)"
        ],
        instructions="""Rotkohl marinieren: 60g fein gehobelten Rotkohl mit 2 EL Apfelessig, 1 TL Ahornsirup, Zitronensaft und Kreuzkümmel kräftig massieren. Mind. 1h ziehen lassen.
Pilz-Nuss-Füllung: Pilze klein hacken, trocken in Pfanne anbraten bis Wasser verdampft (5 Min).
1 TL Olivenöl, 1 Knoblauchzehe hinzufügen. Walnüsse und Cashews (fein gehackt) hinzufügen.
1,5 EL Sojasauce, 1/2 TL Ahornsirup, geräucherte Paprika und Thymian hinzufügen. 5-7 Min braten bis goldbraun.
Wrap zusammenstellen: Hummus auf Wrap streichen. Pilz-Nuss-Füllung, marinierten Rotkohl und Rucola darauf verteilen.
Mit Tahini-Dressing beträufeln. Wrap fest einrollen, halbieren und servieren.""",
        calories="450",
        protein="28g",
        carbs="52g",
        fat="16g",
        fiber="12g"
    )


def create_kichererbsen_curry_spinat_tofu():
    """Kichererbsen-Curry mit Spinat, Pilzen und Tofu"""
    return create_recipe(
        name="Kichererbsen-Curry mit Spinat, Pilzen und Tofu",
        description="Protein-reiches Curry mit 41g Protein! Tofu wird separat angebraten für perfekte Textur. Spinat erst am Ende hinzufügen. Frisch zubereiten - 20 Min.",
        prep_time="PT10M",
        cook_time="PT20M",
        meal_type="Mittagessen",
        ingredients=[
            "50g Kichererbsen (ca. 150g gekocht)",
            "150g Tofu (gewürfelt)",
            "100g Champignons (in Scheiben)",
            "80g Spinat (frisch)",
            "50g Zwiebel (gewürfelt)",
            "2 Knoblauchzehen (gehackt)",
            "2 EL Currypaste (z.B. gelbe Currypaste)",
            "1 TL Ingwer (frisch, gerieben)",
            "150ml Kokosmilch",
            "50ml Gemüsebrühe",
            "1 TL Kurkuma",
            "1/2 TL Kreuzkümmel",
            "1 EL Kokosöl",
            "30g Quinoa (ca. 80g gekocht, zum Servieren)",
            "1 EL Kürbiskerne (zum Topping)"
        ],
        instructions="""Tofu würfeln und in 1 TL Kokosöl kräftig anbraten (5 Min), aus der Pfanne nehmen.
Zwiebel und Knoblauch im restlichen Öl glasig anbraten.
Champignons hinzufügen, 3 Min anbraten.
Currypaste, Ingwer, Kurkuma und Kreuzkümmel hinzufügen, 1 Min unter Rühren anbraten.
Kichererbsen, Kokosmilch und Gemüsebrühe hinzufügen. 10 Min köcheln lassen.
Spinat und gebratenen Tofu hinzufügen, 2 Min mitköcheln bis Spinat zusammenfällt. Mit Salz und Pfeffer abschmecken.
Über gekochte Quinoa servieren, mit Kürbiskernen bestreuen.""",
        calories="540",
        protein="41g",
        carbs="56g",
        fat="18g",
        fiber="13g"
    )


def create_rotkohl_apfel_salat_tofu():
    """Rotkohl-Apfel-Salat mit Cannellini-Bohnen und mariniertem Tofu"""
    return create_recipe(
        name="Rotkohl-Apfel-Salat mit Cannellini-Bohnen und mariniertem Tofu",
        description="Protein-reicher Salat mit 33g Protein. Frischer Rotkohl kombiniert mit gebratenen Tofu-Würfeln. Dressing separat lagern für Meal Prep!",
        prep_time="PT15M",
        cook_time="PT7M",
        meal_type="Abendessen",
        ingredients=[
            "120g Rotkohl (fein gehobelt)",
            "80g Cannellini-Bohnen (ca. 120g gekocht)",
            "180g Tofu (mariniert und angebraten)",
            "1 Apfel (in Spalten geschnitten)",
            "20g Walnüsse (gehackt)",
            "30g Rucola",
            "2 EL Apfelessig (für Dressing)",
            "1 EL Olivenöl (für Dressing)",
            "1 TL Ahornsirup (für Dressing)",
            "2 EL Sojasauce (für Tofu-Marinade)",
            "1/2 TL Senf (für Dressing)"
        ],
        instructions="""Tofu-Marinade: Tofu in Würfel schneiden, mit 2 EL Sojasauce marinieren (mind. 30 Min).
Marinierten Tofu in heißer Pfanne 5-7 Min von allen Seiten goldbraun braten. Beiseite stellen.
Rotkohl fein hobeln. Apfel in dünne Spalten schneiden.
Dressing: 2 EL Apfelessig, 1 EL Olivenöl, 1 TL Ahornsirup und 1/2 TL Senf in Schraubglas schütteln.
Salat zusammenstellen: Rotkohl, Cannellini-Bohnen, gebratenen Tofu, Apfel und Rucola in Schüssel geben.
Mit Dressing beträufeln, gehackte Walnüsse darüberstreuen.""",
        calories="524",
        protein="33g",
        carbs="56g",
        fat="18g",
        fiber="14g"
    )


def create_linsen_gemuese_salat_rote_bete():
    """Linsen-Gemüse-Salat mit Rote-Bete"""
    return create_recipe(
        name="Linsen-Gemüse-Salat mit Rote Bete (Protein-optimiert)",
        description="Bunter, protein-reicher Salat mit 31g Protein und 16g Ballaststoffen. Rote Bete färbt - separat lagern! Dressing vor dem Servieren hinzufügen.",
        prep_time="PT15M",
        cook_time="PT30M",
        meal_type="Abendessen",
        ingredients=[
            "60g Grüne Linsen (ca. 180g gekocht)",
            "80g Rote Bete (gekocht, gewürfelt)",
            "80g Kirschtomaten (halbiert)",
            "60g Gurke (gewürfelt)",
            "30g Rucola",
            "15g Walnüsse (gehackt)",
            "2 EL Zitronensaft (frisch gepresst)",
            "1 EL Olivenöl",
            "1/2 Knoblauchzehe (gepresst)"
        ],
        instructions="""Grüne Linsen kochen: 60g Linsen mit 150ml Wasser 25 Min köcheln bis bissfest. Abgießen, abkühlen lassen.
Rote Bete kochen: Würfeln, in Wasser 30 Min kochen bis weich (Handschuhe tragen!). Abkühlen lassen.
Dressing: 2 EL Zitronensaft, 1 EL Olivenöl und 1/2 Zehe gepressten Knoblauch vermischen. Mit Salz und Pfeffer abschmecken.
Kirschtomaten halbieren, Gurke würfeln.
Salat zusammenstellen: Linsen, Rote Bete, Tomaten, Gurke und Rucola in Schüssel geben.
Mit Dressing beträufeln, gehackte Walnüsse darüberstreuen.""",
        calories="432",
        protein="31g",
        carbs="58g",
        fat="10g",
        fiber="16g"
    )


def create_geroesteter_rotkohl_salat_kichererbsen():
    """Gerösteter Rotkohl-Salat mit Kichererbsen und Walnüssen"""
    return create_recipe(
        name="Gerösteter Rotkohl-Salat mit Kichererbsen und Walnüssen (Protein-optimiert)",
        description="Herzhafter Salat mit 44g Protein und 18g Ballaststoffen! Karamellisierter Rotkohl und knusprige Kichererbsen. Komplett warm servieren für beste Textur.",
        prep_time="PT10M",
        cook_time="PT30M",
        meal_type="Abendessen",
        ingredients=[
            "150g Rotkohl (in Wedges geschnitten)",
            "100g Kichererbsen (ca. 300g gekocht, geröstet)",
            "30g Quinoa (ca. 80g gekocht)",
            "30g Walnüsse (gehackt, geröstet)",
            "30g Rucola (frisch)",
            "1 EL Olivenöl (zum Rösten)",
            "1 TL Ahornsirup (zum Rösten)",
            "2 EL Balsamico (für Dressing)",
            "1 TL Kreuzkümmel (für Kichererbsen)",
            "1 TL Paprikapulver (für Kichererbsen)"
        ],
        instructions="""Ofen auf 200°C vorheizen.
Rotkohl in Wedges schneiden, mit 1 EL Olivenöl und 1 TL Ahornsirup marinieren. Auf Backblech geben.
Kichererbsen mit 1 TL Kreuzkümmel, 1 TL Paprikapulver, Salz und Pfeffer würzen. Auf separatem Backblech verteilen.
Beide Bleche im Ofen: Rotkohl 20-25 Min (bis Ränder karamellisieren), Kichererbsen 25-30 Min (bis knusprig).
Walnüsse in den letzten 5 Min mitrösten.
Quinoa kochen: 30g Quinoa mit 60ml Wasser 15 Min köcheln, 5 Min ruhen lassen.
Salat zusammenstellen: Quinoa als Basis, gerösteten Rotkohl, knusprige Kichererbsen und frischen Rucola arrangieren. Mit Balsamico beträufeln, Walnüsse darüberstreuen.""",
        calories="570",
        protein="44g",
        carbs="72g",
        fat="16g",
        fiber="18g"
    )


def create_buddha_bowl_linsen_tofu_rohkost():
    """Buddha-Bowl mit Linsen, Tofu und buntem Rohkost-Gemüse"""
    return create_recipe(
        name="Buddha-Bowl mit Linsen, Tofu und buntem Rohkost-Gemüse",
        description="Meal-Prep-freundliche Bowl mit Rohkost statt geröstetem Gemüse. Rohkost bleibt 4-5 Tage knackig! 36g Protein pro Portion.",
        prep_time="PT15M",
        cook_time="PT30M",
        meal_type="Abendessen",
        ingredients=[
            "40g Braune Linsen (ca. 120g gekocht)",
            "120g Tofu (mariniert und angebraten)",
            "30g Quinoa (ca. 80g gekocht)",
            "100g Karotten (in Julienne-Streifen, roh)",
            "80g Rote Bete (gekocht, gewürfelt)",
            "80g Rotkohl (fein gehobelt, roh)",
            "2 EL Tahini-Dressing",
            "1 EL Hanfsamen",
            "1 EL Kürbiskerne",
            "Petersilie (frisch, zum Garnieren)",
            "1 EL Sojasauce (für Tofu-Marinade)",
            "1/2 TL Ingwer (gerieben, für Marinade)"
        ],
        instructions="""Tofu-Marinade: Tofu in 2x2cm Würfel schneiden. Mit 1 EL Sojasauce und 1/2 TL Ingwer marinieren (mind. 30 Min).
Linsen kochen: 40g braune Linsen mit 100ml Wasser 20-25 Min köcheln bis bissfest.
Quinoa kochen: 30g Quinoa mit 60ml Wasser 15 Min köcheln, 5 Min ruhen lassen.
Rote Bete kochen: Würfeln, in Wasser 30 Min kochen bis weich (Handschuhe tragen!).
Rohkost vorbereiten: Karotten in Julienne-Streifen schneiden. Rotkohl fein hobeln. In luftdichten Containern lagern (hält 5 Tage!).
Tofu anbraten: Marinierten Tofu in heißer Pfanne 5-7 Min von allen Seiten goldbraun braten.
Bowl zusammenstellen: Quinoa als Basis, alle Komponenten arrangieren. Mit Tahini-Dressing beträufeln, Hanfsamen und Kürbiskerne darüberstreuen.""",
        calories="455",
        protein="36g",
        carbs="58g",
        fat="16g",
        fiber="16g"
    )


def create_linsen_feldsalat_rohkost():
    """Linsen-Feldsalat mit buntem Rohkost-Gemüse"""
    return create_recipe(
        name="Linsen-Feldsalat mit buntem Rohkost-Gemüse (Protein-optimiert)",
        description="Leichter, protein-reicher Salat mit 31g Protein und 18g Ballaststoffen. Rohkost-Gemüse für optimale Meal-Prep-Haltbarkeit (4-5 Tage). Apfel und Walnüsse am besten frisch hinzufügen.",
        prep_time="PT15M",
        cook_time="PT25M",
        meal_type="Abendessen",
        ingredients=[
            "60g Grüne Linsen (ca. 180g gekocht)",
            "80g Karotten (in Julienne-Streifen, roh)",
            "60g Gurke (in Streifen, roh)",
            "80g Feldsalat (gewaschen)",
            "1 Apfel (dünn geschnitten)",
            "20g Walnüsse (gehackt)",
            "30g Quinoa (ca. 80g gekocht)",
            "1,5 EL Apfelessig (für Dressing)",
            "1 EL Balsamico (für Dressing)",
            "1/2 EL Ahornsirup (für Dressing)",
            "1/2 TL Dijon-Senf (für Dressing)",
            "1/2 EL Olivenöl (für Dressing)"
        ],
        instructions="""Grüne Linsen kochen: 60g Linsen mit 150ml Wasser 25 Min köcheln bis bissfest. Abgießen, abkühlen lassen.
Quinoa kochen: 30g Quinoa mit 60ml Wasser 15 Min köcheln, 5 Min ruhen lassen.
Apfel-Balsamico-Vinaigrette: 1,5 EL Apfelessig, 1 EL Balsamico, 1/2 EL Ahornsirup, 1/2 TL Senf und 1/2 EL Olivenöl in Schraubglas schütteln.
Rohkost vorbereiten: Karotten in Julienne-Streifen schneiden. Gurke in Streifen schneiden. Feldsalat waschen.
Am Servieren: Apfel dünn schneiden, Walnüsse hacken.
Salat zusammenstellen: Quinoa und Linsen als Basis, Rohkost-Gemüse, Feldsalat, Apfel und Walnüsse hinzufügen. Mit Vinaigrette beträufeln.""",
        calories="420",
        protein="31g",
        carbs="60g",
        fat="12g",
        fiber="18g"
    )


# ============================================================================
# MAIN EXPORT
# ============================================================================

if __name__ == "__main__":
    # Create all November 2024 recipes
    recipes = [
        ("apfel_zimt_overnight_oats_protein_optimiert.json", create_apfel_zimt_overnight_oats_protein()),
        ("kichererbsen_buddha_bowl_rohkost.json", create_kichererbsen_buddha_bowl_rohkost()),
        ("rotkohl_curry_tofu_protein_optimiert.json", create_rotkohl_curry_tofu()),
        ("lauch_miso_suppe_tofu.json", create_lauch_miso_suppe_tofu()),
        ("vollkorn_wrap_pilz_nuss.json", create_vollkorn_wrap_pilz_nuss()),
        ("kichererbsen_curry_spinat_tofu.json", create_kichererbsen_curry_spinat_tofu()),
        ("rotkohl_apfel_salat_tofu.json", create_rotkohl_apfel_salat_tofu()),
        ("linsen_gemuese_salat_rote_bete.json", create_linsen_gemuese_salat_rote_bete()),
        ("geroesteter_rotkohl_salat_kichererbsen.json", create_geroesteter_rotkohl_salat_kichererbsen()),
        ("buddha_bowl_linsen_tofu_rohkost.json", create_buddha_bowl_linsen_tofu_rohkost()),
        ("linsen_feldsalat_rohkost.json", create_linsen_feldsalat_rohkost())
    ]

    print("📦 Exporting November 2024 recipes in schema.org format...\n")

    for filename, recipe in recipes:
        save_recipe(recipe, filename)

    print("\n✅ All recipes exported to mealie_exports/")
    print("📝 Import these JSON files directly into Mealie")
    print("\n🌟 November 2024 Recipes - Komplett-Set (11 Rezepte):")
    print("\n   FRÜHSTÜCK:")
    print("   • Apfel-Zimt Overnight Oats (28g Protein)")
    print("\n   MITTAGESSEN:")
    print("   • Kichererbsen-Buddha-Bowl mit Rohkost (24g Protein)")
    print("   • Rotkohl-Curry mit Tofu (42g Protein)")
    print("   • Lauch-Miso-Suppe mit Tofu (28g Protein)")
    print("   • Vollkorn-Wrap mit Pilz-Nuss-Füllung (28g Protein)")
    print("   • Kichererbsen-Curry mit Spinat und Tofu (41g Protein)")
    print("\n   ABENDESSEN:")
    print("   • Rotkohl-Apfel-Salat mit Tofu (33g Protein)")
    print("   • Linsen-Gemüse-Salat mit Rote-Bete (31g Protein)")
    print("   • Gerösteter Rotkohl-Salat mit Kichererbsen (44g Protein)")
    print("   • Buddha-Bowl mit Linsen, Tofu und Rohkost (36g Protein)")
    print("   • Linsen-Feldsalat mit Rohkost (31g Protein)")
    print("\n✨ Alle im korrekten schema.org Format mit rohen Mengenangaben!")
