---
name: whole-food-meal-planner
description: Comprehensive meal planning system for the Whole Food Challenge with verified recipes, nutritional validation, Mealie integration, and automated meal prep strategies. Use when creating meal plans that require only whole foods (no processed foods, no animal products), have specific caloric/protein targets (typically 1200 kcal, 100+g protein), need nutritional verification, require Mealie-compatible recipe exports, or need detailed meal prep workflows with shopping lists. Especially useful for multi-day plans (3-7 days) with ingredient synergies.
---

# Whole Food Challenge Meal Planner

Complete meal planning system für die Whole Food Challenge mit Rezept-Datenbank, Nährwert-Verifikation und Mealie-Integration.

## External Recipe Database Support

**This skill supports project-specific recipe databases!**

When invoked from a project, the skill will:
1. **First check** for `recipe-database.md` in the current project directory
2. **Fall back** to bundled recipes (in `references/recipe-database.md`) if no external database exists
3. Support **custom paths** if specified by the user (e.g., `my-recipes/database.md`)

**Benefits:**
- Update recipes without skill releases
- Maintain multiple recipe collections (family recipes, seasonal, experimental)
- Version control your personal recipes separately
- Share recipe collections independently

**To use external recipes:**
1. Create a `recipe-database.md` file in your project directory
2. Follow the same format as the bundled recipe database (see bundled resources below)
3. Invoke this skill from your project - it will automatically use your recipes
4. The bundled recipes remain available as reference templates

**When working with external recipes:**
- Always check which recipe source is being used (external vs. bundled)
- Maintain the same structure: Challenge rules, nutritional info, meal prep notes
- The skill will indicate which recipe source it's using

## Quick Start

**Typischer Workflow:**
1. Anforderungen sammeln (siehe `references/meal-plan-workflow.md` Abschnitt 1)
2. Rezepte aus Datenbank auswählen (externe `recipe-database.md` oder `references/recipe-database.md`)
3. Meal Plan erstellen (Templates in `meal-plan-workflow.md`)
4. Mit `scripts/verify_nutrition.py` validieren
5. Optional: Mealie-Export mit `scripts/mealie_export.py`

**Für neue Meal Plans:**
```bash
# 1. Workflow-Guide lesen für vollständigen Prozess
view references/meal-plan-workflow.md

# 2. Check for external recipes first, then bundled recipes
ls recipe-database.md  # Check if external database exists
view recipe-database.md || view references/recipe-database.md

# 3. Nach Plan-Erstellung: Nährwerte verifizieren
python3 scripts/verify_nutrition.py

# 4. Optional: Mealie-Rezepte exportieren
python3 scripts/mealie_export.py
```

## Challenge-Regeln

**Erlaubte Zutaten:**
- Vollkornprodukte (Hafer, Quinoa, Buchweizen, Dinkel, etc.)
- Hülsenfrüchte (Linsen, Kichererbsen, Cannellini-Bohnen, schwarze Bohnen)
- Früchte (frisch oder getrocknet)
- Gemüse (alle Sorten)
- Nüsse und Samen
- Nussmus (natürlich, ohne Zusätze)
- Pflanzenmilch (ungesüßt)
- Currypasten (vegan)
- Nährhefe
- Gewürze, Kräuter, Essig, Öl

**Ausgeschlossen:**
- Auberginen
- Dicke Bohnen (Ackerbohnen/Puffbohnen)
- Grünkohl
- Rosenkohl
- Wirsing
- Alle tierischen Produkte
- Verarbeitete Lebensmittel

## Standard-Targets

**Tägliche Ziele (typisch):**
- Kalorien: 1200 kcal (Range: 1150-1250)
- Protein: 100-110g (Minimum: 100g)
- Ballaststoffe: 40g (Minimum: 30g)

**Mahlzeiten-Ranges:**
- Frühstück: 300-400 kcal, 10-15g Protein
- Mittagessen: 250-450 kcal, 15-25g Protein
- Abendessen: 250-400 kcal, 15-25g Protein

## Bundled Resources

### Scripts

**`scripts/verify_nutrition.py`** - Nährwert-Verifikation
- Validiert Tagespläne gegen Targets
- Zeigt Abweichungen und Warnungen
- Output: Text-Report + JSON
- **Wann verwenden:** Nach jedem Meal Plan, vor Finalisierung

**`scripts/mealie_export.py`** - Mealie-Integration
- Generiert Mealie-kompatible JSON-Rezepte
- Inkl. Nährwerte, Zutaten, Instruktionen
- **Wann verwenden:** Wenn Nutzer Mealie verwendet oder Rezepte digital verwalten möchte

### References

**Recipe Database** - Verifizierte Rezepte
- **Location:** `recipe-database.md` (external, if present) or `references/recipe-database.md` (bundled)
- Komplette Rezept-Sammlung mit Nährwerten
- Frühstück, Mittag/Abend, Dressings, Snacks
- Meal-Prep-Hinweise und Haltbarkeit
- **Wann lesen:** Bei jeder Meal Plan Erstellung für Rezept-Auswahl
- **External support:** Create `recipe-database.md` in your project for custom recipes

**`references/meal-plan-workflow.md`** - Workflow-Guide
- Schritt-für-Schritt Anleitung
- Templates für Tagespläne
- Meal Prep Strategien
- Einkaufslisten-Generator
- Optimierungs-Tipps
- **Wann lesen:** Vor der ersten Meal Plan Erstellung und als Referenz

## Meal Planning Workflow

### 1. Anforderungen sammeln
Nutze das Template aus `meal-plan-workflow.md` Abschnitt 1:
- Zeitraum (3-7 Tage typisch)
- Ernährungsziele (Kalorien, Protein)
- Mahlzeitenstruktur
- Präferenzen/Ausschlüsse
- Zu verbrauchende Zutaten

### 2. Rezeptauswahl
**First check for external recipe database in project root, otherwise use bundled recipes:**
```bash
# Check which recipe source is available
ls recipe-database.md && echo "Using external recipes" || echo "Using bundled recipes"
```

Aus der Recipe Database (external oder `references/recipe-database.md`):
- **Frühstück:** 3-5 Rezepte rotieren (Overnight Oats, Porridge, Bowls)
- **Mittag/Abend:** 5-7 Rezepte mit Synergie-Fokus
- **Kriterien:**
  - Verschiedene Proteinquellen
  - Mix warm/kalt
  - Meal-Prep-freundlich
  - Nutzer-Präferenzen

### 3. Plan erstellen
Format nach Template in `meal-plan-workflow.md` Abschnitt 3:
```markdown
## TAG X - Datum

### Frühstück: [Rezept]
**Kalorien:** XXX | **Protein:** XXg | **Prep:** XX Min
[Details...]

### Mittagessen: [Rezept]
[...]

### Abendessen: [Rezept]
[...]

**Tageszusammenfassung:**
- Gesamt Kalorien: XXX kcal
- Gesamt Protein: XXg
```

### 4. Verifikation
**KRITISCH:** Nach Plan-Erstellung IMMER verifizieren:
```python
# In verify_nutrition.py: Meal/DailyPlan Objekte mit tatsächlichen Werten erstellen
python3 scripts/verify_nutrition.py
```

**Bei Abweichungen anpassen:**
- Kalorien zu niedrig → Nüsse/Avocado ergänzen
- Protein zu niedrig → Mehr Hülsenfrüchte/Tofu
- Kalorien zu hoch → Portionen reduzieren

### 5. Einkaufsliste
Generiere nach Template (Workflow Abschnitt 5):
- Nach Kategorien gruppiert
- Mengen für gesamten Zeitraum
- Saisonale Alternativen
- Lagerungs-Tipps

### 6. Meal Prep Strategie
Erstelle Timeline nach Template (Workflow Abschnitt 6):
- **Phase 1:** Grundlagen (Getreide, Hülsenfrüchte)
- **Phase 2:** Gemüse rösten, Protein vorbereiten
- **Phase 3:** Spezial-Komponenten
- **Phase 4:** Portionieren & Lagern

**Optimierung:**
- Parallele Tasks maximieren
- Passive Kochzeit nutzen
- Ofen-Kapazität ausnutzen

### 7. Optional: Mealie-Export
Falls gewünscht:
```python
# In mealie_export.py: Rezept-Objekte erstellen
python3 scripts/mealie_export.py
# Output: mealie_exports/*.json
```

## Best Practices

### Zeit-Effizienz
- Meal Prep am Sonntag: 3-4 Stunden für 5 Tage
- Täglicher Aufwand: 5-15 Minuten
- Paralleles Kochen: Getreide + Hülsenfrüchte gleichzeitig

### Nährwert-Optimierung
- **Protein boosten:** Tofu, Tempeh, extra Hülsenfrüchte
- **Kalorien reduzieren:** Öl/Nüsse limitieren
- **Ballaststoffe erhöhen:** Mehr Gemüse, Vollkorn

### Abwechslung
- Gleiche Basis, verschiedene Gewürze
- Internationale Variationen (Mediterran, Asiatisch, Mexikanisch)
- Textur-Kontraste (knusprig + cremig)

### Meal-Prep-Synergien
- **Rotkohl:** Curry, Salat, mariniert, Suppe
- **Kichererbsen:** Geröstet, Buddha Bowl, Hummus
- **Quinoa:** Frühstück, Bowl-Basis, Salat

## Häufige Szenarien

### Szenario 1: Standard 5-Tage Plan
```
1. Anforderungen: 5 Tage, 1200 kcal, 100g Protein
2. Rezepte aus DB wählen (meal-plan-workflow.md Abschnitt 2)
3. Plan nach Template erstellen
4. verify_nutrition.py ausführen
5. Einkaufsliste + Meal Prep Timeline
```

### Szenario 2: Spezifische Zutaten verwerten
```
1. Nutzer hat z.B. viel Rotkohl
2. Recipe Database (external oder bundled) nach Rotkohl-Rezepten durchsuchen:
   - Rotkohl-Curry
   - Rotkohl-Salat mit Walnüssen
   - Rotkohl-Miso-Suppe
   - Rotkohl-Wrap-Marinade
3. Plan mit Rotkohl-Fokus erstellen
4. Verifikation + Anpassung
```

### Szenario 3: Protein-Boost erforderlich
```
1. Erste Verifikation zeigt <100g Protein
2. Anpassungen:
   - Tofu zu Suppen hinzufügen (+15g)
   - Tempeh statt Kichererbsen (+8g)
   - Extra Nussmus im Frühstück (+4g)
   - Edamame als Snack (+11g)
3. Erneut verifizieren
```

### Szenario 4: Mealie-Integration
```
1. Standard Meal Plan erstellen
2. mealie_export.py mit Plan-Rezepten anpassen
3. Rezepte als JSON exportieren
4. In Mealie importieren für Tracking
```

## Troubleshooting

**Problem:** Nährwerte stimmen nicht
→ verify_nutrition.py zeigt genaue Abweichungen
→ Siehe Workflow Abschnitt 4 für Anpassungs-Strategien

**Problem:** Zu viel Meal Prep Aufwand
→ Mehr Synergien nutzen (gleiche Basis-Komponenten)
→ Simplere Rezepte wählen
→ Batch-Größen erhöhen (Tiefkühler nutzen)

**Problem:** Zu monoton
→ Gewürz-Variationen für gleiche Basis
→ Verschiedene Zubereitungsarten (roh/geröstet/gedämpft)
→ Frische Toppings täglich variieren

**Problem:** Mealie-Export funktioniert nicht
→ Prüfe JSON-Format in mealie_exports/
→ Mealie erwartet spezifische Felder (siehe mealie_export.py)
→ Test mit Beispiel-Rezepten zuerst

## Qualitätskontrolle

Vor Finalisierung prüfen:
- [ ] Challenge-Regeln eingehalten (keine ausgeschlossenen Zutaten)
- [ ] Nährwerte verifiziert und im Target-Bereich
- [ ] Meal Prep Synergien maximiert
- [ ] Einkaufsliste vollständig und kategorisiert
- [ ] Realistische Zubereitungszeiten
- [ ] Lagerungshinweise enthalten
- [ ] Abwechslung über die Woche
- [ ] Saisonale und verfügbare Zutaten (Deutschland)
