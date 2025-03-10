import streamlit as st
import pandas as pd
import os

# 📌 Słownik z kodami odpadu i odpowiadającymi im opisami
odpady_dict = {
    "": "",    
    "02 01 03": "Odpadowa masa roślinna",
    "03 01 04*": "Trociny, wióry, ścinki, drewno, płyta wiórowa i fornir zawierające substancje niebezpieczne",
    "03 01 05": "Trociny, wióry, ścinki, drewno, płyta wiórowa i fornir niezawierajacy substancji niebezpiecznych",
    "07 04 80*": "Przeterminowane środki ochrony roślin zawierające substancje niebezpieczne",
    "07 04 81": "Przeterminowane środki ochrony roślin inne niż wymienione w 07 04 80",
    "08 01 11*": "Odpady farb i lakierów zawierających rozpuszczalniki organiczne lub inne substancje niebezpieczne",
    "08 01 12": "Odpady farb i lakierów inne niż wymienione w 08 01 11",
    "08 03 17*": "Odpadowy toner drukarski zawierający substancje niebezpieczne",
    "08 03 18": "Odpadowy toner drukarski niezawierajacy substancji niebezpiecznych",
    "08 04 09*": "Odpadowe kleje i szczeliwa zawierające rozpuszczalniki organiczne lub inne substancje niebezpieczne",
    "08 04 10": "Odpadowe kleje i szczeliwa inne niż wymienione w 08 04 09",
    "08 03 99": "Inne nie wymienione odpady",
    "13 01 10*": "Mineralne oleje hydrauliczne niezawierające związków chlorowcoorganicznych",
    "13 01 11*": "Syntetyczne oleje hydrauliczne",
    "13 01 13*": "Inne oleje hydrauliczne",
    "13 02 08*": "Inne oleje silnikowe, przekładniowe i smarowe",
    "13 07 01*": "Olej opałowy i olej napędowy",
    "13 07 02*": "Benzyna",
    "13 07 03*": "Inne paliwa (włącznie z mieszaninami)",
    "15 01 01": "Opakowania z papieru i tektury",
    "15 01 02": "Opakowania z tworzyw sztucznych",
    "15 01 03": "Opakowania z drewna",
    "15 01 04": "Opakowania z metali",
    "15 01 05": "Opakowania wielomateriałowe",
    "15 01 06": "Zmieszane odpady opakowaniowe",
    "15 01 07": "Opakowania ze szkła",
    "15 01 10*": "Opakowania zawierające pozostałości substancji niebezpiecznych lub nimi zanieczyszczone",
    "15 01 11*": "Opakowania z metali zawierające niebezpieczne porowate elementy wzmocnienia konstrukcyjnego",
    "15 02 02*": "Sorbenty, materiały filtracyjne zawierające substancje niebezpieczne",
    "15 02 03": "Sorbenty, materiały filtracyjne inne niż wymienione",
    "16 01 03": "Zużyte opony",
    "16 02 11*": "Zużyte urządzenia zawierające freony",
    "16 02 13*": "Zużyte urządzenia zawierające niebezpieczne elementy",
    "16 02 14": "Zużyte urządzenia inne niż wymienione",
    "16 02 15*": "Niebezpieczne elementy usunięte ze zużytych urządzeń",
    "16 03 03*": "Nieorganiczne odpady zawierające substancje niebezpieczne",
    "16 03 04": "Nieorganiczne odpady niezawierajace substancji niebezpiecznych",
    "16 03 05*": "Organiczne odpady zawierajace substancje niebezpieczne",
    "16 06 01*": "Baterie ołowiowe",
    "16 06 02*": "Baterie niklowo-kadmowe",
    "17 01 01": "Odpady betonu oraz gruz",
    "17 01 07": "Zmieszane odpady betonu, gruzu",
    "20 01 01": "Papier i tektura",
    "20 01 02": "Szkło",
    "20 01 08": "Odpady kuchenne ulegające biodegradacji",
    "20 01 39": "Metale i tworzywa sztuczne",
    "20 01 21*": "Lampy fluorescencyjne zawierające rtęć",
}

# 📌 Nagłówek aplikacji
st.title("Tabela Odpadowa - Test")

# 📌 Inicjalizacja przechowywania danych w sesji
if "data" not in st.session_state:
    st.session_state.data = []

# 📌 Formularz do dodawania nowych danych
with st.form("form_danych", clear_on_submit=True):
    sklep = st.number_input("Numer sklepu", min_value=1, step=1, format="%d", value=None)
    data_odpadu = st.date_input("Data przekazania odpadu", key="data_odpadu", value=None)
    kod_odpadu = st.selectbox("Kod odpadu", options=[f"{kod} - {opis}" for kod, opis in odpady_dict.items()])
    
    wybrany_kod = kod_odpadu.split(" - ")[0]  
    opis_kodu = odpady_dict.get(wybrany_kod, "")
    
    masa_odpadu = st.number_input("Masa przekazanych odpadów [tony (Mg)]", min_value=0.0, value=None)  # Brak domyślnej wartości
    kwota_netto = st.number_input("Kwota netto [zł]", min_value=-500.0, value=None)  # Brak domyślnej wartości
    proces_odzysku = st.text_input("Proces odzysku lub unieszkodliwiania odpadów", value="")  # Puste pole tekstowe
    ilosc_pojemnikow = st.number_input("Ilość pojemników", min_value=0, value=None)  # Brak domyślnej wartości
    pojemnosc_pojemnikow = st.number_input("Pojemność pojemników [m3]", min_value=0.0, value=None)  # Brak domyślnej wartości
    odbiorca_odpadów = st.text_input("Odbiorca Odpadów", value="")  # Puste pole tekstowe
    
    submit = st.form_submit_button("Dodaj dane")

# 📌 Zapis nowego wpisu do sesji
if submit:
    new_row = {
        "Numer sklepu": sklep,
        "Data przekazania odpadu": str(data_odpadu),
        "Kod odpadu": wybrany_kod,
        "Opis kodu": opis_kodu,
        "Masa [Mg]": masa_odpadu,
        "Kwota netto [zł]": kwota_netto,
        "Proces odzysku": proces_odzysku,
    }
    st.session_state.data.append(new_row)
    st.success("Dane dodane!")

# 📌 Edytowalna tabela danych
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)  # Konwersja listy słowników na DataFrame
    
    # 📌 Edytowalna tabela
    edited_df = st.data_editor(df, key="editable_table", num_rows="dynamic")
    
    # 📌 Aktualizacja danych w sesji
    st.session_state.data = edited_df.to_dict("records")
    
    st.write("Możesz edytować dane  dopóki nie odświeżysz strony!")