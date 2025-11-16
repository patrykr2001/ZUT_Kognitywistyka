import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro, kruskal, f_oneway

# Wczytaj dane z pliku CSV
df = pd.read_csv('wyniki_przetworzone.csv')

# Konwersja odpowiedzi tekstowych na wartości numeryczne (skala Likerta)
odpowiedzi_mapping = {
    'Zdecydowanie bym tego nie zrobił/a': 1,
    'Raczej nie chciał(a)bym tak mieszkać': 2,
    'Nie mam zdania / Jest mi to obojętne': 3,
    'Chętnie bym tak umeblował/a mieszkanie': 4,
    'Zdecydowanie chciał(a)bym tak mieszkać': 5
}

df['wartość'] = df['odpowiedz'].map(odpowiedzi_mapping)

print("=" * 80)
print("ANALIZA STATYSTYCZNA DANYCH ANKIETOWYCH")
print("=" * 80)
print(f"\nLiczba respondentów: {df['user'].nunique()}")
print(f"Liczba kategorii: {df['kategoria'].nunique()}")
print(f"Kategorie: {', '.join(df['kategoria'].unique())}")
print(f"\nWszystkie odpowiedzi zakodowane numerycznie (1-5)")

# Oblicz średnie dla każdej kategorii
print("\n" + "=" * 80)
print("STATYSTYKI OPISOWE DLA KAŻDEJ KATEGORII")
print("=" * 80)

kategorie_stats = df.groupby('kategoria')['wartość'].agg(['mean', 'std', 'median', 'count'])
print(kategorie_stats)

# Przygotuj dane dla każdej kategorii do testów statystycznych
grupy = {}
for kategoria in df['kategoria'].unique():
    grupy[kategoria] = df[df['kategoria'] == kategoria]['wartość'].values

# Test normalności rozkładu (Shapiro-Wilk) dla każdej kategorii
print("\n" + "=" * 80)
print("TEST NORMALNOŚCI ROZKŁADU (Shapiro-Wilk)")
print("=" * 80)

normalnosc = {}
for kategoria, dane in grupy.items():
    stat, p_value = shapiro(dane)
    normalnosc[kategoria] = p_value > 0.05
    print(f"{kategoria:15} - p-value: {p_value:.4f} - ", end="")
    if p_value > 0.05:
        print("Rozkład NORMALNY ✓")
    else:
        print("Rozkład NIE-NORMALNY ✗")

# Sprawdź czy wszystkie grupy mają rozkład normalny
wszystkie_normalne = all(normalnosc.values())

print("\n" + "=" * 80)
if wszystkie_normalne:
    print("TEST STATYSTYCZNY: ANOVA (wszystkie rozkłady normalne)")
else:
    print("TEST STATYSTYCZNY: Kruskal-Wallis (co najmniej jeden rozkład nie-normalny)")
print("=" * 80)

# Wykonaj odpowiedni test statystyczny
if wszystkie_normalne:
    # Test ANOVA
    stat, p_value = f_oneway(*grupy.values())
    test_name = "ANOVA"
else:
    # Test Kruskal-Wallis
    stat, p_value = kruskal(*grupy.values())
    test_name = "Kruskal-Wallis"

print(f"\n{test_name}:")
print(f"Statystyka testowa: {stat:.4f}")
print(f"P-value: {p_value:.4f}")
print(f"\nWynik: ", end="")
if p_value < 0.2:
    print("Istnieją ISTOTNE STATYSTYCZNIE różnice między kategoriami (p < 0.2)")
else:
    print("BRAK istotnych statystycznie różnic między kategoriami (p >= 0.2)")

# Wizualizacja wyników
print("\n" + "=" * 80)
print("TWORZENIE WYKRESÓW")
print("=" * 80)

# Utwórz figurę z czterema wykresami
fig = plt.figure(figsize=(16, 10))
fig.suptitle('Analiza Statystyczna Preferencji Stylu Mieszkania', fontsize=16, fontweight='bold')
gs = fig.add_gridspec(2, 2, hspace=0.4, wspace=0.3)

# Wykres 1: Wykres słupkowy średnich
ax1 = fig.add_subplot(gs[0, 0])
kategorie_stats['mean'].plot(kind='bar', ax=ax1, color='skyblue', edgecolor='black')
ax1.set_title('Średnie oceny dla każdej kategorii')
ax1.set_xlabel('Kategoria stylu')
ax1.set_ylabel('Średnia ocena (1-5)')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
ax1.axhline(y=3, color='red', linestyle='--', alpha=0.5, label='Neutralna (3)')
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# Kolory dla każdej kategorii
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
kategorie_lista = list(df['kategoria'].unique())

# Wykres 2: Heatmapa - procentowy rozkład odpowiedzi
ax2 = fig.add_subplot(gs[0, 1])
# Utwórz macierz odpowiedzi (kategoria x ocena)
heatmap_data = pd.crosstab(df['kategoria'], df['wartość'], normalize='index') * 100
sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax2, cbar_kws={'label': 'Procent [%]'})
ax2.set_title('Rozkład procentowy odpowiedzi')
ax2.set_xlabel('Ocena')
ax2.set_ylabel('Kategoria')

# Wykres 3: Wykres skumulowany pokazujący rozkład pozytywnych/negatywnych opinii
ax3 = fig.add_subplot(gs[1, 0])
# Oblicz procent dla każdej oceny w każdej kategorii
sentiment_data = []
for kategoria in kategorie_lista:
    dane_kat = df[df['kategoria'] == kategoria]['wartość']
    negatywne = (dane_kat <= 2).sum() / len(dane_kat) * 100
    neutralne = (dane_kat == 3).sum() / len(dane_kat) * 100
    pozytywne = (dane_kat >= 4).sum() / len(dane_kat) * 100
    sentiment_data.append([negatywne, neutralne, pozytywne])

sentiment_df = pd.DataFrame(sentiment_data, 
                           columns=['Negatywne (1-2)', 'Neutralne (3)', 'Pozytywne (4-5)'],
                           index=kategorie_lista)

sentiment_df.plot(kind='bar', stacked=True, ax=ax3, 
                 color=['#FF6B6B', '#FFD93D', '#6BCF7F'], edgecolor='black')
ax3.set_title('Rozkład sentymentu odpowiedzi')
ax3.set_xlabel('Kategoria stylu')
ax3.set_ylabel('Procent odpowiedzi [%]')
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha='right')
ax3.legend(loc='upper left', bbox_to_anchor=(1, 1))
ax3.grid(axis='y', alpha=0.3)

# Wykres 4: Multiple Comparison (podobny do MATLAB multcompare)
# Pokazuje średnie z przedziałami ufności dla każdej kategorii
ax4 = fig.add_subplot(gs[1, 1])

from scipy import stats

# Oblicz średnie i przedziały ufności (95%) dla każdej kategorii
means = []
ci_lower = []
ci_upper = []
categories_for_plot = []

for kategoria in kategorie_lista:
    dane = grupy[kategoria]
    mean = np.mean(dane)
    sem = stats.sem(dane)  # Standard Error of Mean
    ci = stats.t.interval(0.95, len(dane)-1, loc=mean, scale=sem)
    
    means.append(mean)
    ci_lower.append(ci[0])
    ci_upper.append(ci[1])
    categories_for_plot.append(kategoria)

# Rysuj wykres z przedziałami ufności
y_positions = np.arange(len(categories_for_plot))

for i, (cat, mean, lower, upper) in enumerate(zip(categories_for_plot, means, ci_lower, ci_upper)):
    # Rysuj przedział ufności jako linię
    ax4.plot([lower, upper], [i, i], 'o-', linewidth=2.5, markersize=8, 
             color=colors[i], label=cat, alpha=0.8)
    # Rysuj średnią jako większy punkt
    ax4.plot(mean, i, 'D', markersize=10, color=colors[i], 
             markeredgecolor='black', markeredgewidth=1.5)
    
    # Dodaj wartości liczbowe
    ax4.text(upper + 0.1, i, f'{mean:.2f}', va='center', fontsize=9, fontweight='bold')

ax4.set_yticks(y_positions)
ax4.set_yticklabels(categories_for_plot)
ax4.set_xlabel('Średnia ocena z 95% przedziałem ufności', fontsize=11)
ax4.set_ylabel('Kategoria', fontsize=11)
ax4.set_title('Multiple Comparison - Porównanie średnich z przedziałami ufności (95% CI)', 
              fontsize=12, fontweight='bold')
ax4.grid(axis='x', alpha=0.3, linestyle='--')
ax4.axvline(x=3, color='red', linestyle='--', alpha=0.5, linewidth=1.5, label='Neutralna (3)')
ax4.set_xlim(0.5, 5.5)
ax4.invert_yaxis()  # Odwróć oś Y dla lepszej czytelności
ax4.legend(loc='lower right', fontsize=9)

plt.tight_layout()
plt.savefig('analiza_statystyczna.png', dpi=300, bbox_inches='tight')
print("Wykres zapisany jako 'analiza_statystyczna.png'")

plt.show()

print("\n" + "=" * 80)
print("ANALIZA ZAKOŃCZONA")
print("=" * 80)