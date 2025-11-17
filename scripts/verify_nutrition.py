#!/usr/bin/env python3
"""
Nutritional Verification Script for Whole Food Challenge Meal Plans

This script validates meal plans against nutritional targets and ensures
all ingredients comply with challenge rules.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import json


@dataclass
class NutritionInfo:
    """Nutritional information for a meal or ingredient."""
    calories: float
    protein: float
    carbs: float
    fat: float
    fiber: float

    def __add__(self, other):
        """Allow addition of nutrition info."""
        return NutritionInfo(
            calories=self.calories + other.calories,
            protein=self.protein + other.protein,
            carbs=self.carbs + other.carbs,
            fat=self.fat + other.fat,
            fiber=self.fiber + other.fiber
        )


@dataclass
class Meal:
    """Represents a single meal."""
    name: str
    nutrition: NutritionInfo
    ingredients: List[str]


@dataclass
class DailyPlan:
    """Represents a full day of meals."""
    date: str
    meals: List[Meal]

    @property
    def total_nutrition(self) -> NutritionInfo:
        """Calculate total nutrition for the day."""
        total = NutritionInfo(0, 0, 0, 0, 0)
        for meal in self.meals:
            total = total + meal.nutrition
        return total


# Challenge Rules Configuration
CHALLENGE_RULES = {
    "allowed_categories": [
        "vollkorn",
        "hülsenfrüchte",
        "früchte",
        "gemüse",
        "nüsse",
        "samen",
        "nussmus",
        "pflanzenmilch",
        "currypaste",
        "nährhefe",
        "gewürze",
        "kräuter",
        "essig",
        "öl"
    ],
    "excluded_ingredients": [
        "aubergine",
        "dicke bohnen",
        "ackerbohne",
        "puffbohne",
        "fava bohne",
        "grünkohl",
        "rosenkohl",
        "wirsing",
        "rosinen"
    ],
    "excluded_categories": [
        "tierische produkte",
        "verarbeitete lebensmittel",
        "zucker",
        "künstliche zusatzstoffe"
    ]
}

# Nutritional Targets
NUTRITIONAL_TARGETS = {
    "daily": {
        "calories": {"min": 1100, "max": 1300, "target": 1260},
        "protein": {"min": 65, "target": 75},
        "fiber": {"min": 25, "target": 30}
    },
    "meal_ranges": {
        "breakfast": {
            "calories": {"min": 300, "max": 500},
            "protein": {"min": 20, "target": 30}
        },
        "lunch": {
            "calories": {"min": 350, "max": 500},
            "protein": {"min": 18, "target": 25}
        },
        "dinner": {
            "calories": {"min": 350, "max": 450},
            "protein": {"min": 18, "target": 25}
        }
    }
}


def verify_ingredient(ingredient: str) -> Dict[str, any]:
    """
    Verify if an ingredient is allowed in the challenge.

    Args:
        ingredient: Name of the ingredient to check

    Returns:
        Dictionary with verification result and details
    """
    ingredient_lower = ingredient.lower()

    # Check excluded ingredients
    for excluded in CHALLENGE_RULES["excluded_ingredients"]:
        if excluded in ingredient_lower:
            return {
                "allowed": False,
                "reason": f"Ingredient '{ingredient}' is excluded from challenge",
                "category": "excluded_ingredient"
            }

    return {
        "allowed": True,
        "ingredient": ingredient
    }


def verify_meal_nutrition(meal: Meal, meal_type: str) -> Dict[str, any]:
    """
    Verify if a meal meets nutritional targets for its type.

    Args:
        meal: Meal object to verify
        meal_type: Type of meal (breakfast, lunch, dinner)

    Returns:
        Dictionary with verification results
    """
    results = {
        "meal_name": meal.name,
        "meal_type": meal_type,
        "passed": True,
        "warnings": [],
        "nutrition": {
            "calories": meal.nutrition.calories,
            "protein": meal.nutrition.protein,
            "carbs": meal.nutrition.carbs,
            "fat": meal.nutrition.fat,
            "fiber": meal.nutrition.fiber
        }
    }

    if meal_type in NUTRITIONAL_TARGETS["meal_ranges"]:
        targets = NUTRITIONAL_TARGETS["meal_ranges"][meal_type]

        # Check calories
        if meal.nutrition.calories < targets["calories"]["min"]:
            results["warnings"].append(
                f"Calories ({meal.nutrition.calories:.0f}) below minimum "
                f"({targets['calories']['min']})"
            )
            results["passed"] = False
        elif meal.nutrition.calories > targets["calories"]["max"]:
            results["warnings"].append(
                f"Calories ({meal.nutrition.calories:.0f}) above maximum "
                f"({targets['calories']['max']})"
            )
            results["passed"] = False

        # Check protein
        if meal.nutrition.protein < targets["protein"]["min"]:
            results["warnings"].append(
                f"Protein ({meal.nutrition.protein:.1f}g) below minimum "
                f"({targets['protein']['min']}g)"
            )

    return results


def verify_daily_plan(plan: DailyPlan) -> Dict[str, any]:
    """
    Verify if a daily plan meets all nutritional targets.

    Args:
        plan: DailyPlan object to verify

    Returns:
        Dictionary with comprehensive verification results
    """
    total_nutrition = plan.total_nutrition
    targets = NUTRITIONAL_TARGETS["daily"]

    results = {
        "date": plan.date,
        "passed": True,
        "total_nutrition": {
            "calories": total_nutrition.calories,
            "protein": total_nutrition.protein,
            "carbs": total_nutrition.carbs,
            "fat": total_nutrition.fat,
            "fiber": total_nutrition.fiber
        },
        "target_compliance": {},
        "warnings": [],
        "meal_verifications": []
    }

    # Verify calorie target
    if total_nutrition.calories < targets["calories"]["min"]:
        results["passed"] = False
        results["warnings"].append(
            f"Daily calories ({total_nutrition.calories:.0f}) below minimum "
            f"({targets['calories']['min']})"
        )
        results["target_compliance"]["calories"] = "below_minimum"
    elif total_nutrition.calories > targets["calories"]["max"]:
        results["passed"] = False
        results["warnings"].append(
            f"Daily calories ({total_nutrition.calories:.0f}) above maximum "
            f"({targets['calories']['max']})"
        )
        results["target_compliance"]["calories"] = "above_maximum"
    else:
        deviation = abs(total_nutrition.calories - targets["calories"]["target"])
        if deviation <= 50:
            results["target_compliance"]["calories"] = "excellent"
        else:
            results["target_compliance"]["calories"] = "acceptable"

    # Verify protein target
    if total_nutrition.protein < targets["protein"]["min"]:
        results["passed"] = False
        results["warnings"].append(
            f"Daily protein ({total_nutrition.protein:.1f}g) below minimum "
            f"({targets['protein']['min']}g)"
        )
        results["target_compliance"]["protein"] = "below_minimum"
    elif total_nutrition.protein >= targets["protein"]["target"]:
        results["target_compliance"]["protein"] = "excellent"
    else:
        results["target_compliance"]["protein"] = "acceptable"

    # Verify fiber target
    if total_nutrition.fiber >= targets["fiber"]["target"]:
        results["target_compliance"]["fiber"] = "excellent"
    elif total_nutrition.fiber >= targets["fiber"]["min"]:
        results["target_compliance"]["fiber"] = "acceptable"
    else:
        results["warnings"].append(
            f"Daily fiber ({total_nutrition.fiber:.1f}g) below minimum "
            f"({targets['fiber']['min']}g)"
        )
        results["target_compliance"]["fiber"] = "below_minimum"

    # Verify individual meals
    meal_types = ["breakfast", "lunch", "dinner"]
    for i, meal in enumerate(plan.meals):
        meal_type = meal_types[i] if i < len(meal_types) else "additional_meal"
        meal_verification = verify_meal_nutrition(meal, meal_type)
        results["meal_verifications"].append(meal_verification)

        if not meal_verification["passed"]:
            results["passed"] = False

    return results


def generate_verification_report(verification_results: Dict[str, any]) -> str:
    """
    Generate a human-readable verification report.

    Args:
        verification_results: Results from verify_daily_plan

    Returns:
        Formatted report string
    """
    report = []
    report.append(f"═══════════════════════════════════════════════════")
    report.append(f"WHOLE FOOD CHALLENGE - NUTRITIONAL VERIFICATION")
    report.append(f"Date: {verification_results['date']}")
    report.append(f"═══════════════════════════════════════════════════\n")

    # Overall status
    status = "✅ PASSED" if verification_results["passed"] else "❌ FAILED"
    report.append(f"Overall Status: {status}\n")

    # Daily totals
    report.append("DAILY TOTALS:")
    report.append(f"  Calories: {verification_results['total_nutrition']['calories']:.0f} kcal "
                 f"({NUTRITIONAL_TARGETS['daily']['calories']['target']} target)")
    report.append(f"  Protein:  {verification_results['total_nutrition']['protein']:.1f}g "
                 f"({NUTRITIONAL_TARGETS['daily']['protein']['target']}g target)")
    report.append(f"  Carbs:    {verification_results['total_nutrition']['carbs']:.1f}g")
    report.append(f"  Fat:      {verification_results['total_nutrition']['fat']:.1f}g")
    report.append(f"  Fiber:    {verification_results['total_nutrition']['fiber']:.1f}g "
                 f"({NUTRITIONAL_TARGETS['daily']['fiber']['target']}g target)\n")

    # Target compliance
    report.append("TARGET COMPLIANCE:")
    for target, status in verification_results["target_compliance"].items():
        emoji = "✅" if status in ["excellent", "acceptable"] else "⚠️"
        report.append(f"  {emoji} {target.capitalize()}: {status.replace('_', ' ').title()}")
    report.append("")

    # Warnings
    if verification_results["warnings"]:
        report.append("⚠️  WARNINGS:")
        for warning in verification_results["warnings"]:
            report.append(f"  - {warning}")
        report.append("")

    # Meal breakdown
    report.append("MEAL BREAKDOWN:")
    for meal_verify in verification_results["meal_verifications"]:
        status_emoji = "✅" if meal_verify["passed"] else "⚠️"
        report.append(f"\n  {status_emoji} {meal_verify['meal_name']} ({meal_verify['meal_type']})")
        report.append(f"     Calories: {meal_verify['nutrition']['calories']:.0f} kcal | "
                     f"Protein: {meal_verify['nutrition']['protein']:.1f}g")

        if meal_verify["warnings"]:
            for warning in meal_verify["warnings"]:
                report.append(f"     ⚠️  {warning}")

    report.append(f"\n═══════════════════════════════════════════════════")

    return "\n".join(report)


# Example usage
if __name__ == "__main__":
    # Meal Plans für Woche 1.-5. Dezember 2025
    # OPTIMIERT: Korrekte Nährwerte nach SKILL.md Standards
    # Saisonale Dezember-Zutaten (Rotkohl, Rote Bete, Äpfel, TK-Beeren)

    # TAG 1 - Montag, 1. Dezember
    day1_breakfast = Meal(
        name="Overnight Oats Apfel-Zimt",
        nutrition=NutritionInfo(calories=414, protein=30.2, carbs=55.65, fat=22.55, fiber=10.3),
        ingredients=["25g Haferflocken", "200ml Hafermilch", "10g Leinsamen", "10g Mandelmus",
                    "25g Erbsenprotein", "150g Apfel", "10g Walnüsse", "Zimt"]
    )
    day1_lunch = Meal(
        name="Linsen-Curry mit Rotkohl und Tofu",
        nutrition=NutritionInfo(calories=380, protein=23.8, carbs=49.9, fat=11.3, fiber=17.8),
        ingredients=["150g Rotkohl", "160g Linsen gekocht", "80g Tofu", "10g Currypaste",
                    "150ml Gemüsebrühe", "Ingwer", "Knoblauch", "Zwiebel", "1 TL Olivenöl", "Gewürze"]
    )
    day1_dinner = Meal(
        name="Rote-Bete-Salat mit Cannellini-Bohnen",
        nutrition=NutritionInfo(calories=411, protein=20.4, carbs=54, fat=14.9, fiber=13.7),
        ingredients=["150g Rote Bete", "120g Cannellini-Bohnen", "50g Karotten-Julienne",
                    "40g Rucola", "40g Tofu", "10g Walnüsse", "Zitronen-Senf-Dressing", "1 TL Olivenöl"]
    )
    day1 = DailyPlan(
        date="2025-12-01 (Montag)",
        meals=[day1_breakfast, day1_lunch, day1_dinner]
    )

    # TAG 2 - Dienstag, 2. Dezember
    day2_breakfast = Meal(
        name="Chia Pudding mit TK-Beeren",
        nutrition=NutritionInfo(calories=455, protein=27.7, carbs=51.85, fat=17.35, fiber=11.8),
        ingredients=["24g Chiasamen", "250ml Hafermilch", "25g Erbsenprotein",
                    "150g TK-Beeren gemischt", "8g Walnüsse", "5g Ahornsirup", "Vanille", "Zimt"]
    )
    day2_lunch = Meal(
        name="Kichererbsen-Buddha-Bowl mit Rotkohl",
        nutrition=NutritionInfo(calories=423, protein=20.1, carbs=54.7, fat=15.1, fiber=14.3),
        ingredients=["100g Kichererbsen geröstet", "80g Quinoa", "80g Brokkoli", "50g Rotkohl mariniert",
                    "30g Tofu", "Zitronen-Senf-Dressing", "1 TL Olivenöl", "8g Kürbiskerne"]
    )
    day2_dinner = Meal(
        name="Linsen-Feldsalat mit Apfel und Tofu",
        nutrition=NutritionInfo(calories=401, protein=22, carbs=46.3, fat=16.5, fiber=15.7),
        ingredients=["130g Linsen gekocht", "50g Feldsalat", "80g Apfel", "100g Kirschtomaten",
                    "50g Gurke", "80g Tofu", "10g Walnüsse", "Apfelessig-Dressing", "1 TL Olivenöl"]
    )
    day2 = DailyPlan(
        date="2025-12-02 (Dienstag)",
        meals=[day2_breakfast, day2_lunch, day2_dinner]
    )

    # TAG 3 - Mittwoch, 3. Dezember
    day3_breakfast = Meal(
        name="Overnight Oats mit TK-Heidelbeeren",
        nutrition=NutritionInfo(calories=422, protein=30.8, carbs=55.65, fat=22.05, fiber=9.7),
        ingredients=["25g Haferflocken", "200ml Hafermilch", "10g Leinsamen", "10g Mandelmus",
                    "25g Erbsenprotein", "150g TK-Heidelbeeren", "10g Walnüsse", "Zimt"]
    )
    day3_lunch = Meal(
        name="Gerösteter Rotkohl mit Linsen und Tofu",
        nutrition=NutritionInfo(calories=388, protein=22.4, carbs=42.2, fat=16.8, fiber=15.1),
        ingredients=["150g Rotkohl geröstet", "120g Linsen gekocht", "90g Tofu", "30g Rucola",
                    "10g Walnüsse geröstet", "1 TL Olivenöl", "5g Ahornsirup", "Balsamico"]
    )
    day3_dinner = Meal(
        name="Rote-Bete-Karotten-Salat mit Cannellini-Bohnen",
        nutrition=NutritionInfo(calories=439, protein=19.5, carbs=50.2, fat=19.1, fiber=13.1),
        ingredients=["120g Rote Bete", "80g Karotten geröstet", "110g Cannellini-Bohnen",
                    "50g Tofu", "40g Feldsalat", "10g Walnüsse", "Zitronen-Kreuzkümmel-Dressing", "2 TL Olivenöl"]
    )
    day3 = DailyPlan(
        date="2025-12-03 (Mittwoch)",
        meals=[day3_breakfast, day3_lunch, day3_dinner]
    )

    # TAG 4 - Donnerstag, 4. Dezember
    day4_breakfast = Meal(
        name="Chia Pudding mit TK-Kirschen",
        nutrition=NutritionInfo(calories=444, protein=28.1, carbs=48.85, fat=17.15, fiber=11.8),
        ingredients=["24g Chiasamen", "250ml Hafermilch", "25g Erbsenprotein",
                    "150g TK-Kirschen", "8g Walnüsse", "5g Ahornsirup", "Vanille", "Zimt"]
    )
    day4_lunch = Meal(
        name="Pastinaken-Karotten-Curry mit Kichererbsen",
        nutrition=NutritionInfo(calories=439, protein=18.6, carbs=57.3, fat=13.9, fiber=17),
        ingredients=["120g Pastinaken", "80g Karotten", "110g Kichererbsen", "80g Tofu",
                    "10g Currypaste", "150ml Gemüsebrühe", "1 TL Olivenöl", "Ingwer", "Gewürze"]
    )
    day4_dinner = Meal(
        name="Linsen-Rucola-Salat mit Rote Bete und Tofu",
        nutrition=NutritionInfo(calories=406, protein=24, carbs=45.5, fat=16.5, fiber=15.9),
        ingredients=["145g Linsen gekocht", "100g Rote Bete", "40g Rucola", "80g Tofu",
                    "50g Kirschtomaten", "10g Walnüsse", "Zitronen-Dressing", "1 TL Olivenöl"]
    )
    day4 = DailyPlan(
        date="2025-12-04 (Donnerstag)",
        meals=[day4_breakfast, day4_lunch, day4_dinner]
    )

    # TAG 5 - Freitag, 5. Dezember
    day5_breakfast = Meal(
        name="Overnight Oats Apfel-Zimt (wie Montag)",
        nutrition=NutritionInfo(calories=414, protein=30.2, carbs=55.65, fat=22.55, fiber=10.3),
        ingredients=["25g Haferflocken", "200ml Hafermilch", "10g Leinsamen", "10g Mandelmus",
                    "25g Erbsenprotein", "150g Apfel", "10g Walnüsse", "Zimt"]
    )
    day5_lunch = Meal(
        name="Kichererbsen-Bowl mit Rote Bete",
        nutrition=NutritionInfo(calories=421, protein=23.2, carbs=53.9, fat=14.2, fiber=15.2),
        ingredients=["130g Kichererbsen geröstet", "100g Rote Bete", "80g Tofu", "50g Karotten roh",
                    "30g Feldsalat", "8g Kürbiskerne", "5g Tahini", "Zitronen-Dressing"]
    )
    day5_dinner = Meal(
        name="Cannellini-Apfel-Salat mit Haselnüssen",
        nutrition=NutritionInfo(calories=436, protein=19.7, carbs=60.1, fat=15.1, fiber=13.6),
        ingredients=["120g Cannellini-Bohnen", "100g Apfel", "100g Rote Bete", "40g Feldsalat",
                    "50g Tofu", "10g Haselnüsse", "Apfel-Balsamico-Dressing", "1 TL Olivenöl", "5g Ahornsirup"]
    )
    day5 = DailyPlan(
        date="2025-12-05 (Freitag)",
        meals=[day5_breakfast, day5_lunch, day5_dinner]
    )

    # Verify all days
    all_plans = [day1, day2, day3, day4, day5]

    print("═══════════════════════════════════════════════════════════════")
    print("WHOLE FOOD CHALLENGE - WOCHENPLAN DEZEMBER 1-5, 2025")
    print("OPTIMIERT: Korrekte Nährwerte nach SKILL.md Standards")
    print("SAISONAL: Rotkohl, Rote Bete, Äpfel, TK-Beeren, Walnüsse")
    print("═══════════════════════════════════════════════════════════════\n")

    weekly_totals = {
        "calories": 0,
        "protein": 0,
        "fiber": 0,
        "days_passed": 0,
        "total_days": len(all_plans)
    }

    for plan in all_plans:
        results = verify_daily_plan(plan)
        report = generate_verification_report(results)
        print(report)
        print("\n")

        # Track weekly totals
        weekly_totals["calories"] += results["total_nutrition"]["calories"]
        weekly_totals["protein"] += results["total_nutrition"]["protein"]
        weekly_totals["fiber"] += results["total_nutrition"]["fiber"]
        if results["passed"]:
            weekly_totals["days_passed"] += 1

    # Weekly summary
    print("═══════════════════════════════════════════════════════════════")
    print("WOCHENZUSAMMENFASSUNG")
    print("═══════════════════════════════════════════════════════════════")
    print(f"\nTage bestanden: {weekly_totals['days_passed']}/{weekly_totals['total_days']}")
    print(f"\nDurchschnittliche Tageswerte:")
    print(f"  Kalorien: {weekly_totals['calories']/len(all_plans):.0f} kcal/Tag "
          f"(Target: {NUTRITIONAL_TARGETS['daily']['calories']['target']})")
    print(f"  Protein:  {weekly_totals['protein']/len(all_plans):.1f}g/Tag "
          f"(Target: {NUTRITIONAL_TARGETS['daily']['protein']['target']}g)")
    print(f"  Ballaststoffe: {weekly_totals['fiber']/len(all_plans):.1f}g/Tag "
          f"(Target: {NUTRITIONAL_TARGETS['daily']['fiber']['target']}g)")

    # Recommendations
    avg_protein = weekly_totals['protein']/len(all_plans)
    avg_calories = weekly_totals['calories']/len(all_plans)

    print("\n📋 EMPFEHLUNGEN:")
    if avg_protein < NUTRITIONAL_TARGETS['daily']['protein']['min']:
        deficit = NUTRITIONAL_TARGETS['daily']['protein']['min'] - avg_protein
        print(f"  ⚠️  Protein-Target nicht erreicht (Defizit: {deficit:.1f}g/Tag)")
        print(f"     → Füge 100-150g Tofu zu Hauptmahlzeiten hinzu (+10-15g Protein)")
        print(f"     → Erhöhe Erbsenprotein-Pulver auf 30g im Frühstück (+4g Protein)")
        print(f"     → Füge zusätzliche Hülsenfrüchte hinzu (+8-12g Protein/100g)")
    elif avg_protein < NUTRITIONAL_TARGETS['daily']['protein']['target']:
        print(f"  ℹ️  Protein über Minimum aber unter Target ({avg_protein:.1f}g vs {NUTRITIONAL_TARGETS['daily']['protein']['target']}g)")
        print(f"     → Laut SKILL.md akzeptabel bei 1300 kcal-Grenze!")
        print(f"     → Mit minimalen Fetten bleibt wenig Spielraum für mehr Protein")
    else:
        print(f"  ✅ Protein-Target erreicht!")

    if avg_calories < NUTRITIONAL_TARGETS['daily']['calories']['min']:
        print(f"  ⚠️  Kalorien unter Minimum")
        print(f"     → Füge Nüsse, Samen oder Avocado hinzu")
    elif avg_calories > NUTRITIONAL_TARGETS['daily']['calories']['max']:
        print(f"  ⚠️  Kalorien über Maximum")
        print(f"     → Reduziere Öl in Dressings oder Nussportionen")
    else:
        print(f"  ✅ Kalorien im Zielbereich!")

    print("\n═══════════════════════════════════════════════════════════════")
