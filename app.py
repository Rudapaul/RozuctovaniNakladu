import streamlit as st
import pandas as pd
from fpdf import FPDF

# Hlavní nastavení aplikace
st.title("Rozúčtování nákladů na vytápění a vodu podle legislativy ČR")

# Hlavní data
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

# Zobrazení předvyplněných dat o bytech
st.header("Data o bytech")
data_byty = pd.DataFrame({
    "Číslo bytu": [1, 2, 3, 4, 5],
    "Poloha": ["4P/L", "PK/L", "PK/S", "PK/PO", "1P/PO"],
    "Jméno bytu": ["Ilona", "Brada", "Taras", "Natty", "Joga 1 patro"],
    "Velikost (m2)": [93, 39, 68, 56, 62],
    "Počet radiátorů": [4, 2, 3, 4, 3],
})
edited_byty = st.experimental_data_editor(data_byty, num_rows="dynamic")

# Zobrazení a úpravy odečtů tepla
st.header("Odečty tepla")
data_teplo = pd.DataFrame({
    "Číslo bytu": [1, 2, 3, 4, 5],
    "Typ a velikost radiátoru": ["22/500x1000", "22/600x1000", "22/600x600", "22/600x1000", "22/600x1200"],
    "VČ-radio": [33834458, 4957573, 4530926, 4957555, 33834455],
    "Aktuální hodnota": [1048, 415, 734, 497, 202],
})
edited_teplo = st.experimental_data_editor(data_teplo, num_rows="dynamic")

# Zobrazení a úpravy odečtů vody
st.header("Odečty vody")
data_voda = pd.DataFrame({
    "Číslo bytu": [1, 2, 3, 4, 5],
    "Typ média": ["TV", "SV", "TV", "SV", "TV"],
    "Objem (m3)": [58.245, 46.566, 31.926, 15.421, 3.148],
    "VČ vodoměru": [33834458, 4975034, 4530926, 4975637, 33834455],
})
edited_voda = st.experimental_data_editor(data_voda, num_rows="dynamic")

# Funkce pro vytvoření PDF protokolu
def vytvorit_pdf(data_byty, data_teplo, data_voda):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for _, row in data_byty.iterrows():
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Protokol o rozúčtování nákladů", ln=True, align="C")
        pdf.ln(10)

        # Informace o bytě
        pdf.cell(100, 10, txt=f"Číslo bytu: {row['Číslo bytu']}", ln=True)
        pdf.cell(100, 10, txt=f"Poloha: {row['Poloha']}", ln=True)
        pdf.cell(100, 10, txt=f"Jméno bytu: {row['Jméno bytu']}", ln=True)
        pdf.cell(100, 10, txt=f"Velikost (m²): {row['Velikost (m2)']}", ln=True)
        pdf.cell(100, 10, txt=f"Počet radiátorů: {row['Počet radiátorů']}", ln=True)
        pdf.ln(5)

        # Odečty tepla
        pdf.cell(100, 10, txt="Odečty tepla:", ln=True)
        teplo = data_teplo[data_teplo["Číslo bytu"] == row["Číslo bytu"]]
        for _, trow in teplo.iterrows():
            pdf.cell(100, 10, txt=f"  Radiátor: {trow['Typ a velikost radiátoru']}, Hodnota: {trow['Aktuální hodnota']}", ln=True)

        # Odečty vody
        pdf.ln(5)
        pdf.cell(100, 10, txt="Odečty vody:", ln=True)
        voda = data_voda[data_voda["Číslo bytu"] == row["Číslo bytu"]]
        for _, vrow in voda.iterrows():
            pdf.cell(100, 10, txt=f"  Vodoměr: {vrow['VČ vodoměru']}, Objem: {vrow['Objem (m3)']} m3", ln=True)

        pdf.ln(10)
        pdf.cell(200, 10, txt="------------------------------", ln=True, align="C")
        pdf.ln(10)

    return pdf

# Tlačítko pro export PDF
if st.button("Generovat PDF protokoly"):
    pdf = vytvorit_pdf(edited_byty, edited_teplo, edited_voda)
    pdf_file = "protokoly.pdf"
    pdf.output(pdf_file)
    st.success(f"PDF bylo úspěšně vytvořeno jako {pdf_file}.")
    with open(pdf_file, "rb") as f:
        st.download_button("Stáhnout PDF", f, file_name=pdf_file)