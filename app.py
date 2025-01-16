import streamlit as st
import pandas as pd
from fpdf import FPDF

# Hlavní data
st.title("Rozúčtování nákladů na vytápění a vodu podle legislativy ČR")

hlavni_data = {
    "Adresa objektu": "Ve smečkách 592/22",
    "PSČ": "11000 Praha 1",
    "Náklady na spotřebu tepla na ÚT (Kč)": 719656,
    "Náklady na spotřebu tepla na výrobu TV (Kč)": 217326,
    "Náklady na spotřebu vody na výrobu TV (Kč)": 104108,
    "Náklady na spotřebu studené vody (Kč)": 249836,
    "Náklady celkem (Kč)": 1290926,
}
st.header("Hlavní data")
st.json(hlavni_data)

# Data o bytech
st.header("Data o bytech")
data_byty = pd.DataFrame({
    "Číslo bytu": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    "Poloha": [
        "4P/L", "PK/L", "PK/S", "PK/PO", "1P/PO", "3P/PO", "3P/PO", "3P/PO",
        "3P/L", "3P/L", "2P/S", "1P/S", "PR/L", "PR/PO", "2P/PO", "PR/PO", "4P/PO", "1P/PO"
    ],
    "Jméno bytu": [
        "Ilona", "Brada", "Taras", "Natty", "Jóga 1p do ulice", "Šatny 3p", "Jóga 3p malá",
        "Jóga 3p do ulice", "Jóga 3p velká", "Kancl 3p do ulice", "2 patro do ulice",
        "Studio", "Little Bali", "Kytky", "2 patro do zah.", "David", "Michal", "Babča"
    ],
    "Velikost (m2)": [93, 39, 68, 56, 62, 45, 73, 122, 303, 42, 166, 696, 343, 111, 116, 457, 128, 110],
    "Počet radiátorů": [4, 2, 3, 4, 3, 3, 4, 5, 7, 2, 4, 1, 2, 1, 3, 1, 1, 1],
})
st.write("Editovatelné údaje o bytech:")
response_byty = st.experimental_data_editor(data_byty, num_rows="dynamic")
st.write("Aktualizovaná data o bytech:")
st.dataframe(response_byty)

# Odečty tepla
st.header("Odečty tepla")
data_tepla = pd.DataFrame({
    "Číslo bytu": [1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    "Typ a velikost radiátoru": [
        "22/500x1000", "22/500x1000", "22/600x1000", "22/600x600", "22/600x1000",
        "22/600x1200", "22/600x1200", "22/600x1200", "22/600x1200", "22/600x1200",
        "22/600x1200", "1", "1", "1", "1", "1", "1", "1", "1"
    ],
    "VČ-radio": [
        33834458, 33834459, 33834487, 33834484, 33834480, 33834455, 33834452,
        33834440, 33834473, 33834444, 33834471, 70575313, 70590191, 7680617,
        4958549, 4957297, 4975044, 4975685
    ],
    "Typ média": ["HCA"] * 18,
    "Aktuální hodnota": [
        1048, 1811, 415, 734, 497, 202, 436, 581, 135, 0, 4, 11197, 5483, 2131, 4640, 18280, 5443, 4400
    ],
})
st.write("Editovatelné odečty tepla:")
response_tepla = st.experimental_data_editor(data_tepla, num_rows="dynamic")
st.write("Aktualizované odečty tepla:")
st.dataframe(response_tepla)

# Odečty vody
st.header("Odečty vody")
data_voda = pd.DataFrame({
    "Číslo bytu": [1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    "Typ média": ["TV", "SV", "TV", "SV", "TV", "SV", "TV", "SV", "TV", "SV", "TV", "SV", "TV", "SV", "TV", "SV", "TV", "SV", "TV"],
    "Objem (m3)": [
        58.245, 63.587, 28.369, 46.566, 11.568, 40.148, 1.143, 0, 0, 0, 0, 325,
        109.121, 25.258, 74.596, 79.563, 45.854, 56.214, 45.834
    ],
    "VČ-vodoměru": [
        33834458, 33834458, 4957573, 4975034, 4957555, 4957526, 33834440, 0, 0,
        0, 33834471, 42011624508, 4516031, 7680617, 7458621, 4957297, 4975044, 4975685
    ],
})
st.write("Editovatelné odečty vody:")
response_voda = st.experimental_data_editor(data_voda, num_rows="dynamic")
st.write("Aktualizované odečty vody:")
st.dataframe(response_voda)

# Funkce pro gener

Z důvodu délky textu byl kód přerušen. Doplním zbývající část funkce pro generování PDF a uzavření kódu:

```python
# Funkce pro generování PDF
def generovat_pdf(hlavni_data, byty, tepla, voda):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Rozúčtování nákladů na vytápění a vodu", ln=True, align="C")

    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Hlavní data:", ln=True)
    for key, value in hlavni_data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    pdf.cell(200, 10, txt="Data o bytech:", ln=True)
    for index, row in byty.iterrows():
        pdf.cell(200, 10, txt=f"{row.to_dict()}", ln=True)

    pdf.cell(200, 10, txt="Odečty tepla:", ln=True)
    for index, row in tepla.iterrows():
        pdf.cell(200, 10, txt=f"{row.to_dict()}", ln=True)

    pdf.cell(200, 10, txt="Odečty vody:", ln=True)
    for index, row in voda.iterrows():
        pdf.cell(200, 10, txt=f"{row.to_dict()}", ln=True)

    return pdf.output(dest="S").encode("latin1")

# Tlačítko pro generování PDF
if st.button("Generovat PDF"):
    pdf_content = generovat_pdf(hlavni_data, response_byty, response_tepla, response_voda)
    st.download_button(
        label="Stáhnout PDF",
        data=pdf_content,
        file_name="rozuctovani.pdf",
        mime="application/pdf",
