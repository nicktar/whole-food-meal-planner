---
name: whole-food-meal-planner
description: Comprehensive meal planning system for the Whole Food Challenge with recipe generation, verified recipes, nutritional validation, Mealie integration, and automated meal prep strategies. Can create new custom recipes based on available ingredients, dietary targets, and preferences - all automatically validated against challenge rules. Use when creating meal plans that require only whole foods (no processed foods, no animal products), generating new recipe ideas within strict dietary constraints, having specific caloric/protein targets (typically 1200 kcal, 100+g protein), needing nutritional verification, requiring Mealie-compatible recipe exports, or needing detailed meal prep workflows with shopping lists. Especially useful for multi-day plans (3-7 days) with ingredient synergies and custom recipe development.
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
- Erbsenprotein-Pulver (pur, ohne Zusätze)
- Früchte (frisch oder getrocknet)
- Gemüse (alle Sorten)
- Nüsse und Samen
- Nussmus (natürlich, ohne Zusätze)
- Pflanzenmilch (ungesüßt)
- Würzpasten (Curry-, Miso- etc., vegan)
- Nährhefe-Flocken
- Gewürze, Kräuter, Essig, Öl

**Ausgeschlossen:**
- Auberginen
- Dicke Bohnen/Ackerbohnen/Puffbohnen (alle anderen Bohnen sind erlaubt!)
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

## Neue Rezepte generieren

**Ein Key-Feature dieses Skills:** Erstelle neue, maßgeschneiderte Rezepte basierend auf Nutzer-Anforderungen!

### Wann neue Rezepte generieren?

- Nutzer hat spezifische Zutaten, die verbraucht werden sollen
- Bestimmte Geschmacksrichtungen oder Cuisines gewünscht
- Nährwert-Ziele, die mit vorhandenen Rezepten nicht erreicht werden
- Nutzer möchte Abwechslung oder neue Ideen
- Saisonale oder regional verfügbare Zutaten optimal nutzen
- Spezielle Präferenzen (z.B. "schnell", "batch-freundlich", "kalt")

### Prozess für Rezept-Generierung

1. **Anforderungen sammeln:**
   - Verfügbare/gewünschte Hauptzutaten
   - Nährwert-Targets (Kalorien, Protein pro Portion)
   - Mahlzeitentyp (Frühstück, Mittag, Abend, Snack)
   - Geschmacksrichtung (asiatisch, mediterran, mexikanisch, etc.)
   - Prep-Zeit und Komplexität
   - Meal-Prep-Eignung

2. **Challenge-Compliance prüfen:**
   - ✅ Nur erlaubte Zutaten verwenden (siehe Challenge-Regeln oben)
   - ❌ Keine ausgeschlossenen Zutaten (Auberginen, Dicke Bohnen, Grünkohl, Rosenkohl, Wirsing)
   - ❌ Keine tierischen Produkte
   - ❌ Keine verarbeiteten Lebensmittel

3. **Rezept entwickeln:**
   - Basis-Komponenten wählen (Getreide + Protein + Gemüse)
   - Geschmacks-Profile aufbauen (Gewürze, Dressings)
   - Nährwerte kalkulieren (pro Zutat summieren)
   - Zubereitung strukturieren (Schritt-für-Schritt)

4. **Nährwerte validieren:**
   - Gegen Meal-Ranges prüfen (siehe Standard-Targets oben)
   - Bei Bedarf anpassen (mehr Protein, weniger Kalorien, etc.)
   - `verify_nutrition.py` kann für finale Validierung verwendet werden

5. **Meal-Prep-Hinweise hinzufügen:**
   - Vorbereitung im Voraus
   - Haltbarkeit im Kühlschrank
   - Aufwärm-Tipps
   - Batch-Größen-Empfehlungen

### Template für neue Rezepte

```markdown
## [Rezeptname]

**Portionen:** X | **Kalorien:** XXX kcal | **Protein:** XXg | **Prep:** XX Min

### Zutaten (pro Portion):
- [Menge] [Zutat] (X kcal, Xg Protein)
- ...

### Zubereitung:
1. [Schritt 1]
2. [Schritt 2]
...

### Nährwerte pro Portion:
- Kalorien: XXX kcal
- Protein: XXg
- Kohlenhydrate: XXg
- Fett: XXg
- Ballaststoffe: XXg

### Meal Prep Hinweise:
- Vorbereitung: [was kann vorab gemacht werden]
- Haltbarkeit: X Tage im Kühlschrank
- Aufwärmen: [Tipps]
- Variationen: [mögliche Anpassungen]
```

### Tipps für erfolgreiche Rezept-Generierung

**Protein-Balance:**
- Linsen: ~9g Protein/100g (gekocht)
- Kichererbsen: ~9g Protein/100g (gekocht)
- Tofu: ~8g Protein/100g
- Tempeh: ~19g Protein/100g
- Quinoa: ~4g Protein/100g (gekocht)
- Edamame: ~11g Protein/100g

**Kalorien-Management:**
- Nüsse/Nussmus: sehr kaloriendicht (~600 kcal/100g)
- Öl: 120 kcal pro EL
- Avocado: ~160 kcal/100g
- Getreide: ~350-370 kcal/100g (trocken)
- Gemüse: meist <50 kcal/100g

**Geschmacks-Profile:**
- **Asiatisch:** Ingwer, Knoblauch, Misopaste, Sesamöl, Reisessig
- **Mediterran:** Zitrone, Kräuter (Basilikum, Oregano), Knoblauch, Olivenöl
- **Mexikanisch:** Kreuzkümmel, Koriander, Limette, Chilipulver
- **Indisch:** Currypaste, Kurkuma, Kreuzkümmel, Koriander, Ingwer

**Meal-Prep-Eignung:**
- Suppen und Currys: sehr gut (5-7 Tage)
- Buddha Bowls mit getrennten Komponenten: sehr gut (4-5 Tage)
- Salate: nur Basis vorkochen, Dressing separat (3-4 Tage)
- Overnight Oats/Chia Pudding: perfekt (5 Tage)

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

### Szenario 5: Neue Rezepte generieren
```
1. Anforderungen sammeln:
   - Nutzer: "Ich habe viel Blumenkohl und möchte ein asiatisches Abendessen"
   - Target: 350 kcal, 20g Protein, meal-prep-freundlich

2. Rezept entwickeln:
   - Basis: Quinoa (150g gekocht) als Getreide-Base
   - Protein: Tofu (120g) mariniert
   - Gemüse: Blumenkohl (200g) geröstet mit asiatischen Gewürzen
   - Sauce: Misopaste + Ingwer + Knoblauch + Sesamöl

3. Nährwerte kalkulieren:
   - Quinoa: 180 kcal, 6g Protein
   - Tofu: 95 kcal, 10g Protein
   - Blumenkohl: 50 kcal, 4g Protein
   - Sauce: 25 kcal, 1g Protein
   - Gesamt: 350 kcal, 21g Protein ✅

4. Zubereitung strukturieren:
   - Tofu marinieren (Misopaste, Ingwer, Knoblauch)
   - Blumenkohl in Röschen schneiden, würzen, rösten
   - Quinoa kochen
   - Servieren mit Sesam und Frühlingszwiebeln

5. Meal-Prep-Hinweise:
   - Alle Komponenten 4-5 Tage haltbar
   - Getrennt lagern, täglich frisch kombinieren
   - Tofu wird beim Aufwärmen noch besser

6. Optional: Zu recipe-database.md hinzufügen für zukünftige Meal Plans
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
