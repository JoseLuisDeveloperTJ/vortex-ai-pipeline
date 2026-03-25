import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
import sys

# SET UP
SHEET_NAME = "Agent_Hourly_Output_Report" 
JSON_FILE = "../credentials.json"

def run_simulation(mode, until_hour=None):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1

    
    hour_to_col = {8:'B', 9:'C', 10:'D', 11:'E', 12:'F', 13:'G', 14:'H', 15:'I', 16:'J', 17:'K', 18:'L'}

# --- Reset
    if mode == "reset":
        print("🧹 Cleaning report (preserving labels)...")
        empty_hours = [["" for _ in range(11)] for _ in range(40)]
        sheet.update("B2:L41", empty_hours)       
        
        empty_totals = [[""] for _ in range(44)] 
        sheet.update("M2:M45", empty_totals)
        
        print("✨ Clean report. Global Total wiped from M42/M43.")
        return

    # --- LOGIC INYECTION-
    ranges = {"low": (1, 3), "normal": (5, 8), "high": (10, 15)}
    low, high = ranges.get(mode, (5, 8))
    
    target_hour = int(until_hour) if until_hour else 17
    print(f"🚀 Inyecting ({mode}) from 8 AM until {target_hour}:00...")

    for h, col in hour_to_col.items():
        if h <= target_hour:
            output = [[random.randint(low, high)] for _ in range(40)]
            sheet.update(f"{col}2:{col}41", output)
            print(f"✅ Column {h}:00 ({col}) Updated.")

if __name__ == "__main__":
    
    m = sys.argv[1] if len(sys.argv) > 1 else "normal"
    h = sys.argv[2] if len(sys.argv) > 2 else None
    run_simulation(m, h)