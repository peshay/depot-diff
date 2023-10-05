# Portfolio Differenzen Analyse

Dieses Repository enthält ein Python-Skript, um Unterschiede zwischen einem aktuellen Portfolio (Bestands-CSV) und einer Handelshistorie (Handelshistorie-CSVs) zu analysieren.

## Abhängigkeiten

- Python (empfohlen: Version 3.8 oder höher)
- pandas
- chardet

## Installation

Um die notwendigen Python-Pakete zu installieren:
```bash
pip install pandas chardet
```

## Verwendung

Sie können das Skript über die Kommandozeile mit den erforderlichen Argumenten ausführen:
```bash
python depot_diffs.py bestands_datei.csv handelshistorie_datei1.csv handelshistorie_datei2.csv ...
```

- `script_name.py` durch den tatsächlichen Namen Ihres Python-Skripts ersetzen.
- `bestands_datei.csv` ersetzen durch den Pfad zu Ihrer Bestands-CSV-Datei.
- `handelshistorie_datei1.csv`, `handelshistorie_datei2.csv`, ... ersetzen durch die Pfade zu Ihren Handelshistorie-CSV-Dateien.

Für zusätzliche Hilfe und Optionen:
```bash
python depot_diffs.py -h
```

## Input Format

### Bestands-CSV

Ihre Bestands-CSV-Datei sollte die folgenden Spalten enthalten:

- `WKN`: Die WKN des Wertpapiers.
- `Stück/Nom.`: Anzahl der Stücke/Nominal des Wertpapiers, das Sie halten.
- `Kaufkurs in EUR`: Der durchschnittliche Kaufkurs des Wertpapiers in EUR.

### Handelshistorie-CSV

Jede Handelshistorie-CSV-Datei sollte die folgenden Spalten enthalten:

- `WKN`: Die WKN des Wertpapiers.
- `Typ`: Der Typ der Transaktion (Kauf oder Verkauf).
- `Stück`: Anzahl der Stücke/Nominal des Wertpapiers, das gekauft/verkauft wurde.
- `Wert`: Der Wert der Transaktion in EUR.

## Output

Das Skript gibt eine Tabelle aus, die die Differenzen zwischen Ihrem aktuellen Portfolio und Ihrer Handelshistorie zeigt. Es wird der erwartete Bestand und der durchschnittliche Kaufkurs basierend auf Ihrer Handelshistorie berechnet und mit Ihrem aktuellen Portfolio verglichen.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz - siehe die [LICENSE.md](LICENSE.md) Datei für Details.
