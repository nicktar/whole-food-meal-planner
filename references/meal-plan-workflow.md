# Meal Plan Generation Guide

Dieser Guide beschreibt den Workflow zur Erstellung eines Whole Food Challenge Meal Plans.

## Workflow-Übersicht

```
1. Anforderungen sammeln
   ↓
2. Rezepte aus Datenbank auswählen
   ↓
3. Meal Plan erstellen
   ↓
4. Nährwerte verifizieren (verify_nutrition.py)
   ↓
5. Anpassungen vornehmen (falls nötig)
   ↓
6. Einkaufsliste generieren
   ↓
7. Meal Prep Strategie erstellen
   ↓
8. (Optional) Mealie-Export generieren
```

---

## 1. Anforderungen-Template

Verwende dieses Template, um alle notwendigen Informationen vom Nutzer zu sammeln:

```
📋 MEAL PLAN ANFORDERUNGEN

Zeitraum:
- Anzahl Tage: [___]
- Datum von/bis: [___]

Ernährungsziele:
- Tägliche Kalorien: [___ kcal]
- Protein-Minimum: [___ g]
- Besondere Anforderungen: [___]

Mahlzeitenstruktur:
- Frühstück: [Ja/Nein]
- Mittagessen: [Ja/Nein]
- Abendessen: [Ja/Nein]

Präferenzen:
- Bevorzugte Zutaten: [___]
- Zu verbrauchende Zutaten: [___]
- Ausgeschlossene Zutaten: [___]

Meal Prep:
- Vorbereitungstag: [___]
- Verfügbare Zeit: [___ Std]
- Meal Prep Erfahrung: [Anfänger/Fortgeschritten/Profi]
```

---

## 2. Rezeptauswahl-Strategie

### Frühstücks-Rotation (3-5 Rezepte)
**Kriterien:**
- 300-400 kcal
- 15-30g Protein
- Schnelle Zubereitung oder Overnight
- Abwechslung in Textur (cremig, knusprig, warm, kalt)

**Beispiel-Rotation:**
- Tag 1-2: Overnight Oats
- Tag 3-4: Chia Pudding
- Tag 5: Overnight Oats (variiert)

### Mittags-/Abendessen-Rotation (5-7 Rezepte)
**Kriterien:**
- 350-450 kcal
- 25-45g Protein
- Meal Prep freundlich
- Verschiedene Proteinquellen (Linsen, Kichererbsen, Bohnen)
- Mix aus warmen und kalten Gerichten

**Auswahlprozess:**
1. Nutzer-Präferenzen berücksichtigen
2. Zu verbrauchende Zutaten priorisieren
3. Synergien identifizieren (gleiche Basis-Komponenten)
4. **Zutatenwiderholungen begrenzen:** Geschmacksgebende Komponenten maximal 4x verwenden (Hülsenfrüchte/Getreide/Paprika/Süßkartoffeln/Zucchini unbegrenzt OK)
5. Ausgewogene Makro-Verteilung sicherstellen

---

## 3. Meal Plan Struktur

### Tagesplan-Template

```markdown
## TAG [X] - [Datum]

### Frühstück: [Rezeptname]
**Kalorien:** [___] | **Protein:** [___]g | **Prep:** [___] Min

**Zutaten (bereits vorbereitet):**
- [Zutat 1]
- [Zutat 2]

**Zubereitung:**
[Kurze Anleitung]

---

### Mittagessen: [Rezeptname]
**Kalorien:** [___] | **Protein:** [___]g | **Prep:** [___] Min

[...]

---

### Abendessen: [Rezeptname]
[...]

---

**Tageszusammenfassung:**
- Gesamt Kalorien: [___] kcal
- Gesamt Protein: [___] g
- Gesamt Ballaststoffe: [___] g
```

---

## 4. Nährwert-Verifikation

Nach der Plan-Erstellung IMMER das Verifikations-Script ausführen:

```bash
python3 scripts/verify_nutrition.py
```

### Verifikations-Checkliste

**Tägliche Targets:**
- ✅ Kalorien: 1100-1300 kcal (Ziel: 1200)
- ✅ Protein: >100g (Ziel: 110g)
- ✅ Ballaststoffe: >25g (Ziel: 30g)

**Mahlzeiten-Ranges:**
- ✅ Frühstück: 300-400 kcal, 15-30g Protein
- ✅ Mittagessen: 350-450 kcal, 25-45g Protein
- ✅ Abendessen: 350-400 kcal, 25-45g Protein

**Anpassungen bei Abweichungen:**
- Kalorien zu niedrig → Nüsse/Samen/Avocado hinzufügen
- Kalorien zu hoch → Portionen reduzieren
- Protein zu niedrig → Mehr Hülsenfrüchte, Tofu ergänzen
- Ballaststoffe zu niedrig → Gemüse-Portionen erhöhen

---

## 5. Einkaufslisten-Generator

### Struktur

```markdown
# 🛒 EINKAUFSLISTE - [Zeitraum]

## Vollkornprodukte & Getreide
- [ ] [Menge] [Produkt]

## Hülsenfrüchte
- [ ] [Menge] [Produkt] (getrocknet/gekocht)

## Frisches Gemüse
- [ ] [Menge] [Produkt]

## Frisches Obst
- [ ] [Menge] [Produkt]

## Nüsse & Samen
- [ ] [Menge] [Produkt]

## Pflanzenmilch & Nussmus
- [ ] [Menge] [Produkt]

## Gewürze & Basics
- [ ] [Menge] [Produkt]

---

**Einkaufs-Tipps:**
- [Saisonale Alternativen]
- [Lagerungs-Hinweise]
- [Preis-Tipps]
```

---

## 6. Meal Prep Strategie

### Prep-Day Timeline Template

```markdown
# 🍳 MEAL PREP STRATEGIE - [Datum]

**Gesamtzeit:** ~[X] Stunden
**Schwierigkeitsgrad:** [Leicht/Mittel/Anspruchsvoll]

---

## VORBEREITUNG (Vorabend)
⏰ **5-10 Min**

- [ ] Hülsenfrüchte einweichen (Kichererbsen, Bohnen)
- [ ] Einkaufsliste finalisieren
- [ ] Container bereitstellen

---

## PHASE 1: GRUNDLAGEN (Start)
⏰ **30-45 Min**

**Parallel-Tasks:**

1. **Getreide kochen** (20 Min aktiv, 15 Min passiv)
   - Quinoa: [___]g → [___]g gekocht
   - Buchweizen: [___]g → [___]g gekocht

2. **Hülsenfrüchte kochen** (15 Min aktiv, 45-60 Min passiv)
   - Linsen: [___]g
   - Kichererbsen: [___]g (eingeweicht)

3. **Overnight Oats vorbereiten** (10 Min)
   - [Anzahl] Portionen in Gläsern

---

## PHASE 2: GEMÜSE & PROTEIN (Nach 30 Min)
⏰ **45-60 Min**

**Parallel-Tasks:**

1. **Gemüse rösten** (10 Min Prep, 25 Min Ofen)
   - [Gemüse 1]: [___]g
   - [Gemüse 2]: [___]g

2. **Kichererbsen würzen & rösten** (5 Min Prep, 25 Min Ofen)
   - [___]g Kichererbsen mit Gewürzen

3. **Dressings & Saucen** (15 Min)
   - Tahini-Dressing
   - [Weitere Dressings]

---

## PHASE 3: SPEZIAL-KOMPONENTEN
⏰ **30-45 Min**

1. **Rotkohl marinieren** (10 Min)
2. **Pilz-Füllung** (15 Min)
3. **[Weitere spezifische Komponenten]**

---

## PHASE 4: PORTIONIEREN & LAGERN
⏰ **20-30 Min**

**Portionierung:**
- [ ] Frühstück: [Anzahl] Portionen in Gläsern
- [ ] Mittagessen: [Anzahl] Portionen in Containern
- [ ] Abendessen: [Anzahl] Portionen in Containern

**Lagerung:**
- Kühlschrank: [Liste]
- Tiefkühler: [Liste]
- Raumtemperatur: [Liste]

---

## TÄGLICHER AUFWAND

**Montag-Freitag:** 5-15 Min/Tag
- Frühstück: Aus Kühlschrank nehmen
- Mittagessen: Aufwärmen (falls nötig)
- Abendessen: Zusammenstellen/Aufwärmen

**Wochenmitte-Check (Mi/Do):** 15 Min
- Frische Salate schneiden
- Dressings auffrischen
- Portionen kontrollieren
```

---

## 7. Optimierungs-Strategien

### Zeit-Optimierung
1. **Paralleles Kochen:** Getreide + Hülsenfrüchte gleichzeitig
2. **Ofen ausnutzen:** Mehrere Bleche gleichzeitig rösten
3. **Passive Zeit:** Während Kochzeit andere Aufgaben erledigen

### Kosten-Optimierung
1. **Getrocknete Hülsenfrüchte:** Günstiger als Dosen
2. **Saisonales Gemüse:** Günstiger und frischer
3. **Bulk-Einkauf:** Nüsse, Samen, Getreide in größeren Mengen

### Geschmacks-Optimierung
1. **Gewürz-Variation:** Gleiche Basis, verschiedene Würzungen
2. **Frische Komponenten:** Täglich frische Kräuter/Toppings hinzufügen
3. **Textur-Kontraste:** Knusprige + cremige Elemente kombinieren
4. **Zutatenwiderholungen begrenzen:** Geschmacksgebende Komponenten maximal 4x pro Woche (Rotkohl, Hokkaido, etc. - Hülsenfrüchte/Getreide/Paprika/Süßkartoffeln/Zucchini unbegrenzt)

---

## 8. Häufige Anpassungen

### Problem: Zu wenig Protein
**Lösungen:**
- Tofu-Würfel hinzufügen (+10-15g Protein)
- Extra Hülsenfrüchte zu Mahlzeiten (+8-12g Protein/100g)
- Extra Nussmus (+3-4g Protein/EL)

### Problem: Zu viele Kalorien
**Lösungen:**
- Nüsse/Samen reduzieren (-90 kcal pro EL)
- Avocado-Portion halbieren (-80 kcal)
- Öl in Dressings reduzieren (-45 kcal pro TL)

### Problem: Zu wenig Abwechslung
**Lösungen:**
- Verschiedene Gewürzmischungen für gleiche Basis
- Roh vs. geröstet vs. gedämpft variieren
- Internationale Würzungen (Mediterran, Asiatisch, Mexikanisch)

---

## 9. Qualitätskontrolle-Checkliste

Vor Finalisierung des Plans:

- [ ] Alle Challenge-Regeln eingehalten
- [ ] Nährwerte verifiziert (verify_nutrition.py)
- [ ] Ausgeschlossene Zutaten vermieden
- [ ] **Zutatenwiderholungs-Regel beachtet:** Geschmacksgebende Komponenten maximal 4x verwendet
- [ ] Meal Prep Synergie maximiert
- [ ] Einkaufsliste vollständig
- [ ] Zubereitungszeiten realistisch
- [ ] Lagerungshinweise enthalten
- [ ] Abwechslung über die Woche

---

## 10. Mealie-Export (Optional)

Falls der Nutzer Mealie verwendet:

```bash
# Einzelne Rezepte exportieren
python3 scripts/mealie_export.py

# Export-Dateien befinden sich in: mealie_exports/
```

**Import in Mealie:**
1. Mealie öffnen
2. "Import" → "JSON"
3. Generierte JSON-Dateien hochladen
4. Rezepte werden automatisch mit Nährwerten angelegt
