# Whole Food Meal Planner Skill - Installation

## Schnellstart

### Option 1: Direkter Download (Empfohlen)

```bash
# Download des Skills aus dem Repository
wget https://github.com/nicktar/whole-food-meal-planner/raw/main/whole-food-meal-planner.skill

# Oder mit curl:
curl -L -O https://github.com/nicktar/whole-food-meal-planner/raw/main/whole-food-meal-planner.skill
```

### Option 2: Aus Repository klonen

```bash
# Repository klonen
git clone https://github.com/nicktar/whole-food-meal-planner.git
cd whole-food-meal-planner

# Skill-Tarball ist bereits vorhanden:
ls -lh whole-food-meal-planner.skill
```

## Installation

### In Claude Code (Web)

1. **Skill installieren:**
   - Ziehe die `whole-food-meal-planner.skill` Datei in deine Claude Code Session
   - Oder: Verwende den Skill-Manager in Claude Code

2. **Skill aufrufen:**
   ```
   @whole-food-meal-planner Create a 5-day meal plan with 1200 kcal/day
   ```

### Lokale Installation (für Development)

Wenn du den Skill lokal entwickeln möchtest:

```bash
# Skills-Verzeichnis erstellen
mkdir -p ~/.claude/skills

# Skill entpacken
tar -xzf whole-food-meal-planner.skill -C ~/.claude/skills/whole-food-meal-planner

# Oder: Repository-Link erstellen
ln -s $(pwd) ~/.claude/skills/whole-food-meal-planner
```

## Was ist im Skill enthalten?

Der Skill-Tarball (`whole-food-meal-planner.skill`) enthält:

```
whole-food-meal-planner.skill (36 KB)
├── SKILL.md                              # Skill-Definition mit Frontmatter
├── scripts/
│   ├── verify_nutrition.py              # Parser-basierte Nährwert-Validierung
│   ├── mealie_export.py                 # Parser-basierter Mealie-Export
│   └── nutrition-recalculation.md       # Bundled Nährwert-Standardwerte
├── references/
│   ├── recipe-database.md               # Bundled Rezepte (Fallback)
│   ├── meal-plan-workflow.md            # 8-Schritte Workflow
│   └── external-recipes-guide.md        # Guide für externe Ressourcen
└── example-recipe-project/              # Template für User-Projekte
    ├── README.md
    ├── recipe-database.md
    └── .gitignore
```

## Verwendung

### Grundlegende Verwendung

```
@whole-food-meal-planner Create a 3-day meal plan with 1200 kcal/day and 75g protein
```

### Mit eigenen Rezepten

1. Erstelle `recipe-database.md` in deinem Projekt:
   ```bash
   cp ~/.claude/skills/whole-food-meal-planner/references/recipe-database.md ./recipe-database.md
   ```

2. Bearbeite deine Rezepte

3. Skill aufrufen - verwendet automatisch deine Rezepte:
   ```
   @whole-food-meal-planner Create a meal plan using my recipes
   ```

### Mit eigenen Nährwerten

1. Erstelle `nutrition-recalculation.md` in deinem Projekt:
   ```bash
   cp ~/.claude/skills/whole-food-meal-planner/scripts/nutrition-recalculation.md ./nutrition-recalculation.md
   ```

2. Füge eigene Zutaten/Werte hinzu

3. Skill verwendet automatisch deine Werte

## Validierung

### Test 1: Skill-Verfügbarkeit

```
@whole-food-meal-planner help
```

Sollte eine Übersicht der Skill-Funktionen zeigen.

### Test 2: Meal Plan erstellen

```
@whole-food-meal-planner Create a 1-day meal plan with 1200 kcal
```

Sollte einen vollständigen Meal Plan mit Nährwerten generieren.

### Test 3: Nährwert-Verifikation

Nach Erstellung eines Meal Plans:

```bash
python3 scripts/verify_nutrition.py meal-plans/wochenplan-*.md
```

Sollte nutritionale Validierung durchführen.

## Troubleshooting

### Skill wird nicht erkannt

**Problem:** Skill taucht nicht in Skill-Liste auf

**Lösung:**
- Prüfe, ob `SKILL.md` Frontmatter hat (zwischen `---`)
- Stelle sicher, dass Skill-Tarball korrekt entpackt wurde
- Restart Claude Code Session

### Externe Ressourcen werden nicht geladen

**Problem:** Skill verwendet nicht meine `recipe-database.md`

**Lösung:**
- Stelle sicher, Datei heißt exakt `recipe-database.md` (mit Bindestrich)
- Datei muss im Projekt-Root liegen (wo du Skill aufrufst)
- Prüfe Format mit: `head -20 recipe-database.md`

### Python-Scripts funktionieren nicht

**Problem:** `verify_nutrition.py` oder `mealie_export.py` werfen Fehler

**Lösung:**
```bash
# Prüfe Python-Version (benötigt 3.11+)
python3 --version

# Teste Script direkt
python3 scripts/verify_nutrition.py --help
```

## Updates

### Skill aktualisieren

```bash
# Neuen Skill-Tarball herunterladen
wget https://github.com/nicktar/whole-food-meal-planner/raw/main/whole-food-meal-planner.skill

# Alte Installation ersetzen
# (Skills-Manager in Claude Code verwenden oder manuell ersetzen)
```

### Development-Updates

Wenn du aus dem Git-Repository arbeitest:

```bash
cd whole-food-meal-planner
git pull origin main

# Skill neu bauen (optional, wenn du Änderungen gemacht hast)
tar -czf whole-food-meal-planner.skill \
  SKILL.md scripts/ references/ example-recipe-project/
```

## Support & Resources

- **Repository:** https://github.com/nicktar/whole-food-meal-planner
- **Issues:** https://github.com/nicktar/whole-food-meal-planner/issues
- **Dokumentation:** Siehe `references/` Ordner im Skill
- **Beispiel-Projekt:** `example-recipe-project/` im Skill

## Features

- ✅ Automatische Nährwert-Validierung (Parser-basiert)
- ✅ Mealie Recipe Export (Parser-basiert)
- ✅ Externe Rezept-Datenbanken Support
- ✅ Externe Nährwert-Standardwerte Support
- ✅ 8-Schritte Meal Planning Workflow
- ✅ Challenge Rules Validation (Whole Food Challenge)
- ✅ Meal Prep Strategien
- ✅ Shopping List Generation
- ✅ Multi-Day Plans (3-7 Tage)
- ✅ Custom Recipe Generation

## Lizenz

Siehe LICENSE im Repository.
