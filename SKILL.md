---
name: whole-food-meal-planner
description: Comprehensive meal planning system for the Whole Food Challenge with recipe generation, verified recipes, nutritional validation, Mealie integration, and automated meal prep strategies. Can create new custom recipes based on available ingredients, dietary targets, and preferences - all automatically validated against challenge rules. Use when creating meal plans that require only whole foods (no processed foods, no animal products), generating new recipe ideas within strict dietary constraints, having specific caloric/protein targets (typically 1200 kcal, 75-90g protein), needing nutritional verification, requiring Mealie-compatible recipe exports, or needing detailed meal prep workflows with shopping lists. Especially useful for multi-day plans (3-7 days) with ingredient synergies and custom recipe development.
---

# Whole Food Challenge Meal Planner

Complete meal planning system für die Whole Food Challenge mit Rezept-Datenbank, Nährwert-Verifikation und Mealie-Integration.

## Quick Start

**Workflow für neue Meal Plans:**
```bash
# 1. Workflow-Guide lesen
view references/meal-plan-workflow.md

# 2. Rezepte prüfen (externe recipe-database.md hat Vorrang)
view recipe-database.md || view references/recipe-database.md

# 2b. Nährwert-Standardwerte prüfen (externe nutrition-recalculation.md hat Vorrang)
view nutrition-recalculation.md || view scripts/nutrition-recalculation.md

# 3. Plan erstellen (Templates aus workflow.md)
# Dateiname: meal-plans/wochenplan-YYYY-MM-DD-bis-DD.md

# 4. Nährwerte verifizieren (KRITISCH!)
python3 scripts/verify_nutrition.py meal-plans/wochenplan-YYYY-MM-DD-bis-DD.md

# 5. Optional: Mealie-Export
python3 scripts/mealie_export.py meal-plans/wochenplan-2024-12-08-bis-12.md --prefix 2024_12_08
```

**Schritte:** Anforderungen sammeln → Rezepte wählen → Plan erstellen → **Nährwerte manuell berechnen** → Verifizieren → Optional: Mealie-Export

## 🎯 KRITISCHE ERFOLGSKRITERIEN

**Diese 6 Punkte MÜSSEN bei JEDEM Meal Plan erfüllt sein:**

### 1. 🧮 NÄHRWERTE KORREKT BERECHNET (HÄUFIGSTE FEHLERQUELLE!)

**✅ NEU:** Das `verify_nutrition.py` Script **parst automatisch** Nährwerte aus Markdown-Meal-Plans! Es liest deine **Nährwerte:**-Sektionen und validiert sie gegen Targets.

**MANUELLE Berechnung im Meal Plan ist PFLICHT:**

1. **Zutatenliste mit exakten Mengen** erstellen
2. **JEDE Zutat einzeln berechnen** mit Standardwerten (siehe `nutrition-recalculation.md` im Projekt oder `scripts/nutrition-recalculation.md`)
3. **Alle Werte summieren**
4. **Gegen Meal-Ranges prüfen**
5. **In Meal Plan eintragen** unter **Nährwerte:**-Sektion
6. **DANN** `verify_nutrition.py meal-plans/dein-plan.md` ausführen

**Häufigste Fehler (führen zu +180-420 kcal pro Mahlzeit!):**

- **Nüsse/Nussmus:** 600-650 kcal/100g
  - 1 EL Mandelmus (15g) = **92 kcal** (oft als "50 kcal" unterschätzt)
  - 15g Walnüsse = **98 kcal** (oft als "30 kcal" unterschätzt)
- **Tahini:** 595 kcal/100g
  - 2 EL (30g) = **179 kcal** ⚠️ SEHR HÄUFIG UNTERSCHÄTZT! (oft als "100 kcal")
- **Kokosmilch:** 230 kcal/100ml
  - 75ml = **172 kcal** ⚠️ (oft als "50 kcal" unterschätzt → +120 kcal Fehler!)
- **Öle:** 884 kcal/100ml
  - 1 TL (5ml) = **44 kcal**
- **Erbsenprotein-Pulver:** 375 kcal/100g
  - 20g = **75 kcal**, 16g Protein (manchmal vergessen zu zählen!)

**Warnsignale für Fehler:**

🚨 **Wenn ein Rezept diese Zutaten hat, aber unter 400 kcal angegeben ist → FEHLER!**
- 2 EL Tahini + Nüsse + Öl
- Kokosmilch (75ml+) + Nussmus + Nüsse
- Mehrere EL Nussmus (2+ EL)

**IMMER verwenden:** Standardwerte aus `nutrition-recalculation.md` (projekt-spezifisch) oder `scripts/nutrition-recalculation.md` (bundled) - PFLICHTLEKTÜRE!

### 2. ⚠️ KALORIENLIMIT (HARTE GRENZE!)

- **1300 kcal ist eine HARTE Grenze** - NIEMALS überschreiten!
- **Kalorien-Limit hat IMMER Priorität** über Protein-Ziel
- Nur mit korrekten Nährwerten (Punkt 1!) erreichbar
- Bei Konflikten: Lieber 72g Protein bei 1295 kcal als 85g Protein bei 1320 kcal
- Range: 1100-1300 kcal (optimal: 1200 kcal)

**Realistische Kalorienverteilung (1200 kcal/Tag):**
- Frühstück: 350-450 kcal (mit Proteinpulver, Nussmus, Nüssen wird es schnell 500+)
- Mittagessen: 350-450 kcal (Curry mit Kokosmilch = schwierig unter 450!)
- Abendessen: 350-450 kcal (Salat mit Tahini + Nüssen = schnell 450+)

**Wenn alle drei Mahlzeiten Nüsse/Nussmus/Tahini/Öle enthalten → typisch 1800-2000 kcal!**

### 3. 💪 PROTEINZIEL

- Minimum: 75g pro Tag
- Optimal: 80-90g
- **Bei Konflikt mit Kalorien:** Kalorienlimit hat Vorrang!
- **Akzeptabel:** 70-75g Protein, wenn dadurch unter 1300 kcal geblieben wird
- Mit 30g Proteinpulver-Limit pro Mahlzeit + 1300 kcal-Grenze ist 75-90g gut erreichbar

**Protein-Boosting:**
- Tofu zu Mahlzeiten hinzufügen (+10-15g pro 120g)
- Extra Nussmus im Frühstück (+4g per EL)
- Erbsenprotein-Pulver in Flüssig-Mahlzeiten erhöhen (Overnight Oats, Smoothies, Porridge)
- Extra Hülsenfrüchte (+8-12g per 100g)

### 4. 🚫 CHALLENGEREGELN EINGEHALTEN

**Ausgeschlossen:**
- **Gemüse:** Auberginen, Dicke Bohnen/Ackerbohnen/Puffbohnen, Grünkohl, Rosenkohl, Wirsing
- **Früchte:** Rosinen
- **Alle tierischen Produkte**
- **Alle verarbeiteten Lebensmittel**

**Erlaubt:** Vollkorn, Hülsenfrüchte (außer Dicke Bohnen!), Tofu, Erbsenprotein-Pulver, Früchte, Gemüse, Nüsse/Samen, Nussmus, Hafermilch (ungesüßt), Würzpasten (vegan), Nährhefe, Gewürze, Kräuter, Essig, Öl

### 5. 🔄 WIEDERHOLUNGSREGEL

**Geschmacksgebende Komponenten: MAXIMAL 4 MAHLZEITEN pro Wochenplan**

- ⚠️ **WICHTIG:** Jede Mahlzeit zählt einzeln, auch wenn das gleiche Rezept wiederholt wird!
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

**Geschmacksgebende Komponenten:** Rotkohl, Hokkaido-Kürbis, Fenchel, Sellerie, Brokkoli, Blumenkohl, Mangold, etc.

**Unbegrenzt verwendbar:** Hülsenfrüchte, Getreide, Paprika, Süßkartoffeln, Zucchini, Rote Beete, Karotten

### 6. 📦 MEAL-PREP TAUGLICH

- **Haltbarkeit:** 4-5 Tage im Kühlschrank
- **Komponenten getrennt lagern** (Dressings separat)
- ⚠️ **KEINE gerösteten Gemüse in kalten Bowls!** (wird matschig nach 4-5 Tagen)
- **Für kalte/lauwarme Bowls:** Rohkost verwenden (Karotten-Julienne, Gurke, Rotkohl hobeln)
- **Geröstetes Gemüse:** Nur wenn Bowl komplett warm serviert wird

**Meal-Prep-Eignung:**
- Suppen und Currys: sehr gut (5-7 Tage)
- Buddha Bowls mit getrennten Komponenten: sehr gut (4-5 Tage, Rohkost!)
- Salate: nur Basis vorkochen, Dressing separat (3-4 Tage)
- Overnight Oats/Chia Pudding: perfekt (5 Tage)

**Verifikation vor Finalisierung:**
```bash
python3 scripts/verify_nutrition.py meal-plans/wochenplan-YYYY-MM-DD-bis-DD.md  # PFLICHT!
```

## Challenge-Regeln

**Erlaubte Zutaten:**
- Vollkornprodukte (Hafer, Quinoa, Buchweizen, Dinkel, etc.)
- Hülsenfrüchte (Linsen, Kichererbsen, Cannellini-Bohnen, schwarze Bohnen)
- Tofu
- Erbsenprotein-Pulver (pur, ohne Zusätze)
- Früchte (frisch oder getrocknet, außer Rosinen)
- Gemüse (alle Sorten, siehe Ausschlüsse unten)
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
1. **Nährwerte korrekt berechnen** (ohne das ist alles andere wertlos!)
2. **1300 kcal ist eine HARTE Grenze** - NIEMALS überschreiten!
3. **Kalorien-Limit hat IMMER Priorität** über Protein-Ziel
4. Akzeptabel: 70-75g Protein, wenn dadurch unter 1300 kcal

## Meal Planning Workflow

**Folge dem 8-Schritt-Workflow** (vollständige Details in `references/meal-plan-workflow.md`):

1. **Anforderungen sammeln** → Zeitraum, Ernährungsziele, Präferenzen
2. **Rezepte auswählen** → External `recipe-database.md` oder bundled `references/recipe-database.md`
3. **Plan erstellen** → Template-Format verwenden, Dateiname: `wochenplan-YYYY-MM-DD-bis-DD.md`
4. **Nährwerte MANUELL berechnen** → JEDE Zutat einzeln mit Standardwerten aus `nutrition-recalculation.md`
5. **Verifikation** → `python3 scripts/verify_nutrition.py meal-plans/wochenplan-file.md` (**KRITISCH!**)
6. **Anpassungen** → Protein/Kalorien optimieren bei Abweichungen

**Optional (nur auf expliziten Nutzer-Wunsch):**
7. **Einkaufsliste** → Nach Kategorien gruppieren, Dateiname: `einkaufsliste-YYYY-MM-DD-bis-DD.md`
8. **Meal Prep Strategie** → 4-Phasen-Timeline, Dateiname: `meal-prep-strategie-YYYY-MM-DD-bis-DD.md`
9. **Mealie-Export** → `python3 scripts/mealie_export.py wochenplan-file.md --prefix YYYY_MM_DD`

**Wichtigste Punkte:**
- ✅ **Nährwerte MANUELL berechnen** vor verify_nutrition.py!
- ✅ Externe Rezepte prüfen: `ls recipe-database.md`
- ✅ Zutatenwiderholungen prüfen (max. 4 Mahlzeiten pro geschmacksgebender Komponente)
- ✅ Bei Protein <75g: Tofu/Erbsenprotein ergänzen
- ✅ Bei Kalorien >1300: Öl/Nüsse reduzieren
- ⚠️ **Einkaufsliste & Meal Prep Strategie:** Nur auf expliziten Nutzer-Wunsch!

## Bundled Resources

### Scripts

**`scripts/verify_nutrition.py`** - Parser-basierte Nährwert-Validierung
- Parst **Nährwerte:**-Sektionen automatisch aus Markdown
- Validiert gegen Daily und Meal-Ranges
- `python3 scripts/verify_nutrition.py meal-plans/wochenplan-08-12.md`
- Optional: `--json` Flag für programmatische Verarbeitung
- **Wann verwenden:** Nach MANUELLER Nährwertberechnung im Meal Plan, vor Finalisierung

**`scripts/mealie_export.py`** - Parser-basierte Mealie-Integration
- Vollautomatischer Export aus Markdown-Rezepten
- `python3 scripts/mealie_export.py meal-plans/wochenplan-08-12.md --prefix 2024_12_08`
- **Wann verwenden:** Bei jedem neuen Wochenplan für Mealie-Import

**`nutrition-recalculation.md`** - Nährwert-Standardwerte Referenz
- **PFLICHTLEKTÜRE vor jeder Nährwertberechnung!**
- Präzise Standardwerte für ALLE gängigen Zutaten (pro 100g/100ml)
- Dokumentiert systematische Fehlerquellen (+180-420 kcal Fehler!)
- **Location**: Projekt-Root (`nutrition-recalculation.md`) oder bundled (`scripts/nutrition-recalculation.md`)
- **Tipp**: Erstelle projekt-spezifische Version für eigene Zutat-Erweiterungen!

### References

**Recipe Database** - Verifizierte Rezepte
- **External:** `recipe-database.md` (im Projekt-Verzeichnis, falls vorhanden)
- **Bundled:** `references/recipe-database.md` (Fallback)
- Komplette Rezept-Sammlung mit Nährwerten, Meal-Prep-Hinweisen
- **Wann lesen:** Bei jeder Meal Plan Erstellung

**`references/meal-plan-workflow.md`** - Workflow-Guide
- Schritt-für-Schritt Anleitung mit Templates
- Meal Prep Strategien, Einkaufslisten-Generator
- **Wann lesen:** Vor der ersten Meal Plan Erstellung

**`references/external-recipes-guide.md`** - Guide für externe Rezept-Datenbanken
- Anleitung zum Erstellen eigener recipe-database.md
- Format-Anforderungen und Best Practices

## Nährwertberechnung - Prozess (PFLICHT!)

**VOR dem Ausführen von verify_nutrition.py:**

### Schritt 1: Zutatenliste mit exakten Mengen
```
- 30g Haferflocken
- 150ml Hafermilch
- 1 EL Chiasamen (12g)
- 1 EL Mandelmus (15g)
- 20g Erbsenprotein
- 15g Walnüsse
```

### Schritt 2: JEDE Zutat einzeln berechnen
Nutze Standardwerte aus `nutrition-recalculation.md` (projekt-spezifisch) oder `scripts/nutrition-recalculation.md` (bundled):
```
30g Haferflocken: 111 kcal, 3.9g P, 18g C, 2.1g F, 3g Fiber
150ml Hafermilch: 52 kcal, 0.75g P, 9g C, 1.5g F, 0g Fiber
12g Chiasamen: 58 kcal, 2g P, 5g C, 3.7g F, 4.1g Fiber
15g Mandelmus: 92 kcal, 3.2g P, 3.2g C, 8g F, 1.2g Fiber
20g Erbsenprotein: 75 kcal, 16g P, 1g C, 1.4g F, 0g Fiber
15g Walnüsse: 98 kcal, 2.3g P, 2.1g C, 9.8g F, 1g Fiber
```

### Schritt 3: Summieren
```
SUMME: 486 kcal, 28.15g P, 38.3g C, 26.5g F, 9.3g Fiber
```

### Schritt 4: Prüfen gegen Meal-Ranges
- Frühstück sollte 300-400 kcal haben
- 486 kcal ist zu viel! → Nussmus/Walnüsse reduzieren

### Schritt 5: In Meal Plan eintragen und verify_nutrition.py ausführen

**Nährwerte in Markdown eintragen:**
```markdown
**Nährwerte:**
- Kalorien: 486 kcal
- Protein: 28.15g
- Kohlenhydrate: 38.3g
- Fett: 26.5g
- Ballaststoffe: 9.3g
```

**Dann validieren:**
```bash
python3 scripts/verify_nutrition.py meal-plans/wochenplan-YYYY-MM-DD-bis-DD.md
```

**Wichtigste Standardwerte (pro 100g/100ml):**
- Haferflocken: 370 kcal, 13g P
- Quinoa gekocht: 120 kcal, 4g P
- Kichererbsen gekocht: 164 kcal, 9g P
- Tofu: 76 kcal, 8g P
- **Tahini: 595 kcal, 17g P** ⚠️
- **Mandelmus: 614 kcal, 21g P** ⚠️
- **Walnüsse: 654 kcal, 15g P** ⚠️
- **Kokosmilch: 230 kcal, 2.3g P** ⚠️
- **Olivenöl: 884 kcal** ⚠️

**Vollständige Liste:** Siehe `nutrition-recalculation.md` (Projekt) oder `scripts/nutrition-recalculation.md` (bundled)

## Neue Rezepte generieren

**Ein Key-Feature:** Erstelle neue, maßgeschneiderte Rezepte basierend auf Nutzer-Anforderungen!

### Wann neue Rezepte generieren?
- Spezifische Zutaten sollen verbraucht werden
- Nährwert-Ziele mit vorhandenen Rezepten nicht erreichbar
- Nutzer möchte Abwechslung oder neue Ideen
- Saisonale/regionale Zutaten optimal nutzen

### Prozess für Rezept-Generierung

**1. Anforderungen sammeln:**
- Verfügbare/gewünschte Hauptzutaten
- Nährwert-Targets (Kalorien, Protein pro Portion)
- Mahlzeitentyp (Frühstück, Mittag, Abend)
- Geschmacksrichtung (asiatisch, mediterran, mexikanisch)
- Meal-Prep-Eignung

**2. Challenge-Compliance prüfen:**
- ✅ Nur erlaubte Zutaten
- ❌ Keine ausgeschlossenen Zutaten
- ❌ Keine tierischen/verarbeiteten Produkte

**3. Rezept entwickeln:**
- Basis-Komponenten wählen (Getreide + Protein + Gemüse)
- Geschmacks-Profile aufbauen (Gewürze, Dressings)
- **Nährwerte kalkulieren:** JEDE Zutat einzeln summieren (siehe Nährwertberechnung oben!)
- Zubereitung strukturieren (Schritt-für-Schritt)

**4. Rezept auf Vollständigkeit prüfen:**
- ✅ **Proteinpulver richtig eingesetzt:** NUR in Flüssigkeiten (Smoothies, Porridge, Overnight Oats)
- ✅ **Marinaden vorhanden:** Tofu braucht Marinaden (Miso, Sojasauce, Gewürze + Öl)
- ✅ **Ausreichend gewürzt:** Nicht nur Salz & Pfeffer
- ✅ **Konsistenz stimmig:** Genug Sauce/Dressing, nicht zu trocken
- ✅ **Texturen ergänzen sich:** Knusprig + cremig, weich + bissfest
- ✅ **Fette/Öle enthalten:** 1-2 EL Öl oder Nussmus für Geschmack
- ⚠️ **Häufige Fehler vermeiden:**
  - Trockenes Tofu ohne Marinade
  - Geröstetes Gemüse in kalten Meal-Prep-Bowls (wird matschig!)
  - Erbsenprotein in Salaten/Bowls (funktioniert nicht!)

**5. Nährwerte validieren:**
- Gegen Meal-Ranges prüfen
- Bei Bedarf anpassen
- `verify_nutrition.py` für finale Validierung

**6. Meal-Prep-Hinweise hinzufügen:**
- Vorbereitung im Voraus, Haltbarkeit, Aufwärm-Tipps

### Beispiel Rezept-Generierung

**Anforderung:** "Blumenkohl + asiatisch + 350 kcal, 20g Protein, meal-prep-freundlich"

**Entwicklung:**
```
Quinoa (150g gekocht, 180 kcal, 6g P) +
Marinierter Tofu (120g, 95 kcal, 10g P) +
Blumenkohl geröstet (200g, 50 kcal, 4g P) +
Miso-Sauce (25 kcal, 1g P)
→ Gesamt: 350 kcal, 21g Protein ✅
```

**Qualitätskontrolle:**
- ✅ Tofu mariniert (Miso + Sesamöl + Ingwer, 30 Min)
- ✅ Sauce vorhanden, ausreichend gewürzt
- ✅ Fette enthalten (Sesamöl), Texturen komplementär
- → Stimmig!

**Strukturieren:**
1. Tofu marinieren (30 Min)
2. Blumenkohl rösten (200°C, 25 Min)
3. Quinoa kochen (15 Min)
4. Bowl zusammenstellen

**Meal Prep:** 4-5 Tage haltbar, getrennt lagern, täglich frisch kombinieren

## Best Practices

### Nährwert-Optimierung
- **Protein boosten:** Tofu, extra Hülsenfrüchte, Erbsenprotein in Flüssigkeiten
- **Kalorien reduzieren:** Öl/Nüsse limitieren, richtig dosieren
- **Ballaststoffe erhöhen:** Mehr Gemüse, Vollkorn

### Abwechslung
- Gleiche Basis, verschiedene Gewürze (Mediterran, Asiatisch, Mexikanisch)
- Textur-Kontraste (knusprig + cremig)
- **Zutatenwiderholungen begrenzen:** Max. 4 Mahlzeiten pro geschmacksgebender Komponente

### Meal-Prep-Synergien
- **Rotkohl:** Curry, Salat, mariniert, Suppe
- **Kichererbsen:** Geröstet, Buddha Bowl, Hummus
- **Quinoa:** Frühstück, Bowl-Basis, Salat

### Zeit-Effizienz
- Meal Prep am Sonntag: 3-4 Stunden für 5 Tage
- Täglicher Aufwand: 5-15 Minuten
- Paralleles Kochen: Getreide + Hülsenfrüchte gleichzeitig

## Häufige Szenarien

### Szenario 1: Standard 5-Tage Plan
```
1. Anforderungen: 5 Tage, 1200 kcal, 75g+ Protein
2. Rezepte wählen (externe oder bundled recipe-database.md)
3. Plan nach Template erstellen
4. Nährwerte MANUELL berechnen (nutrition-recalculation.md)
5. verify_nutrition.py ausführen
6. (Optional) Einkaufsliste + Meal Prep Strategie
```

### Szenario 2: Protein-Boost erforderlich
```
1. Verifikation zeigt <75g Protein
2. Anpassungen:
   - Tofu hinzufügen (+10-15g)
   - Extra Nussmus im Frühstück (+4g)
   - Erbsenprotein in Flüssig-Mahlzeiten erhöhen
3. Nährwerte neu berechnen
4. Erneut verifizieren
```

### Szenario 3: Neue Rezepte generieren
```
1. Anforderungen: "Fenchel + mediterran + 350 kcal, 20g Protein"
2. Entwickeln: Quinoa + Cannellini-Bohnen + Fenchel + Zitronen-Kräuter-Dressing
3. Nährwerte MANUELL berechnen (jede Zutat einzeln!)
4. Qualitätskontrolle (siehe Checkliste oben)
5. Strukturieren, Meal Prep Hinweise
6. Optional: Zu recipe-database.md hinzufügen
```

## Troubleshooting

**Problem:** Nährwerte stimmen nicht
→ Häufigste Ursache: Nüsse/Nussmus/Tahini/Kokosmilch unterschätzt
→ JEDE Zutat mit `nutrition-recalculation.md` neu berechnen
→ verify_nutrition.py zeigt Abweichungen

**Problem:** Neue Rezepte schmecken fade
→ Qualitätskontrolle-Checkliste durchgehen
→ Häufigste Fehler: Tofu ohne Marinade, zu wenig Gewürze, fehlendes Fett
→ Nach Korrekturen Nährwerte neu berechnen!

**Problem:** Zu viel Meal Prep Aufwand
→ Mehr Synergien nutzen (gleiche Basis-Komponenten)
→ Simplere Rezepte wählen
→ Batch-Größen erhöhen

**Problem:** Kalorienlimit überschritten
→ Ursache meist: Fehlerhafte Nährwertberechnung bei Fetten/Nüssen
→ Neu berechnen mit korrekten Werten
→ Portionen reduzieren: Nussmus (1 EL → 1 TL), Tahini (2 EL → 1 EL), Öl minimieren

## Qualitätskontrolle

### Für Meal Plans (vor Finalisierung):
- [ ] **Nährwerte MANUELL berechnet** (jede Zutat einzeln mit nutrition-recalculation.md)
- [ ] **verify_nutrition.py ausgeführt** und alle Targets erfüllt
- [ ] **Kalorienlimit eingehalten** (≤1300 kcal pro Tag)
- [ ] **Proteinziel erreicht** (75-90g, akzeptabel: 70-75g wenn <1300 kcal)
- [ ] **Challenge-Regeln eingehalten** (keine ausgeschlossenen Zutaten)
- [ ] **Zutatenwiderholungs-Regel beachtet:** Geschmacksgebende Komponenten max. 4 MAHLZEITEN (jede Mahlzeit zählt einzeln!)
- [ ] **Meal-Prep-Kompatibilität:** Geröstetes Gemüse nur für warme Gerichte; für kalte Bowls Rohkost
- [ ] Realistische Zubereitungszeiten
- [ ] Lagerungshinweise enthalten
- [ ] Abwechslung über die Woche
- [ ] Saisonale/verfügbare Zutaten (Deutschland)

### Für neue Rezepte (vor Nährwert-Validierung):
- [ ] **Nährwerte vollständig MANUELL berechnet** (jede Zutat einzeln summiert)
- [ ] Erbsenprotein-Pulver nur in Flüssigkeiten (NICHT in Bowls/Salaten)
- [ ] Tofu haben Marinaden (mind. 30 Min)
- [ ] Alle Komponenten ausreichend gewürzt
- [ ] Konsistenz stimmig (nicht zu trocken/wässrig)
- [ ] Fette/Öle enthalten (1-2 EL pro Portion)
- [ ] Alle Zubereitungsschritte vollständig
- [ ] **KEINE internen Optimierungskommentare** in finalen Rezepten
- [ ] Meal-Prep-Tauglichkeit: Rohkost für kalte Komponenten

### Für optionale Komponenten (nur auf Nutzer-Wunsch):
- [ ] **Einkaufsliste:** Vollständig und nach Kategorien organisiert
- [ ] **Meal Prep Strategie:** 4-Phasen-Timeline mit realistischen Zeitangaben
