import streamlit as st
import sqlite3

# Připojení k SQLite databázi
conn = sqlite3.connect("rozuctovani.db")
cursor = conn.cursor()

# Vytvoření tabulek
cursor.execute("""
CREATE TABLE IF NOT EXISTS objekt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    adresa TEXT,
    mesto TEXT,
    psc TEXT,
    naklady_teplo REAL,
    naklady_tepla_voda REAL,
    naklady_studena_voda REAL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS byty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    poloha TEXT,
    velikost REAL,
    jmeno_najemnika TEXT,
    namerena_hodnota_tepla REAL,
    namerena_hodnota_tepla_cena REAL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS vodomery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    byt_id INTEGER,
    cislo TEXT,
    typ TEXT, -- "studená" nebo "teplá"
    mnozstvi REAL,
    cena REAL,
    FOREIGN KEY(byt_id) REFERENCES byty(id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS radiatory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    byt_id INTEGER,
    cislo_indikatoru TEXT,
    velikost TEXT,
    namerena_hodnota REAL,
    FOREIGN KEY(byt_id) REFERENCES byty(id)
)
""")
conn.commit()

# Funkce pro ukládání a načítání dat
def ulozit_objekt(adresa, mesto, psc, naklady_teplo, naklady_tepla_voda, naklady_studena_voda):
    cursor.execute("DELETE FROM objekt")  # Umožní přepsat hodnoty
    cursor.execute("""
    INSERT INTO objekt (adresa, mesto, psc, naklady_teplo, naklady_tepla_voda, naklady_studena_voda)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (adresa, mesto, psc, naklady_teplo, naklady_tepla_voda, naklady_studena_voda))
    conn.commit()

def nacti_objekt():
    cursor.execute("SELECT * FROM objekt")
    return cursor.fetchone()

def ulozit_byt(poloha, velikost, jmeno, namerena_teplo, cena_tepla):
    cursor.execute("""
    INSERT INTO byty (poloha, velikost, jmeno_najemnika, namerena_hodnota_tepla, namerena_hodnota_tepla_cena)
    VALUES (?, ?, ?, ?, ?)
    """, (poloha, velikost, jmeno, namerena_teplo, cena_tepla))
    conn.commit()
    return cursor.lastrowid

def ulozit_vodomer(byt_id, cislo, typ, mnozstvi, cena):
    cursor.execute("""
    INSERT INTO vodomery (byt_id, cislo, typ, mnozstvi, cena)
    VALUES (?, ?, ?, ?, ?)
    """, (byt_id, cislo, typ, mnozstvi, cena))
    conn.commit()

def ulozit_radiator(byt_id, cislo_indikatoru, velikost, namerena_hodnota):
    cursor.execute("""
    INSERT INTO radiatory (byt_id, cislo_indikatoru, velikost, namerena_hodnota)
    VALUES (?, ?, ?, ?)
    """, (byt_id, cislo_indikatoru, velikost, namerena_hodnota))
    conn.commit()

def nacti_byty():
    cursor.execute("SELECT * FROM byty")
    return cursor.fetchall()

def nacti_vodomery(byt_id):
    cursor.execute("SELECT * FROM vodomery WHERE byt_id = ?", (byt_id,))
    return cursor.fetchall()

def nacti_radiatory(byt_id):
    cursor.execute("SELECT * FROM radiatory WHERE byt_id = ?", (byt_id,))
    return cursor.fetchall()

# Výpočet nákladů na vytápění
def vypocitat_naklady_teplo(naklady_teplo, velikosti_bytu, namerene_hodnoty):
    zakladni_slozka = 0.4 * naklady_teplo
    spotrebni_slozka = 0.6 * naklady_teplo

    # Výpočet základní složky podle velikosti bytu
    soucet_velikosti = sum(velikosti_bytu)
    zakladni_naklady = [
        (velikost / soucet_velikosti) * zakladni_slozka for velikost in velikosti_bytu
    ]

    # Výpočet spotřební složky podle naměřených hodnot tepla
    soucet_hodnot = sum(namerene_hodnoty)
    spotrebni_naklady = [
        (hodnota / soucet_hodnot) * spotrebni_slozka for hodnota in namerene_hodnoty
    ]

    # Celkové náklady na teplo pro každý byt
    celkove_naklady = [
        round(zakladni + spotrebni, 2)
        for zakladni, spotrebni in zip(zakladni_naklady, spotrebni_naklady)
    ]

    return celkove_naklady

# Streamlit aplikace
st.title("Rozúčtování nákladů na vytápění a vodu")

# Formulář pro zadání údajů o objektu
st.header("Údaje o objektu")
ulozeny_objekt = nacti_objekt() or ("", "", "", 0.0, 0.0, 0.0)
adresa = st.text_input("Adresa objektu:", value=ulozeny_objekt[0])
mesto = st.text_input("Město:", value=ulozeny_objekt[1])
psc = st.text_input("PSČ:", value=ulozeny_objekt[2])
naklady_teplo = st.number_input("Celkové roční náklady na vytápění (Kč):", min_value=0.0, value=ulozeny_objekt[3])
naklady_tepla_voda = st.number_input("Celkové roční náklady na teplou vodu (Kč):", min_value=0.0, value=ulozeny_objekt[4])
naklady_studena_voda = st.number_input("Celkové roční náklady na studenou vodu (Kč):", min_value=0.0, value=ulozeny_objekt[5])

if st.button("Uložit údaje o objektu"):
    ulozit_objekt(adresa, mesto, psc, naklady_teplo, naklady_tepla_voda, naklady_studena_voda)
    st.success("Údaje o objektu byly uloženy!")

# Zadání dat pro byty
st.header("Přidat nový byt")
poloha = st.text_input("Poloha bytu:")
velikost = st.number_input("Velikost bytu (m²):", min_value=0.0)
jmeno = st.text_input("Jméno nájemníka:")
namerena_teplo = st.number_input("Naměřené hodnoty tepla (počet dílků):", min_value=0.0)
cena_tepla = 0  # Bude vypočítáno po rozdělení nákladů

# Uložení dat o bytě
if st.button("Uložit byt"):
    byt_id = ulozit_byt(poloha, velikost, jmeno, namerena_teplo, cena_tepla)
    st.success("Byt byl úspěšně uložen!")

# Zobrazení dat a výpočet nákladů
st.header("Výpočet a zobrazení uložených dat")
byty = nacti_byty()
velikosti = [byt[2] for byt in byty]
namerene_hodnoty = [byt[4] for byt in byty]

if byty:
    st.subheader("Náklady na vytápění")
    rozdeleni_tepla = vypocitat_naklady_teplo(naklady_teplo, velikosti, namerene_hodnoty)
    for byt, naklad in zip(byty, rozdeleni_tepla):
        st.write(f"Byt {byt[1]} ({byt[3]}): Náklady na teplo: {naklad} Kč")
else:
    st.write("Zatím nejsou uložena žádná data.")