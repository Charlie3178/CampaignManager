import sqlite3
import os

# Update this path to match your actual location
db_path = r"F:\__CampaignManager\data\campaign.db"

if not os.path.exists(db_path):
    print(f"File not found at {db_path}")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print(f"Checking schema for table: characters")
    cursor.execute("PRAGMA table_info(characters)")
    columns = cursor.fetchall()

    found_is_pc = False
    for col in columns:
        print(f"Column ID: {col[0]} | Name: {col[1]} | Type: {col[2]}")
        if col[1] == 'is_pc':
            found_is_pc = True

    if found_is_pc:
        print("\n[SUCCESS] 'is_pc' exists in the physical database file.")
    else:
        print("\n[ERROR] 'is_pc' IS MISSING from the physical database file.")

    conn.close()
