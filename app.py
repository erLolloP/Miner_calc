import streamlit as st
import numpy as np
import pandas as pd

# Function to calculate daily profits with corrected profit calculation
def calcola_profitti_giornalieri_corretto(cicli_accensione, giorni, costo_energia_per_kWh, potenza_kW, hash_rate, profit_per_TH_per_day, tempo_sincronizzazione, usura_hardware=False):
    profitti = []
    costi_energetici = []
    usura = 1 if usura_hardware else 1

    for giorno in range(giorni):
        ore_attive = cicli_accensione[giorno % len(cicli_accensione)]
        profit_per_day = (ore_attive - tempo_sincronizzazione) * hash_rate * profit_per_TH_per_day / 24 * usura
        costo_energetico = ore_attive * potenza_kW * costo_energia_per_kWh
        profitti.append(profit_per_day)
        costi_energetici.append(costo_energetico)

        if usura_hardware:
            usura -= 0.0001  # Simulate hardware wear and tear

    profitto_totale = sum(profitti)
    costo_energetico_totale = sum(costi_energetici)
    profitto_netto = profitto_totale - costo_energetico_totale

    return profitto_totale, costo_energetico_totale, profitto_netto

st.title('Simulazione Profitti Antminer')

# Input parameters
costo_energia_per_kWh = st.number_input('Costo dell\'energia (USD/kWh)', value=0.12)
potenza_kW = st.number_input('Potenza (kW)', value=3.25)
hash_rate = st.number_input('Hash Rate (TH/s)', value=110)
profit_per_TH_per_day = st.number_input('Profitto per TH/s al giorno (USD)', value=0.12)
tempo_sincronizzazione = st.number_input('Tempo di sincronizzazione (minuti)', value=10) / 60  # in ore
giorni = st.number_input('Numero di giorni', value=30)
usura_hardware = st.checkbox('Considerare usura hardware', value=False)

# Simulation scenarios
cicli_continui = [24] * giorni
cicli_8_16 = [8] * giorni
cicli_12_12 = [12] * giorni
cicli_16_8 = [16] * giorni

# Recalculate profits with corrected function
profitti_continui_corretto = calcola_profitti_giornalieri_corretto(cicli_continui, giorni, costo_energia_per_kWh, potenza_kW, hash_rate, profit_per_TH_per_day, tempo_sincronizzazione, usura_hardware)
profitti_8_16_corretto = calcola_profitti_giornalieri_corretto(cicli_8_16, giorni, costo_energia_per_kWh, potenza_kW, hash_rate, profit_per_TH_per_day, tempo_sincronizzazione, usura_hardware)
profitti_12_12_corretto = calcola_profitti_giornalieri_corretto(cicli_12_12, giorni, costo_energia_per_kWh, potenza_kW, hash_rate, profit_per_TH_per_day, tempo_sincronizzazione, usura_hardware)
profitti_16_8_corretto = calcola_profitti_giornalieri_corretto(cicli_16_8, giorni, costo_energia_per_kWh, potenza_kW, hash_rate, profit_per_TH_per_day, tempo_sincronizzazione, usura_hardware)

# Create a DataFrame to display the results
risultati_corretto = pd.DataFrame({
    'Scenario': ['Continua', '8 ore accensione / 16 ore spegnimento', '12 ore accensione / 12 ore spegnimento', '16 ore accensione / 8 ore spegnimento'],
    'Profitti Totali (USD)': [profitti_continui_corretto[0], profitti_8_16_corretto[0], profitti_12_12_corretto[0], profitti_16_8_corretto[0]],
    'Costi Energetici Totali (USD)': [profitti_continui_corretto[1], profitti_8_16_corretto[1], profitti_12_12_corretto[1], profitti_16_8_corretto[1]],
    'Profitti Netti (USD)': [profitti_continui_corretto[2], profitti_8_16_corretto[2], profitti_12_12_corretto[2], profitti_16_8_corretto[2]]
})

st.write(risultati_corretto)
