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

**Workflow für neue Meal Plans:**
```bash
# 1. Workflow-Guide lesen
view references/meal-plan-workflow.md

# 2. Rezepte prüfen (externe recipe-database.md hat Vorrang)
view recipe-database.md || view references/recipe-database.md

# 3. Plan erstellen (Templates aus workflow.md)
# 4. Nährwerte verifizieren (KRITISCH!)
python3 scripts/verify_nutrition.py

# 5. Optional: Mealie-Export
python3 scripts/mealie_export.py
```

**Schritte:** Anforderungen sammeln → Rezepte wählen → Plan erstellen → Verifizieren → Optional: Mealie-Export

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
- Protein: 100-110g (Minimum: 100g)
- Ballaststoffe: 30g (Minimum: 25g)

**Mahlzeiten-Ranges:**
- Frühstück: 300-400 kcal, 15-30g Protein
- Mittagessen: 350-450 kcal, 25-45g Protein
- Abendessen: 350-400 kcal, 25-45g Protein

**WICHTIG - Ziel-Priorisierung:**
- ⚠️ **1300 kcal ist eine HARTE Grenze** - NIEMALS überschreiten!
- **Kalorien-Limit hat IMMER Priorität** über Protein-Ziel
- Bei Konflikten zwischen Zielen: Kalorien-Grenze einhalten, auch wenn Protein darunter leidet
- Beispiel: Lieber 90g Protein bei 1299 kcal als 105g Protein bei 1320 kcal
- Mit 30g Proteinpulver-Limit pro Mahlzeit + 1300 kcal-Grenze ist 100g Protein oft nicht erreichbar
- **Akzeptabel:** 85-95g Protein, wenn dadurch unter 1300 kcal geblieben wird

## Bundled Resources

### Scripts

**`scripts/verify_nutrition.py`** - Nährwert-Verifikation
- Validiert Tagespläne gegen Targets
- Zeigt Abweichungen und Warnungen
- Output: Text-Report + JSON
- **Wann verwenden:** Nach jedem Meal Plan, vor Finalisierung

**`scripts/mealie_export.py`** - Mealie-Integration
- Generiert Mealie-kompatible JSON-Rezepte im schema.org Format
- **Format-Anforderungen:**
  - **Vorgekochte Zutaten:** "50g Rote Linsen (ca. 100g gekocht)" - immer rohe Menge + gekochte Menge in Klammern
  - **Farben groß:** Rote Linsen, Schwarze Bohnen, Rote Bete (für Parser-Erkennung)
  - **Anmerkungen:** "80g Heidelbeeren (TK)" - Format "Menge Zutat (Anmerkung)"
  - **Keywords:** Comma-separated String mit "whole food,KI Rezepte,food prep,vegetarisch,vegan,{mahlzeit}"
  - **Anweisungen:** Ein String mit \n Zeilenumbrüchen (nicht Array)
  - **Zutaten:** Array von Strings (nicht Objekte)
- **Wann verwenden:** Wenn Nutzer Mealie verwendet oder Rezepte digital verwalten möchte

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

## Meal Planning Workflow

**Folge dem 8-Schritte-Prozess** (vollständige Details in `references/meal-plan-workflow.md`):

1. **Anforderungen sammeln** → Zeitraum, Ernährungsziele, Präferenzen (Template in workflow.md)
2. **Rezepte auswählen** → External `recipe-database.md` oder bundled `references/recipe-database.md`
3. **Plan erstellen** → Template-Format verwenden (siehe workflow.md Abschnitt 3)
4. **Verifikation** → `python3 scripts/verify_nutrition.py` ausführen (**KRITISCH!**)
5. **Anpassungen** → Protein/Kalorien optimieren bei Abweichungen
6. **Einkaufsliste** → Nach Kategorien gruppieren, Mengen summieren
7. **Meal Prep Strategie** → 4-Phasen-Timeline (Grundlagen → Gemüse → Spezial → Portionieren)
8. **Optional: Mealie-Export** → `python3 scripts/mealie_export.py`

**Wichtigste Punkte:**
- ✅ Immer verify_nutrition.py nach Plan-Erstellung ausführen
- ✅ Externe Rezepte prüfen: `ls recipe-database.md` (falls vorhanden, werden diese verwendet)
- ✅ **Zutatenwiderholungen prüfen:** Geschmacksgebende Komponenten maximal 4x pro Woche (Hülsenfrüchte/Getreide/Paprika/Süßkartoffeln/Zucchini unbegrenzt)
- ✅ Bei Protein <100g: Tofu/Hülsenfrüchte/Erbsenprotein in Flüssigkeiten ergänzen
- ✅ Bei Kalorien >1300: Öl/Nüsse reduzieren
- ✅ Bei Kalorien <1100: Nüsse/Avocado hinzufügen
- ✅ Meal Prep Synergien maximieren (gleiche Basis-Komponenten für mehrere Gerichte)

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
- [ ] Meal Prep Synergien maximiert
- [ ] Einkaufsliste vollständig und kategorisiert
- [ ] Realistische Zubereitungszeiten
- [ ] Lagerungshinweise enthalten
- [ ] Abwechslung über die Woche
- [ ] **Zutatenwiderholungs-Regel beachtet:** Geschmacksgebende Komponenten maximal 4 MAHLZEITEN pro Woche (jede Mahlzeit zählt einzeln, auch Wiederholungen!)
  - Beispiel: Rotkohl-Curry Mo + Do = 2 Mahlzeiten (nicht 1!)
  - Unbegrenzt: Hülsenfrüchte, Getreide, Paprika, Süßkartoffeln, Zucchini, Rote Beete, Karotten
- [ ] Saisonale und verfügbare Zutaten (Deutschland)
- [ ] **Meal-Prep-Kompatibilität:** Geröstetes Gemüse nur wenn komplett warm serviert wird; für kalte/lauwarme Bowls Rohkost verwenden (Karotten-Julienne, Gurke, Rotkohl)

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
