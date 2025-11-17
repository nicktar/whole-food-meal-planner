# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The **Whole Food Meal Planner** is a meal planning system for the "Whole Food Challenge" - a strict plant-based, whole-food dietary program. The project is written in **German** and provides tools for:

- Creating nutritionally-balanced meal plans (typically 1200 kcal/day, 75-90g protein)
- Validating meals against challenge rules and nutritional targets
- Managing a database of verified recipes
- Exporting recipes to Mealie (self-hosted recipe manager)

**Technology**: Python 3.11.14 with **no external dependencies** (standard library only)

## Claude Skill Architecture

**This repository defines a Claude skill** that can be invoked by other Claude instances. The skill is defined in `SKILL.md` with:

- **Skill name**: `whole-food-meal-planner`
- **Skill description**: Provides meal planning capabilities for the Whole Food Challenge
- **When to invoke**: Creating multi-day plans (3-7 days) with specific caloric/protein targets, ingredient synergies, and meal prep strategies

The SKILL.md file serves as the skill's prompt that gets loaded when the skill is invoked. It contains:
- Quick start workflow
- Challenge rules and nutritional targets
- Links to bundled resources (scripts, reference docs)
- Best practices and common scenarios
- Quality control checklist

When working on this codebase, remember that changes to SKILL.md affect how other Claude instances will use this skill.

## External Recipe Database Architecture

**NEW**: The skill now supports project-specific recipe databases, allowing users to maintain recipes separately from the skill itself.

### How It Works

When the skill is invoked from a project:
1. **Check external**: Look for `recipe-database.md` in the project root
2. **Use external if found**: Load recipes from the project's database
3. **Fall back to bundled**: Use `references/recipe-database.md` if no external database exists
4. **Support custom paths**: Accept user-specified paths (e.g., `my-recipes/database.md`)

### Benefits

- ✅ **No skill releases needed**: Users update recipes without modifying the skill
- ✅ **Multiple collections**: Different projects can have different recipe sets
- ✅ **Version control**: Users can track recipe changes independently
- ✅ **Privacy**: Personal recipes stay in user projects
- ✅ **Sharing**: Recipe collections can be shared without the entire skill

### File Structure

```
User's project/
├── recipe-database.md        # External recipes (auto-detected)
└── meal-plans/              # Generated meal plans

This skill repo/
├── references/
│   ├── recipe-database.md         # Bundled recipes (fallback)
│   ├── external-recipes-guide.md  # Guide for external recipes
│   └── meal-plan-workflow.md      # Workflow guide
└── example-recipe-project/        # Template for users
    ├── README.md
    ├── recipe-database.md
    └── .gitignore
```

### For Developers

When working on the skill:
- **Bundled recipes** in `references/recipe-database.md` serve as:
  - Default recipes when no external database exists
  - Reference templates for format
  - Examples for new users
- **External recipe guide** at `references/external-recipes-guide.md` explains how users can create their own recipe databases
- **Example project** in `example-recipe-project/` provides a ready-to-use template

### Maintaining Recipe Format

Both bundled and external recipes must follow the same format:
- Challenge rules section (ingredient compliance)
- Recipe sections: FRÜHSTÜCK, MITTAGESSEN & ABENDESSEN, DRESSINGS & SAUCEN
- Each recipe: name, metadata (portion/calories/protein/prep), ingredients, instructions, meal prep notes
- Separator `---` between recipes

See `references/external-recipes-guide.md` for detailed format requirements.

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
scripts/                        # Python automation tools
  verify_nutrition.py           # Validates meal plans (381 lines)
  mealie_export.py              # Exports to Mealie format (340 lines)
references/                     # Documentation and recipes
  meal-plan-workflow.md         # 8-step planning guide
  recipe-database.md            # Bundled recipes (fallback)
  external-recipes-guide.md     # Guide for external recipe databases
example-recipe-project/         # Template for external recipes
  README.md                     # Setup instructions
  recipe-database.md            # Sample external recipe collection
  .gitignore                    # Git configuration
mealie_exports/                 # Generated JSON files for Mealie
SKILL.md                        # Skill definition and documentation
CLAUDE.md                       # This file - developer guidance
```

## Challenge Rules & Targets

### Excluded Ingredients
The challenge has specific exclusions (check before suggesting recipes):
- **Vegetables**: Auberginen (eggplant), Dicke Bohnen (fava beans), Grünkohl (kale), Rosenkohl (Brussels sprouts), Wirsing (savoy cabbage)
- **Fruits**: Rosinen (raisins)
- **All animal products**
- **All processed foods**

### Nutritional Targets (Daily)
- **Calories**: 1200 kcal (acceptable range: 1100-1300)
- **Protein**: 80g target (minimum: 75g)
- **Fiber**: 30g target (minimum: 25g)

### Meal Ranges
- **Frühstück (Breakfast)**: 300-400 kcal, 15-30g protein
- **Mittagessen (Lunch)**: 350-450 kcal, 20-35g protein
- **Abendessen (Dinner)**: 350-400 kcal, 20-35g protein

## Meal Planning Workflow

**Always follow this 8-step process** (detailed in `references/meal-plan-workflow.md`):

1. **Gather Requirements**: Time period, calorie/protein targets, preferences
2. **Select Recipes**: From `recipe-database.md`, focus on ingredient synergies
3. **Create Plan**: Use templates from workflow guide
4. **Verify Nutrition**: Run `verify_nutrition.py` - **CRITICAL STEP**
5. **Adjust if Needed**:
   - Protein too low → Add Tofu/extra legumes
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

### Bundled Recipes

The `references/recipe-database.md` contains:
- **Breakfast**: Overnight Oats, Quinoa Bowls, Porridge variations
- **Lunch/Dinner**: Buddha Bowls, Curries, Salads, Soups, Wraps
- **Components**: Base grains, legumes, dressings

Each recipe includes:
- Complete nutritional information
- Meal prep notes
- Storage duration
- Variations

**Key principle**: Maximize ingredient synergies (e.g., Rotkohl for curry, salad, soup, wraps)

### External Recipe Support

Users can now maintain their own recipe databases:
- **Location**: `recipe-database.md` in their project directory
- **Usage**: Automatically detected when skill is invoked
- **Benefits**: Update recipes without skill releases, version control separately
- **Template**: See `example-recipe-project/` for ready-to-use template
- **Guide**: Full instructions in `references/external-recipes-guide.md`

When the skill is invoked, it checks for external recipes first, then falls back to bundled recipes.

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

### Modifying the Skill Definition
When updating `SKILL.md`:
1. **Frontmatter**: The YAML frontmatter (`name` and `description`) defines how the skill appears to other Claude instances
2. **Description field**: Should clearly state when to invoke this skill and what it provides
3. **Content structure**: Keep the existing sections (Quick Start, Challenge Rules, Workflow, etc.) as they form the skill's "prompt"
4. **Resource links**: Ensure all references to bundled files (scripts, references) are accurate
5. **Test changes**: After modifying SKILL.md, test by simulating how another Claude instance would use the skill

The skill can be created/updated using the `session-start-hook` skill if needed.

### Common Adjustments

**Protein too low (<75g)**:
- Add 80-100g tofu to meals (+10-15g protein)
- Add extra Nussmus to breakfast (+4g protein)
- Add extra legumes to meals (+8-12g protein per 100g)
- Increase Erbsenprotein-Pulver in liquid meals (Overnight Oats, Smoothies)

**Calories too high (>1300)**:
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
- [ ] No excluded ingredients (Auberginen, Dicke Bohnen, Grünkohl, Rosenkohl, Wirsing, Rosinen)
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
- Bundled recipe collection: `references/recipe-database.md`
- External recipe guide: `references/external-recipes-guide.md`
- Example recipe project: `example-recipe-project/`
- Verification script: `scripts/verify_nutrition.py`
- Mealie export: `scripts/mealie_export.py`
