# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The **Whole Food Meal Planner** is a meal planning system for the "Whole Food Challenge" - a strict plant-based, whole-food dietary program. The project is written in **German** and provides tools for:

- Creating nutritionally-balanced meal plans (typically 1200 kcal/day, 100+g protein)
- Validating meals against challenge rules and nutritional targets
- Managing a database of verified recipes
- Exporting recipes to Mealie (self-hosted recipe manager)

**Technology**: Python 3.11.14 with **no external dependencies** (standard library only)

## Key Commands

### Nutritional Verification
```bash
python3 scripts/verify_nutrition.py
```
Validates meal plans against nutritional targets and challenge rules. After creating any meal plan, always run this script to verify compliance.

### Mealie Recipe Export
```bash
python3 scripts/mealie_export.py
```
Generates Mealie-compatible JSON recipe files in `mealie_exports/` directory.

### View Documentation
```bash
# Complete workflow guide (read before creating meal plans)
view references/meal-plan-workflow.md

# Recipe database with nutritional information
view references/recipe-database.md

# Project overview and quick reference
view SKILL.md
```

## Architecture

### Code Structure

The codebase uses **data-oriented architecture** with clear patterns:

1. **Dataclasses for Domain Models**:
   - `NutritionInfo` - nutritional data with arithmetic operations
   - `Meal` - single meal with nutrition and ingredients
   - `DailyPlan` - full day of meals with computed properties
   - `MealieRecipe` - Mealie-compatible recipe format

2. **Functional Patterns**:
   - Pure functions for validation (`verify_ingredient`, `verify_meal_nutrition`)
   - Data transformation pipelines
   - Immutable data structures with computed properties

3. **Configuration-Driven**:
   - `CHALLENGE_RULES` dict defines allowed/excluded ingredients
   - `NUTRITIONAL_TARGETS` dict defines daily and per-meal ranges
   - Easy to modify targets without changing logic

### File Organization

```
scripts/              # Python automation tools
  verify_nutrition.py # Validates meal plans (381 lines)
  mealie_export.py    # Exports to Mealie format (340 lines)
references/           # Documentation and recipes
  meal-plan-workflow.md   # 8-step planning guide
  recipe-database.md      # Verified recipes with nutrition
mealie_exports/       # Generated JSON files for Mealie
SKILL.md             # Project documentation and quick reference
```

## Challenge Rules & Targets

### Excluded Ingredients
The challenge has specific exclusions (check before suggesting recipes):
- **Vegetables**: Auberginen (eggplant), Dicke Bohnen (fava beans), Grünkohl (kale), Rosenkohl (Brussels sprouts), Wirsing (savoy cabbage)
- **All animal products**
- **All processed foods**

### Nutritional Targets (Daily)
- **Calories**: 1200 kcal (acceptable range: 1150-1250)
- **Protein**: 110g target (minimum: 100g)
- **Fiber**: 40g target (minimum: 30g)

### Meal Ranges
- **Frühstück (Breakfast)**: 300-400 kcal, 10-15g protein
- **Mittagessen (Lunch)**: 250-450 kcal, 15-25g protein
- **Abendessen (Dinner)**: 250-400 kcal, 15-25g protein

## Meal Planning Workflow

**Always follow this 8-step process** (detailed in `references/meal-plan-workflow.md`):

1. **Gather Requirements**: Time period, calorie/protein targets, preferences
2. **Select Recipes**: From `recipe-database.md`, focus on ingredient synergies
3. **Create Plan**: Use templates from workflow guide
4. **Verify Nutrition**: Run `verify_nutrition.py` - **CRITICAL STEP**
5. **Adjust if Needed**:
   - Protein too low → Add Tofu/Tempeh/extra legumes
   - Calories too high → Reduce nuts/oil
   - Calories too low → Add nuts/avocado
6. **Generate Shopping List**: Group by category, add storage tips
7. **Create Meal Prep Timeline**: 4-phase approach (grains → vegetables → special components → portioning)
8. **Optional**: Export to Mealie

## Working with Scripts

### verify_nutrition.py

When creating meal plans, you must modify the script to add your meal data:

```python
# Define meals using dataclasses
breakfast = Meal(
    name="Overnight Oats",
    nutrition=NutritionInfo(calories=350, protein=12, carbs=55, fat=9, fiber=10),
    ingredients=["Haferflocken", "Beeren", "Mandelmilch", "Chiasamen"]
)

# Create daily plan
day1 = DailyPlan(
    date="2024-01-15",
    meals=[breakfast, lunch, dinner]
)

# Run verification
verify_daily_plan(day1)
```

The script outputs:
- Human-readable report with emojis (✅/⚠️/❌)
- JSON format for programmatic processing
- Detailed warnings for out-of-range values
- Ingredient compliance checks

### mealie_export.py

To export recipes, add `MealieRecipe` objects:

```python
recipe = MealieRecipe(
    name="Recipe Name",
    description="Description",
    recipe_yield="2 servings",
    prep_time="PT15M",  # ISO 8601 format
    perform_time="PT30M",
    total_time="PT45M",
    recipe_category=["Breakfast"],
    tags=["Whole Food Challenge", "Meal Prep"],
    recipe_ingredient=[...],  # Use MealieIngredient objects
    recipe_instructions=[...],
    nutrition=MealieNutrition(...)
)
```

## Recipe Database

The `references/recipe-database.md` contains:
- **Breakfast**: Overnight Oats, Quinoa Bowls, Porridge variations
- **Lunch/Dinner**: Buddha Bowls, Curries, Salads, Soups, Wraps
- **Components**: Base grains, legumes, dressings
- **Snacks**: Energy balls, roasted chickpeas

Each recipe includes:
- Complete nutritional information
- Meal prep notes
- Storage duration
- Variations

**Key principle**: Maximize ingredient synergies (e.g., Rotkohl for curry, salad, soup, wraps)

## Development Notes

### Language
All documentation, comments, and user-facing content is in **German**. Maintain this convention when adding new content.

### No Build/Test Framework
This is a personal toolkit without formal testing or CI/CD. Manual verification of scripts is expected.

### Extending Scripts
When modifying scripts:
1. Keep using dataclasses for clean data modeling
2. Maintain type hints for clarity
3. Update example code in `if __name__ == "__main__"` blocks
4. Test with actual meal plan data before finalizing

### Common Adjustments

**Protein too low (<100g)**:
- Add 100g tofu (+15g protein)
- Swap chickpeas for tempeh (+8g protein)
- Add extra Nussmus to breakfast (+4g protein)
- Include edamame snack (+11g protein)

**Calories too high (>1250)**:
- Reduce oil in dressings
- Smaller nut portions
- Replace avocado with vegetables

**Too monotonous**:
- Same base ingredients, different spices (Mediterranean → Asian → Mexican)
- Vary cooking methods (raw, roasted, steamed)
- Different textures (crispy chickpeas, creamy hummus, whole chickpeas)

## Integration Points

### Mealie
- Self-hosted recipe manager (https://mealie.io)
- Import generated JSON files from `mealie_exports/`
- Useful for digital recipe tracking and meal planning UI

### Meal Prep Strategy
The workflow emphasizes **4-phase meal prep** (detailed in workflow guide):
1. **Grundlagen** (Foundations): Cook grains and legumes in parallel
2. **Gemüse** (Vegetables): Roast vegetables, prepare proteins
3. **Spezial-Komponenten** (Special): Dressings, overnight oats, special preparations
4. **Portionieren** (Portion): Container assembly, labeling, storage

Typical time: **3-4 hours on Sunday for 5 days**, with 5-15 min daily assembly.

## Quality Checklist

Before finalizing any meal plan, verify:
- [ ] No excluded ingredients (Auberginen, Dicke Bohnen, Grünkohl, Rosenkohl, Wirsing)
- [ ] All animal products and processed foods excluded
- [ ] Nutritional targets met (run `verify_nutrition.py`)
- [ ] Meal prep synergies maximized
- [ ] Shopping list complete and categorized
- [ ] Realistic prep times included
- [ ] Storage instructions provided
- [ ] Variety across the week
- [ ] Seasonal and available ingredients (Germany-based)

## Resources

- Full documentation: `SKILL.md`
- Step-by-step workflow: `references/meal-plan-workflow.md`
- Recipe collection: `references/recipe-database.md`
- Verification script: `scripts/verify_nutrition.py`
- Mealie export: `scripts/mealie_export.py`
