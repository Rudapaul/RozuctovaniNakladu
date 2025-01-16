from fpdf import FPDF

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

    def pridat_byt(self, byt, odečty_tepla, odečty_vody):
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

# Přidání české podpory (font s podporou UTF-8)
PDF_FONT_PATH = "DejaVuSans.ttf"  # Stáhněte font DejaVuSans.ttf a umístěte jej do pracovního adresáře

class CZProtokolPDF(ProtokolPDF):
    def __init__(self, hlavni_data):
        super().__init__(hlavni_data)
        self.add_font("DejaVu", "", PDF_FONT_PATH, uni=True)

    def header(self):
        self.set_font("DejaVu", size=12)
        self.cell(0, 10, "Protokol o ročním rozúčtování nákladů", border=0, ln=1, align="C")
        self.ln(10)

    def pridat_hlavni_data(self):
        self.add_page()
        self.set_font("DejaVu", size=10)
        self.cell(0, 10, "Hlavní údaje o objektu:", ln=1)
        for klic, hodnota in self.hlavni_data.items():
            self.cell(0, 10, f"{klic}: {hodnota}", ln=1)
        self.ln(10)

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

# Data o bytech (zkráceně)
byty = [
    {"Číslo bytu": 1, "Poloha": "4P/L", "Příjmení": "Ilona", "Plocha m2": 93},
    {"Číslo bytu": 2, "Poloha": "PK/L", "Příjmení": "Brada", "Plocha m2": 39},
    # Další byty...
]

odečty_tepla = [
    {"Číslo bytu": 1, "Typ a velikost radiátoru": "22/500x1000", "VČ-radio": 33834458, "Typ média": "HCA", "Aktuální hodnota": 1048},
    {"Číslo bytu": 2, "Typ a velikost radiátoru": "22/600x1000", "VČ-radio": 33834487, "Typ média": "HCA", "Aktuální hodnota": 415},
    # Další odečty...
]

odečty_vody = [
    {"Číslo bytu": 1, "VČ vodoměru": 33834458, "Typ média": "TV", "Objem m3": 58.245},
    {"Číslo bytu": 1, "VČ vodoměru": 33834458, "Typ média": "SV", "Objem m3": 63.587},
    # Další odečty...
]

# Generování PDF
pdf = CZProtokolPDF(hlavni_data)
pdf.pridat_hlavni_data()

for byt in byty:
    pdf.pridat_byt(byt, odečty_tepla, odečty_vody)

# Uložení PDF
pdf.output("roční_protokoly.pdf")