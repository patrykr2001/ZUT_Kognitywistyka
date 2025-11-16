import pandas as pd
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

# Utwórz figurę z kilkoma wykresami
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Analiza Statystyczna Preferencji Stylu Mieszkania', fontsize=16, fontweight='bold')

# Wykres 1: Boxplot dla każdej kategorii
ax1 = axes[0, 0]
df.boxplot(column='wartość', by='kategoria', ax=ax1)
ax1.set_title('Rozkład ocen dla każdej kategorii')
ax1.set_xlabel('Kategoria stylu')
ax1.set_ylabel('Ocena (1-5)')
ax1.get_figure().suptitle('')  # Usuń domyślny tytuł

# Wykres 2: Wykres słupkowy średnich
ax2 = axes[0, 1]
kategorie_stats['mean'].plot(kind='bar', ax=ax2, color='skyblue', edgecolor='black')
ax2.set_title('Średnie oceny dla każdej kategorii')
ax2.set_xlabel('Kategoria stylu')
ax2.set_ylabel('Średnia ocena (1-5)')
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')
ax2.axhline(y=3, color='red', linestyle='--', alpha=0.5, label='Neutralna (3)')
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

# Wykres 3: Violin plot
ax3 = axes[1, 0]
df_sorted = df.sort_values('kategoria')
sns.violinplot(data=df_sorted, x='kategoria', y='wartość', ax=ax3, palette='Set2')
ax3.set_title('Rozkład gęstości ocen (Violin Plot)')
ax3.set_xlabel('Kategoria stylu')
ax3.set_ylabel('Ocena (1-5)')
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha='right')

# Wykres 4: Heatmapa średnich ocen per użytkownik
ax4 = axes[1, 1]
pivot_table = df.pivot_table(values='wartość', index='user', columns='kategoria', aggfunc='mean')
sns.heatmap(pivot_table, annot=True, fmt='.1f', cmap='RdYlGn', ax=ax4, 
            vmin=1, vmax=5, cbar_kws={'label': 'Średnia ocena'})
ax4.set_title('Mapa cieplna ocen (użytkownik x kategoria)')
ax4.set_xlabel('Kategoria stylu')
ax4.set_ylabel('ID użytkownika')

plt.tight_layout()
plt.savefig('analiza_statystyczna.png', dpi=300, bbox_inches='tight')
print("Wykres zapisany jako 'analiza_statystyczna.png'")

plt.show()

print("\n" + "=" * 80)
print("ANALIZA ZAKOŃCZONA")
print("=" * 80)