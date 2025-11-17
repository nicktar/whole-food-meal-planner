---
name: whole-food-meal-planner
description: Comprehensive meal planning system for the Whole Food Challenge with recipe generation, verified recipes, nutritional validation, Mealie integration, and automated meal prep strategies. Can create new custom recipes based on available ingredients, dietary targets, and preferences - all automatically validated against challenge rules. Use when creating meal plans that require only whole foods (no processed foods, no animal products), generating new recipe ideas within strict dietary constraints, having specific caloric/protein targets (typically 1200 kcal, 75-90g protein), needing nutritional verification, requiring Mealie-compatible recipe exports, or needing detailed meal prep workflows with shopping lists. Especially useful for multi-day plans (3-7 days) with ingredient synergies and custom recipe development.
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

**Workflow für neue Meal Plans:**
```bash
# 1. Workflow-Guide lesen
view references/meal-plan-workflow.md

# 2. Rezepte prüfen (externe recipe-database.md hat Vorrang)
view recipe-database.md || view references/recipe-database.md

# 3. Plan erstellen (Templates aus workflow.md)
# Dateiname: meal-plans/wochenplan-YYYY-MM-DD-bis-DD.md

# 4. Nährwerte verifizieren (KRITISCH!)
python3 scripts/verify_nutrition.py

# 5. Optional: Mealie-Export (Parser-basiert, vollautomatisch!)
python3 scripts/mealie_export_v2.py meal-plans/wochenplan-2024-12-08-bis-12.md --prefix 2024_12_08
```

**Schritte:** Anforderungen sammeln → Rezepte wählen → Plan erstellen (mit Datumsbereich-Dateinamen) → Verifizieren → Optional: Mealie-Export

## Challenge-Regeln

**Erlaubte Zutaten:**
- Vollkornprodukte (Hafer, Quinoa, Buchweizen, Dinkel, etc.)
- Hülsenfrüchte (Linsen, Kichererbsen, Cannellini-Bohnen, schwarze Bohnen)
- Tofu
- Erbsenprotein-Pulver (pur, ohne Zusätze)
- Früchte (frisch oder getrocknet)
- Gemüse (alle Sorten)
- Nüsse und Samen
- Nussmus (natürlich, ohne Zusätze)
- Hafermilch (ungesüßt)
- Würzpasten (Curry-, Miso- etc., vegan)
- Nährhefe-Flocken
- Gewürze, Kräuter, Essig, Öl

**Ausgeschlossen:**
- Auberginen
- Dicke Bohnen/Ackerbohnen/Puffbohnen (alle anderen Bohnen sind erlaubt!)
- Grünkohl
- Rosenkohl
- Wirsing
- Rosinen
- Alle tierischen Produkte
- Verarbeitete Lebensmittel

**Zutatenwiderholungs-Regel:**
- **Geschmacksgebende Komponenten** (Gemüse mit starkem Eigengeschmack): Maximal **4 MAHLZEITEN** pro Wochenplan
  - **WICHTIG:** Jede Mahlzeit zählt einzeln, auch wenn das gleiche Rezept wiederholt wird!
  - Beispiele: Rotkohl, Hokkaido-Kürbis, Fenchel, Sellerie, Brokkoli, Blumenkohl, Mangold, etc.
  - **Erlaubtes Beispiel:**
    - Mo Mittag: Rotkohl-Curry (1)
    - Di Mittag: Buddha-Bowl mit Rotkohl (2)
    - Di Abend: Rotkohl-Apfel-Salat (3)
    - Mi Mittag: Gerösteter Rotkohl-Salat (4)
    - → **4 Mahlzeiten total, perfekt!** ✅
  - **NICHT erlaubt:**
    - Mo Mittag: Rotkohl-Curry (1)
    - Di Mittag: Buddha-Bowl mit Rotkohl (2)
    - Di Abend: Rotkohl-Apfel-Salat (3)
    - Mi Mittag: Gerösteter Rotkohl-Salat (4)
    - Do Mittag: Rotkohl-Curry (5) ← **ZU VIEL!** ❌
    - → Auch wenn "Rotkohl-Curry" schon existiert, zählt die Wiederholung als 5. Mahlzeit!
- **Unbegrenzt verwendbar** (Ausnahmen von der 4-Mahlzeiten-Regel):
  - Alle Hülsenfrüchte (Sättigungskomponenten): Linsen, Kichererbsen, Bohnen, etc.
  - Alle Getreide (Sättigungskomponenten): Quinoa, Hafer, Buchweizen, Dinkel, etc.
  - Flexible Gemüse: Paprika, Süßkartoffeln, Zucchini, Rote Beete, Karotten

## Standard-Targets

**Tägliche Ziele (typisch):**
- Kalorien: 1200 kcal (Range: 1100-1300)
- Protein: 75-90g (Minimum: 75g)
- Ballaststoffe: 30g (Minimum: 25g)

**Mahlzeiten-Ranges:**
- Frühstück: 300-400 kcal, 15-30g Protein
- Mittagessen: 350-450 kcal, 20-35g Protein
- Abendessen: 350-400 kcal, 20-35g Protein

**WICHTIG - Ziel-Priorisierung:**
- ⚠️ **1300 kcal ist eine HARTE Grenze** - NIEMALS überschreiten!
- **Kalorien-Limit hat IMMER Priorität** über Protein-Ziel
- Bei Konflikten zwischen Zielen: Kalorien-Grenze einhalten, auch wenn Protein darunter leidet
- Beispiel: Lieber 72g Protein bei 1299 kcal als 85g Protein bei 1320 kcal
- Mit 30g Proteinpulver-Limit pro Mahlzeit + 1300 kcal-Grenze ist das 75-90g Protein-Ziel gut erreichbar
- **Ziel-Range:** 75-90g Protein bei unter 1300 kcal

## Bundled Resources

### Scripts

**`scripts/verify_nutrition.py`** - Nährwert-Verifikation
- Validiert Tagespläne gegen Targets
- Zeigt Abweichungen und Warnungen
- Output: Text-Report + JSON
- **Wann verwenden:** Nach jedem Meal Plan, vor Finalisierung

**`scripts/mealie_export_v2.py`** - Parser-basierte Mealie-Integration (NEU!)
- **Vollautomatischer Export:** Parst Markdown-Rezepte und konvertiert automatisch zu Mealie-Format
- **Keine manuelle Code-Änderung nötig** - funktioniert mit beliebigen Rezept-Markdown-Dateien
- **Verwendung:**
  ```bash
  # Aus Wochenplan exportieren
  python3 scripts/mealie_export_v2.py meal-plans/wochenplan-08-12-dezember.md --prefix 2024_12_08

  # Aus separater Rezeptdatei
  python3 scripts/mealie_export_v2.py rezepte-2024-12-08-bis-12.md
  ```
- **Unterstützte Formate:**
  - Wochenplan-Format (TAG 1, TAG 2 mit ### Frühstück:, ### Mittagessen:, ### Abendessen:)
  - Standalone-Rezepte (## REZEPTNAME Format)
  - Extrahiert automatisch: Name, Zutaten, Anleitung, Nährwerte, Zeiten
- **Dateinamen:** Datumsbereich-basiert (z.B. `2024_12_08_overnight_oats_beeren.json`)
- **Wann verwenden:** Bei jedem neuen Wochenplan oder neuen Rezepten für Mealie-Import

**`scripts/nutrition_recalculation.md`** - Nährwert-Standardwerte Referenz
- **PFLICHTLEKTÜRE vor jeder Nährwertberechnung!**
- Enthält präzise Standardwerte für ALLE gängigen Zutaten (pro 100g/100ml)
- Vollständige Neuberechnung der November 2024 Rezepte als Beispiel
- Dokumentiert systematische Fehlerquellen und deren Auswirkungen (+180-420 kcal Fehler!)
- **Verwende diese Werte** für manuelle Nährwertberechnungen
- **Wann lesen:** IMMER vor dem Erstellen neuer Rezepte oder Meal Plans

### References

**Recipe Database** - Verifizierte Rezepte
- **Location:** `recipe-database.md` (external, if present) or `references/recipe-database.md` (bundled)
- Komplette Rezept-Sammlung mit Nährwerten
- Frühstück, Mittag/Abend, Dressings
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

## ⚠️ KRITISCH: Nährwertberechnung - Häufige Fehlerquellen

**WICHTIG:** Das `verify_nutrition.py` Script **validiert** nur hardcoded Werte gegen Targets. Es **berechnet NICHT** automatisch die Nährwerte aus Zutaten!

### Typische Unterschätzungen (führen zu massiven Fehlern!)

**Die folgenden Zutaten werden systematisch unterschätzt und führen zu 180-420 kcal Differenz pro Mahlzeit:**

#### 1. Nüsse & Samen (600-650 kcal/100g!)
- **Walnüsse:** 654 kcal/100g → **15g = 98 kcal** (oft als "30 kcal" unterschätzt)
- **Cashews:** 553 kcal/100g → **15g = 83 kcal**
- **Kürbiskerne:** 559 kcal/100g → **1 EL (10g) = 56 kcal**
- **Hanfsamen:** 553 kcal/100g → **1 EL (10g) = 55 kcal**
- **Sonnenblumenkerne:** 584 kcal/100g → **1 EL (10g) = 58 kcal**

#### 2. Nussmus (590-650 kcal/100g!)
- **Mandelmus:** 614 kcal/100g → **1 EL (15g) = 92 kcal** (oft als "50 kcal" unterschätzt)
- **Erdnussmus:** 588 kcal/100g → **1 EL (15g) = 88 kcal**
- **Cashewmus:** 587 kcal/100g → **1 EL (15g) = 88 kcal**
- **Tahini:** 595 kcal/100g → **2 EL (30g) = 179 kcal** ⚠️ SEHR HÄUFIG UNTERSCHÄTZT!

#### 3. Öle & Fette (880-900 kcal/100ml!)
- **Olivenöl:** 884 kcal/100ml → **1 TL (5ml) = 44 kcal**
- **Kokosöl:** 862 kcal/100ml → **1 TL (5ml) = 43 kcal**
- **Avocado:** 160 kcal/100g → **1/4 Avocado (40g) = 64 kcal**

#### 4. Kokosmilch (230 kcal/100ml!)
- **Kokosmilch:** 230 kcal/100ml → **75ml = 172 kcal** ⚠️ SEHR KALORIENREICH!
- Oft als "50 kcal" unterschätzt → führt zu +120 kcal Fehler pro Curry!

#### 5. Erbsenprotein-Pulver
- **Erbsenprotein:** 375 kcal/100g → **20g = 75 kcal**, 16g Protein
- Manchmal komplett vergessen zu zählen!

### Realistische EL/TL Mengen

**1 Esslöffel (EL) = je nach Zutat unterschiedlich!**
- Chiasamen: ~12g
- Leinsamen gemahlen: ~10g
- Nussmus: ~15g
- Tahini: ~15g
- Kürbiskerne/Hanfsamen: ~10g
- Haferflocken: ~10g

**1 Teelöffel (TL) = 5ml/5g** (bei Ölen und Pulvern)

### Nährwertberechnung-Prozess (PFLICHT!)

**VOR dem Eintragen in verify_nutrition.py:**

1. **Erstelle Zutatenliste mit exakten Mengen**
   ```
   - 30g Haferflocken
   - 150ml Hafermilch
   - 1 EL Chiasamen (12g)
   - 1 EL Mandelmus (15g)
   - 20g Erbsenprotein
   - 15g Walnüsse
   ```

2. **Rechne JEDE Zutat einzeln aus** (nutze Standardwerte aus `scripts/nutrition_recalculation.md`)
   ```
   30g Haferflocken: 111 kcal, 3.9g P, 18g C, 2.1g F, 3g Fiber
   150ml Hafermilch: 52 kcal, 0.75g P, 9g C, 1.5g F, 0g Fiber
   12g Chiasamen: 58 kcal, 2g P, 5g C, 3.7g F, 4.1g Fiber
   15g Mandelmus: 92 kcal, 3.2g P, 3.2g C, 8g F, 1.2g Fiber
   20g Erbsenprotein: 75 kcal, 16g P, 1g C, 1.4g F, 0g Fiber
   15g Walnüsse: 98 kcal, 2.3g P, 2.1g C, 9.8g F, 1g Fiber
   ```

3. **Summiere alle Werte**
   ```
   SUMME: 486 kcal, 28.15g P, 38.3g C, 26.5g F, 9.3g Fiber
   ```

4. **Prüfe gegen Meal-Ranges**
   - Frühstück sollte 300-400 kcal haben
   - 486 kcal ist zu viel! → Nussmus/Walnüsse reduzieren

5. **ERST JETZT** in verify_nutrition.py eintragen

### Standardwerte-Referenz

**Vollständige Standardwerte für alle gängigen Zutaten:** Siehe `scripts/nutrition_recalculation.md`

Die wichtigsten Werte (pro 100g/100ml):
- Haferflocken: 370 kcal, 13g P
- Quinoa gekocht: 120 kcal, 4g P
- Kichererbsen gekocht: 164 kcal, 9g P
- Grüne Linsen gekocht: 116 kcal, 9g P
- Tofu: 76 kcal, 8g P
- Tahini: 595 kcal, 17g P ⚠️
- Mandelmus: 614 kcal, 21g P ⚠️
- Walnüsse: 654 kcal, 15g P ⚠️
- Kokosmilch: 230 kcal, 2.3g P ⚠️
- Olivenöl: 884 kcal ⚠️

### Warnsignale für Fehler

🚨 **Wenn ein Rezept diese Zutaten hat, aber unter 400 kcal angegeben ist → FEHLER!**
- 2 EL Tahini + Nüsse + Öl
- Kokosmilch (75ml+) + Nussmus + Nüsse
- Mehrere EL Nussmus (2+ EL)

🚨 **Typische Unterschätzungen:**
- Overnight Oats mit Nussmus + Nüssen + Proteinpulver als "390 kcal" → **FALSCH!** (Realität: 550-650 kcal)
- Curry mit Kokosmilch als "500 kcal" → Prüfen! (Kokosmilch allein = 170+ kcal)
- Salat mit 2 EL Tahini als "400 kcal" → Prüfen! (Tahini allein = 180 kcal)

### Realistische Kalorienverteilung (1200 kcal/Tag)

**Damit ein 1200 kcal Tagesplan funktioniert:**
- Frühstück: **350-450 kcal** (mit Proteinpulver, Nussmus, Nüssen wird es schnell 500+)
- Mittagessen: **350-450 kcal** (Curry mit Kokosmilch = schwierig unter 450!)
- Abendessen: **350-450 kcal** (Salat mit Tahini + Nüssen = schnell 450+)

**Wenn alle drei Mahlzeiten Nüsse/Nussmus/Tahini/Öle enthalten → typisch 1800-2000 kcal!**

### Anpassungen für 1200 kcal Ziel

**Um 1200 kcal zu erreichen, EINE der folgenden Strategien:**

**Option 1: Portionen reduzieren**
- Nussmus: 1 EL → 1 TL (60 kcal gespart)
- Walnüsse: 15g → 5g (65 kcal gespart)
- Tahini: 2 EL → 1 EL (90 kcal gespart)
- Öl: Sprühöl statt gegossen (30 kcal gespart)

**Option 2: Nur 1-2 Mahlzeiten mit Fett-Toppings**
- Frühstück: MIT Nussmus + Nüssen (500 kcal)
- Mittagessen: OHNE Öl/Nussmus, nur gedämpft (350 kcal)
- Abendessen: MIT Dressing, aber ohne extra Nüsse (400 kcal)
- = 1250 kcal ✅

**Option 3: Größeres Kalorienziel akzeptieren**
- 1200 kcal mit Nüssen/Ölen/Tahini ist sehr restriktiv
- 1600-1800 kcal ist realistischer für ausgewogene Whole Food Ernährung
- User fragen ob Ziel angepasst werden soll

## Meal Planning Workflow

**Folge dem Basis-Workflow** (vollständige Details in `references/meal-plan-workflow.md`):

1. **Anforderungen sammeln** → Zeitraum, Ernährungsziele, Präferenzen (Template in workflow.md)
2. **Rezepte auswählen** → External `recipe-database.md` oder bundled `references/recipe-database.md`
3. **Plan erstellen** → Template-Format verwenden, Dateiname: `wochenplan-YYYY-MM-DD-bis-DD.md` (siehe workflow.md Abschnitt 3)
4. **Verifikation** → `python3 scripts/verify_nutrition.py` ausführen (**KRITISCH!**)
5. **Anpassungen** → Protein/Kalorien optimieren bei Abweichungen

**Optional (nur auf expliziten Nutzer-Wunsch):**
6. **Einkaufsliste** → Nach Kategorien gruppieren, Mengen summieren, Dateiname: `einkaufsliste-YYYY-MM-DD-bis-DD.md`
7. **Meal Prep Strategie** → 4-Phasen-Timeline (Grundlagen → Gemüse → Spezial → Portionieren), Dateiname: `meal-prep-strategie-YYYY-MM-DD-bis-DD.md`
8. **Mealie-Export** → `python3 scripts/mealie_export_v2.py wochenplan-file.md --prefix YYYY_MM_DD`

**Wichtigste Punkte:**
- ✅ Immer verify_nutrition.py nach Plan-Erstellung ausführen
- ✅ Externe Rezepte prüfen: `ls recipe-database.md` (falls vorhanden, werden diese verwendet)
- ✅ **Zutatenwiderholungen prüfen:** Geschmacksgebende Komponenten maximal 4x pro Woche (Hülsenfrüchte/Getreide/Paprika/Süßkartoffeln/Zucchini unbegrenzt)
- ✅ Bei Protein <75g: Tofu/Hülsenfrüchte/Erbsenprotein in Flüssigkeiten ergänzen
- ✅ Bei Kalorien >1300: Öl/Nüsse reduzieren
- ✅ Bei Kalorien <1100: Nüsse/Avocado hinzufügen
- ✅ Meal Prep Synergien maximieren (gleiche Basis-Komponenten für mehrere Gerichte)
- ⚠️ **Einkaufsliste & Meal Prep Strategie-Dokument:** Nur auf expliziten Nutzer-Wunsch erstellen!

## File Naming Conventions

**Datumsbereich-basierte Benennung** für alle Meal Plans und Rezeptdateien:

**Wochenpläne:**
- Format: `wochenplan-YYYY-MM-DD-bis-DD.md`
- Beispiel: `meal-plans/wochenplan-2024-12-08-bis-12.md`
- Vorher: `wochenplan-08-12-dezember.md` ❌ (unklar, Jahr fehlt)
- Jetzt: `wochenplan-2024-12-08-bis-12.md` ✅ (eindeutig, maschinenlesbar)

**Rezeptdateien:**
- Format: `rezepte-YYYY-MM-DD-bis-DD.md`
- Beispiel: `rezepte-2024-12-08-bis-12.md`
- Für Wochenrezepte: Start- und Enddatum der Woche
- Für einzelne Rezepte: Erstellungsdatum oder Verwendungsdatum

**Einkaufslisten:**
- Format: `einkaufsliste-YYYY-MM-DD-bis-DD.md`
- Beispiel: `meal-plans/einkaufsliste-2024-12-08-bis-12.md`

**Meal Prep Strategien:**
- Format: `meal-prep-strategie-YYYY-MM-DD-bis-DD.md`
- Beispiel: `meal-plans/meal-prep-strategie-2024-12-08-bis-12.md`

**Mealie Exports:**
- Format: `YYYY_MM_DD_rezeptname.json`
- Beispiel: `mealie_exports/2024_12_08_overnight_oats_beeren_power.json`
- Automatisch generiert durch `mealie_export_v2.py` mit `--prefix` Option

**Warum Datumsbereich-basiert?**
- ✅ Eindeutig identifizierbar (kein Raten welches Jahr)
- ✅ Maschinenlesbar und sortierbar
- ✅ Kompatibel mit Parser-Tools
- ✅ Internationale Eindeutigkeit (keine Monatsnamen)
- ✅ Einfache Zuordnung zwischen Plan, Einkaufsliste und Rezepten

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
   - Mahlzeitentyp (Frühstück, Mittag, Abend)
   - Geschmacksrichtung (asiatisch, mediterran, mexikanisch, etc.)
   - Prep-Zeit und Komplexität
   - Meal-Prep-Eignung

2. **Challenge-Compliance prüfen:**
   - ✅ Nur erlaubte Zutaten verwenden (siehe Challenge-Regeln oben)
   - ❌ Keine ausgeschlossenen Zutaten (Auberginen, Dicke Bohnen, Grünkohl, Rosenkohl, Wirsing, Rosinen)
   - ❌ Keine tierischen Produkte
   - ❌ Keine verarbeiteten Lebensmittel

3. **Rezept entwickeln:**
   - Basis-Komponenten wählen (Getreide + Protein + Gemüse)
   - Geschmacks-Profile aufbauen (Gewürze, Dressings)
   - Nährwerte kalkulieren (pro Zutat summieren)
   - Zubereitung strukturieren (Schritt-für-Schritt)

4. **Rezept auf Vollständigkeit und Stimmigkeit prüfen:**
   - ✅ **Proteinpulver richtig eingesetzt:** Erbsenprotein-Pulver NUR in Flüssigkeiten (Smoothies, Porridge, Overnight Oats) - NICHT in trockenen Gerichten
   - ✅ **Marinaden vorhanden:** Tofu braucht Marinaden (Misopaste, Sojasauce, Gewürze + Öl)
   - ✅ **Ausreichend gewürzt:** Alle Komponenten haben Würzung/Geschmack (nicht nur Salz & Pfeffer)
   - ✅ **Konsistenz stimmig:**
     - Nicht zu trocken (genug Sauce/Dressing/Flüssigkeit)
     - Nicht zu wässrig (Gemüse richtig zubereitet, nicht überkocht)
     - Texturen ergänzen sich (knusprig + cremig, weich + bissfest)
   - ✅ **Zubereitungsschritte vollständig:** Alle Komponenten werden in der Anleitung behandelt
   - ✅ **Garzeiten realistisch:** Quinoa 15 Min, Linsen 20-25 Min, Kichererbsen 60-90 Min
   - ✅ **Fette/Öle enthalten:** Für Geschmack und Nährstoffaufnahme (1-2 EL Öl oder Nussmus)
   - ⚠️ **Häufige Fehler vermeiden:**
     - Trockenes Tofu ohne Marinade
     - Rohes Gemüse ohne Dressing in warmen Gerichten
     - **Geröstetes Gemüse in Meal-Prep-Bowls:** Gemüse nach 4-5 Tagen aufwärmen + kombinieren mit kalten Komponenten = matschig/glibbrig! Besser: Rohkost (Karotten-Julienne, Gurke, Rotkohl hobeln) oder Gemüse komplett getrennt warm servieren
     - Nur Basis-Zutaten ohne Geschmacksträger
     - Erbsenprotein in Salaten/Bowls (funktioniert nicht!)

   **Wenn Probleme gefunden werden:** Rezept JETZT anpassen, bevor Nährwerte validiert werden!

5. **Nährwerte validieren:**
   - Gegen Meal-Ranges prüfen (siehe Standard-Targets oben)
   - Bei Bedarf anpassen (mehr Protein, weniger Kalorien, etc.)
   - `verify_nutrition.py` kann für finale Validierung verwendet werden

6. **Meal-Prep-Hinweise hinzufügen:**
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
  - ⚠️ **Wichtig:** Für kalte/lauwarme Bowls Rohkost verwenden (Karotten-Julienne, Gurke, Rotkohl), NICHT geröstetes Gemüse (wird matschig nach 4-5 Tagen)
  - Geröstetes Gemüse nur wenn Bowl komplett warm serviert wird
- Salate: nur Basis vorkochen, Dressing separat (3-4 Tage)
- Overnight Oats/Chia Pudding: perfekt (5 Tage)

## Best Practices

### Zeit-Effizienz
- Meal Prep am Sonntag: 3-4 Stunden für 5 Tage
- Täglicher Aufwand: 5-15 Minuten
- Paralleles Kochen: Getreide + Hülsenfrüchte gleichzeitig

### Nährwert-Optimierung
- **Protein boosten:** Tofu, extra Hülsenfrüchte
- **Kalorien reduzieren:** Öl/Nüsse limitieren
- **Ballaststoffe erhöhen:** Mehr Gemüse, Vollkorn - oder auf zusätzliche Flohsamenschalen hinweisen (nicht in Rezepte einbauen)

### Abwechslung
- Gleiche Basis, verschiedene Gewürze
- Internationale Variationen (Mediterran, Asiatisch, Mexikanisch)
- Textur-Kontraste (knusprig + cremig)
- **Zutatenwiderholungen begrenzen:** Geschmacksgebende Komponenten maximal 4x pro Woche verwenden (siehe Challenge-Regeln)

### Meal-Prep-Synergien
- **Rotkohl:** Curry, Salat, mariniert, Suppe
- **Kichererbsen:** Geröstet, Buddha Bowl, Hummus
- **Quinoa:** Frühstück, Bowl-Basis, Salat

## Häufige Szenarien

### Szenario 1: Standard 5-Tage Plan
```
1. Anforderungen: 5 Tage, 1200 kcal, 75g+ Protein
2. Rezepte aus DB wählen (meal-plan-workflow.md Abschnitt 2)
3. Plan nach Template erstellen
4. verify_nutrition.py ausführen
5. (Optional, nur auf Wunsch) Einkaufsliste + Meal Prep Strategie
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
1. Erste Verifikation zeigt <75g Protein
2. Anpassungen:
   - Tofu zu Suppen hinzufügen (+10-15g)
   - Extra Nussmus im Frühstück (+4g)
   - Erbsenprotein-Pulver in Flüssig-Mahlzeiten erhöhen (Overnight Oats, Smoothies, Porridge)
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
1. Anforderungen: "Blumenkohl + asiatisch + 350 kcal, 20g Protein, meal-prep-freundlich"

2. Entwickeln:
   Quinoa (150g, 180 kcal, 6g) + marinierter Tofu (120g, 95 kcal, 10g) +
   Blumenkohl geröstet (200g, 50 kcal, 4g) + Miso-Sauce (25 kcal, 1g)
   → Gesamt: 350 kcal, 21g Protein ✅

3. Qualitätskontrolle (siehe Checkliste unten):
   ✅ Tofu mariniert, Sauce vorhanden, ausreichend gewürzt
   ✅ Fette enthalten (Sesamöl), Texturen komplementär
   ✅ Alle Zubereitungsschritte dokumentiert
   → Stimmig, zu Nährwert-Validierung übergehen

4. Strukturieren: Tofu marinieren (30 Min) → Blumenkohl rösten (200°C, 25 Min) →
   Quinoa kochen (15 Min) → Bowl zusammenstellen

5. Meal Prep: 4-5 Tage haltbar, getrennt lagern, täglich frisch kombinieren

6. Optional: Zu recipe-database.md hinzufügen
```

## Troubleshooting

**Problem:** Neue Rezepte schmecken fade oder Konsistenz stimmt nicht
→ Qualitätskontrolle-Checkliste durchgehen (siehe "Rezept auf Vollständigkeit und Stimmigkeit prüfen")
→ Häufigste Fehler:
  - Tofu ohne Marinade → Mindestens 30 Min marinieren
  - Zu wenig Gewürze → Pro Portion mind. 1 TL Gewürzmischung
  - Fehlendes Fett → 1-2 EL Öl oder Nussmus hinzufügen
  - Erbsenprotein falsch verwendet → Nur in Flüssigkeiten/Brei
→ Nach Korrekturen Nährwerte neu berechnen!

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

### Für Meal Plans (vor Finalisierung):
- [ ] Challenge-Regeln eingehalten (keine ausgeschlossenen Zutaten)
- [ ] Nährwerte verifiziert und im Target-Bereich
- [ ] Realistische Zubereitungszeiten
- [ ] Lagerungshinweise enthalten
- [ ] Abwechslung über die Woche
- [ ] **Zutatenwiderholungs-Regel beachtet:** Geschmacksgebende Komponenten maximal 4 MAHLZEITEN pro Woche (jede Mahlzeit zählt einzeln, auch Wiederholungen!)
  - Beispiel: Rotkohl-Curry Mo + Do = 2 Mahlzeiten (nicht 1!)
  - Unbegrenzt: Hülsenfrüchte, Getreide, Paprika, Süßkartoffeln, Zucchini, Rote Beete, Karotten
- [ ] Saisonale und verfügbare Zutaten (Deutschland)
- [ ] **Meal-Prep-Kompatibilität:** Geröstetes Gemüse nur wenn komplett warm serviert wird; für kalte/lauwarme Bowls Rohkost verwenden (Karotten-Julienne, Gurke, Rotkohl)

### Für optionale Komponenten (nur auf Nutzer-Wunsch):
- [ ] **Einkaufsliste:** Vollständig und nach Kategorien organisiert
- [ ] **Meal Prep Strategie:** 4-Phasen-Timeline mit realistischen Zeitangaben

### Für neue Rezepte (vor Nährwert-Validierung):
- [ ] Erbsenprotein-Pulver nur in Flüssigkeiten verwendet (NICHT in Bowls/Salaten)
- [ ] Tofu haben Marinaden (mind. 30 Min Marinierzeit)
- [ ] Alle Komponenten ausreichend gewürzt (nicht fade)
- [ ] Konsistenz stimmig (nicht zu trocken, nicht zu wässrig)
- [ ] Texturen ergänzen sich (knusprig + cremig, weich + bissfest)
- [ ] Fette/Öle enthalten (1-2 EL pro Portion für Geschmack)
- [ ] Alle Zubereitungsschritte vollständig dokumentiert
- [ ] Garzeiten realistisch und spezifisch angegeben
- [ ] **Meal-Prep-Tauglichkeit:** Geröstetes Gemüse nur für sofort-Verzehr oder komplett warme Gerichte; für Meal-Prep-Bowls (4-5 Tage) Rohkost bevorzugen
- [ ] **KEINE internen Optimierungskommentare** in finalen Rezepten (z.B. "(MAXIMAL erlaubt!)", "(erhöht für bessere Konsistenz)", "(mehr wäre über Kalorien-Limit!)")
  - Diese Kommentare gehören in Entwicklungsnotizen, nicht in fertige Meal Plans
  - Nutzer sollen nur die finale Zutatenliste sehen, ohne interne Begründungen
- [ ] Bei Korrekturen: Nährwerte entsprechend angepasst
