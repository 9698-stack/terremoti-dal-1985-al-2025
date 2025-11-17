
# coding: utf-8

# In[9]:


import requests
import pandas as pd
import time

# URL API INGV
url = "https://webservices.ingv.it/fdsnws/event/1/query"

# Parametri generali
start_year = 1985
end_year = 2025
min_magnitude = 2.5

# Bounding box Italia
min_latitude = 35.5
max_latitude = 47.1
min_longitude = 6.5
max_longitude = 18.5

# Parametri retry
max_retries = 5
retry_delay = 5  # secondi tra i tentativi

dfs = []

for year in range(start_year, end_year + 1):
    starttime = f"{year}-01-01"
    endtime = f"{year}-12-31"
    
    params = {
        "format": "geojson",
        "starttime": starttime,
        "endtime": endtime,
        "minmagnitude": min_magnitude,
        "minlatitude": min_latitude,
        "maxlatitude": max_latitude,
        "minlongitude": min_longitude,
        "maxlongitude": max_longitude
    }
    
    print(f"\nScaricando dati Italia: {starttime} -> {endtime}")
    
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, params=params, timeout=60)
            response.raise_for_status()
            data = response.json()
            events = [f["properties"] for f in data.get("features", [])]
            
            if events:
                df = pd.DataFrame(events)
                dfs.append(df)
                print(f"  ✅ {len(events)} eventi trovati")
            else:
                print("  ⚠️ Nessun evento trovato")
            break  # uscita dal loop dei retry se successo
            
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Tentativo {attempt}/{max_retries} fallito: {e}")
            if attempt < max_retries:
                print(f"     Attesa {retry_delay} secondi prima del retry...")
                time.sleep(retry_delay)
            else:
                print("     ⚠️ Massimi tentativi raggiunti, salto questo anno")
                break

# Concatenare tutti gli anni in un unico DataFrame
if dfs:
    df_total = pd.concat(dfs, ignore_index=True)
    df_total.to_csv("terremoti_italia_ingv.csv", index=False)
    print(f"\n✅ Tutti i dati salvati in 'terremoti_italia_ingv.csv' ({len(df_total)} eventi totali)")
else:
    print("\n⚠️ Nessun dato scaricato")

import pandas as pd
import matplotlib.pyplot as plt

# Convertiamo la colonna 'time' in datetime
df['time'] = pd.to_datetime(df['time'], errors='coerce')

# Creiamo una colonna con l'anno
df['year'] = df['time'].dt.year

# Raggruppiamo per anno
events_per_year = df.groupby('year').size()
avg_mag_per_year = df.groupby('year')['mag'].mean()

# Creiamo il grafico
fig, ax1 = plt.subplots(figsize=(12,6))

# Linea numero di eventi
color = 'tab:blue'
ax1.set_xlabel('Anno')
ax1.set_ylabel('Numero di eventi', color=color)
ax1.plot(events_per_year.index, events_per_year.values, marker='o', color=color, label='Numero di eventi')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True)

# Linea magnitudo media (secondo asse y)
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Magnitudo media', color=color)
ax2.plot(avg_mag_per_year.index, avg_mag_per_year.values, marker='x', linestyle='--', color=color, label='Magnitudo media')
ax2.tick_params(axis='y', labelcolor=color)

# Titolo e legenda
fig.suptitle('Terremoti anno per anno: Numero di eventi e Magnitudo media')
fig.tight_layout()
plt.show()