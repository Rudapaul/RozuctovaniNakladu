import pandas as pd
from fpdf import FPDF

# Hlavní údaje o objektu
hlavni_data = {
    "Adresa objektu": "Ve smečkách 592/22, 11000 Praha 1",
    "Náklady na spotřebu tepla na ÚT (Kč)": 719656,
    "Náklady na spotřebu tepla na výrobu TV (Kč)": 217326,
    "Náklady na spotřebu vody na výrobu TV (Kč)": 104108,
    "Náklady na spotřebu studené vody (Kč)": 249836,
    "Náklady celkem (Kč)": 1290926,
    "Teplo na ÚT (GJ)": 709.37,
    "Teplo na výrobu TV (GJ)": 214.22,
    "Voda na výrobu TV (m³)": 658,
    "Studená voda (m³)": 1579,
    "Měrný ukazatel nákladů na teplo pro ÚT (Kč/m²)": 237.43,
    "Měrná spotřeba tepla pro ÚT (GJ/m²)": 0.234
}

# Data o bytech
byty = [
    {"Číslo bytu": 1, "Poloha": "4P/L", "Příjmení": "Ilona", "Plocha m²": 93},
    {"Číslo bytu": 2, "Poloha": "PK/L", "Příjmení": "Brada", "Plocha m²": 39},
    {"Číslo bytu": 3, "Poloha": "PK/S", "Příjmení": "Taras", "Plocha m²": 68},
    {"Číslo bytu": 4, "Poloha": "PK/PO", "Příjmení": "Natty", "Plocha m²": 56},
    {"Číslo bytu": 5, "Poloha": "1P/PO", "Příjmení": "Joga 1 patro", "Plocha m²": 62},
    # ... Doplnit všechny byty až po č. 18 ...
]

# Odečty tepla
odečty_tepla = [
    {"Číslo bytu": 1, "Typ a velikost radiátoru": "22/500x1000", "VČ-radio": "33834458", "Typ média": "HCA", "Aktuální hodnota": 1048},
    # Doplnit další záznamy ...
]

# Odečty vody
odečty_vody = [
    {"Číslo bytu": 1, "VČ vodoměru": "33834458", "Typ média": "TV", "Objem m³": 58.245},
    {"Číslo bytu": 1, "VČ vodoměru": "33834458", "Typ média": "SV", "Objem m³": 63.587},
    # Doplnit další záznamy ...
]

# Výpočet nákladů pro byt
def vypocet_nakladu(byt, odečty_tepla, odečty_vody):
    teplo_základní = hlavní_data["Náklady na spotřebu tepla na ÚT (Kč)"] * 0.4
    teplo_spotřební = hlavní_data["Náklady na spotřebu tepla na ÚT (Kč)"] * 0.6
    voda_celkem = hlavní_data["Náklady na spotřebu studené vody (Kč)"]
    return {
        "Teplo základní složka (Kč)": round(teplo_základní, 2),
        "Teplo spotřební složka (Kč)": round(teplo_spotřební, 2),
        "Voda celkem (Kč)": round(voda_celkem, 2),
    }

# Třída pro tvorbu PDF protokolu
class ProtokolPDF(FPDF):
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
        for klíč, hodnota in hlavní_data.items():
            self.cell(0, 10, f"{klíč}: {hodnota}", ln=1)
        self.ln(10)

    def pridat_byt(self, byt, náklady, tepla, vody):
        self.add_page()
        self.set_font("Arial", size=10)
        self.cell(0, 10, f"Číslo bytu: {byt['Číslo bytu']}, Poloha: {byt['Poloha']}, Nájemník: {byt['Příjmení']}", ln=1)
        self.cell(0, 10, f"Plocha: {byt['Plocha m²']} m²", ln=1)
        self.ln(5)
        self.cell(0, 10, "Odečty tepla:", ln=1)
        for záznam in tepla:
            if záznam["Číslo bytu"] == byt["Číslo bytu"]:
                self.cell(0, 10, f"{záznam}", ln=1)
        self.ln(5)
        self.cell(0, 10, "Odečty vody:", ln=1)
        for záznam in vody:
            if záznam["Číslo bytu"] == byt["Číslo bytu"]:
                self.cell(0, 10, f"{záznam}", ln=1)
        self.ln(5)
        self.cell(0, 10, "Rekapitulace nákladů:", ln=1)
        for klíč, hodnota in náklady.items():
            self.cell(0, 10, f"{klíč}: {hodnota}", ln=1)

# Generování PDF
pdf = ProtokolPDF()
pdf.pridat_hlavni_data()

for byt in byty:
    náklady = vypocet_nakladu(byt, odečty_tepla, odečty_vody)
    pdf.pridat_byt(byt, náklady, odečty_tepla, odečty_vody)

# Uložení PDF
pdf.output("roční_protokoly.pdf")