import pandas as pd
import os

# Mapowanie pytań na kategorie
kategorie_mapping = {
    1: "skandynawski",
    2: "boho",
    3: "boho",
    4: "boho",
    5: "boho",
    6: "boho",
    7: "industrialny",
    8: "industrialny",
    9: "industrialny",
    10: "industrialny",
    11: "industrialny",
    12: "skandynawski",
    13: "skandynawski",
    14: "skandynawski",
    15: "skandynawski"
}

# Licznik instancji dla każdej kategorii
licznik_instancji = {
    "skandynawski": {},
    "boho": {},
    "industrialny": {}
}

# Przypisanie numeru instancji w ramach kategorii
instancja_mapping = {}
for pytanie_nr, kategoria in kategorie_mapping.items():
    if kategoria not in licznik_instancji:
        licznik_instancji[kategoria] = {}
    
    ile_w_kategorii = len(licznik_instancji[kategoria])
    instancja_mapping[pytanie_nr] = ile_w_kategorii + 1
    licznik_instancji[kategoria][pytanie_nr] = ile_w_kategorii + 1

# Wczytanie danych z pliku Excel
excel_path = "Preferencje estetyczne w stylach wnętrz(1-7).xlsx"
df = pd.read_excel(excel_path)

# Wyświetlenie pierwszych kilku wierszy i kolumn
print("Struktura danych:")
print(df.head())
print("\nKolumny w pliku:")
print(df.columns.tolist())

# Tworzenie tablicy danych o strukturze: user, kategoria, instancja, odpowiedz
dane_przetworzone = []

# Iteracja po każdym użytkowniku (wierszu)
for idx, row in df.iterrows():
    user_id = row['ID'] if 'ID' in df.columns else idx + 1
    
    # Iteracja po każdym pytaniu (1-15)
    for pytanie_nr in range(1, 16):
        # Znalezienie właściwej kolumny
        if pytanie_nr == 1:
            col_name = 'Jak chętnie umeblowałbyś/aś swoje mieszkanie w ten sposób?'
        else:
            col_name = f'Jak chętnie umeblowałbyś/aś swoje mieszkanie w ten sposób?{pytanie_nr}'
        
        if col_name in df.columns:
            odpowiedz = row[col_name]
            kategoria = kategorie_mapping[pytanie_nr]
            instancja = instancja_mapping[pytanie_nr]
            
            dane_przetworzone.append({
                'user': user_id,
                'kategoria': kategoria,
                'instancja': instancja,
                'odpowiedz': odpowiedz
            })

# Utworzenie DataFrame z przetworzonych danych
df_wyniki = pd.DataFrame(dane_przetworzone)

print("\n\nPrzetworzone dane:")
print(df_wyniki.head(20))
print(f"\n\nŁączna liczba rekordów: {len(df_wyniki)}")

# Podstawowe statystyki
print("\n\nStatystyki według kategorii:")
print(df_wyniki.groupby('kategoria')['odpowiedz'].value_counts())

print("\n\nLiczba odpowiedzi według kategorii:")
print(df_wyniki.groupby('kategoria').size())

# Zapisanie wyników do CSV
output_path = "wyniki_przetworzone.csv"
df_wyniki.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"\n\nWyniki zapisano do: {output_path}")
