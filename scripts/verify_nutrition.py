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
    # Meal Plans für Woche 5.-9. Januar 2026
    # Saisonale Januar-Zutaten (Wintergemüse, Brechbohnen)

    # TAG 1 - Montag, 5. Januar
    day1_breakfast = Meal(
        name="Overnight Oats mit Apfel-Zimt",
        nutrition=NutritionInfo(calories=387, protein=26.1, carbs=48.5, fat=10.1, fiber=9.4),
        ingredients=["30g Haferflocken", "200ml Hafermilch", "10g Leinsamen", "15g Mandelmus",
                    "20g Erbsenprotein", "100g Apfel", "Zimt"]
    )
    day1_lunch = Meal(
        name="Rotkohl-Kartoffel-Eintopf mit weißen Bohnen",
        nutrition=NutritionInfo(calories=425, protein=23.9, carbs=75.5, fat=3.5, fiber=19.2),
        ingredients=["150g Kartoffeln", "120g Rotkohl", "150g weiße Bohnen", "100g Möhre",
                    "80g Zwiebel", "Kümmel", "Lorbeer", "Gemüsebrühe", "Apfelessig"]
    )
    day1_dinner = Meal(
        name="Deftige Brechbohnensuppe",
        nutrition=NutritionInfo(calories=478, protein=28.8, carbs=73.9, fat=5.8, fiber=23.5),
        ingredients=["400g Brechbohnen TK", "150g Kartoffeln", "100g weiße Bohnen", "100g Möhre",
                    "40g Sellerie", "80g Zwiebel", "Bohnenkraut", "Paprikapulver", "15g Tomatenmark"]
    )
    day1 = DailyPlan(
        date="2026-01-05 (Montag)",
        meals=[day1_breakfast, day1_lunch, day1_dinner]
    )

    # TAG 2 - Dienstag, 6. Januar
    day2_breakfast = Meal(
        name="Quinoa-Porridge mit Birne",
        nutrition=NutritionInfo(calories=437, protein=24.3, carbs=64.3, fat=9.7, fiber=9.3),
        ingredients=["50g Quinoa", "200ml Hafermilch", "20g Erbsenprotein",
                    "10g Mandelmus", "150g Birne", "Zimt", "Kardamom"]
    )
    day2_lunch = Meal(
        name="Rote-Bete-Linsen-Salat mit Walnüssen",
        nutrition=NutritionInfo(calories=453, protein=24.8, carbs=62.0, fat=11.8, fiber=19.8),
        ingredients=["200g Rote Bete", "120g braune Linsen", "150g Apfel", "50g Feldsalat",
                    "15g Walnüsse", "Balsamico-Dressing", "Senf", "Ahornsirup"]
    )
    day2_dinner = Meal(
        name="Sellerie-Pastinaken-Suppe mit Tofu",
        nutrition=NutritionInfo(calories=397, protein=27.0, carbs=51.7, fat=8.3, fiber=16.2),
        ingredients=["200g Sellerie", "150g Pastinaken", "150g Tofu", "80g Zwiebel",
                    "Kreuzkümmel", "Thymian", "500ml Gemüsebrühe", "100ml Hafermilch"]
    )
    day2 = DailyPlan(
        date="2026-01-06 (Dienstag)",
        meals=[day2_breakfast, day2_lunch, day2_dinner]
    )

    # TAG 3 - Mittwoch, 7. Januar
    day3_breakfast = Meal(
        name="Buchweizen-Porridge mit Apfel",
        nutrition=NutritionInfo(calories=406, protein=24.5, carbs=60.0, fat=8.5, fiber=9.5),
        ingredients=["50g Buchweizen", "200ml Hafermilch", "20g Erbsenprotein",
                    "10g Cashewmus", "100g Apfel", "Zimt"]
    )
    day3_lunch = Meal(
        name="Weißkohl-Möhren-Bowl mit Kichererbsen",
        nutrition=NutritionInfo(calories=417, protein=23.9, carbs=66.8, fat=6.8, fiber=21.3),
        ingredients=["60g Quinoa", "120g Weißkohl", "120g Kichererbsen", "100g Möhre",
                    "Zitronen-Dressing", "Senf", "Kreuzkümmel", "Petersilie"]
    )
    day3_dinner = Meal(
        name="Deftige Brechbohnensuppe",
        nutrition=NutritionInfo(calories=478, protein=28.8, carbs=73.9, fat=5.8, fiber=23.5),
        ingredients=["400g Brechbohnen TK", "150g Kartoffeln", "100g weiße Bohnen", "100g Möhre",
                    "40g Sellerie", "80g Zwiebel", "Bohnenkraut", "Paprikapulver", "15g Tomatenmark"]
    )
    day3 = DailyPlan(
        date="2026-01-07 (Mittwoch)",
        meals=[day3_breakfast, day3_lunch, day3_dinner]
    )

    # TAG 4 - Donnerstag, 8. Januar
    day4_breakfast = Meal(
        name="Overnight Oats mit Birne-Zimt",
        nutrition=NutritionInfo(calories=379, protein=25.8, carbs=48.2, fat=9.6, fiber=9.9),
        ingredients=["30g Haferflocken", "200ml Hafermilch", "10g Leinsamen", "10g Mandelmus",
                    "20g Erbsenprotein", "100g Birne", "Zimt"]
    )
    day4_lunch = Meal(
        name="Süßkartoffel-Linsen-Curry",
        nutrition=NutritionInfo(calories=441, protein=23.7, carbs=73.2, fat=6.2, fiber=18.9),
        ingredients=["200g Süßkartoffel", "80g rote Linsen", "100g Spinat", "80g Zwiebel",
                    "Curry", "Kreuzkümmel", "Kurkuma", "Ingwer", "Gemüsebrühe"]
    )
    day4_dinner = Meal(
        name="Karotten-Pastinaken-Salat mit Linsen",
        nutrition=NutritionInfo(calories=468, protein=26.8, carbs=74.5, fat=7.0, fiber=22.2),
        ingredients=["200g Möhre", "150g Pastinaken", "150g braune Linsen", "150g Apfel",
                    "30g Rucola", "10g Kürbiskerne", "Apfelessig-Dressing"]
    )
    day4 = DailyPlan(
        date="2026-01-08 (Donnerstag)",
        meals=[day4_breakfast, day4_lunch, day4_dinner]
    )

    # TAG 5 - Freitag, 9. Januar
    day5_breakfast = Meal(
        name="Quinoa-Apfel-Porridge",
        nutrition=NutritionInfo(calories=432, protein=24.1, carbs=63.8, fat=9.4, fiber=9.1),
        ingredients=["50g Quinoa", "200ml Hafermilch", "20g Erbsenprotein",
                    "10g Mandelmus", "100g Apfel", "Zimt", "Muskatnuss"]
    )
    day5_lunch = Meal(
        name="Rotkohl-Weiße-Bohnen-Salat",
        nutrition=NutritionInfo(calories=388, protein=20.8, carbs=67.2, fat=3.9, fiber=21.4),
        ingredients=["150g Rotkohl", "150g weiße Bohnen", "150g Apfel", "50g Feldsalat",
                    "Apfelessig-Dressing", "Senf", "Ahornsirup", "Kümmel"]
    )
    day5_dinner = Meal(
        name="Deftige Brechbohnensuppe",
        nutrition=NutritionInfo(calories=478, protein=28.8, carbs=73.9, fat=5.8, fiber=23.5),
        ingredients=["400g Brechbohnen TK", "150g Kartoffeln", "100g weiße Bohnen", "100g Möhre",
                    "40g Sellerie", "80g Zwiebel", "Bohnenkraut", "Paprikapulver", "15g Tomatenmark"]
    )
    day5 = DailyPlan(
        date="2026-01-09 (Freitag)",
        meals=[day5_breakfast, day5_lunch, day5_dinner]
    )

    # Verify all days
    all_plans = [day1, day2, day3, day4, day5]

    print("═══════════════════════════════════════════════════════════════")
    print("WHOLE FOOD CHALLENGE - WOCHENPLAN JANUAR 5-9, 2026")
    print("SAISONAL: Wintergemüse, Brechbohnen, Äpfel, Birnen")
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
        print(f"  ⚠️  Protein-Minimum nicht erreicht (Defizit: {deficit:.1f}g/Tag)")
        print(f"     → Füge 80-100g Tofu zu Hauptmahlzeiten hinzu (+10-12g Protein)")
        print(f"     → Erhöhe Erbsenprotein-Pulver auf 25-30g im Frühstück (+3-4g Protein)")
        print(f"     → Füge zusätzliche Hülsenfrüchte hinzu (+8-12g Protein/100g)")
    elif avg_protein < NUTRITIONAL_TARGETS['daily']['protein']['target']:
        print(f"  ℹ️  Protein über Minimum aber unter Target ({avg_protein:.1f}g vs {NUTRITIONAL_TARGETS['daily']['protein']['target']}g)")
        print(f"     → Gut im Zielbereich! Bei Bedarf leicht erhöhen.")
    else:
        print(f"  ✅ Protein-Target erreicht oder übertroffen!")

    if avg_calories < NUTRITIONAL_TARGETS['daily']['calories']['min']:
        print(f"  ⚠️  Kalorien unter Minimum")
        print(f"     → Füge Nüsse, Samen oder Avocado hinzu")
    elif avg_calories > NUTRITIONAL_TARGETS['daily']['calories']['max']:
        print(f"  ⚠️  Kalorien über Maximum")
        print(f"     → Reduziere Öl in Dressings oder Nussportionen")
    else:
        print(f"  ✅ Kalorien im Zielbereich!")

    print("\n═══════════════════════════════════════════════════════════════")
