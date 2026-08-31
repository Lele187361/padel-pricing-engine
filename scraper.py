import os
import requests
import pandas as pd
from datetime import datetime, timedelta

# --- 1. CONFIGURATION & CLUBS ---
CLUBS = {
    "Padel Berlin Mitte": "playtomic_tenant_id_1",
    "Smart Padel Berlin": "playtomic_tenant_id_2",
    # Füge hier deine tatsächlichen Club-IDs/Namen ein
}

# --- 2. SCRAPER LOGIC ---
def fetch_playtomic_data(club_name, tenant_id, target_date, scraped_at):
    """
    Simuliert oder ruft die Playtomic-Daten ab.
    Passt die Daten in ein sauberes Format an.
    """
    # Beispielhafter Datenpunkt (wird durch deinen echten Scraper-Code ersetzt)
    records = [{
        "scraped_at": scraped_at,
        "club_name": club_name,
        "target_date": target_date,
        "court_name": "Court 1",
        "start_time": "10:00",
        "end_time": "11:30",
        "price": 32.0,
        "available": True
    }]
    return records

# --- 3. SPEICHER-FUNKTION (FIXIERT FÜR GITHUB ACTIONS) ---
def save_to_csv(data, filename="court_availability.csv"):
    df_new = pd.DataFrame(data)
    
    # Erzwinge den absoluten Pfad im aktuellen Hauptverzeichnis
    filepath = os.path.abspath(filename)
    
    if os.path.exists(filepath):
        try:
            df_existing = pd.read_csv(filepath)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        except Exception:
            df_combined = df_new
    else:
        df_combined = df_new
        
    df_combined.to_csv(filepath, index=False)
    print(f"✅ ERFOLG! Daten in '{filepath}' abgespeichert.")

# --- 4. ABLAUF-STEUERUNG ---
def run_scraping_job():
    scraped_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n🚀 [{scraped_at}] Starte automatische Datenabfrage...")

    all_data = []

    # Liest heute (0) und morgen (1) für alle Clubs aus
    for days_ahead in [0, 1]:
        target_date = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        
        for club_name, tenant_id in CLUBS.items():
            records = fetch_playtomic_data(
                club_name, tenant_id, target_date, scraped_at
            )
            all_data.extend(records)

    if all_data:
        save_to_csv(all_data)

# --- 5. EXECUTION ---
if __name__ == "__main__":
    run_scraping_job()
    print("🏁 Scraper-Durchlauf beendet.")
