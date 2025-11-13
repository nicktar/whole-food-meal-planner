# External Recipe Database Guide

This guide explains how to use external recipe databases with the Whole Food Meal Planner skill.

## Overview

The `whole-food-meal-planner` skill supports **project-specific recipe databases**, allowing you to:
- Maintain your own recipe collections without modifying the skill
- Update recipes without requiring skill releases
- Version control recipes separately from the skill
- Share recipe collections independently
- Manage multiple recipe projects (family recipes, seasonal, experimental)

## How It Works

When you invoke the `whole-food-meal-planner` skill from a project, Claude will:

1. **Check for external recipes**: Look for `recipe-database.md` in your project directory
2. **Use external recipes**: If found, use your project's recipe database
3. **Fall back to bundled recipes**: If not found, use the skill's bundled recipes in `references/recipe-database.md`
4. **Support custom paths**: Accept custom recipe file paths if you specify them

## Setting Up an External Recipe Database

### Step 1: Create Your Project

Create a new project directory for your recipes:

```bash
mkdir my-meal-plans
cd my-meal-plans
git init  # Optional: version control your recipes
```

### Step 2: Create recipe-database.md

Create a `recipe-database.md` file in your project root. Use the bundled recipe database as a template:

```bash
# Copy the bundled template as a starting point
cp /path/to/whole-food-meal-planner/references/recipe-database.md ./recipe-database.md
```

### Step 3: Customize Your Recipes

Edit `recipe-database.md` to add your own recipes. **Important:** Maintain the same structure:

```markdown
# Whole Food Challenge Rezept-Datenbank

## Challenge-Konforme Zutaten
[Keep the rules section - this is important for validation]

## FRÜHSTÜCK

### Recipe Name
**Portion: X Person | Kalorien: ~XXX | Protein: ~XXg | Prep: XX Min**

**Zutaten:**
- Ingredient 1
- Ingredient 2
...

**Zubereitung:**
1. Step 1
2. Step 2
...

**Meal Prep:** Storage and prep notes

---
```

### Step 4: Invoke the Skill

When working in your project, invoke the skill as usual:

```
@whole-food-meal-planner Create a 3-day meal plan with 1200 kcal/day
```

The skill will automatically detect and use your `recipe-database.md`.

## Recipe Database Format Requirements

Your external recipe database must follow these conventions:

### 1. File Structure

```markdown
# Whole Food Challenge Rezept-Datenbank

## Challenge-Konforme Zutaten
[Rules section with allowed/excluded ingredients]

## FRÜHSTÜCK
[Breakfast recipes]

## MITTAGESSEN & ABENDESSEN
[Lunch and dinner recipes]

## DRESSINGS & SAUCEN
[Dressings and sauces]

## SNACKS & EXTRAS
[Snacks]

## MEAL PREP BASISKOMPONENTEN
[Base components for meal prep]

## NÄHRWERT-DURCHSCHNITTE
[Nutritional averages summary]
```

### 2. Recipe Format

Each recipe should include:

- **Header**: Recipe name (### level)
- **Metadata line**: `**Portion: X | Kalorien: ~XXX | Protein: ~XXg | Prep: XX Min**`
- **Zutaten section**: Bulleted list of ingredients
- **Zubereitung section**: Numbered preparation steps
- **Meal Prep notes**: Storage duration and prep tips
- **Separator**: `---` between recipes

### 3. Required Information

For each recipe, include:
- ✅ Accurate calorie and protein counts
- ✅ Realistic portion sizes
- ✅ Clear prep/cook times
- ✅ Meal prep and storage information
- ✅ Only challenge-compliant ingredients

### 4. Challenge Compliance

Ensure all recipes exclude:
- ❌ Auberginen (eggplant)
- ❌ Dicke Bohnen (fava beans)
- ❌ Grünkohl (kale)
- ❌ Rosenkohl (Brussels sprouts)
- ❌ Wirsing (savoy cabbage)
- ❌ All animal products
- ❌ All processed foods

## Multiple Recipe Collections

You can maintain multiple recipe projects:

```
~/meal-planning/
├── family-recipes/
│   └── recipe-database.md       # Family favorites
├── seasonal-winter/
│   └── recipe-database.md       # Winter seasonal recipes
├── meal-prep-batch/
│   └── recipe-database.md       # Batch cooking recipes
└── experimental/
    └── recipe-database.md       # New recipes being tested
```

Each project can have its own recipe collection. Simply work in the desired project and invoke the skill.

## Custom Recipe Locations

If you want to use a different filename or path:

```
@whole-food-meal-planner Using recipes from my-recipes/database.md, create a 5-day meal plan
```

Explicitly specify the path when invoking the skill.

## Workflow with External Recipes

### Initial Setup
1. Create project directory
2. Copy bundled `recipe-database.md` as template
3. Customize with your recipes
4. Optional: Set up git for version control

### Regular Usage
1. Work in your recipe project
2. Invoke skill normally - it auto-detects external recipes
3. Update recipes as needed (no skill release required!)
4. Commit changes to version control

### Sharing Recipes
1. Share your recipe project directory
2. Others can use it by invoking the skill from that directory
3. No need to modify or fork the skill itself

## Validating Your External Recipes

After creating your external recipe database:

1. **Test with a simple meal plan**:
   ```
   @whole-food-meal-planner Create a 1-day meal plan using my recipes
   ```

2. **Verify the skill uses your recipes**:
   - Claude will indicate which recipe source it's using
   - Check that your custom recipes appear in the plan

3. **Run nutritional verification**:
   ```bash
   python3 scripts/verify_nutrition.py
   ```

4. **Check challenge compliance**:
   - Ensure no excluded ingredients
   - Verify nutritional targets are met

## Benefits Over Bundled Recipes

### Flexibility
- Update recipes anytime without waiting for skill releases
- Test experimental recipes without affecting the stable skill

### Organization
- Separate recipe collections for different purposes
- Version control your personal recipe evolution
- Track what works for your family/preferences

### Collaboration
- Share recipe collections with others
- Contribute to community recipe repositories
- Maintain personal forks with custom tweaks

### Privacy
- Keep personal recipes private
- No need to submit PRs for personal modifications
- Full control over your recipe data

## Bundled Recipes as Reference

The bundled recipes in `references/recipe-database.md` remain useful as:
- **Template**: Format example for creating your own recipes
- **Reference**: Verified, tested recipes to learn from
- **Fallback**: Available when no external database exists
- **Inspiration**: Ideas for meal combinations and prep strategies

You can always reference bundled recipes:
```bash
view references/recipe-database.md
```

## Troubleshooting

### Skill doesn't detect my external recipes

**Check:**
1. File is named `recipe-database.md` exactly
2. File is in the project root directory (where you invoked the skill)
3. File has proper markdown formatting

**Solution:**
```bash
ls -la recipe-database.md  # Verify file exists
head -20 recipe-database.md  # Check format
```

### Recipes don't match bundled format

**Check:**
- Recipe headers use `###` level
- Metadata line uses bold formatting: `**Portion: ...**`
- Sections use proper names: "Zutaten", "Zubereitung", "Meal Prep"

**Solution:**
Compare your recipe format to bundled examples:
```bash
diff recipe-database.md references/recipe-database.md
```

### Nutritional validation fails

**Check:**
- Calorie/protein counts are accurate
- Portion sizes are realistic
- No excluded ingredients

**Solution:**
Run the verification script after creating meal plans:
```bash
python3 scripts/verify_nutrition.py
```

### Want to switch between external and bundled

**Option 1**: Rename your external database temporarily
```bash
mv recipe-database.md my-recipes-backup.md
# Skill will use bundled recipes
```

**Option 2**: Work in a different directory
```bash
cd /tmp  # No external recipes here
# Invoke skill - uses bundled recipes
```

## Example: Creating Your First External Recipe

Here's a complete example of adding a custom breakfast recipe:

```markdown
### Buchweizen-Porridge mit Banane und Mandeln
**Portion: 1 Person | Kalorien: ~340 | Protein: ~11g | Prep: 15 Min**

**Zutaten:**
- 50g Buchweizen (roh)
- 200ml Mandelmilch (ungesüßt)
- 1 mittelgroße Banane, in Scheiben
- 15g Mandeln, gehackt
- 1 TL Ahornsirup (optional)
- 1/2 TL Vanilleextrakt
- Prise Kardamom
- Prise Salz

**Zubereitung:**
1. Buchweizen nach Packungsanweisung kochen (ca. 10-12 Min)
2. Mandelmilch, Vanille und Salz unterrühren
3. Weitere 2-3 Min köcheln bis cremig
4. In Schüssel geben, mit Bananenscheiben belegen
5. Mandeln und Kardamom darüberstreuen
6. Optional mit Ahornsirup süßen

**Meal Prep:** Buchweizen vorkochen (4 Tage haltbar), morgens nur mit Milch erwärmen und toppen (3-4 Min)

**Variationen:**
- Im Sommer: Mit frischen Beeren statt Banane
- Im Winter: Mit getrockneten Datteln und Zimt
- Protein-Boost: Mit 1 EL Mandelbutter (+4g Protein)

**Nährwert-Details:**
- Kohlenhydrate: ~52g
- Fett: ~9g
- Ballaststoffe: ~7g

---
```

## Best Practices

1. **Start with bundled recipes**: Copy as template, modify gradually
2. **Test thoroughly**: Verify nutrition and compliance before relying on new recipes
3. **Document changes**: Keep notes on recipe modifications and results
4. **Version control**: Use git to track recipe evolution
5. **Share carefully**: When sharing, include the challenge rules section
6. **Stay compliant**: Always check against excluded ingredients list
7. **Maintain format**: Consistent formatting makes skill parsing reliable
8. **Include meal prep notes**: Critical for effective planning

## Resources

- **Bundled recipe database**: `/references/recipe-database.md`
- **Meal planning workflow**: `/references/meal-plan-workflow.md`
- **Verification script**: `/scripts/verify_nutrition.py`
- **SKILL.md**: Main skill documentation with external recipe support details

## Support

If you encounter issues with external recipe databases:

1. Check this guide for troubleshooting steps
2. Compare your format to bundled examples
3. Run verification scripts to check compliance
4. Review SKILL.md for workflow details

Remember: The bundled recipes remain available as a fallback and reference at all times!
