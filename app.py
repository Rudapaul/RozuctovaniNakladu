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

# Funkce pro generování PDF
def generovat_protokol(data, nazev="protokol.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Protokol o rozúčtování nákladů", ln=True, align="C")

    for byt, hodnoty in data.items():
        pdf.cell(200, 10, txt=f"{byt}:", ln=True, align="L")
        for popis, hodnota in hodnoty.items():
            pdf.cell(200, 10, txt=f"  {popis}: {hodnota}", ln=True, align="L")
    pdf.output(nazev)
    return nazev

# Streamlit UI
st.title("Rozúčtování nákladů na vytápění a vodu podle legislativy")

# Vstupy pro náklady
st.header("Zadejte roční náklady:")
naklady_UT = st.number_input("Náklady na spotřebu tepla na ÚT (Kč):", min_value=0.0, step=100.0)
naklady_TV_teplo = st.number_input("Náklady na spotřebu tepla na výrobu TV (Kč):", min_value=0.0, step=100.0)
naklady_TV_voda = st.number_input("Náklady na spotřebu vody na výrobu TV (Kč):", min_value=0.0, step=100.0)
naklady_SV = st.number_input("Náklady na spotřebu studené vody (Kč):", min_value=0.0, step=100.0)

# Počet bytů
pocet_bytu = st.number_input("Počet bytů:", min_value=1, step=1)

# Data pro jednotlivé byty
velikosti_bytu = []
spotreby_tepla = []
spotreby_studene_vody = []
spotreby_teple_vody = []

for i in range(int(pocet_bytu)):
    st.subheader(f"Byt {i+1}")
    velikost = st.number_input(f"Velikost bytu {i+1} (m²):", min_value=0.0, step=1.0, key=f"velikost_{i}")
    spotreba_tepla = st.number_input(f"Spotřeba tepla bytu {i+1} (dílky):", min_value=0.0, step=1.0, key=f"spotreba_tepla_{i}")
    spotreba_studene_vody = st.number_input(f"Spotřeba studené vody bytu {i+1} (m³):", min_value=0.0, step=1.0, key=f"spotreba_studene_{i}")
    spotreba_teple_vody = st.number_input(f"Spotřeba teplé vody bytu {i+1} (m³):", min_value=0.0, step=1.0, key=f"spotreba_teple_{i}")
    
    velikosti_bytu.append(velikost)
    spotreby_tepla.append(spotreba_tepla)
    spotreby_studene_vody.append(spotreba_studene_vody)
    spotreby_teple_vody.append(spotreba_teple_vody)

if st.button("Vypočítat rozúčtování"):
    if (
        len(velikosti_bytu) == pocet_bytu 
        and len(spotreby_tepla) == pocet_bytu
        and len(spotreby_studene_vody) == pocet_bytu
        and len(spotreby_teple_vody) == pocet_bytu
    ):
        # Výpočty
        naklady_teplo_UT = vypocitat_naklady(naklady_UT, velikosti_bytu, spotreby_tepla, zakladni_podil=40)
        naklady_teplo_TV = vypocitat_naklady(naklady_TV_teplo, velikosti_bytu, spotreby_teple_vody, zakladni_podil=30)
        naklady_studena_voda = vypocitat_naklady(naklady_SV, velikosti_bytu, spotreby_studene_vody, zakladni_podil=50)
        naklady_voda_TV = vypocitat_naklady(naklady_TV_voda, velikosti_bytu, spotreby_teple_vody, zakladni_podil=30)

        # Výstupy
        st.header("Rozdělení nákladů:")
        data = {}
        for i in range(int(pocet_bytu)):
            st.write(f"Byt {i+1}:")
            st.write(f" - Náklady na teplo na ÚT: {naklady_teplo_UT[i]} Kč")
            st.write(f" - Náklady na teplo na výrobu TV: {naklady_teplo_TV[i]} Kč")
            st.write(f" - Náklady na studenou vodu: {naklady_studena_voda[i]} Kč")
            st.write(f" - Náklady na vodu pro výrobu TV: {naklady_voda_TV[i]} Kč")
            st.write("---")

            data[f"Byt {i+1}"] = {
                "Náklady na teplo na ÚT": naklady_teplo_UT[i],
                "Náklady na teplo na výrobu TV": naklady_teplo_TV[i],
                "Náklady na studenou vodu": naklady_studena_voda[i],
                "Náklady na vodu pro výrobu TV": naklady_voda_TV[i],
            }

        if st.button("Generovat PDF"):
            nazev_pdf = generovat_protokol(data)
            st.success(f"Protokol byl vygenerován: {nazev_pdf}")
    else:
        st.error("Ujistěte se, že jste zadali všechny údaje pro všechny byty.")