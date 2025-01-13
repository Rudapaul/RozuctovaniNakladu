import streamlit as st
from fpdf import FPDF

# Funkce pro výpočet nákladů
def vypocitat_naklady_vytapeni(celkove_naklady, velikosti_bytu, spotreby, zakladni_podil=40):
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

def vypocitat_naklady_tepla_voda(celkove_naklady, velikosti_bytu, spotreby, zakladni_podil=30):
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

def vypocitat_naklady_studena_voda(celkove_naklady, spotreby):
    soucet_spotreby = sum(spotreby)
    rozdeleni_nakladu = [
        round((spotreba / soucet_spotreby) * celkove_naklady, 2) for spotreba in spotreby
    ]
    return rozdeleni_nakladu

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

st.header("Zadejte roční náklady:")
celkove_naklady_vytapeni = st.number_input("Celkové roční náklady na vytápění (Kč):", min_value=0.0, step=100.0)
celkove_naklady_studena_voda = st.number_input("Celkové roční náklady na studenou vodu (Kč):", min_value=0.0, step=100.0)
celkove_naklady_tepla_voda = st.number_input("Celkové roční náklady na teplou vodu (Kč):", min_value=0.0, step=100.0)

pocet_bytu = st.number_input("Počet bytů:", min_value=1, step=1)

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
        # Výpočty nákladů
        naklady_teplo = vypocitat_naklady_vytapeni(celkove_naklady_vytapeni, velikosti_bytu, spotreby_tepla)
        naklady_studena_voda = vypocitat_naklady_studena_voda(celkove_naklady_studena_voda, spotreby_studene_vody)
        naklady_tepla_voda = vypocitat_naklady_tepla_voda(celkove_naklady_tepla_voda, velikosti_bytu, spotreby_teple_vody)

        st.header("Rozdělení nákladů:")
        data = {}
        for i in range(int(pocet_bytu)):
            st.write(f"Byt {i+1}:")
            st.write(f" - Náklady na vytápění: {naklady_teplo[i]} Kč")
            st.write(f" - Náklady na studenou vodu: {naklady_studena_voda[i]} Kč")
            st.write(f" - Náklady na teplou vodu: {naklady_tepla_voda[i]} Kč")
            st.write("---")

            data[f"Byt {i+1}"] = {
                "Náklady na vytápění": naklady_teplo[i],
                "Náklady na studenou vodu": naklady_studena_voda[i],
                "Náklady na teplou vodu": naklady_tepla_voda[i]
            }

        if st.button("Generovat PDF"):
            nazev_pdf = generovat_protokol(data)
            st.success(f"Protokol byl vygenerován: {nazev_pdf}")
    else:
        st.error("Ujistěte se, že jste zadali všechny údaje pro všechny byty.")
