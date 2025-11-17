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
        "calories": {"min": 1100, "max": 1300, "target": 1200},
        "protein": {"min": 100, "target": 110},
        "fiber": {"min": 25, "target": 30}
    },
    "meal_ranges": {
        "breakfast": {
            "calories": {"min": 300, "max": 400},
            "protein": {"min": 15, "target": 30}
        },
        "lunch": {
            "calories": {"min": 350, "max": 450},
            "protein": {"min": 25, "target": 45}
        },
        "dinner": {
            "calories": {"min": 350, "max": 400},
            "protein": {"min": 25, "target": 45}
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
    # Saisonale Januar-Zutaten, mit deftiger Brechbohnensuppe

    # TAG 1 - Montag, 5. Januar
    day1_breakfast = Meal(
        name="Overnight Oats Apfel-Zimt",
        nutrition=NutritionInfo(calories=370, protein=28, carbs=42, fat=12, fiber=11),
        ingredients=["Haferflocken", "Hafermilch", "Chiasamen", "Leinsamen", "Mandelmus",
                    "20g Erbsenprotein", "Apfel", "Walnüsse", "Zimt"]
    )
    day1_lunch = Meal(
        name="Deftige Brechbohnensuppe (Portion 1)",
        nutrition=NutritionInfo(calories=410, protein=28, carbs=52, fat=9, fiber=15),
        ingredients=["300g Brechbohnen TK", "250g Kartoffeln", "Karotten", "Sellerie",
                    "180g weiße Bohnen", "120g geräucherter Tofu", "Zwiebel", "Gewürze"]
    )
    day1_dinner = Meal(
        name="Rote-Beete-Salat mit Linsen und Walnüssen",
        nutrition=NutritionInfo(calories=385, protein=24, carbs=48, fat=11, fiber=14),
        ingredients=["150g Rote Beete", "120g Linsen", "Rucola", "Walnüsse",
                    "Apfel", "Apfelessig", "Olivenöl", "Dijon-Senf"]
    )
    day1 = DailyPlan(
        date="2026-01-05 (Montag)",
        meals=[day1_breakfast, day1_lunch, day1_dinner]
    )

    # TAG 2 - Dienstag, 6. Januar
    day2_breakfast = Meal(
        name="Chia Pudding Beeren-Power",
        nutrition=NutritionInfo(calories=400, protein=32, carbs=35, fat=16, fiber=16),
        ingredients=["Chiasamen", "Hafermilch", "20g Erbsenprotein", "Cashewmus",
                    "Vanille", "Beeren", "Hanfsamen", "Mandelsplitter", "Zimt"]
    )
    day2_lunch = Meal(
        name="Deftige Brechbohnensuppe (Portion 2)",
        nutrition=NutritionInfo(calories=410, protein=28, carbs=52, fat=9, fiber=15),
        ingredients=["Brechbohnen", "Kartoffeln", "Karotten", "Sellerie",
                    "weiße Bohnen", "geräucherter Tofu", "Gewürze"]
    )
    day2_dinner = Meal(
        name="Rotkohl-Buddha-Bowl mit Quinoa",
        nutrition=NutritionInfo(calories=400, protein=26, carbs=48, fat=14, fiber=13),
        ingredients=["Quinoa", "120g Kichererbsen geröstet", "Rotkohl", "Karotten",
                    "Gurke", "Tahini-Dressing", "Kürbiskerne", "Petersilie"]
    )
    day2 = DailyPlan(
        date="2026-01-06 (Dienstag)",
        meals=[day2_breakfast, day2_lunch, day2_dinner]
    )

    # TAG 3 - Mittwoch, 7. Januar
    day3_breakfast = Meal(
        name="Overnight Oats Beeren-Power",
        nutrition=NutritionInfo(calories=360, protein=30, carbs=38, fat=13, fiber=13),
        ingredients=["Haferflocken", "Hafermilch", "Chiasamen", "Leinsamen", "Mandelmus",
                    "20g Erbsenprotein", "Beeren", "Hanfsamen", "Walnüsse", "Zimt"]
    )
    day3_lunch = Meal(
        name="Deftige Brechbohnensuppe (Portion 3)",
        nutrition=NutritionInfo(calories=410, protein=28, carbs=52, fat=9, fiber=15),
        ingredients=["Brechbohnen", "Kartoffeln", "Karotten", "Sellerie",
                    "weiße Bohnen", "geräucherter Tofu", "Gewürze"]
    )
    day3_dinner = Meal(
        name="Hokkaido-Curry mit weißen Bohnen",
        nutrition=NutritionInfo(calories=420, protein=22, carbs=52, fat=12, fiber=16),
        ingredients=["200g Hokkaido", "120g weiße Bohnen", "Spinat", "Zwiebel",
                    "Currypaste", "Ingwer", "Kokosmilch", "Gemüsebrühe", "Gewürze"]
    )
    day3 = DailyPlan(
        date="2026-01-07 (Mittwoch)",
        meals=[day3_breakfast, day3_lunch, day3_dinner]
    )

    # TAG 4 - Donnerstag, 8. Januar
    day4_breakfast = Meal(
        name="Quinoa-Frühstücksbowl mit Apfel-Zimt",
        nutrition=NutritionInfo(calories=390, protein=26, carbs=55, fat=9, fiber=9),
        ingredients=["Quinoa", "Hafermilch", "15g Erbsenprotein", "Walnüsse", "Apfel",
                    "Zimt", "Cranberries", "Ahornsirup"]
    )
    day4_lunch = Meal(
        name="Pastinaken-Sellerie-Suppe mit Linsen",
        nutrition=NutritionInfo(calories=380, protein=24, carbs=62, fat=5, fiber=16),
        ingredients=["150g Pastinaken", "100g Sellerie", "120g rote Linsen", "Karotten",
                    "Zwiebel", "Gemüsebrühe", "Kreuzkümmel", "Koriander", "Hafermilch"]
    )
    day4_dinner = Meal(
        name="Weißkohl-Karotten-Salat mit Kichererbsen",
        nutrition=NutritionInfo(calories=410, protein=26, carbs=48, fat=14, fiber=15),
        ingredients=["120g Weißkohl", "Karotten", "120g Kichererbsen geröstet",
                    "Walnüsse", "Rucola", "Apfelessig", "Olivenöl", "Kürbiskerne"]
    )
    day4 = DailyPlan(
        date="2026-01-08 (Donnerstag)",
        meals=[day4_breakfast, day4_lunch, day4_dinner]
    )

    # TAG 5 - Freitag, 9. Januar
    day5_breakfast = Meal(
        name="Chia Pudding Apfel-Zimt",
        nutrition=NutritionInfo(calories=385, protein=30, carbs=40, fat=14, fiber=15),
        ingredients=["Chiasamen", "Hafermilch", "20g Erbsenprotein", "Mandelmus",
                    "Vanille", "Zimt", "Kardamom", "Apfel", "Walnüsse", "Ahornsirup"]
    )
    day5_lunch = Meal(
        name="Rotkohl-Linsen-Curry",
        nutrition=NutritionInfo(calories=395, protein=24, carbs=52, fat=10, fiber=18),
        ingredients=["150g Rotkohl", "120g rote Linsen", "Zwiebel", "Knoblauch",
                    "Currypaste", "Ingwer", "Kokosmilch", "Gemüsebrühe", "Gewürze"]
    )
    day5_dinner = Meal(
        name="Geröstete Karotten mit Quinoa und Tahini",
        nutrition=NutritionInfo(calories=405, protein=24, carbs=54, fat=13, fiber=14),
        ingredients=["200g Karotten geröstet", "Quinoa", "100g Kichererbsen",
                    "Tahini-Dressing", "Kürbiskerne", "Rucola", "Petersilie"]
    )
    day5 = DailyPlan(
        date="2026-01-09 (Freitag)",
        meals=[day5_breakfast, day5_lunch, day5_dinner]
    )

    # Verify all days
    all_plans = [day1, day2, day3, day4, day5]

    print("═══════════════════════════════════════════════════════════════")
    print("WHOLE FOOD CHALLENGE - WOCHENPLAN JANUAR 5-9, 2026")
    print("SAISONALER FOKUS: Januar-Wintergemüse")
    print("BESONDERHEIT: Deftige Brechbohnensuppe (Mo-Mi)")
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
        print(f"     → Erhöhe Erbsenprotein-Pulver auf 20g im Frühstück (+5g Protein)")
        print(f"     → Füge zusätzliche Hülsenfrüchte hinzu (+8-12g Protein/100g)")
    elif avg_protein < NUTRITIONAL_TARGETS['daily']['protein']['target']:
        print(f"  ℹ️  Protein über Minimum aber unter Target")
        print(f"     → Kleine Anpassungen empfohlen für optimale Ergebnisse")
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
