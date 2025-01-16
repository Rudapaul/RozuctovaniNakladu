import streamlit as st
import pandas as pd

# ----------------------------- Hlavní data -----------------------------
st.title("Rozúčtování nákladů na vytápění a vodu podle legislativy ČR")
st.header("Hlavní data")

hlavni_data = {
    "Adresa objektu": "Ve smečkách 592/22",
    "PSČ": "11000 Praha 1",
    "Náklady na spotřebu tepla na ÚT (Kč)": 719656,
    "Náklady na spotřebu tepla na výrobu TV (Kč)": 217326,
    "Náklady na spotřebu vody na výrobu TV (Kč)": 104108,
    "Náklady na spotřebu studené vody (Kč)": 249836,
    "Náklady celkem (Kč)": 1290926,
}

st.json(hlavni_data)

# ----------------------------- Data o bytech -----------------------------
st.header("Data o bytech")
data_byty = [
    {"Číslo bytu": 1, "Poloha": "4P/L", "Jméno bytu": "Ilona", "Plocha (m2)": 93},
    {"Číslo bytu": 2, "Poloha": "PK/L", "Jméno bytu": "Brada", "Plocha (m2)": 39},
    {"Číslo bytu": 3, "Poloha": "PK/S", "Jméno bytu": "Taras", "Plocha (m2)": 68},
    {"Číslo bytu": 4, "Poloha": "PK/PO", "Jméno bytu": "Natty", "Plocha (m2)": 56},
    {"Číslo bytu": 5, "Poloha": "1P/PO", "Jméno bytu": "Jóga 1 patro", "Plocha (m2)": 62},
    {"Číslo bytu": 6, "Poloha": "3P/PO", "Jméno bytu": "Šatny 3p", "Plocha (m2)": 45},
    {"Číslo bytu": 7, "Poloha": "3P/PO", "Jméno bytu": "Jóga 3p malá", "Plocha (m2)": 73},
    {"Číslo bytu": 8, "Poloha": "3P/PO", "Jméno bytu": "Jóga 3p do ulice", "Plocha (m2)": 122},
    {"Číslo bytu": 9, "Poloha": "3P/L", "Jméno bytu": "Jóga 3p velká", "Plocha (m2)": 303},
    {"Číslo bytu": 10, "Poloha": "3P/L", "Jméno bytu": "Kancl 3p do ulice", "Plocha (m2)": 42},
    {"Číslo bytu": 11, "Poloha": "2P/S", "Jméno bytu": "2 patro do ulice", "Plocha (m2)": 166},
    {"Číslo bytu": 12, "Poloha": "1P/S", "Jméno bytu": "Studio", "Plocha (m2)": 696},
    {"Číslo bytu": 13, "Poloha": "PR/L", "Jméno bytu": "Little Bali", "Plocha (m2)": 343},
    {"Číslo bytu": 14, "Poloha": "PR/PO", "Jméno bytu": "Kytky", "Plocha (m2)": 111},
    {"Číslo bytu": 15, "Poloha": "2P/S", "Jméno bytu": "2 patro do zah.", "Plocha (m2)": 116},
    {"Číslo bytu": 16, "Poloha": "PR/PO", "Jméno bytu": "David", "Plocha (m2)": 457},
    {"Číslo bytu": 17, "Poloha": "4P/PO", "Jméno bytu": "Michal", "Plocha (m2)": 128},
    {"Číslo bytu": 18, "Poloha": "1P/PO", "Jméno bytu": "Babča", "Plocha (m2)": 110},
]

# Zobrazení a úprava dat v interaktivní tabulce
df_byty = pd.DataFrame(data_byty)
edited_byty = st.experimental_data_editor(df_byty, num_rows="dynamic")

# ----------------------------- Odečty tepla -----------------------------
st.header("Odečty tepla")
data_tepla = [
    {"Číslo bytu": 1, "Typ a velikost radiátoru": "22/500x1000", "VČ-radio": 33834458, "Typ média": "HCA", "Aktuální hodnota": 1048},
    {"Číslo bytu": 1, "Typ a velikost radiátoru": "22/500x1000", "VČ-radio": 33834459, "Typ média": "HCA", "Aktuální hodnota": 1811},
    # Další data...
]

df_tepla = pd.DataFrame(data_tepla)
edited_tepla = st.experimental_data_editor(df_tepla, num_rows="dynamic")

# ----------------------------- Odečty vody -----------------------------
st.header("Odečty vody")
data_voda = [
    {"Číslo bytu": 1, "Poloha": "4P/L", "Typ média": "TV", "Objem m3": 58.245, "VČ vodoměru": 33834458},
    {"Číslo bytu": 1, "Poloha": "4P/L", "Typ média": "SV", "Objem m3": 63.587, "VČ vodoměru": 33834458},
    # Další data...
]

df_voda = pd.DataFrame(data_voda)
edited_voda = st.experimental_data_editor(df_voda, num_rows="dynamic")

# ----------------------------- Generování protokolů -----------------------------
st.header("Generování protokolů")
for byt in edited_byty.to_dict(orient="records"):
    st.subheader(f"Protokol pro byt {byt['Číslo bytu']} - {byt['Jméno bytu']}")
    st.write(f"Poloha: {byt['Poloha']}")
    st.write(f"Plocha: {byt['Plocha (m2)']} m2")

    # Přidání údajů o teple
    tepla = edited_tepla[edited_tepla["Číslo bytu"] == byt["Číslo bytu"]]
    st.write("Odečty tepla:")
    st.table(tepla)

    # Přidání údajů o vodě
    voda = edited_voda[edited_voda["Číslo bytu"] == byt["Číslo bytu"]]
    st.write("Odečty vody:")
    st.table(voda)