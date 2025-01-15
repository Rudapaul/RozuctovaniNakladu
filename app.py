import streamlit as st
import pandas as pd

# Funkce pro načtení Excel souboru
def load_excel(file):
    data = {}
    with pd.ExcelFile(file) as xls:
        data['Odečty teplo'] = pd.read_excel(xls, sheet_name='Odečty teplo')
        data['Odečty voda'] = pd.read_excel(xls, sheet_name='Odečty voda')
        data['Celkový soupis'] = pd.read_excel(xls, sheet_name='Celkový soupis')
        if 'Hlavní data' in xls.sheet_names:
            data['Hlavní data'] = pd.read_excel(xls, sheet_name='Hlavní data')
    return data

# Funkce pro spojení dat podle čísla bytu
def merge_data(data):
    merged = pd.merge(data['Celkový soupis'], data['Odečty teplo'], how='left', left_on='Číslo bytu', right_on='Byt číslo')
    merged = pd.merge(merged, data['Odečty voda'], how='left', left_on='Číslo bytu', right_on='Byt')
    return merged

# Streamlit aplikace
st.title("Rozúčtování nákladů na vytápění a vodu")

# Načtení souboru
uploaded_file = st.file_uploader("Nahrajte Excel soubor s daty", type="xlsx")
if uploaded_file:
    try:
        # Načtení dat
        data = load_excel(uploaded_file)
        
        # Spojení dat
        merged_data = merge_data(data)
        
        # Výpis spojených dat
        st.subheader("Spojená data pro byty")
        st.dataframe(merged_data)
        
        # Možnost stažení spojených dat
        st.download_button(
            label="Stáhnout spojená data",
            data=merged_data.to_csv(index=False).encode('utf-8'),
            file_name='spojena_data.csv',
            mime='text/csv'
        )
    except Exception as e:
        st.error(f"Chyba při načítání souboru: {e}")

# Ukázka jednotlivých bytů
if uploaded_file:
    st.subheader("Podrobnosti jednotlivých bytů")
    for _, row in merged_data.iterrows():
        st.write(f"**Byt číslo {row['Číslo bytu']}**")
        st.write(f"Poloha: {row['Poloha']}")
        st.write(f"Velikost bytu: {row['Plocha m2']} m²")
        st.write(f"Jméno nájemníka: {row['Příjmení']}")
        st.write(f"Radiátory: {row['Typ a velikost radiátoru']}")
        st.write(f"Teplo - aktuální hodnota: {row['Aktuální hodnota']}")
        st.write(f"Vodoměry: {row['VČ-radio']} ({row['Objem m3']} m³)")
        st.write("---")