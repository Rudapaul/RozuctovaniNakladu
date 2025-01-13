import streamlit as st
from fpdf import FPDF
import pandas as pd  # Knihovna pro načítání dat z Excelu

# Funkce pro načtení Excel souboru
def nacti_data_z_excelu():
    uploaded_file = st.file_uploader("Nahrajte Excel soubor s údaji o bytech:", type=["xlsx"])
    if uploaded_file is not None:
        data = pd.read_excel(uploaded_file)
        return data
    return None

# Funkce pro výpočet nákladů
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
        pdf.cell(200, 10, txt="---", ln=True)
    
    pdf.output(nazev)

# Streamlit UI
st.title("Rozúčtování nákladů na vytápění a vodu podle legislativy")

# Načítání dat z Excelu
data = nacti_data_z_excelu()
if data is not None:
    st.write("Načtená data z Excelu:")
    st.dataframe(data)
else:
    st.header("Zadejte údaje manuálně")

    # Údaje o objektu
    st.header("Údaje o objektu")
    adresa_objektu = st.text_input("Adresa objektu:")
    mesto_objektu = st.text_input("Město:")
    psc_objektu = st.text_input("PSČ:")

    # Údaje o bytech
    st.header("Údaje o bytech")
    pocet_bytu = st.number_input("Počet bytů:", min_value=1, step=1)

    velikosti_bytu = []
    spotreby_tepla = []
    spotreby_studene_vody = []
    spotreby_teple_vody = []
    jmena_odberatelu = []
    cisla_vodomeru_sv = []
    cisla_vodomeru_tv = []
    cisla_indikatoru = []
    typy_radiatoru = []
    velikosti_radiatoru = []
    polohy_bytu = []

    for i in range(int(pocet_bytu)):
        st.subheader(f"Byt {i+1}")
        velikost = st.number_input(f"Velikost bytu {i+1} (m²):", min_value=0.0, key=f"velikost_{i}")
        spotreba_tepla = st.number_input(f"Spotřeba tepla bytu {i+1} (dílky):", min_value=0.0, key=f"spotreba_tepla_{i}")
        spotreba_studene_vody = st.number_input(f"Spotřeba studené vody bytu {i+1} (m³):", min_value=0.0, key=f"spotreba_studena_{i}")
        spotreba_teple_vody = st.number_input(f"Spotřeba teplé vody bytu {i+1} (m³):", min_value=0.0, key=f"spotreba_tepla_{i}")
        jmeno_odberatele = st.text_input(f"Jméno odběratele pro byt {i+1}:", key=f"jmeno_{i}")
        cislo_vodomeru_sv = st.text_input(f"Číslo vodoměru pro studenou vodu (byt {i+1}):", key=f"vodomer_sv_{i}")
        cislo_vodomeru_tv = st.text_input(f"Číslo vodoměru pro teplou vodu (byt {i+1}):", key=f"vodomer_tv_{i}")
        cislo_indikatoru = st.text_input(f"Číslo indikátoru na radiátoru (byt {i+1}):", key=f"indikator_{i}")
        typ_radiatoru = st.text_input(f"Typ radiátoru v bytě {i+1}:", key=f"typ_radiatoru_{i}")
        velikost_radiatoru = st.text_input(f"Velikost radiátoru v bytě {i+1}:", key=f"velikost_radiatoru_{i}")
        poloha_bytu = st.text_input(f"Poloha bytu {i+1}:", key=f"poloha_bytu_{i}")

        velikosti_bytu.append(velikost)
        spotreby_tepla.append(spotreba_tepla)
        spotreby_studene_vody.append(spotreba_studene_vody)
        spotreby_teple_vody.append(spotreba_teple_vody)
        jmena_odberatelu.append(jmeno_odberatele)
        cisla_vodomeru_sv.append(cislo_vodomeru_sv)
        cisla_vodomeru_tv.append(cislo_vodomeru_tv)
        cisla_indikatoru.append(cislo_indikatoru)
        typy_radiatoru.append(typ_radiatoru)
        velikosti_radiatoru.append(velikost_radiatoru)
        polohy_bytu.append(poloha_bytu)

# Výpočet a PDF generování
if st.button("Vypočítat rozúčtování"):
    st.success("Výpočet dokončen. Generování PDF...")