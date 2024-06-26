# Let's perform an analysis of expected profit per kilowatt without considering the cost of energy and machine cost.
# We'll vary the Antminer models and the algorithms used.

import pandas as pd

# Defining some sample Antminer models with their respective power consumption (kW) and hash rate (TH/s) for different algorithms
antminers = {
    'Antminer S19': {'SHA-256': {'power_kW': 3.25, 'hash_rate': 95}},
    'Antminer S19 Pro': {'SHA-256': {'power_kW': 3.25, 'hash_rate': 110}},
    'Antminer S19j': {'SHA-256': {'power_kW': 3.1, 'hash_rate': 90}},
    'Antminer S17': {'SHA-256': {'power_kW': 2.92, 'hash_rate': 73}},
    'Antminer L7': {'Scrypt': {'power_kW': 3.42, 'hash_rate': 9.5}},
    'Antminer D7': {'X11': {'power_kW': 1.65, 'hash_rate': 1.3}},
}

# Defining a sample profit per TH/s per day for different algorithms
profit_per_ths_per_day = {
    'SHA-256': 0.12,  # USD per TH/s per day
    'Scrypt': 2.5,    # USD per GH/s per day
    'X11': 0.15       # USD per GH/s per day
}

# Calculating expected profit per kilowatt for each Antminer model and algorithm
data = []
for model, algos in antminers.items():
    for algo, specs in algos.items():
        power_kW = specs['power_kW']
        hash_rate = specs['hash_rate']
        profit_per_ths = profit_per_ths_per_day[algo]
        expected_profit_per_kW = (hash_rate * profit_per_ths) / power_kW
        data.append({
            'Antminer Model': model,
            'Algorithm': algo,
            'Power Consumption (kW)': power_kW,
            'Hash Rate': hash_rate,
            'Profit per TH/s per day (USD)': profit_per_ths,
            'Expected Profit per kW (USD)': expected_profit_per_kW
        })

# Creating a DataFrame from the data
df = pd.DataFrame(data)

import ace_tools as tools; tools.display_dataframe_to_user(name="Antminer Expected Profit Analysis", dataframe=df)

df
