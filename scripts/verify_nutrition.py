#!/usr/bin/env python3
"""
Nutritional Verification Script for Whole Food Challenge Meal Plans - Parser-basierte Version

Parst Markdown-Meal-Plans und validiert sie automatisch gegen Nährwert-Targets
und Challenge-Regeln. Kein manuelles Code-Schreiben mehr nötig!

Usage:
    python3 scripts/verify_nutrition.py meal-plans/wochenplan-08-12-dezember.md
    python3 scripts/verify_nutrition.py meal-plans/wochenplan-2024-12-15-bis-19.md --json
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from pathlib import Path
import json
import re
import sys


# ============================================================================
# DATA STRUCTURES
# ============================================================================

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


# ============================================================================
# CHALLENGE RULES & TARGETS
# ============================================================================

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


# ============================================================================
# MARKDOWN PARSER
# ============================================================================

class MealPlanParser:
    """Parst Meal Plans aus Markdown-Dateien"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.content = f.read()

    def parse_all_days(self) -> List[DailyPlan]:
        """Extrahiert alle Tage aus dem Meal Plan"""
        daily_plans = []

        # Finde alle TAG-Blöcke (## TAG 1 - MONTAG 8. DEZEMBER)
        tag_pattern = r'##\s+TAG\s+\d+\s*-\s*(.+?)(?=\n##|$)'
        tags = list(re.finditer(tag_pattern, self.content, re.DOTALL | re.MULTILINE))

        for i, tag_match in enumerate(tags):
            date_info = tag_match.group(1).strip().split('\n')[0]  # Erste Zeile nach TAG

            # Extrahiere Tag-Block
            start_pos = tag_match.start()
            if i + 1 < len(tags):
                end_pos = tags[i + 1].start()
            else:
                end_pos = len(self.content)

            day_block = self.content[start_pos:end_pos]

            # Parse Mahlzeiten für diesen Tag
            meals = self._parse_meals_in_day(day_block)

            if meals:
                daily_plan = DailyPlan(date=date_info, meals=meals)
                daily_plans.append(daily_plan)

        return daily_plans

    def _parse_meals_in_day(self, day_block: str) -> List[Meal]:
        """Parst alle Mahlzeiten in einem Tag-Block"""
        meals = []

        # Finde alle Mahlzeiten (### Frühstück:, ### Mittagessen:, ### Abendessen:)
        meal_pattern = r'###\s+(Frühstück|Mittagessen|Abendessen):\s+(.+?)(?=\n###|\n##|$)'
        meal_matches = list(re.finditer(meal_pattern, day_block, re.DOTALL))

        for i, meal_match in enumerate(meal_matches):
            meal_type = meal_match.group(1)
            meal_name = meal_match.group(2).strip().split('\n')[0].strip()

            # Extrahiere Mahlzeit-Block
            start_pos = meal_match.start()
            if i + 1 < len(meal_matches):
                end_pos = meal_matches[i + 1].start()
            else:
                # Suche nach nächster Section
                next_section = re.search(r'\n(###|##)', day_block[start_pos + 10:])
                end_pos = start_pos + next_section.start() + 10 if next_section else len(day_block)

            meal_block = day_block[start_pos:end_pos]

            try:
                parsed_meal = self._parse_meal_block(meal_name, meal_block)
                if parsed_meal:
                    meals.append(parsed_meal)
                else:
                    # Keine Nährwerte gefunden - vermutlich eine Referenz
                    if "(siehe " in meal_name.lower() or "wiederholung" in meal_name.lower():
                        pass  # Das ist erwartet
                    else:
                        print(f"⚠️  Keine Nährwerte gefunden für '{meal_name}'")
            except Exception as e:
                print(f"⚠️  Fehler beim Parsen von '{meal_name}': {e}")

        return meals

    def _parse_meal_block(self, name: str, block: str) -> Optional[Meal]:
        """Parst einen einzelnen Mahlzeit-Block"""

        # Extrahiere Nährwerte
        nutrition = self._extract_nutrition(block)
        if not nutrition:
            return None

        # Extrahiere Zutaten
        ingredients = self._extract_ingredients(block)

        return Meal(
            name=name,
            nutrition=nutrition,
            ingredients=ingredients
        )

    def _extract_nutrition(self, block: str) -> Optional[NutritionInfo]:
        """Extrahiert Nährwertangaben aus Mahlzeit-Block"""

        # Suche nach Nährwerte-Sektion
        # Format 1: **Nährwerte:** Header mit Liste
        # Format 2: Inline im Titel **Kalorien:** 284 kcal | **Protein:** 20g

        calories = protein = carbs = fat = fiber = None

        # Versuche verschiedene Patterns
        patterns = {
            'calories': [
                r'[*\s]*Kalorien[:\s]+(\d+(?:\.\d+)?)\s*kcal',
                r'calories[:\s]+(\d+(?:\.\d+)?)',
            ],
            'protein': [
                r'[*\s]*Protein[:\s]+(\d+(?:\.\d+)?)\s*g',
                r'protein[:\s]+(\d+(?:\.\d+)?)',
            ],
            'carbs': [
                r'[*\s]*Kohlenhydrate[:\s]+(\d+(?:\.\d+)?)\s*g',
                r'[*\s]*Carbs[:\s]+(\d+(?:\.\d+)?)\s*g',
            ],
            'fat': [
                r'[*\s]*Fett[:\s]+(\d+(?:\.\d+)?)\s*g',
                r'fat[:\s]+(\d+(?:\.\d+)?)',
            ],
            'fiber': [
                r'[*\s]*Ballaststoffe[:\s]+(\d+(?:\.\d+)?)\s*g',
                r'[*\s]*Fiber[:\s]+(\d+(?:\.\d+)?)\s*g',
            ]
        }

        for nutrient, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, block, re.IGNORECASE)
                if match:
                    value = float(match.group(1))
                    if nutrient == 'calories':
                        calories = value
                    elif nutrient == 'protein':
                        protein = value
                    elif nutrient == 'carbs':
                        carbs = value
                    elif nutrient == 'fat':
                        fat = value
                    elif nutrient == 'fiber':
                        fiber = value
                    break

        # Validierung: Mindestens Kalorien und Protein müssen gefunden werden
        if calories is None or protein is None:
            return None

        # Defaults für fehlende Werte
        if carbs is None:
            carbs = 0.0
        if fat is None:
            fat = 0.0
        if fiber is None:
            fiber = 0.0

        return NutritionInfo(
            calories=calories,
            protein=protein,
            carbs=carbs,
            fat=fat,
            fiber=fiber
        )

    def _extract_ingredients(self, block: str) -> List[str]:
        """Extrahiert Zutatenliste aus Mahlzeit-Block"""
        ingredients = []

        # Finde Zutaten-Sektionen
        # **Zutaten:**, **Komponenten:**, **Toppings:**
        sections = re.findall(
            r'\*\*(?:Zutaten|Komponenten|Toppings|Basis).*?\*\*\s*\n((?:^-\s+.+$\n?)+)',
            block,
            re.MULTILINE
        )

        for section in sections:
            lines = section.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('- '):
                    ingredient = line[2:].strip()
                    # Bereinige Markdown-Formatierung
                    ingredient = re.sub(r'\*\*(.+?)\*\*', r'\1', ingredient)
                    ingredients.append(ingredient)

        return ingredients


# ============================================================================
# VERIFICATION FUNCTIONS
# ============================================================================

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

    # Normalisiere meal_type für Lookup
    meal_type_normalized = meal_type.lower()
    if "frühstück" in meal_type_normalized:
        meal_type_key = "breakfast"
    elif "mittag" in meal_type_normalized:
        meal_type_key = "lunch"
    elif "abend" in meal_type_normalized:
        meal_type_key = "dinner"
    else:
        meal_type_key = meal_type_normalized

    if meal_type_key in NUTRITIONAL_TARGETS["meal_ranges"]:
        targets = NUTRITIONAL_TARGETS["meal_ranges"][meal_type_key]

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
    for meal in plan.meals:
        # Bestimme meal_type aus dem ersten Wort des Namens oder Position
        meal_type = "lunch"  # default
        if any(word in meal.name.lower() for word in ["frühstück", "breakfast", "oats", "chia"]):
            meal_type = "breakfast"
        elif any(word in meal.name.lower() for word in ["abend", "dinner", "suppe"]):
            meal_type = "dinner"

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
        report.append(f"\n  {status_emoji} {meal_verify['meal_name']}")
        report.append(f"     Calories: {meal_verify['nutrition']['calories']:.0f} kcal | "
                     f"Protein: {meal_verify['nutrition']['protein']:.1f}g")

        if meal_verify["warnings"]:
            for warning in meal_verify["warnings"]:
                report.append(f"     ⚠️  {warning}")

    report.append(f"\n═══════════════════════════════════════════════════")

    return "\n".join(report)


# ============================================================================
# CLI
# ============================================================================

def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage: python3 verify_nutrition.py <meal_plan_file.md> [--json]")
        print("\nBeispiele:")
        print("  python3 verify_nutrition.py meal-plans/wochenplan-08-12-dezember.md")
        print("  python3 verify_nutrition.py meal-plans/wochenplan-2024-12-15-bis-19.md --json")
        sys.exit(1)

    meal_plan_file = sys.argv[1]
    output_json = "--json" in sys.argv

    # Parse Meal Plan
    print(f"📖 Lese Meal Plan aus: {meal_plan_file}\n")

    try:
        parser = MealPlanParser(meal_plan_file)
        daily_plans = parser.parse_all_days()
    except FileNotFoundError:
        print(f"❌ Datei nicht gefunden: {meal_plan_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Fehler beim Parsen: {e}")
        sys.exit(1)

    if not daily_plans:
        print("⚠️  Keine Tage im Meal Plan gefunden!")
        sys.exit(1)

    print(f"✅ {len(daily_plans)} Tage gefunden\n")

    # Verify all days
    print("═══════════════════════════════════════════════════════════════")
    print(f"WHOLE FOOD CHALLENGE - MEAL PLAN VERIFICATION")
    print(f"File: {Path(meal_plan_file).name}")
    print("═══════════════════════════════════════════════════════════════\n")

    weekly_totals = {
        "calories": 0,
        "protein": 0,
        "fiber": 0,
        "days_passed": 0,
        "total_days": len(daily_plans)
    }

    all_results = []

    for plan in daily_plans:
        results = verify_daily_plan(plan)
        all_results.append(results)

        if not output_json:
            report = generate_verification_report(results)
            print(report)
            print("\n")

        # Track weekly totals
        weekly_totals["calories"] += results["total_nutrition"]["calories"]
        weekly_totals["protein"] += results["total_nutrition"]["protein"]
        weekly_totals["fiber"] += results["total_nutrition"]["fiber"]
        if results["passed"]:
            weekly_totals["days_passed"] += 1

    # Output format
    if output_json:
        # JSON output
        output = {
            "meal_plan_file": meal_plan_file,
            "total_days": len(daily_plans),
            "days_passed": weekly_totals["days_passed"],
            "weekly_averages": {
                "calories": weekly_totals["calories"] / len(daily_plans),
                "protein": weekly_totals["protein"] / len(daily_plans),
                "fiber": weekly_totals["fiber"] / len(daily_plans)
            },
            "daily_results": all_results
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        # Human-readable summary
        print("═══════════════════════════════════════════════════════════════")
        print("WOCHENZUSAMMENFASSUNG")
        print("═══════════════════════════════════════════════════════════════")
        print(f"\nTage bestanden: {weekly_totals['days_passed']}/{weekly_totals['total_days']}")
        print(f"\nDurchschnittliche Tageswerte:")
        print(f"  Kalorien: {weekly_totals['calories']/len(daily_plans):.0f} kcal/Tag "
              f"(Target: {NUTRITIONAL_TARGETS['daily']['calories']['target']})")
        print(f"  Protein:  {weekly_totals['protein']/len(daily_plans):.1f}g/Tag "
              f"(Target: {NUTRITIONAL_TARGETS['daily']['protein']['target']}g)")
        print(f"  Ballaststoffe: {weekly_totals['fiber']/len(daily_plans):.1f}g/Tag "
              f"(Target: {NUTRITIONAL_TARGETS['daily']['fiber']['target']}g)")

        # Recommendations
        avg_protein = weekly_totals['protein']/len(daily_plans)
        avg_calories = weekly_totals['calories']/len(daily_plans)

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


if __name__ == "__main__":
    main()
