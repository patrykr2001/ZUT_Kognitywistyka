# 🧠 Badanie EEG - Analiza Aktywności Mózgu

Eksperyment badający aktywność elektryczną mózgu (EEG) podczas wykonywania różnych zadań poznawczych i stanów fizjologicznych.

## 📋 Opis projektu

Automatyzowany eksperyment EEG składający się z 10 różnych zadań/stanów mierzących aktywność mózgu w kontrolowanych warunkach. Badanie obejmuje pomiary baseline'u (zamknięte/otwarte oczy), artefaktów (mruganie, ruchy), oraz zadań poznawczych (matematyka, wyobraźnia, relaks).

## 📂 Pliki w projekcie

### `zadania.py`
Główny skrypt eksperymentu automatyzującego sesję badawczą EEG.

**Struktura eksperymentu (10 zadań):**
1. **Zamknięte oczy** (30s) - baseline bez bodźców wizualnych
2. **Otwarte oczy, normalne mruganie** (30s) - baseline z bodźcami wizualnymi
3. **Otwarte oczy, bez mrugania** (30s) - pomiar bez artefaktów mrugania
4. **Szybkie mruganie** (30s) - pomiar artefaktów mrugania
5. **Zaciskanie szczęk, normalne mruganie** (30s) - pomiar artefaktów mięśniowych
6. **Ruchy oczu w prawo i w lewo** (30s) - pomiar artefaktów ruchów oczu
7. **Mówienie, normalne mruganie** (30s) - pomiar podczas aktywności werbalnej
8. **Ruchy głowy bez mrugania** (30s) - pomiar artefaktów ruchowych
9. **Relaks przy muzyce** (60s) - stan relaksacyjny z brown noise
10. **Zadania poznawcze** (różne czasy) - seria zadań matematycznych i wyobraźniowych

### `Events.txt`
Plik logu zawierający znaczniki czasowe (event markers) dla każdego zadania.

**Format:**
```
Latency         timeStamp          type
34.567      1731684579.123     Task 1
67.891      1731684612.456     Task 2
...
```

**Pola:**
- `Latency` - czas od rozpoczęcia eksperymentu (w sekundach)
- `timeStamp` - znacznik czasowy Unix (timestamp)
- `type` - typ zdarzenia/zadania

### Pliki dźwiękowe

#### `brown_noise.wav`
Szum brunatny (brown noise) używany w zadaniu relaksacyjnym. Brown noise charakteryzuje się niższymi częstotliwościami niż white noise i jest często używany do релаксации i poprawy koncentracji.

#### `beep.wav`
Sygnał dźwiękowy oznaczający rozpoczęcie nowego zadania.

### Pliki danych EEG

#### `20251115161939_Patienftytft01.easy`
Surowe dane EEG w formacie .easy (format używany przez systemy Mitsar EEG).

#### `20251115161939_Patienftytft01.info`
Plik metadanych zawierający informacje o sesji EEG (ustawienia, pacjent, data nagrania).

## 🚀 Jak uruchomić eksperyment

### Wymagania
```bash
pip install pygame
```

**Pliki dźwiękowe:** Upewnij się, że `brown_noise.wav` i `beep.wav` znajdują się w tym samym folderze co `zadania.py`.

### Uruchomienie
```bash
python zadania.py
```

## 📊 Zadania poznawcze (Task 10)

Ostatnie zadanie zawiera serię aktywności poznawczych:

### Zadania matematyczne (5s każde)
- Dodawanie: 198 + 679
- Mnożenie: 54 × 23
- Dzielenie: 987 ÷ 32
- Dodawanie: 345 + 678

### Zadania wyobraźniowe (10s każde)
- Wyobrażanie sobie fioletowej krowy latającej nad zielonymi wzgórzami
- Liczenie w myślach od 100 do 0 co 3
- Wyobrażanie sobie lotu na wielorybie przez ocean

### Zadania kategoryzacyjne (5s każde)
- Znajdź niepasujący element: jabłko, banan, **marchewka**, gruszka
- Znajdź niepasujący element: stół, krzesło, sofa, **rower**

## ⏱️ Harmonogram czasowy

| Zadanie | Czas trwania | Typ aktywności |
|---------|--------------|----------------|
| 1 | 30s | Baseline (zamknięte oczy) |
| 2 | 30s | Baseline (otwarte oczy) |
| 3 | 30s | Kontrola artefaktów |
| 4 | 30s | Artefakt mrugania |
| 5 | 30s | Artefakt mięśniowy |
| 6 | 30s | Artefakt ruchów oczu |
| 7 | 30s | Aktywność werbalna |
| 8 | 30s | Artefakt ruchowy |
| 9 | 60s | Relaksacja |
| 10 | ~75s | Zadania poznawcze |

**Łączny czas:** ~6 minut 45 sekund

## 🔬 Cel badania

### Baseline
- Pomiar podstawowej aktywności mózgu w stanie spoczynku
- Porównanie stanu z zamkniętymi vs. otwartymi oczami

### Artefakty
- Identyfikacja i charakteryzacja różnych źródeł szumu w sygnale EEG
- Ruchy oczu (EOG - elektrookulografia)
- Aktywność mięśniowa (EMG - elektromiografia)
- Artefakty ruchowe

### Zadania poznawcze
- Analiza aktywności mózgu podczas różnych procesów poznawczych
- Obliczenia matematyczne (funkcje wykonawcze, pamięć robocza)
- Wyobraźnia wizualna (obszary wzrokowe, pamięć)
- Kategoryzacja (rozumowanie, pamięć semantyczna)

### Relaksacja
- Pomiar aktywności mózgu w stanie zrelaksowanym
- Analiza wpływu bodźców dźwiękowych (brown noise)

## 📈 Analiza danych

Po zakończeniu eksperymentu:
1. Dane EEG zapisywane są w plikach `.easy` i `.info`
2. Znaczniki czasowe dostępne w `Events.txt`
3. Dane można zaimportować do oprogramowania do analizy EEG (np. EEGLAB, MNE-Python)
4. Synchronizacja zdarzeń z danymi EEG poprzez timestamps

## ⚙️ Parametry eksperymentu

```python
long_wait = 60   # Długie zadanie (relaksacja)
short_wait = 30  # Standardowe zadanie
```

Można dostosować czasy w zmiennych `long_wait` i `short_wait` w pliku `zadania.py`.

## 📝 Uwagi techniczne

- Skrypt automatycznie czyści ekran (`os.system('cls')`) między zadaniami
- Beep sygnalizuje rozpoczęcie każdego nowego zadania
- Brown noise odtwarzany w pętli podczas zadania relaksacyjnego
- Wszystkie zdarzenia automatycznie logowane z precyzyjnymi timestampami
- Eksperyment wymaga aktywnego udziału badanego (odpowiedzi mentalne)

## 🎯 Zastosowania

- Badania neurokognitywne
- Analiza artefaktów w sygnale EEG
- Trening w metodologii badań EEG
- Projekty studenckie z kognitywistyki i neuronauki
