import streamlit as st
import pandas as pd

# Hlavní nadpis aplikace
st.title("Rozúčtování nákladů na vytápění a vodu podle legislativy ČR")

# ----------------------------- Hlavní data -----------------------------
st.header("Hlavní data")
hlavni_data = {
    "Adresa": st.text_input("Adresa objektu", "Ve smečkách 592/22"),
    "PSČ": st.text_input("PSČ", "11000 Praha 1"),
    "Náklady na spotřebu tepla na ÚT (Kč)": st.number_input("Náklady na ÚT (Kč)", value=719656.0, step=1000.0),
    "Náklady na spotřebu tepla na výrobu TV (Kč)": st.number_input("Náklady na TV (Kč)", value=217326.0, step=1000.0),
    "Náklady na spotřebu vody na výrobu TV (Kč)": st.number_input("Náklady na vodu pro TV (Kč)", value=104108.0, step=1000.0),
    "Náklady na spotřebu studené vody (Kč)": st.number_input("Náklady na studenou vodu (Kč)", value=249836.0, step=1000.0),
    "Náklady celkem (Kč)": st.number_input("Celkové náklady (Kč)", value=1290926.0, step=1000.0),
}
st.write("**Hlavní data:**")
st.json(hlavni_data)

# ----------------------------- Data o bytech -----------------------------
st.header("Data o bytech")
pocet_bytu = st.number_input("Počet bytů", min_value=1, step=1, value=18)

data_byty = []
for i in range(int(pocet_bytu)):
    st.subheader(f"Byt {i + 1}")
    byt = {}
    byt["Číslo bytu"] = st.text_input(f"Číslo bytu {i + 1}", value=f"{i + 1}")
    byt["Poloha"] = st.text_input(f"Poloha bytu {i + 1}")
    byt["Jméno nájemníka"] = st.text_input(f"Jméno nájemníka {i + 1}")
    byt["Plocha (m2)"] = st.number_input(f"Plocha bytu {i + 1} (m²)", min_value=0.0, step=1.0)
    byt["Počet radiátorů"] = st.number_input(f"Počet radiátorů v bytě {i + 1}", min_value=1, step=1, value=1)
    data_byty.append(byt)

st.write("**Data o bytech:**")
st.dataframe(pd.DataFrame(data_byty))

# ----------------------------- Odečty tepla -----------------------------
st.header("Odečty tepla")
pocet_radiatoru = st.number_input("Počet odečtů tepla (radiátory)", min_value=1, step=1, value=50)

data_teplo = []
for i in range(int(pocet_radiatoru)):
    st.subheader(f"Odečet tepla {i + 1}")
    teplo = {}
    teplo["Číslo bytu"] = st.text_input(f"Číslo bytu (teplo) {i + 1}")
    teplo["Poloha"] = st.text_input(f"Poloha (teplo) {i + 1}")
    teplo["Plocha m2"] = st.number_input(f"Plocha m2 (teplo) {i + 1}", min_value=0.0, step=1.0)
    teplo["Typ a velikost radiátoru"] = st.text_input(f"Typ a velikost radiátoru {i + 1}")
    teplo["VČ-radio"] = st.text_input(f"VČ-radio {i + 1}")
    teplo["Typ média"] = st.text_input(f"Typ média {i + 1}")
    teplo["Aktuální hodnota"] = st.number_input(f"Aktuální hodnota {i + 1}", min_value=0.0, step=1.0)
    data_teplo.append(teplo)

st.write("**Odečty tepla:**")
st.dataframe(pd.DataFrame(data_teplo))

# ----------------------------- Odečty vody -----------------------------
st.header("Odečty vody")
pocet_vodomeru = st.number_input("Počet odečtů vody (vodoměry)", min_value=1, step=1, value=50)

data_voda = []
for i in range(int(pocet_vodomeru)):
    st.subheader(f"Odečet vody {i + 1}")
    voda = {}
    voda["Číslo bytu"] = st.text_input(f"Číslo bytu (voda) {i + 1}")
    voda["Poloha"] = st.text_input(f"Poloha (voda) {i + 1}")
    voda["Plocha m2"] = st.number_input(f"Plocha m2 (voda) {i + 1}", min_value=0.0, step=1.0)
    voda["VČ vodoměru"] = st.text_input(f"VČ vodoměru {i + 1}")
    voda["Typ média"] = st.text_input(f"Typ média {i + 1}")
    voda["Objem m3"] = st.number_input(f"Objem m3 {i + 1}", min_value=0.0, step=1.0)
    data_voda.append(voda)

st.write("**Odečty vody:**")
st.dataframe(pd.DataFrame(data_voda))

# ----------------------------- Export dat -----------------------------
st.header("Export dat")
if st.button("Exportovat všechna data do CSV"):
    vsechna_data = {
        "Hlavní data": pd.DataFrame([hlavni_data]),
        "Data o bytech": pd.DataFrame(data_byty),
        "Odečty tepla": pd.DataFrame(data_teplo),
        "Odečty vody": pd.DataFrame(data_voda),
    }
    for nazev, df in vsechna_data.items():
        st.download_button(
            label=f"Stáhnout {nazev} jako CSV",
            data=df.to_csv(index=False),
            file_name=f"{nazev.replace(' ', '_').lower()}.csv",
            mime="text/csv",
        )