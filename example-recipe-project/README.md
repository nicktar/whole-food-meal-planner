# Example Recipe Project

This is a template project showing how to use **external recipe databases** with the `whole-food-meal-planner` skill.

## What's This?

Instead of modifying the skill's bundled recipes, you can maintain your own recipe collection in a separate project. This allows you to:

- ✅ Update recipes without skill releases
- ✅ Version control your personal recipes
- ✅ Create multiple recipe collections
- ✅ Share recipes independently
- ✅ Keep personal recipes private

## Quick Start

### 1. Copy This Template

```bash
cp -r example-recipe-project ~/my-recipes
cd ~/my-recipes
```

### 2. Customize recipe-database.md

Edit `recipe-database.md` to add your own recipes. Keep the same format as shown.

### 3. Invoke the Skill

From within this project directory:

```
@whole-food-meal-planner Create a 3-day meal plan
```

The skill will automatically use your `recipe-database.md` file!

## File Structure

```
example-recipe-project/
├── README.md                 # This file
├── recipe-database.md        # Your custom recipes
└── .gitignore               # Optional: for version control
```

## What's Included

This example includes:

- **recipe-database.md**: A starter recipe collection with a few custom recipes
  - Follows the same format as bundled recipes
  - Includes all required sections
  - Challenge-compliant recipes

## Customization Guide

### Adding New Recipes

1. Open `recipe-database.md`
2. Find the appropriate section (FRÜHSTÜCK, MITTAGESSEN & ABENDESSEN, etc.)
3. Add your recipe following this format:

```markdown
### Recipe Name
**Portion: 1 Person | Kalorien: ~XXX | Protein: ~XXg | Prep: XX Min**

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

### Removing Recipes

Simply delete the recipe section you don't want. Keep the section headers (## FRÜHSTÜCK, etc.).

### Modifying Existing Recipes

Edit the recipes directly. Make sure to update:
- Ingredient quantities
- Nutritional information (calories, protein)
- Prep time
- Instructions

## Validation

After adding/modifying recipes, test them:

1. **Create a test meal plan**:
   ```
   @whole-food-meal-planner Create a 1-day meal plan
   ```

2. **Run nutritional verification** (requires the skill's scripts):
   ```bash
   python3 /path/to/whole-food-meal-planner/scripts/verify_nutrition.py
   ```

## Version Control (Optional)

Track your recipe evolution with git:

```bash
git init
git add recipe-database.md
git commit -m "Initial recipe collection"
```

Update regularly:

```bash
git add recipe-database.md
git commit -m "Added new breakfast recipe"
```

## Multiple Collections

Create different projects for different purposes:

```
~/meal-planning/
├── family-favorites/       # Recipes the family loves
├── seasonal-winter/        # Winter recipes
├── meal-prep-bulk/         # Batch cooking recipes
└── experimental/           # Testing new ideas
```

Each can have its own `recipe-database.md`.

## Challenge Rules

Remember these exclusions in all recipes:
- ❌ Auberginen (eggplant)
- ❌ Dicke Bohnen (fava beans)
- ❌ Grünkohl (kale)
- ❌ Rosenkohl (Brussels sprouts)
- ❌ Wirsing (savoy cabbage)
- ❌ All animal products
- ❌ All processed foods

## Resources

- **Full guide**: See `/references/external-recipes-guide.md` in the skill repo
- **Bundled recipes**: Reference at `/references/recipe-database.md` in the skill repo
- **Workflow guide**: `/references/meal-plan-workflow.md` in the skill repo

## Need Help?

1. Check the format in the bundled recipe database
2. Read `/references/external-recipes-guide.md` for detailed instructions
3. Compare your recipes to the examples in this template

## Tips

- **Start small**: Begin with a few recipes, expand over time
- **Test thoroughly**: Verify nutrition and compliance
- **Document changes**: Keep notes on what works
- **Stay organized**: Use consistent formatting
- **Back up regularly**: Use git or regular file backups

Happy meal planning! 🥗
