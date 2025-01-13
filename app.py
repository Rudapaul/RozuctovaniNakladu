import streamlit as st
import pandas as pd
from fpdf import FPDF

# Titul aplikace
st.title("Rozúčtování nákladů na vytápění a vodu podle legislativy ČR")

# Sekce: Údaje o objektu
st.header("Údaje o objektu")
adresa_objektu = st.text_input("Adresa objektu:")
mesto = st.text_input("Město:")
psc = st.text_input("PSČ:")

# Sekce: Roční náklady
st.header("Roční náklady")
naklady_tepla_ut = st.number_input("Náklady na spotřebu tepla na ÚT (Kč):", min_value=0.0, step=100.0)
naklady_tepla_tv = st.number_input("Náklady na spotřebu tepla na výrobu TV (Kč):", min_value=0.0, step=100.0)
naklady_vody_tv = st.number_input("Náklady na spotřebu vody na výrobu TV (Kč):", min_value=0.0, step=100.0)
naklady_studena_voda = st.number_input("Náklady na spotřebu studené vody (Kč):", min_value=0.0, step=100.0)
naklady_celkem = naklady_tepla_ut + naklady_tepla_tv + naklady_vody_tv + naklady_studena_voda

# Sekce: Výpočetní údaje
st.header("Výpočetní údaje")
zakladni_slozka_ut = st.number_input("Základní složka - teplo na ÚT (Kč):", min_value=0.0, step=100.0)
zakladni_slozka_tv = st.number_input("Základní složka - teplo na výrobu TV (Kč):", min_value=0.0, step=100.0)
soucet_ploch_tv = st.number_input("Součet ploch pro výpočet TV v objektu (m²):", min_value=0.0, step=1.0)
soucet_itn = st.number_input("Součet odečtených náměrů ITN v objektu (dílky):", min_value=0.0, step=1.0)
soucet_sv = st.number_input("Součet odečtených náměrů SV v objektu (m³):", min_value=0.0, step=1.0)
zakladni_podil_teplo = st.slider("Poměr základní a spotřební složky (teplo):", min_value=0, max_value=100, value=40)
zakladni_podil_tv = st.slider("Poměr základní a spotřební složky (TV):", min_value=0, max_value=100, value=30)

# Sekce: Údaje o bytech
st.header("Údaje o bytech")
pocet_bytu = st.number_input("Počet bytů:", min_value=1, step=1)

# Uchovávání údajů o bytech
byty_data = []

# Sběr údajů o bytech
for i in range(int(pocet_bytu)):
    st.subheader(f"Byt {i+1}")
    velikost_bytu = st.number_input(f"Velikost bytu {i+1} (m²):", min_value=0.0, step=1.0, key=f"velikost_{i}")
    spotreba_tepla = st.number_input(f"Spotřeba tepla bytu {i+1} (dílky):", min_value=0.0, step=1.0, key=f"spotreba_tepla_{i}")
    spotreba_studene_vody = st.number_input(f"Spotřeba studené vody bytu {i+1} (m³):", min_value=0.0, step=1.0, key=f"spotreba_studene_{i}")
    spotreba_teple_vody = st.number_input(f"Spotřeba teplé vody bytu {i+1} (m³):", min_value=0.0, step=1.0, key=f"spotreba_teple_{i}")
    jmeno_odberatele = st.text_input(f"Jméno odběratele pro byt {i+1}:", key=f"jmeno_odberatele_{i}")
    cislo_vodomeru_sv = st.text_input(f"Číslo vodoměru pro studenou vodu (byt {i+1}):", key=f"vodomer_sv_{i}")
    cislo_vodomeru_tv = st.text_input(f"Číslo vodoměru pro teplou vodu (byt {i+1}):", key=f"vodomer_tv_{i}")
    poloha_bytu = st.text_input(f"Poloha bytu {i+1}:", key=f"poloha_bytu_{i}")
    
    # Dynamické zadání radiátorů
    pocet_radiatoru = st.number_input(f"Počet radiátorů v bytě {i+1}:", min_value=1, step=1, key=f"pocet_radiatoru_{i}")
    radiatory = []
    for r in range(int(pocet_radiatoru)):
        st.text(f"Radiátor {r+1} v bytě {i+1}:")
        cislo_indikatoru = st.text_input(f"Číslo indikátoru na radiátoru {r+1} (byt {i+1}):", key=f"indikator_{i}_{r}")
        typ_radiatoru = st.text_input(f"Typ radiátoru {r+1} (byt {i+1}):", key=f"typ_radiatoru_{i}_{r}")
        velikost_radiatoru = st.text_input(f"Velikost radiátoru {r+1} (byt {i+1}):", key=f"velikost_radiatoru_{i}_{r}")
        radiatory.append({
            "cislo_indikatoru": cislo_indikatoru,
            "typ_radiatoru": typ_radiatoru,
            "velikost_radiatoru": velikost_radiatoru
        })
    
    # Ukládání dat
    byty_data.append({
        "velikost_bytu": velikost_bytu,
        "spotreba_tepla": spotreba_tepla,
        "spotreba_studene_vody": spotreba_studene_vody,
        "spotreba_teple_vody": spotreba_teple_vody,
        "jmeno_odberatele": jmeno_odberatele,
        "cislo_vodomeru_sv": cislo_vodomeru_sv,
        "cislo_vodomeru_tv": cislo_vodomeru_tv,
        "poloha_bytu": poloha_bytu,
        "radiatory": radiatory
    })

# Výstup výsledků
if st.button("Vypočítat rozúčtování"):
    st.success("Výpočet dokončen. Data můžete nyní exportovat do PDF.")
    st.download_button("Stáhnout PDF", data="PDF Data Placeholder", file_name="rozuctovani.pdf")