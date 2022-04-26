# Cykelkoordinater
Detta pythonskript omvandlar en address i ett Google Sheet till koordinater med hjälp av [OpenCage Geocoder](https://opencagedata.com/). Koordinaterna skrivs sedan in i samma sheet, vald av användaren.

## Installera Python
Installera Python och skapa sedan ett virtual environment med:
    python venv venv

Installera sedan alla dependencies med:
    pip install -r requirements.txt

## Använd skriptet
För att använda skriptet behöver du:
1. En API-nyckel till OpenCage
Det är gratis att skaffa och görs på deras hemsida. Skapa sedan en fil som heter 'opencage-api-key' och klistra in nyckeln i den.

2. Skaffa credentials för att använda Google Sheets API [här](https://developers.google.com/sheets/api/guides/authorizing)!

3. Dela spreadsheeten med mailadressen som tillhör dina credentials och ge kontot tillstånd att ändra, annars kan skriptet inte fylla i koordinaterna!

4. Fyll i config.json-filen
* sheetName är namnet på filen på Google Drive - t.ex. "Anmälan 2020 (Svar)"
* adressStartCell är den cellen där addresserna till deltagarna börjar - t.ex. "B2"
* latitudeCol är den kolumn där du vill att latituden skrivs
* latitudeCol är den kolumn där du vill att longituden skrivs

Både latitud och longitud skrivs på samma rad som adressen.

## Kör skriptet
Kör skriptet med:
    python main.py

Där koordinater inte hittas skriver skriptet "Kunde inte hitta adressen".



