import streamlit as st
from fpdf import FPDF

# Hlavní data
hlavni_data = {
    "Adresa objektu": "Ve smečkách 592/22",
    "PSČ": "11000 Praha 1",
    "Náklady na spotřebu tepla na ÚT (Kč)": 719656,
    "Náklady na spotřebu tepla na výrobu TV (Kč)": 217326,
    "Náklady na spotřebu vody na výrobu TV (Kč)": 104108,
    "Náklady na spotřebu studené vody (Kč)": 249836,
    "Náklady celkem (Kč)": 1290926,
}

# Data o bytech
byty = [
    {"Číslo bytu": 1, "Poloha": "4P/L", "Příjmení": "Ilona", "Plocha m2": 93},
    {"Číslo bytu": 2, "Poloha": "PK/L", "Příjmení": "Brada", "Plocha m2": 39},
    {"Číslo bytu": 3, "Poloha": "PK/S", "Příjmení": "Taras", "Plocha m2": 68},
    {"Číslo bytu": 4, "Poloha": "PK/PO", "Příjmení": "Natty", "Plocha m2": 56},
    {"Číslo bytu": 5, "Poloha": "1P/PO", "Příjmení": "Joga 1 patro", "Plocha m2": 62},
    {"Číslo bytu": 6, "Poloha": "3P/PO", "Příjmení": "Šatny 3p", "Plocha m2": 45},
    {"Číslo bytu": 7, "Poloha": "3P/PO", "Příjmení": "Joga 3p do z.", "Plocha m2": 73},
    {"Číslo bytu": 8, "Poloha": "3P/PO", "Příjmení": "Joga 3p do ulice", "Plocha m2": 122},
    {"Číslo bytu": 9, "Poloha": "3P/L", "Příjmení": "Joga 3p velka", "Plocha m2": 303},
    {"Číslo bytu": 10, "Poloha": "3P/L", "Příjmení": "Kancl 3p na levo", "Plocha m2": 42},
    {"Číslo bytu": 11, "Poloha": "2P/S", "Příjmení": "2p do ulice", "Plocha m2": 166},
    {"Číslo bytu": 12, "Poloha": "1P/S", "Příjmení": "Studio", "Plocha m2": 696},
    {"Číslo bytu": 13, "Poloha": "PR/L", "Příjmení": "Little Bali", "Plocha m2": 343},
    {"Číslo bytu": 14, "Poloha": "PR/PO", "Příjmení": "Květinářství", "Plocha m2": 111},
    {"Číslo bytu": 15, "Poloha": "2P/PO", "Příjmení": "2patro do zah.", "Plocha m2": 116},
    {"Číslo bytu": 16, "Poloha": "PR/PO", "Příjmení": "David", "Plocha m2": 457},
    {"Číslo bytu": 17, "Poloha": "4P/PO", "Příjmení": "Michal", "Plocha m2": 128},
    {"Číslo bytu": 18, "Poloha": "1P/PO", "Příjmení": "Babča", "Plocha m2": 110},
]

# Odečty tepla
odečty_tepla = [
    {"Číslo bytu": 1, "Typ a velikost radiátoru": "22/500x1000", "VČ-radio": 33834458, "Typ média": "HCA", "Aktuální hodnota": 1048},
    {"Číslo bytu": 2, "Typ a velikost radiátoru": "22/600x1000", "VČ-radio": 33834487, "Typ média": "HCA", "Aktuální hodnota": 415},
    # Další odečty tepla zde...
]

# Odečty vody
odečty_vody = [
    {"Číslo bytu": 1, "VČ vodoměru": 33834458, "Typ média": "TV", "Objem m3": 58.245},
    {"Číslo bytu": 1, "VČ vodoměru": 33834458, "Typ média": "SV", "Objem m3": 63.587},
    # Další odečty vody zde...
]

# Třída pro generování PDF protokolů
class ProtokolPDF(FPDF):
    def __init__(self, hlavni_data):
        super().__init__()
        self.hlavni_data = hlavni_data

    def header(self):
        self.set_font("Arial", size=12)
        self.cell(0, 10, "Protokol o ročním rozúčtování nákladů", border=0, ln=1, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", size=8)
        self.cell(0, 10, f"Stránka {self.page_no()}", align="C")

    def pridat_hlavni_data(self):
        self.add_page()
        self.set_font("Arial", size=10)
        self.cell(0, 10, "Hlavní údaje o objektu:", ln=1)
        for klic, hodnota in self.hlavni_data.items():
            self.cell(0, 10, f"{klic}: {hodnota}", ln=1)
        self.ln(10)

    def pridat_byt(self, byt, náklady, odečty_tepla, odečty_vody):
        self.set_font("Arial", size=10)
        self.cell(0, 10, f"Byt č. {byt['Číslo bytu']} - {byt['Poloha']}", ln=1)
        self.cell(0, 10, f"Jméno nájemníka: {byt['Příjmení']}", ln=1)
        self.cell(0, 10, f"Plocha m2: {byt['Plocha m2']}", ln=1)
        self.ln(5)
        self.cell(0, 10, "Odečty tepla:", ln=1)
        for odecet in [o for o in odečty_tepla if o["Číslo bytu"] == byt["Číslo bytu"]]:
            self.cell(0, 10, f"  {odecet}", ln=1)
        self.ln(5)
        self.cell(0, 10, "Odečty vody:", ln=1)
        for odecet in [o for o in odečty_vody if o["Číslo bytu"] == byt["Číslo bytu"]]:
            self.cell(0, 10, f"  {odecet}", ln=1)
        self.ln(10)

# Generování PDF
pdf = ProtokolPDF(hlavni_data)
pdf.pridat_hlavni_data()

for byt in byty:
    náklady = {}  # Vypočítejte náklady zde
    pdf.pridat_byt(byt, náklady, odečty_tepla, odečty_vody)

# Uložení PDF
pdf.output("roční_protokoly.pdf")

st.success("Protokol byl vygenerován a uložen jako roční_protokoly.pdf")