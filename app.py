import streamlit as st
import pandas as pd
import numpy as np

# Funkce pro načtení dat z Excelu
def nacti_data_excelu(soubor):
    try:
        excel_data = pd.ExcelFile(soubor)
        hlavni_data = pd.read_excel(excel_data, sheet_name="Hlavní data")
        odecty_teplo = pd.read_excel(excel_data, sheet_name="Odečty teplo")
        odecty_voda = pd.read_excel(excel_data, sheet_name="Odečty voda")
        celkovy_soupis = pd.read_excel(excel_data, sheet_name="Celkový soupis")
        return hlavni_data, odecty_teplo, odecty_voda, celkovy_soupis
    except Exception as e:
        st.error(f"Chyba při načítání dat z Excelu: {e}")
        return None, None, None, None

# Hlavní aplikace
st.title("Rozúčtování nákladů na vytápění a vodu podle legislativy ČR")

# Možnost nahrát Excel soubor
st.header("Nahrát Excel soubor s daty")
soubor = st.file_uploader("Nahrajte Excel soubor (.xlsx):", type=["xlsx"])

# Zpracování dat
if soubor:
    hlavni_data, odecty_teplo, odecty_voda, celkovy_soupis = nacti_data_excelu(soubor)
    if hlavni_data is not None:
        st.success("Data úspěšně načtena!")

        # Zobrazení dat z jednotlivých listů
        st.subheader("Hlavní data")
        st.write(hlavni_data)

        st.subheader("Odečty tepla")
        st.write(odecty_teplo)

        st.subheader("Odečty vody")
        st.write(odecty_voda)

        st.subheader("Celkový soupis")
        st.write(celkovy_soupis)

        # Sloučení dat podle čísla bytu
        st.header("Podrobnosti jednotlivých bytů")
        try:
            merged_data = celkovy_soupis.merge(
                odecty_teplo, on="Byt číslo", how="left"
            ).merge(odecty_voda, on="Byt číslo", how="left")

            # Zobrazení sloučených dat
            for _, row in merged_data.iterrows():
                st.subheader(f"Byt {row['Byt číslo']}")
                st.write(f"**Poloha:** {row['Poloha']}")
                st.write(f"**Velikost bytu:** {row['Plocha m2']} m²")
                st.write(f"**Jméno nájemníka:** {row['Příjmení']}")
                st.write(f"**Číslo vodoměru na studenou vodu:** {row['VČ-radio']}")
                st.write(f"**Číslo vodoměru na teplou vodu:** {row['VČ-mě']}")
                st.write(f"**Počet radiátorů:** {row['Počet radiátorů']}")
                st.write(f"**Typ a velikost radiátorů:** {row['Typ a velikost radiátoru']}")
                st.write(f"**Naměřené hodnoty tepla (dílky):** {row['Naměřená hodnota']}")

        except Exception as e:
            st.error(f"Chyba při slučování dat: {e}")

# Ruční zadávání dat
else:
    st.header("Ruční zadávání dat")
    st.write("Pokud nemáte Excel, můžete data zadat ručně.")

    # Hlavní údaje
    st.subheader("Údaje o objektu")
    adresa = st.text_input("Adresa objektu")
    mesto = st.text_input("Město")
    psc = st.text_input("PSČ")
    pocet_bytu = st.number_input("Počet bytů", min_value=1, step=1)

    # Data o bytech
    data_bytu = []
    for i in range(pocet_bytu):
        st.subheader(f"Byt {i + 1}")
        byt = {}
        byt["Poloha"] = st.text_input(f"Poloha bytu {i + 1}")
        byt["Velikost bytu (m²)"] = st.number_input(f"Velikost bytu {i + 1} (m²)", min_value=0.0, step=1.0)
        byt["Jméno nájemníka"] = st.text_input(f"Jméno nájemníka bytu {i + 1}")
        byt["Počet radiátorů"] = st.number_input(f"Počet radiátorů v bytě {i + 1}", min_value=1, step=1)
        data_bytu.append(byt)

    if st.button("Uložit data"):
        st.success("Data byla uložena.")
        st.write(data_bytu)