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
st.write(hlavni_data)

# Data o bytech
st.header("Data o bytech")
data_byty = [
    {"Číslo bytu": 1, "Poloha": "4P/L", "Jméno bytu": "Ilona", "Plocha m2": 93},
    {"Číslo bytu": 2, "Poloha": "PK/L", "Jméno bytu": "Brada", "Plocha m2": 39},
    # Přidejte další byty podle potřeby...
]
df_byty = pd.DataFrame(data_byty)
edited_byty = st.experimental_data_editor(df_byty, num_rows="dynamic")

# Odečty tepla
st.header("Odečty tepla")
data_tepla = [
    {"Číslo bytu": 1, "Typ a velikost radiátoru": "22/500x1000", "VČ-radio": 33834458, "Typ média": "HCA", "Aktuální hodnota": 1048},
    {"Číslo bytu": 2, "Typ a velikost radiátoru": "22/600x1000", "VČ-radio": 33834487, "Typ média": "HCA", "Aktuální hodnota": 415},
    # Přidejte další odečty...
]
df_tepla = pd.DataFrame(data_tepla)
edited_tepla = st.experimental_data_editor(df_tepla, num_rows="dynamic")

# Odečty vody
st.header("Odečty vody")
data_vody = [
    {"Číslo bytu": 1, "VČ vodoměru": 33834458, "Typ média": "TV", "Objem m3": 58.245},
    {"Číslo bytu": 2, "VČ vodoměru": 4957573, "Typ média": "TV", "Objem m3": 28.369},
    # Přidejte další odečty...
]
df_vody = pd.DataFrame(data_vody)
edited_vody = st.experimental_data_editor(df_vody, num_rows="dynamic")

# Uložení dat
if st.button("Uložit data"):
    st.success("Data byla uložena.")
    st.write("Byty:")
    st.write(edited_byty)
    st.write("Odečty tepla:")
    st.write(edited_tepla)
    st.write("Odečty vody:")
    st.write(edited_vody)

# Generování PDF protokolu
st.header("Generování protokolu")
if st.button("Generovat PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Protokol o rozúčtování nákladů", ln=True, align="C")
    
    # Přidání hlavních dat
    pdf.cell(200, 10, txt="Hlavní data:", ln=True, align="L")
    for key, value in hlavni_data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True, align="L")
    
    # Přidání dat o bytech
    pdf.cell(200, 10, txt="Data o bytech:", ln=True, align="L")
    for _, row in edited_byty.iterrows():
        pdf.cell(200, 10, txt=f"Byt {row['Číslo bytu']} - {row['Jméno bytu']} ({row['Poloha']}): {row['Plocha m2']} m2", ln=True, align="L")
    
    # Přidání odečtů tepla
    pdf.cell(200, 10, txt="Odečty tepla:", ln=True, align="L")
    for _, row in edited_tepla.iterrows():
        pdf.cell(200, 10, txt=f"Byt {row['Číslo bytu']} - Radiátor {row['Typ a velikost radiátoru']} ({row['Typ média']}): {row['Aktuální hodnota']} jednotek", ln=True, align="L")
    
    # Přidání odečtů vody
    pdf.cell(200, 10, txt="Odečty vody:", ln=True, align="L")
    for _, row in edited_vody.iterrows():
        pdf.cell(200, 10, txt=f"Byt {row['Číslo bytu']} - Vodoměr {row['VČ vodoměru']} ({row['Typ média']}): {row['Objem m3']} m3", ln=True, align="L")
    
    # Uložení PDF
    pdf_file = "protokol.pdf"
    pdf.output(pdf_file)
    st.success(f"PDF protokol byl vytvořen: {pdf_file}")
    with open(pdf_file, "rb") as file:
        st.download_button("Stáhnout PDF", file, file_name=pdf_file)