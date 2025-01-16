import streamlit as st

# Hlavní data o objektu
hlavni_data = {
    "Adresa": "Ve smečkách 592/22",
    "Město": "11000 Praha 1"
}

naklady = {
    "Náklady na spotřebu tepla na ÚT": ("719656 Kč", "Teplo na ÚT", "709,37 GJ", "1014,5 Kč/GJ"),
    "Náklady na spotřebu tepla na výrobu TV": ("217326 Kč", "Teplo na výrobu TV", "214,22 GJ", "1014,49 Kč/GJ"),
    "Náklady na spotřebu vody na výrobu TV": ("104108 Kč", "Voda na výrobu TV", "658 m³", "158,22 Kč/m³"),
    "Náklady na spotřebu studené vody": ("249836 Kč", "Studená voda", "1579 m³", "158,22 Kč/m³"),
    "Náklady celkem": ("1290926 Kč", "Měrný ukazatel nákladů na teplo pro ÚT", "-", "237,43 Kč/m²")
}

rozlozeni_nakladu = {
    "Základní složka - teplo na ÚT 40%": "287862 Kč",
    "Spotřební složka - teplo na ÚT 60%": "431794 Kč",
    "Základní složka - teplo na výrobu TV 30%": "65197,8 Kč",
    "Spotřební složka - teplo na výrobu TV 70%": "152128,2 Kč"
}

vypoctene_hodnoty = {
    "Součet ploch pro výpočet ÚT v objektu (m²)": "3031 m²",
    "Součet odečtených náměrů TV v objektu (m³)": "589 m³",
    "Součet přepočtených náměrů RTN v objektu": "70937",
    "Součet odečtených náměrů SV v objektu (m³)": "1468 m³"
}

jednotkove_ceny = {
    "Spotřební složka - teplo na ÚT /1 dílek/": "6,087 Kč/dílek",
    "Základní složka - teplo na ÚT /1 m²/": "94,97 Kč/m²",
    "Základní složka - teplo na TV /1 m²/": "21,51 Kč/m²",
    "Spotřební složka - teplo na TV /1 m³/": "258,28 Kč/m³",
    "Voda na výrobu TV /1 m³/": "176,75 Kč/m³",
    "Studená voda /1 m³/": "183,03 Kč/m³"
}

pomery = {
    "Poměr základní a spotřební složky (teplo)": "40:60",
    "Poměr základní a spotřební složky (TV)": "30:70"
}

# Streamlit aplikace
st.title("Rozúčtování nákladů na vytápění a vodu podle legislativy ČR")

# Hlavní data
st.header("Hlavní data")
for key, value in hlavni_data.items():
    st.write(f"**{key}:** {value}")

# Náklady
st.header("Náklady")
for key, value in naklady.items():
    st.write(f"**{key}:** {value[0]} ({value[1]}, {value[2]}, {value[3]})")

# Poměrové rozdělení
st.header("Poměrové rozdělení nákladů")
for key, value in rozlozeni_nakladu.items():
    st.write(f"**{key}:** {value}")

# Vypočtené hodnoty
st.header("Vypočtené hodnoty")
for key, value in vypoctene_hodnoty.items():
    st.write(f"**{key}:** {value}")

# Jednotkové ceny
st.header("Jednotkové ceny (vypočtené ze vstupních údajů)")
for key, value in jednotkove_ceny.items():
    st.write(f"**{key}:** {value}")

# Poměry
st.header("Poměry")
for key, value in pomery.items():
    st.write(f"**{key}:** {value}")
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