import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal


def read_info_file(info_filename):
    """
    Wczytuje czas rozpoczęcia zapisu z pliku .info.

    Parameters:
    -----------
    info_filename : str
        Ścieżka do pliku .info

    Returns:
    --------
    float
        Czas rozpoczęcia zapisu w sekundach
    """
    with open(info_filename, 'r') as file:
        for line in file:
            if 'StartDate (firstEEGtimestamp):' in line:
                # Podziel linię i pobierz wartość timestamp
                parts = line.split(':')
                timestamp_ms = float(parts[1].strip())
                # Konwertuj milisekundy na sekundy
                return timestamp_ms / 1000
    return None


def read_events_file(events_filename):
    """
    Wczytuje czasy zdarzeń z pliku Events.txt.

    Parameters:
    -----------
    events_filename : str
        Ścieżka do pliku Events.txt

    Returns:
    --------
    tuple
        Krotka zawierająca (lista latency w sekundach, lista timestampów zdarzeń w sekundach)
    """
    latencies = []
    timestamps = []
    with open(events_filename, 'r') as file:
        # Pomiń nagłówek
        next(file)
        for line in file:
            parts = line.split()
            if len(parts) >= 2:
                latency = float(parts[0])
                timestamp = float(parts[1])
                latencies.append(latency)
                timestamps.append(timestamp)
    return latencies, timestamps


def synchronize_eeg_signal(eeg_data, timestamps, start_time_eeg, first_event_time, experiment_duration, fs):
    """
    Synchronizuje sygnał EEG z czasem rozpoczęcia pierwszego zdarzenia.

    Parameters:
    -----------
    eeg_data : numpy.ndarray
        Macierz danych EEG (kanały x próbki)
    timestamps : numpy.ndarray
        Tablica timestampów
    start_time_eeg : float
        Czas rozpoczęcia zapisu EEG (sekundy)
    first_event_time : float
        Czas pierwszego zdarzenia (sekundy)
    experiment_duration : float
        Czas trwania całego eksperymentu (sekundy)
    fs : float
        Częstotliwość próbkowania (Hz)

    Returns:
    --------
    tuple (numpy.ndarray, numpy.ndarray)
        Zsynchronizowane dane EEG i timestampy
    """
    # Oblicz różnicę czasu między pierwszym zdarzeniem a rozpoczęciem zapisu
    time_difference = first_event_time - start_time_eeg

    # Oblicz liczbę próbek do odcięcia z początku
    samples_to_cut_start = int(time_difference * fs)

    print(f"Czas rozpoczęcia zapisu EEG: {start_time_eeg} s")
    print(f"Czas pierwszego zdarzenia: {first_event_time} s")
    print(f"Różnica czasu: {time_difference} s")
    print(f"Liczba próbek do odcięcia z początku: {samples_to_cut_start}")

    # Odetnij próbki z początku
    eeg_synchronized = eeg_data[:, samples_to_cut_start:]
    timestamps_synchronized = timestamps[samples_to_cut_start:]

    # Oblicz liczbę próbek odpowiadającą czasowi trwania eksperymentu
    experiment_samples = int(experiment_duration * fs)

    print(f"Czas trwania eksperymentu: {experiment_duration} s")
    print(f"Liczba próbek dla eksperymentu: {experiment_samples}")
    print(f"Liczba próbek po odcięciu początku: {eeg_synchronized.shape[1]}")

    # Odetnij nadmiarowe próbki z końca
    if eeg_synchronized.shape[1] > experiment_samples:
        samples_to_cut_end = eeg_synchronized.shape[1] - experiment_samples
        print(f"Liczba próbek do odcięcia z końca: {samples_to_cut_end}")
        eeg_synchronized = eeg_synchronized[:, :experiment_samples]
        timestamps_synchronized = timestamps_synchronized[:experiment_samples]

    print(f"Końcowa liczba próbek: {eeg_synchronized.shape[1]}")

    return eeg_synchronized, timestamps_synchronized


def read_easy_file(filename):
    """
    Wczytuje plik .easy jako macierz.
    
    Parameters:
    -----------
    filename : str
        Ścieżka do pliku .easy
        
    Returns:
    --------
    tuple (numpy.ndarray, numpy.ndarray)
        Macierz danych EEG (kanały x próbki), tablica timestamps (próbki)
    """
    # Wczytaj plik za pomocą pandas - używamy sep='\s+' dla separatora białych znaków
    df = pd.read_csv(filename, sep='\s+', header=None)

    # Wybierz pierwsze 19 kolumn (indeksy 0-18) oraz ostatnią kolumnę (indeks 36)
    # Pierwsze 19 kolumn to dane EEG, ostatnia kolumna to timestampy
    eeg_columns = list(range(19))  # [0, 1, 2, ..., 18]
    timestamp_column = 36

    # Pobierz dane EEG (pierwsze 19 kolumn) i transponuj do formatu (kanały x próbki)
    eeg_data = df.iloc[:, eeg_columns].values.T

    timestamps = df.iloc[:, timestamp_column].values

    return eeg_data // 1000, timestamps


def bandpass_filter(data, lowcut, highcut, fs, order=4):
    """
    Filtr pasmowo-przepustowy (bandpass) dla sygnału EEG.

    Parameters:
    -----------
    data : numpy.ndarray
        Dane do filtracji (kanały x próbki)
    lowcut : float
        Dolna częstotliwość graniczna [Hz]
    highcut : float
        Górna częstotliwość graniczna [Hz]
    fs : float
        Częstotliwość próbkowania [Hz]
    order : int
        Rząd filtra Butterwortha (domyślnie 4)

    Returns:
    --------
    numpy.ndarray
        Przefiltrowane dane
    """
    # Oblicz częstotliwość Nyquista
    nyquist = 0.5 * fs

    # Znormalizuj częstotliwości graniczne
    low = lowcut / nyquist
    high = highcut / nyquist

    # Zaprojektuj filtr Butterwortha
    b, a = signal.butter(order, [low, high], btype='band')

    # Zastosuj filtr do każdego kanału
    filtered_data = np.zeros_like(data)
    for i in range(data.shape[0]):
        filtered_data[i, :] = signal.filtfilt(b, a, data[i, :])

    return filtered_data


def create_eeg_epochs(eeg_data, latencies, fs, epoch_duration=30):
    """
    Tworzy strukturę 3D z epok EEG.

    Parameters:
    -----------
    eeg_data : numpy.ndarray
        Macierz danych EEG (kanały x próbki)
    latencies : list
        Lista wartości latency (czasy rozpoczęcia epok w sekundach)
    fs : float
        Częstotliwość próbkowania [Hz]
    epoch_duration : float
        Czas trwania jednej epoki w sekundach (domyślnie 30s)

    Returns:
    --------
    list
        Lista epok, gdzie każda epoka to macierz (kanały x próbki)
    """
    n_samples_per_epoch = int(epoch_duration * fs)
    n_channels = eeg_data.shape[0]
    epochs = []

    print(f"\nTWORZENIE EPOK:")
    print(f"Liczba kanałów: {n_channels}")
    print(f"Liczba próbek na epokę: {n_samples_per_epoch}")
    print(f"Czas trwania epoki: {epoch_duration} s")
    print(f"Częstotliwość próbkowania: {fs} Hz")

    for i, latency in enumerate(latencies):
        # Oblicz indeks początkowy i końcowy dla epoki
        start_sample = int(latency * fs)
        end_sample = start_sample + n_samples_per_epoch

        # Sprawdź czy nie wykraczamy poza zakres danych
        if end_sample > eeg_data.shape[1]:
            print(f"Uwaga: Epoka {i+1} wykracza poza zakres danych. Pomijam.")
            continue

        # Wytnij epokę
        epoch = eeg_data[:, start_sample:end_sample]
        epochs.append(epoch)

        print(f"Epoka {i+1}: Latency={latency:.3f}s, "
              f"Próbki [{start_sample}:{end_sample}], "
              f"Kształt: {epoch.shape}")

    print(f"Utworzono {len(epochs)} epok\n")

    return epochs


# Wczytaj plik .easy
filename = './20251115161939_Patienftytft01.easy'
info_filename = './20251115161939_Patienftytft01.info'
events_filename = './Events.txt'

eeg_data, timestamps = read_easy_file(filename)

print(f"Kształt macierzy EEG: {eeg_data.shape}")
print(f"Kształt tablicy timestamps: {timestamps.shape}")
print(f"Typ danych: {eeg_data.dtype}")

# Wczytaj czasy z plików
start_time_eeg = read_info_file(info_filename)
latencies, event_timestamps = read_events_file(events_filename)
first_event_time = event_timestamps[0]
last_event_time = event_timestamps[-1]

# Oblicz czas trwania eksperymentu (od pierwszego zdarzenia do 60 sekund po ostatnim)
experiment_duration = (last_event_time - first_event_time) + 60

# Parametry
fs = 500  # Częstotliwość próbkowania [Hz]

# Synchronizuj sygnał EEG
eeg_data, timestamps = synchronize_eeg_signal(eeg_data, timestamps, start_time_eeg,
                                               first_event_time, experiment_duration, fs)

# Parametry filtracji
lowcut = 0.5  # Dolna częstotliwość graniczna [Hz]
highcut = 50  # Górna częstotliwość graniczna [Hz]

# Zastosuj filtr pasmowo-przepustowy
eeg_filtered = bandpass_filter(eeg_data, lowcut, highcut, fs)

# Wykres porównawczy - sygnał oryginalny vs przefiltrowany dla kanału 17 (indeks 16)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 8))

# Sygnał oryginalny
ax1.plot(timestamps // 1000, eeg_data[16, :], linewidth=0.5, color='blue')
ax1.set_xlabel('Czas [s]')
ax1.set_ylabel('Amplituda [mV]')
ax1.set_title('Sygnał EEG - Kanał 17 (Fp1) - ORYGINALNY')
ax1.grid(True, alpha=0.3)

# Sygnał przefiltrowany
ax2.plot(timestamps // 1000, eeg_filtered[16, :], linewidth=0.5, color='red')
ax2.set_xlabel('Czas [s]')
ax2.set_ylabel('Amplituda [mV]')
ax2.set_title(f'Sygnał EEG - Kanał 17 (Fp1) - PRZEFILTROWANY ({lowcut}-{highcut} Hz)')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ============================================================================
# TWORZENIE STRUKTURY 3D - EEGsignal3D
# ============================================================================

# Utwórz epoki z przefiltrowanego sygnału
EEGsignal3D = create_eeg_epochs(eeg_filtered, latencies, fs, epoch_duration=30)

# Wyświetl informacje o strukturze
print("\nINFORMACJE O STRUKTURZE EEGsignal3D:")
print("="*60)
print(f"Liczba epok: {len(EEGsignal3D)}")
if len(EEGsignal3D) > 0:
    print(f"Wymiary każdej epoki: {EEGsignal3D[0].shape}")
    print(f"Format: (kanały x próbki) = ({EEGsignal3D[0].shape[0]} x {EEGsignal3D[0].shape[1]})")
    print(f"Łączny rozmiar struktury: {len(EEGsignal3D)} epok × {EEGsignal3D[0].shape}")
print("="*60 + "\n")

# ============================================================================
# WIZUALIZACJA EPOK
# ============================================================================

# Wybierz kanał do wizualizacji (np. kanał 17 - Fp1, indeks 16)
channel_idx = 2
channel_name = "Cz"

# Utwórz macierz wykresów dla wszystkich epok
n_epochs = len(EEGsignal3D)
n_cols = 2  # 2 kolumny
n_rows = (n_epochs + n_cols - 1) // n_cols  # Oblicz liczbę wierszy

fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 3*n_rows))
axes = axes.flatten() if n_epochs > 1 else [axes]

# Utwórz oś czasu dla jednej epoki (0-30 sekund)
time_axis = np.arange(0, 30, 1/fs)

for i, epoch in enumerate(EEGsignal3D):
    ax = axes[i]
    ax.plot(time_axis, epoch[channel_idx, :], linewidth=0.5, color='blue')
    ax.set_xlabel('Czas [s]')
    ax.set_ylabel('Amplituda [mV]')
    ax.set_title(f'Epoka {i+1} - Kanał {channel_idx+1} ({channel_name})')
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 30])

# Ukryj puste subploty
for i in range(n_epochs, len(axes)):
    axes[i].set_visible(False)

plt.suptitle(f'Sygnał EEG - Wszystkie epoki - Kanał {channel_idx+1} ({channel_name})',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()