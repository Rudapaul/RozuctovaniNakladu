import streamlit as st
import pandas as pd
from fpdf import FPDF

# Hlavní data
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

# Data o bytech
st.header("Data o bytech")
data_byty = [
    {"Číslo bytu": 1, "Poloha": "4P/L", "Jméno bytu": "Ilona", "Plocha m2": 93},
    {"Číslo bytu": 2, "Poloha": "PK/L", "Jméno bytu": "Brada", "Plocha m2": 39},
    {"Číslo bytu": 3, "Poloha": "PK/S", "Jméno bytu": "Taras", "Plocha m2": 68},
    {"Číslo bytu": 4, "Poloha": "PK/PO", "Jméno bytu": "Natty", "Plocha m2": 56},
    {"Číslo bytu": 5, "Poloha": "1P/PO", "Jméno bytu": "Joga 1 patro", "Plocha m2": 62},
    {"Číslo bytu": 6, "Poloha": "3P/PO", "Jméno bytu": "Šatny 3p", "Plocha m2": 45},
    {"Číslo bytu": 7, "Poloha": "3P/PO", "Jméno bytu": "Joga 3p malá", "Plocha m2": 73},
    {"Číslo bytu": 8, "Poloha": "3P/PO", "Jméno bytu": "Joga 3p do ulice", "Plocha m2": 122},
    {"Číslo bytu": 9, "Poloha": "3P/L", "Jméno bytu": "Joga 3p velká", "Plocha m2": 303},
    {"Číslo bytu": 10, "Poloha": "3P/L", "Jméno bytu": "Kancl 3p do ulice", "Plocha m2": 42},
    {"Číslo bytu": 11, "Poloha": "2P/S", "Jméno bytu": "2 patro do ulice", "Plocha m2": 166},
    {"Číslo bytu": 12, "Poloha": "1P/S", "Jméno bytu": "Studio", "Plocha m2": 696},
    {"Číslo bytu": 13, "Poloha": "PR/L", "Jméno bytu": "Little Bali", "Plocha m2": 343},
    {"Číslo bytu": 14, "Poloha": "PR/PO", "Jméno bytu": "Kytky", "Plocha m2": 111},
    {"Číslo bytu": 15, "Poloha": "2P/PO", "Jméno bytu": "2 patro do zahrady", "Plocha m2": 116},
    {"Číslo bytu": 16, "Poloha": "PR/PO", "Jméno bytu": "David", "Plocha m2": 457},
    {"Číslo bytu": 17, "Poloha": "4P/PO", "Jméno bytu": "Michal", "Plocha m2": 128},
    {"Číslo bytu": 18, "Poloha": "1P/PO", "Jméno bytu": "Babča", "Plocha m2": 110},
]
df_byty = pd.DataFrame(data_byty)
st.table(df_byty)

# Odečty tepla
st.header("Odečty tepla")
data_tepla = [
    {"Číslo bytu": 1, "Typ a velikost radiátoru": "22/500x1000", "VČ-radio": 33834458, "Typ média": "HCA", "Aktuální hodnota": 1048},
    {"Číslo bytu": 2, "Typ a velikost radiátoru": "22/600x1000", "VČ-radio": 33834487, "Typ média": "HCA", "Aktuální hodnota": 415},
    # Vložte všechna data o radiátorech...
]
df_tepla = pd.DataFrame(data_tepla)
st.table(df_tepla)

# Odečty vody
st.header("Odečty vody")
data_vody = [
    {"Číslo bytu": 1, "VČ vodoměru": 33834458, "Typ média": "TV", "Objem m3": 58.245},
    {"Číslo bytu": 2, "VČ vodoměru": 4957573, "Typ média": "TV", "Objem m3": 28.369},
    # Vložte všechna data o vodoměrech...
]
df_vody = pd.DataFrame(data_vody)
st.table(df_vody)

# Generování PDF protokolu
st.header("Generování protokolu")
if st.button("Generovat PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Protokol o rozúčtování nákladů", ln=True, align="C")
    
    # Hlavní data
    pdf.cell(200, 10, txt="Hlavní data:", ln=True)
    for key, value in hlavni_data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    
    # Data o bytech
    pdf.cell(200, 10, txt="Data o bytech:", ln=True)
    for _, row in df_byty.iterrows():
        pdf.cell(200, 10, txt=f"Byt {row['Číslo bytu']} - {row['Jméno bytu']} ({row['Poloha']}): {row['Plocha m2']} m2", ln=True)
    
    # Odečty tepla
    pdf.cell(200, 10, txt="Odečty tepla:", ln=True)
    for _, row in df_tepla.iterrows():
        pdf.cell(200, 10, txt=f"Byt {row['Číslo bytu']} - Radiátor {row['Typ a velikost radiátoru']} ({row['Typ média']}): {row['Aktuální hodnota']} jednotek", ln=True)
    
    # Odečty vody
    pdf.cell(200, 10, txt="Odečty vody:", ln=True)
    for _, row in df_vody.iterrows():
        pdf.cell(200, 10, txt=f"Byt {row['Číslo bytu']} - Vodoměr {row['VČ vodoměru']} ({row['Typ média']}): {row['Objem m3']} m3", ln=True)
    
    # Uložení PDF
    pdf_file = "protokol.pdf"
    pdf.output(pdf_file)
    st.success(f"PDF protokol byl vytvořen: {pdf_file}")
    with open(pdf_file, "rb") as file:
        st.download_button("Stáhnout PDF", file, file_name=pdf_file)