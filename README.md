# notwendige Dateien

## 1. twitter_api.py:
  - benutzt den 'https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent' Endpunkt der Twitter API
  - nach unten runterscrollen (zu 'starting creation of excel sheet') -> gewünschte Werte für 'num_of_tweets', 'query' und 'num_of_repeats' eingeben
  - 'relevant_date_start', 'relevant_date_end' und 'custom_time' werden benutzt um den Zeitrahmen für die Twitter API einzugrenzen (maximal 7 Tage zurück)
  - timedelta(x) -> x ist der Wert für wie viele Tage man zurückgehen will | x = -1 == Gestern
  - 'create_excel_sheet' ist immer für einen vergangenen Tag -> 'custom_time' anstatt 'relevant_date_start' bei API Calls für 7 Tage vorher
  - 'create_excel_sheet_without_end' ist immer für den jetzigen Tag
  - benötigte Hauptfunktion ausführen
  - Datensatz wird unter 'data/tweets.xlsx' gespeichert
  - die erzeugte 'tweets.xlsx'-Datei sollte, nachdem man fertig ist, aus dem 'data'-Verzeichnis verschoben werden (damit man z.B. für eine andere Query einen weiteren Datensatz erstellen kann)
## 2. stock_ticker_api.py:
  - benutzt die yfinance library, um Marktdaten von der Yahoo! Finance's API zu downloaden
  - zuerst müssen das gewünschte Startdatum und Enddatum, sowie das Interval, das Aktien-Symbol und der Typ ('Adj Close' oder 'Volume') festgelegt werden 
  - die Methode 'create_csv_from_ticker' erstellt dann eine csv-Datei mit den Aktien-Daten unter dem Verzeichnis: 'data/{Aktien-Symbol}'
## 3. us_project.ipynb:
  - Imports ausführen
  - Alle Zellen ausführen -> Datensatz laden, Datensatz bereinigen, Datenanalyse, Modell, Auswertung
  
  ----------------------------------------------------------------------------------------------------------------------------------------
  ----------------------------------------------------------------------------------------------------------------------------------------
  # weitere Verzeichnisse
  
  ### 4. '/cleaned_data' -> hier kommen die Datensätze nach dem Data-Cleaning rein
  ### 5. '/data' -> hier kommen die Datensätze von 'twitter_api.py' und 'stock_ticker_api.py' rein
  ### 6. '/data_save' -> fertige Datensätze um 'us_project.ipynb' auszuführen
  
  ----------------------------------------------------------------------------------------------------------------------------------------
  ----------------------------------------------------------------------------------------------------------------------------------------
  # Weiteres
  
  - ### Bearer-Token wird zusammen mit dem Twitter Account in wenigen Tagen gelöscht werden
