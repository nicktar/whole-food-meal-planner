#!/usr/bin/env python3
"""
Mealie Recipe Export Tool - Parser-basierte Version

Parst Markdown-Rezeptdateien und konvertiert sie automatisch in Mealie-kompatibles
schema.org JSON Format. Kein manuelles Code-Schreiben mehr nötig!

Usage:
    python3 scripts/mealie_export.py rezepte-2024-12-08-bis-12.md
    python3 scripts/mealie_export.py meal-plans/wochenplan-08-12-dezember.md
    python3 scripts/mealie_export.py neue-rezepte-dezember.md --prefix 2024-12-08
"""

import json
import re
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict
import sys


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class RecipeNutrition:
    """Nährwertangaben für ein Rezept"""
    calories: str
    protein: str
    carbs: str
    fat: str
    fiber: str


@dataclass
class ParsedRecipe:
    """Geparste Rezept-Daten aus Markdown"""
    name: str
    description: str
    meal_type: str  # Frühstück, Mittagessen, Abendessen
    prep_time: str  # ISO 8601 Format
    cook_time: str  # ISO 8601 Format
    total_time: str  # ISO 8601 Format
    ingredients: List[str]
    instructions: str
    nutrition: RecipeNutrition
    servings: str = "1 Portion"


# ============================================================================
# MARKDOWN PARSER
# ============================================================================

class RecipeMarkdownParser:
    """Parst Rezepte aus verschiedenen Markdown-Formaten"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.content = f.read()

    def parse_all_recipes(self) -> List[ParsedRecipe]:
        """Extrahiert alle Rezepte aus der Datei"""
        recipes = []

        # Erkennt verschiedene Rezept-Header-Formate
        # Format 1: "### Frühstück: Overnight Oats Beeren-Power"
        # Format 2: "## DEFTIGE LINSEN-WURZELGEMÜSE-SUPPE"
        # Format 3: "### 1. Overnight Oats Beeren-Power"

        # Wochenplan-Format parsen (TAG 1, TAG 2, etc.)
        if "TAG 1" in self.content or "TAG " in self.content:
            recipes.extend(self._parse_wochenplan_format())

        # Standalone Rezepte-Format (## REZEPTNAME)
        elif re.search(r'^##\s+[A-ZÄÖÜ]', self.content, re.MULTILINE):
            recipes.extend(self._parse_standalone_recipes())

        return recipes

    def _parse_wochenplan_format(self) -> List[ParsedRecipe]:
        """Parst Rezepte aus Wochenplan-Format"""
        recipes = []

        # Finde alle Mahlzeiten (### Frühstück:, ### Mittagessen:, ### Abendessen:)
        meal_pattern = r'###\s+(Frühstück|Mittagessen|Abendessen):\s+(.+?)(?=\n\*\*Kalorien)'
        meals = re.finditer(meal_pattern, self.content, re.MULTILINE)

        for match in meals:
            meal_type = match.group(1)
            recipe_name = match.group(2).strip()

            # Überspringe Wiederholungen
            if "Wiederholung" in recipe_name or "(siehe " in recipe_name.lower():
                continue

            # Extrahiere Rezept-Block
            start_pos = match.start()
            next_meal = re.search(r'\n###\s+(Frühstück|Mittagessen|Abendessen|Tageszusammenfassung)',
                                 self.content[start_pos + 1:])
            end_pos = start_pos + next_meal.start() if next_meal else len(self.content)

            recipe_block = self.content[start_pos:end_pos]

            try:
                parsed = self._parse_recipe_block(recipe_name, meal_type, recipe_block)
                if parsed:
                    recipes.append(parsed)
            except Exception as e:
                print(f"⚠️  Fehler beim Parsen von '{recipe_name}': {e}")

        return recipes

    def _parse_standalone_recipes(self) -> List[ParsedRecipe]:
        """Parst Standalone-Rezepte (## REZEPTNAME Format)"""
        recipes = []

        # Splitte nach ## Überschriften
        sections = re.split(r'\n##\s+(?=[A-ZÄÖÜ])', self.content)

        for section in sections[1:]:  # Erste Section ist meist Header/Intro
            try:
                # Extrahiere Rezeptname
                name_match = re.match(r'^([^\n]+)', section)
                if not name_match:
                    continue

                recipe_name = name_match.group(1).strip()

                # Überspringe keine Rezepte
                if any(skip in recipe_name.upper() for skip in ['FRÜHSTÜCK', 'MITTAGESSEN', 'ABENDESSEN',
                                                                  'DRESSINGS', 'SAUCEN']):
                    # Das sind Kategorien, keine Rezepte
                    continue

                # Bestimme Meal Type aus Kontext
                meal_type = self._detect_meal_type(section)

                parsed = self._parse_recipe_block(recipe_name, meal_type, section)
                if parsed:
                    recipes.append(parsed)
            except Exception as e:
                print(f"⚠️  Fehler beim Parsen eines Rezepts: {e}")

        return recipes

    def _parse_recipe_block(self, name: str, meal_type: str, block: str) -> Optional[ParsedRecipe]:
        """Parst einen einzelnen Rezept-Block"""

        # Extrahiere Nährwerte
        nutrition = self._extract_nutrition(block)
        if not nutrition:
            return None

        # Extrahiere Zutaten
        ingredients = self._extract_ingredients(block)
        if not ingredients:
            return None

        # Extrahiere Zubereitung
        instructions = self._extract_instructions(block)
        if not instructions:
            # Fallback für Meal-Prep-Rezepte ohne explizite Zubereitung
            instructions = "Aus Kühlschrank nehmen und servieren. Details siehe Meal Prep Strategie."

        # Extrahiere Zeiten
        prep_time, cook_time = self._extract_times(block)
        total_time = self._calculate_total_time(prep_time, cook_time)

        # Erstelle Beschreibung
        description = self._generate_description(name, nutrition, block)

        return ParsedRecipe(
            name=name,
            description=description,
            meal_type=meal_type,
            prep_time=prep_time,
            cook_time=cook_time,
            total_time=total_time,
            ingredients=ingredients,
            instructions=instructions,
            nutrition=nutrition
        )

    def _extract_nutrition(self, block: str) -> Optional[RecipeNutrition]:
        """Extrahiert Nährwertangaben"""
        # Suche nach Nährwerte-Sektion
        # Unterstützt sowohl Ganzzahlen als auch Dezimalzahlen (z.B. 31.0g)
        patterns = [
            r'\*\*Nährwerte.*?:\*\*.*?Kalorien:\s*([\d.]+)\s*kcal.*?Protein:\s*([\d.]+)g.*?Kohlenhydrate:\s*([\d.]+)g.*?Fett:\s*([\d.]+)g.*?Ballaststoffe:\s*([\d.]+)g',
            r'Kalorien:\s*([\d.]+)\s*kcal.*?Protein:\s*([\d.]+)g.*?Carbs:\s*([\d.]+)g.*?Fett:\s*([\d.]+)g.*?Fiber:\s*([\d.]+)g',
            r'\*\*Kalorien:\*\*\s*([\d.]+)\s*kcal.*?\*\*Protein:\*\*\s*([\d.]+)g'
        ]

        for pattern in patterns:
            match = re.search(pattern, block, re.DOTALL | re.IGNORECASE)
            if match:
                if len(match.groups()) >= 5:
                    return RecipeNutrition(
                        calories=f"{match.group(1)}",
                        protein=f"{match.group(2)}g",
                        carbs=f"{match.group(3)}g",
                        fat=f"{match.group(4)}g",
                        fiber=f"{match.group(5)}g"
                    )

        return None

    def _extract_ingredients(self, block: str) -> List[str]:
        """Extrahiert Zutatenliste"""
        ingredients = []

        # Finde Zutaten-Sektionen
        # Verschiedene Formate: **Zutaten:**, **Basis:**, **Toppings:**, **Komponenten:**
        sections = re.findall(
            r'\*\*(?:Zutaten|Basis|Toppings|Komponenten|Für.*?).*?\*\*\n((?:^-\s+.+$\n?)+)',
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

    def _extract_instructions(self, block: str) -> str:
        """Extrahiert Zubereitungsanleitung"""
        # Finde Zubereitung-Sektion
        patterns = [
            r'\*\*Zubereitung:\*\*\s*\n(.+?)(?=\n\*\*|$)',
            r'\*\*Anleitung:\*\*\s*\n(.+?)(?=\n\*\*|$)',
            r'## Zubereitung\s*\n(.+?)(?=\n##|$)'
        ]

        for pattern in patterns:
            match = re.search(pattern, block, re.DOTALL)
            if match:
                instructions = match.group(1).strip()
                # Bereinige Formatierung
                instructions = re.sub(r'\n\n+', '\n', instructions)
                return instructions

        return ""

    def _extract_times(self, block: str) -> tuple[str, str]:
        """Extrahiert Prep und Cook Time"""
        prep_time = "PT0M"
        cook_time = "PT0M"

        # Suche nach Prep-Angabe
        prep_match = re.search(r'\*\*Prep:\*\*\s*(\d+)\s*Min', block)
        if prep_match:
            prep_time = f"PT{prep_match.group(1)}M"

        # Suche nach Koch-Zeit in Zubereitung
        cook_matches = re.findall(r'(\d+)[-\s]*Min', block)
        if cook_matches:
            # Nimm die größte Zeit als Cook Time
            max_time = max(int(t) for t in cook_matches)
            cook_time = f"PT{max_time}M"

        return prep_time, cook_time

    def _calculate_total_time(self, prep: str, cook: str) -> str:
        """Berechnet Gesamtzeit"""
        prep_min = int(re.search(r'PT(\d+)M', prep).group(1)) if prep != "PT0M" else 0
        cook_min = int(re.search(r'PT(\d+)M', cook).group(1)) if cook != "PT0M" else 0
        total = prep_min + cook_min
        return f"PT{total}M" if total > 0 else "PT0M"

    def _detect_meal_type(self, block: str) -> str:
        """Erkennt Mahlzeit-Typ aus Kontext"""
        block_lower = block.lower()

        if any(word in block_lower for word in ['overnight oats', 'chia pudding', 'frühstück', 'müsli']):
            return "Frühstück"
        elif any(word in block_lower for word in ['suppe', 'curry', 'buddha bowl', 'salat']):
            # Entscheide zwischen Mittag/Abend basierend auf Komplexität
            if 'suppe' in block_lower and 'deftig' in block_lower:
                return "Abendessen"
            return "Mittagessen"

        return "Mittagessen"  # Default

    def _generate_description(self, name: str, nutrition: RecipeNutrition, block: str) -> str:
        """Generiert Rezept-Beschreibung"""
        desc_parts = []

        # Füge Protein-Highlight hinzu (unterstützt Ganzzahlen und Dezimalzahlen)
        protein_value = float(nutrition.protein.replace('g', ''))
        if protein_value >= 30:
            desc_parts.append(f"Protein-reich mit {nutrition.protein} Protein")

        # Suche nach Meal Prep Hinweisen
        if 'meal prep' in block.lower():
            desc_parts.append("Meal-Prep-freundlich")

        # Suche nach Besonderheiten
        if 'roh' in block.lower() or 'ROH' in block:
            desc_parts.append("mit knackigem Rohkost-Anteil")

        if 'saisonal' in block.lower():
            desc_parts.append("mit saisonalen Zutaten")

        if not desc_parts:
            desc_parts.append(f"{nutrition.calories} kcal, {nutrition.protein} Protein")

        return " - ".join(desc_parts) + "."


# ============================================================================
# MEALIE CONVERTER
# ============================================================================

class MealieConverter:
    """Konvertiert ParsedRecipe zu Mealie schema.org Format"""

    @staticmethod
    def convert(recipe: ParsedRecipe) -> Dict:
        """Konvertiert zu Mealie-Format"""
        return {
            "@context": "https://schema.org",
            "@type": "Recipe",
            "name": recipe.name,
            "description": recipe.description,
            "recipeYield": recipe.servings,
            "prepTime": recipe.prep_time,
            "performTime": recipe.cook_time,
            "totalTime": recipe.total_time,
            "recipeCategory": [recipe.meal_type],
            "keywords": "whole food,food prep,vegetarisch,vegan," + recipe.meal_type,
            "recipeIngredient": recipe.ingredients,
            "recipeInstructions": recipe.instructions,
            "nutrition": {
                "calories": recipe.nutrition.calories,
                "proteinContent": recipe.nutrition.protein,
                "carbohydrateContent": recipe.nutrition.carbs,
                "fatContent": recipe.nutrition.fat,
                "fiberContent": recipe.nutrition.fiber
            }
        }


# ============================================================================
# FILE NAMING
# ============================================================================

class FileNamer:
    """Generiert datumsbereiche-basierte Dateinamen"""

    @staticmethod
    def from_filename(source_file: str) -> str:
        """Extrahiert Datumsbereich aus Dateinamen"""
        # Format: rezepte-2024-12-08-bis-12.md -> 2024_12_08
        # Format: wochenplan-08-12-dezember.md -> 2024_12_08 (braucht Jahr aus aktuellem Kontext)

        source = Path(source_file).stem

        # Versuche YYYY-MM-DD Format zu finden
        match = re.search(r'(\d{4})-(\d{2})-(\d{2})', source)
        if match:
            return f"{match.group(1)}_{match.group(2)}_{match.group(3)}"

        # Versuche DD-MM-Monat Format
        match = re.search(r'(\d{2})-(\d{2})-(\w+)', source)
        if match:
            day, month_end, month_name = match.groups()
            month_map = {
                'januar': '01', 'februar': '02', 'märz': '03', 'april': '04',
                'mai': '05', 'juni': '06', 'juli': '07', 'august': '08',
                'september': '09', 'oktober': '10', 'november': '11', 'dezember': '12'
            }
            month_num = month_map.get(month_name.lower(), '01')
            # Nehme aktuelles Jahr an (oder hardcode 2024 für jetzt)
            return f"2024_{month_num}_{day}"

        # Fallback: Use filename as-is
        return source.replace('-', '_')

    @staticmethod
    def generate_filename(prefix: str, recipe_name: str) -> str:
        """Generiert JSON Dateinamen"""
        # Bereinige Rezeptnamen: Lowercase, Umlaute, keine Sonderzeichen
        clean_name = recipe_name.lower()
        clean_name = clean_name.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
        clean_name = re.sub(r'[^\w\s-]', '', clean_name)
        clean_name = re.sub(r'[-\s]+', '_', clean_name)
        clean_name = clean_name[:50]  # Limit length

        return f"{prefix}_{clean_name}.json"


# ============================================================================
# EXPORTER
# ============================================================================

class MealieExporter:
    """Hauptklasse für Export-Prozess"""

    def __init__(self, output_dir: str = "mealie_exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def export_from_file(self, markdown_file: str, prefix: Optional[str] = None) -> int:
        """Exportiert alle Rezepte aus Markdown-Datei"""

        print(f"📖 Lese Rezepte aus: {markdown_file}")

        # Parse Rezepte
        parser = RecipeMarkdownParser(markdown_file)
        recipes = parser.parse_all_recipes()

        if not recipes:
            print("⚠️  Keine Rezepte gefunden!")
            return 0

        print(f"✅ {len(recipes)} Rezepte gefunden\n")

        # Bestimme Dateinamen-Prefix
        if prefix is None:
            prefix = FileNamer.from_filename(markdown_file)

        # Konvertiere und exportiere
        converter = MealieConverter()
        exported_count = 0

        for recipe in recipes:
            try:
                # Konvertiere zu Mealie-Format
                mealie_recipe = converter.convert(recipe)

                # Generiere Dateinamen
                filename = FileNamer.generate_filename(prefix, recipe.name)
                filepath = self.output_dir / filename

                # Speichere JSON
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(mealie_recipe, f, ensure_ascii=False, indent=2)

                print(f"✅ {recipe.name}")
                print(f"   → {filename}")
                exported_count += 1

            except Exception as e:
                print(f"❌ Fehler bei '{recipe.name}': {e}")

        return exported_count


# ============================================================================
# CLI
# ============================================================================

def main():
    """Command-line interface"""
    if len(sys.argv) < 2:
        print("Usage: python3 mealie_export.py <markdown_file> [--prefix YYYY_MM_DD]")
        print("\nBeispiele:")
        print("  python3 mealie_export.py rezepte-2024-12-08-bis-12.md")
        print("  python3 mealie_export.py wochenplan-08-12-dezember.md --prefix 2024_12_08")
        sys.exit(1)

    markdown_file = sys.argv[1]
    prefix = None

    # Check for --prefix argument
    if len(sys.argv) >= 4 and sys.argv[2] == '--prefix':
        prefix = sys.argv[3]

    # Export
    exporter = MealieExporter()

    print("=" * 60)
    print("📦 Mealie Recipe Exporter (Parser-basiert)")
    print("=" * 60)
    print()

    count = exporter.export_from_file(markdown_file, prefix)

    print()
    print("=" * 60)
    print(f"✅ Export abgeschlossen: {count} Rezepte exportiert")
    print(f"📁 Ausgabeverzeichnis: mealie_exports/")
    print("=" * 60)


if __name__ == "__main__":
    main()
