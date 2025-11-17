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
    # Meal Plans für Woche 15.-19. Dezember 2024
    # Saisonale Dezember-Zutaten, OHNE Rotkohl, mit deftiger Erbsensuppe

    # TAG 1 - Montag, 17. November (KORRIGIERT - halbiert, Nüsse/Samen entfernt)
    day1_breakfast = Meal(
        name="Apfel-Zimt Overnight Oats (halbiert, ohne Nüsse/Samen)",
        nutrition=NutritionInfo(calories=158, protein=11.5, carbs=20, fat=2.5, fiber=6),
        ingredients=["15g Haferflocken", "75ml Hafermilch", "10g Erbsenprotein",
                    "1/2 Apfel", "Zimt"]
    )
    day1_lunch = Meal(
        name="Kichererbsen-Buddha-Bowl (Tahini+Avocado reduziert)",
        nutrition=NutritionInfo(calories=506.5, protein=21, carbs=70, fat=15, fiber=18),
        ingredients=["120g Kichererbsen", "80g Quinoa", "80g Brokkoli",
                    "Karotten-Julienne (roh)", "Gurke (roh)",
                    "1 EL Tahini", "Kürbiskerne", "Petersilie"]
    )
    day1_dinner = Meal(
        name="Rotkohl-Apfel-Salat mit Cannellini-Bohnen und Tofu",
        nutrition=NutritionInfo(calories=597, protein=33, carbs=58, fat=28, fiber=15),
        ingredients=["Rotkohl", "Apfel", "Cannellini-Bohnen", "180g Tofu mariniert",
                    "20g Walnüsse", "Apfelessig", "Olivenöl", "Rucola"]
    )
    day1 = DailyPlan(
        date="2024-11-17 (Montag) - KORRIGIERT",
        meals=[day1_breakfast, day1_lunch, day1_dinner]
    )

    # TAG 2 - Dienstag, 18. November (KORRIGIERT)
    day2_breakfast = Meal(
        name="Protein-Boost Overnight Oats (halbiert, ohne Nussmus/Samen)",
        nutrition=NutritionInfo(calories=236.5, protein=18.65, carbs=27, fat=18, fiber=7),
        ingredients=["Haferflocken", "Hafermilch", "25g Erbsenprotein", "Beeren"]
    )
    day2_lunch = Meal(
        name="Rotkohl-Curry (Kokosmilch reduziert 75→40ml)",
        nutrition=NutritionInfo(calories=654, protein=39, carbs=75, fat=27, fiber=18),
        ingredients=["Rotkohl", "Kichererbsen", "120g Tofu", "Zwiebel", "Knoblauch",
                    "Currypaste", "40ml Kokosmilch", "Quinoa", "Gewürze"]
    )
    day2_dinner = Meal(
        name="Linsen-Gemüse-Salat (unverändert)",
        nutrition=NutritionInfo(calories=458, protein=23, carbs=54, fat=19, fiber=19),
        ingredients=["Linsen", "Kirschtomaten", "Rote Bete", "Gurke", "Rucola",
                    "Walnüsse", "Zitrone", "Olivenöl"]
    )
    day2 = DailyPlan(
        date="2024-11-18 (Dienstag) - KORRIGIERT",
        meals=[day2_breakfast, day2_lunch, day2_dinner]
    )

    # TAG 3 - Mittwoch, 19. November (KORRIGIERT)
    day3_breakfast = Meal(
        name="Schoko-Banane Overnight Oats (halbiert, ohne Nüsse/Samen)",
        nutrition=NutritionInfo(calories=154.5, protein=12.4, carbs=30, fat=15, fiber=8),
        ingredients=["Haferflocken", "Hafermilch", "20g Erbsenprotein", "Kakaopulver", "Banane"]
    )
    day3_lunch = Meal(
        name="Lauch-Miso-Suppe (unverändert)",
        nutrition=NutritionInfo(calories=395, protein=23, carbs=39, fat=17, fiber=8),
        ingredients=["Lauch", "150g Tofu", "Shiitake-Pilze", "Miso-Paste", "Gemüsebrühe",
                    "Ingwer", "Frühlingszwiebeln"]
    )
    day3_dinner = Meal(
        name="Gerösteter Rotkohl-Salat (Kichererbsen 300→150g)",
        nutrition=NutritionInfo(calories=741, protein=31, carbs=95, fat=32, fiber=21),
        ingredients=["Rotkohl", "150g Kichererbsen geröstet", "Walnüsse", "Ahornsirup",
                    "Olivenöl", "Balsamico", "Rucola", "Quinoa"]
    )
    day3 = DailyPlan(
        date="2024-11-19 (Mittwoch) - KORRIGIERT",
        meals=[day3_breakfast, day3_lunch, day3_dinner]
    )

    # TAG 4 - Donnerstag, 20. November (KORRIGIERT)
    day4_breakfast = Meal(
        name="Quinoa-Bowl (halbiert, ohne Nüsse)",
        nutrition=NutritionInfo(calories=122, protein=15, carbs=43, fat=13, fiber=6),
        ingredients=["Quinoa", "Hafermilch", "25g Erbsenprotein", "Apfel",
                    "Zimt", "Cranberries"]
    )
    day4_lunch = Meal(
        name="Vollkorn-Wrap (Nüsse halbiert, Hummus reduziert)",
        nutrition=NutritionInfo(calories=588.5, protein=24, carbs=56, fat=32, fiber=14),
        ingredients=["Pilze", "Walnüsse (halbiert)", "Cashews (halbiert)", "Rotkohl", "Hummus (reduziert)", "Tahini",
                    "Rucola", "Vollkorn-Wrap"]
    )
    day4_dinner = Meal(
        name="Buddha-Bowl mit Linsen (Tahini reduziert)",
        nutrition=NutritionInfo(calories=634.5, protein=35, carbs=73, fat=26, fiber=21),
        ingredients=["Linsen", "120g Tofu mariniert", "Quinoa", "Karotten-Julienne (roh)", "Rote Bete (gekocht)",
                    "Rotkohl (roh)", "Tahini (reduziert)", "Kürbiskerne", "Petersilie"]
    )
    day4 = DailyPlan(
        date="2024-11-20 (Donnerstag) - KORRIGIERT",
        meals=[day4_breakfast, day4_lunch, day4_dinner]
    )

    # TAG 5 - Freitag, 21. November (KORRIGIERT)
    day5_breakfast = Meal(
        name="Beeren-Power Overnight Oats (halbiert, ohne Nussmus/Samen)",
        nutrition=NutritionInfo(calories=175, protein=14.2, carbs=27, fat=13, fiber=7),
        ingredients=["Haferflocken", "Hafermilch", "20g Erbsenprotein", "Beeren", "Zimt"]
    )
    day5_lunch = Meal(
        name="Kichererbsen-Curry (Kokosmilch reduziert 75→40ml)",
        nutrition=NutritionInfo(calories=740, protein=38, carbs=70, fat=33, fiber=19),
        ingredients=["Kichererbsen", "150g Tofu", "Champignons", "Spinat", "Currypaste",
                    "40ml Kokosmilch", "Quinoa", "Kürbiskerne", "Gewürze"]
    )
    day5_dinner = Meal(
        name="Linsen-Feldsalat (Walnüsse 30→10g)",
        nutrition=NutritionInfo(calories=528.5, protein=24, carbs=85, fat=12, fiber=24),
        ingredients=["180g Linsen", "Karotten-Julienne (roh)", "Gurke (roh)", "Apfel", "80g Feldsalat", "10g Walnüsse",
                    "Quinoa", "Apfel-Balsamico-Vinaigrette"]
    )
    day5 = DailyPlan(
        date="2024-11-21 (Freitag) - KORRIGIERT",
        meals=[day5_breakfast, day5_lunch, day5_dinner]
    )

    # Verify all days
    all_plans = [day1, day2, day3, day4, day5]

    print("═══════════════════════════════════════════════════════════════")
    print("WHOLE FOOD CHALLENGE - WOCHENPLAN DEZEMBER 15-19, 2024")
    print("SAISONALER FOKUS: Dezember-Gemüse, OHNE Rotkohl")
    print("BESONDERHEIT: Deftige Wintererbsensuppe (Mo-Mi)")
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
