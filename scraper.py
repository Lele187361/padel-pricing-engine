from datetime import datetime, timedelta
import pandas as pd
import requests

# --- 1. CLUBS SPEICHERN ---
CLUBS = {
    "Padel Lankwitz": "f6f12032-198e-4657-ab45-8aeb0b8a24b5",
    "PBC-Club": "9fea856e-7d1a-4cae-9831-79015318967b",
    "Padel Neukölln": "632ca5b0-93bc-4718-a3e9-288bc2fe507d",
    "Padel Arena Berlin": "31bb4900-5ad3-424a-a7fe-ed49ed2bf8e8",
    "NIXE Padel": "934f491a-a565-44cc-96cb-c4d5352dca95",
}


# --- 2. ABFRAGE-FUNKTION ---
def fetch_playtomic_data(club_name, tenant_id, target_date, scraped_at):
    url = f"https://playtomic.com/api/clubs/availability?tenant_id={tenant_id}&date={target_date}&sport_id=PADEL"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []

        data = response.json()
        collected = []

        for item in data:
            court_name = item.get("resource_name", "Padel Court")
            for slot in item.get("slots", []):
                collected.append(
                    {
                        "scraped_at": scraped_at,
                        "target_date": target_date,
                        "club": club_name,
                        "court": court_name,
                        "start_time": slot.get("start_time", ""),
                        "duration_min": slot.get("duration", ""),
                        "price": slot.get("price", "N/A"),
                    }
                )
        return collected
    except Exception as e:
        print(f"Fehler bei {club_name}: {e}")
        return []


# --- 3. DATENSPEICHERUNG ---
def save_to_csv(data, filename="court_availability.csv"):
    if not data:
        print("⚠️ Keine Daten im aktuellen Durchlauf empfangen.")
        return

    df = pd.DataFrame(data)
    try:
        df_existing = pd.read_csv(filename)
        df_combined = pd.concat([df_existing, df], ignore_index=True)
        df_combined.to_csv(filename, index=False)
    except FileNotFoundError:
        df.to_csv(filename, index=False)

    print(
        f"✅ ERFOLG! {len(data)} Datenpunkte in '{filename}' abgespeichert."
    )


# --- 4. ABLAUF-STEUERUNG ---
def run_scraping_job():
    scraped_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n🚀 [{scraped_at}] Starte automatische Datenabfrage...")

    all_data = []

    # Liest heute (0) und morgen (1) für alle 5 Clubs aus
    for days_ahead in [0, 1]:
        target_date = (datetime.now() + timedelta(days=days_ahead)).strftime(
            "%Y-%m-%d"
        )

        for club_name, tenant_id in CLUBS.items():
            records = fetch_playtomic_data(
                club_name, tenant_id, target_date, scraped_at
            )
            all_data.extend(records)

    save_to_csv(all_data)


# --- 5. EINMALIGER DURCHLAUF (FÜR GITHUB ACTIONS CLOUD-CRON) ---
if __name__ == "__main__":
    run_scraping_job()
    print("🏁 Scraper-Durchlauf beendet.")