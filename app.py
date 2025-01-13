import streamlit as st
from fpdf import FPDF

# Funkce pro výpočty
def vypocitat_naklady(celkove_naklady, velikosti_bytu, spotreby, zakladni_podil):
    zakladni_naklady = (zakladni_podil / 100) * celkove_naklady
    spotrebni_naklady = celkove_naklady - zakladni_naklady

    soucet_velikosti = sum(velikosti_bytu)
    soucet_spotreby = sum(spotreby)

    zakladni_naklady_rozdelene = [
        (velikost / soucet_velikosti) * zakladni_naklady for velikost in velikosti_bytu
    ]
    spotrebni_naklady_rozdelene = [
        (spotreba / soucet_spotreby) * spotrebni_naklady for spotreba in spotreby
    ]

    celkove_naklady_na_byt = [
        round(zakladni + spotrebni, 2)
        for zakladni, spotrebni in zip(zakladni_naklady_rozdelene, spotrebni_naklady_rozdelene)
    ]

    return celkove_naklady_na_byt

# Funkce pro generování PDF protokolu
def generovat_pdf(vystupy, nazev="rozcuctovani_protokol.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Protokol o rozúčtování nákladů", ln=True, align="C")

    for byt, data in vystupy.items():
        pdf.cell(200, 10, txt=f"{byt}:", ln=True, align="L")
        for popis, hodnota in data.items():
            pdf.cell(200, 10, txt=f"{popis}: {hodnota}", ln=True, align="L")
    pdf.output(nazev)

# Streamlit UI
st.title("Rozúčtování nákladů na vytápění a vodu podle legislativy")

# Vstupy
st.header("Zadejte údaje o objektu")
naklady_UT = st.number_input("Náklady na spotřebu tepla na ÚT (Kč):", min_value=0.0)
naklady_TV_teplo = st.number_input("Náklady na spotřebu tepla na výrobu TV (Kč):", min_value=0.0)
naklady_TV_voda = st.number_input("Náklady na spotřebu vody na výrobu TV (Kč):", min_value=0.0)
naklady_SV = st.number_input("Náklady na spotřebu studené vody (Kč):", min_value=0.0)
zakladni_slozka_UT = st.slider("Poměr základní složky (teplo na ÚT):", 0, 100, 40)
zakladni_slozka_TV = st.slider("Poměr základní složky (teplo na TV):", 0, 100, 30)

soucet_ploch_UT = st.number_input("Součet ploch pro výpočet ÚT (m²):", min_value=0.0)
soucet_ploch_TV = st.number_input("Součet ploch pro výpočet TV (m²):", min_value=0.0)
soucet_odectu_ITN = st.number_input("Součet odečtených náměrů ITN (dílky):", min_value=0.0)
soucet_odectu_SV = st.number_input("Součet odečtených náměrů SV (m³):", min_value=0.0)

# Data pro byty
st.header("Údaje o bytech")
pocet_bytu = st.number_input("Počet bytů:", min_value=1, step=1)
vystupy = {}

velikosti_bytu = []
spotreby_tepla = []
spotreby_studene_vody = []
spotreby_teple_vody = []

for i in range(int(pocet_bytu)):
    st.subheader(f"Byt {i+1}")
    velikost = st.number_input(f"Velikost bytu {i+1} (m²):", min_value=0.0, key=f"velikost_{i}")
    spotreba_tepla = st.number_input(f"Spotřeba tepla bytu {i+1} (dílky):", min_value=0.0, key=f"spotreba_tepla_{i}")
    spotreba_studene_vody = st.number_input(f"Spotřeba studené vody bytu {i+1} (m³):", min_value=0.0, key=f"spotreba_studena_{i}")
    spotreba_teple_vody = st.number_input(f"Spotřeba teplé vody bytu {i+1} (m³):", min_value=0.0, key=f"spotreba_tepla_{i}")

    velikosti_bytu.append(velikost)
    spotreby_tepla.append(spotreba_tepla)
    spotreby_studene_vody.append(spotreba_studene_vody)
    spotreby_teple_vody.append(spotreba_teple_vody)

# Výpočet a zobrazení výsledků
if st.button("Vypočítat rozúčtování"):
    if len(velikosti_bytu) == pocet_bytu:
        naklady_teplo = vypocitat_naklady(naklady_UT, velikosti_bytu, spotreby_tepla, zakladni_slozka_UT)
        naklady_tepla_voda = vypocitat_naklady(naklady_TV_teplo, velikosti_bytu, spotreby_teple_vody, zakladni_slozka_TV)
        naklady_studena_voda = vypocitat_naklady(naklady_SV, velikosti_bytu, spotreby_studene_vody, 0)

        for i in range(pocet_bytu):
            vystupy[f"Byt {i+1}"] = {
                "Náklady na teplo": naklady_teplo[i],
                "Náklady na teplou vodu": naklady_tepla_voda[i],
                "Náklady na studenou vodu": naklady_studena_voda[i]
            }

        st.write("Výsledky rozúčtování:")
        for byt, data in vystupy.items():
            st.write(byt)
            for popis, hodnota in data.items():
                st.write(f"{popis}: {hodnota} Kč")

        # Generování PDF
        pdf_nazev = generovat_pdf(vystupy)
        st.download_button("Stáhnout protokol", data=open(pdf_nazev, "rb").read(), file_name=pdf_nazev)
    else:
        st.error("Ujistěte se, že jste zadali všechny potřebné údaje.")