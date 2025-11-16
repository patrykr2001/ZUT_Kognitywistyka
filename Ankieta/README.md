# 📊 Analiza Preferencji Estetycznych w Stylach Wnętrz

Projekt badawczy analizujący preferencje estetyczne respondentów dotyczące różnych stylów wnętrz mieszkalnych.

## 📋 Opis projektu

Badanie ankietowe sprawdzające, jak różne osoby oceniają swoje preferencje wobec trzech popularnych stylów wnętrz:
- **Skandynawski** - minimalizm, jasne kolory, naturalne materiały
- **Boho** - eklektyczny, kolorowy, artystyczny
- **Industrialny** - surowy, metalowe elementy, przestronność

## 📂 Pliki w projekcie

### `badanie.py`
Główny skrypt analizy statystycznej i wizualizacji danych.

**Funkcjonalności:**
- Wczytanie i przetworzenie danych ankietowych
- Konwersja odpowiedzi tekstowych na skalę Likerta (1-5)
- Testy statystyczne:
  - Test normalności rozkładu Shapiro-Wilka
  - Test ANOVA (dla rozkładów normalnych)
  - Test Kruskal-Wallis (dla rozkładów nienormalnych)
- Generowanie 4 wykresów analitycznych:
  1. **Średnie oceny** - wykres słupkowy porównujący średnie dla każdej kategorii
  2. **Heatmapa** - procentowy rozkład odpowiedzi (1-5) dla każdej kategorii
  3. **Wykres sentymentu** - skumulowany wykres pokazujący rozkład odpowiedzi negatywnych/neutralnych/pozytywnych
  4. **Multiple Comparison** - wykres przedziałów ufności (95% CI) dla średnich każdej kategorii

### `exceltocsv.py`
Skrypt konwertujący dane z formatu Excel do CSV z odpowiednim mapowaniem pytań na kategorie.

**Funkcjonalności:**
- Mapowanie 15 pytań ankietowych na 3 kategorie stylów
- Numeracja instancji w ramach każdej kategorii
- Transformacja danych do formatu: `user, kategoria, instancja, odpowiedz`
- Eksport do pliku `wyniki_przetworzone.csv`

### `wyniki_przetworzone.csv`
Przetworzone dane ankietowe w formacie CSV gotowe do analizy.

**Struktura:**
```csv
user,kategoria,instancja,odpowiedz
1,skandynawski,1,Zdecydowanie chciał(a)bym tak mieszkać
1,boho,1,Zdecydowanie bym tego nie zrobił/a
...
```

## 🚀 Jak uruchomić

### Wymagania
```bash
pip install pandas numpy matplotlib seaborn scipy openpyxl
```

### Konwersja danych (jeśli masz surowe dane Excel)
```bash
python exceltocsv.py
```

### Uruchomienie analizy
```bash
python badanie.py
```

## 📊 Wyniki

Po uruchomieniu `badanie.py`:
- Wyświetlenie statystyk opisowych w konsoli
- Wyniki testów statystycznych (normalność, ANOVA/Kruskal-Wallis)
- Zapisanie wykresu do pliku `analiza_statystyczna.png` (4 panele, 300 DPI)
- Wyświetlenie interaktywnego wykresu

## 📈 Interpretacja wyników

### Skala Likerta (1-5)
- **1** - Zdecydowanie bym tego nie zrobił/a
- **2** - Raczej nie chciał(a)bym tak mieszkać
- **3** - Nie mam zdania / Jest mi to obojętne
- **4** - Chętnie bym tak umeblował/a mieszkanie
- **5** - Zdecydowanie chciał(a)bym tak mieszkać

### Testy statystyczne
- **p < 0.2** - różnice między kategoriami są istotne statystycznie
- **p ≥ 0.2** - brak istotnych różnic między kategoriami

### Wykresy
- **Multiple Comparison**: Jeśli przedziały ufności dwóch kategorii się nie nakładają, ich średnie są statystycznie różne
- **Heatmapa**: Pokazuje rozkład procentowy dla każdej oceny (1-5) w każdej kategorii
- **Wykres sentymentu**: Szybka wizualizacja ogólnego nastawienia do każdego stylu

## 🔬 Metodologia

1. Zbieranie danych ankietowych (skala Likerta 1-5)
2. Przetwarzanie i czyszczenie danych
3. Test normalności rozkładu (Shapiro-Wilk)
4. Wybór odpowiedniego testu statystycznego:
   - ANOVA - dla rozkładów normalnych
   - Kruskal-Wallis - dla rozkładów nienormalnych
5. Wizualizacja wyników w 4 komplementarnych wykresach

## 📝 Uwagi

- Dane są anonimizowane (identyfikacja tylko przez numer użytkownika)
- Każda kategoria ma 5 instancji (różnych prezentacji stylu)
- Analiza zakłada poziom istotności α = 0.2 (próg p-value)
