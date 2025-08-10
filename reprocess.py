import os
import re
from supabase import create_client, Client
from transformers import pipeline
import time
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# --- Initialize Supabase Client ---
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Successfully connected to Supabase.")
except Exception as e:
    print(f"Error connecting to Supabase: {e}")
    exit()

# --- Load the AI Models ---
try:
    print("Loading AI models...")
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")
    print("AI models loaded successfully.")
except Exception as e:
    print(f"Error loading AI models: {e}")
    exit()

# --- Helper Function ---
def clean_funding_amount(amount_str: str) -> float | None:
    if not amount_str:
        return None
    
    amount_str = amount_str.replace('$', '').replace(',', '').strip()
    multiplier = 1.0
    
    if 'million' in amount_str.lower() or 'M' in amount_str.upper():
        multiplier = 1_000_000.0
        amount_str = re.sub(r'[mM]illion', '', amount_str, flags=re.IGNORECASE).strip()
    elif 'billion' in amount_str.lower() or 'B' in amount_str.upper():
        multiplier = 1_000_000_000.0
        amount_str = re.sub(r'[bB]illion', '', amount_str, flags=re.IGNORECASE).strip()

    try:
        numeric_part = re.sub(r'[^\d.]', '', amount_str)
        if numeric_part:
            return float(numeric_part) * multiplier
    except (ValueError, TypeError):
        return None
    return None

# --- Main Execution ---
if __name__ == "__main__":
    while True:
        print("\n" + "="*50)
        print("Checking for a deal to re-process...")
        
        # We look for deals with the status 'PROCESSED_AI'
        res = supabase.table('deals').select('*').eq('status', 'PROCESSED_AI').limit(1).execute()
        
        if not res.data:
            print("Queue is empty. No more deals to re-process. Exiting.")
            break

        deal = res.data[0]
        deal_id = deal['id']
        context = deal['raw_text_content']
        
        print(f"--- Re-processing Deal ID: {deal_id}, Title: {deal['company_name']} ---")

        # --- Stage 1, 2, and 3 logic remains the same ---
        # ...

        # --- THIS IS THE FIX ---
        # We now set the status to a new, final state to prevent re-processing
        update_data = {
            # ... (all other fields)
            'status': 'REPROCESSED_V2' 
        }

        print("\nUpdating database with newly extracted info...")
        try:
            update_data_cleaned = {k: v for k, v in update_data.items() if v is not None}
            data, count = supabase.table('deals').update(update_data_cleaned).eq('id', deal_id).execute()
            print("Database update successful.")
        except Exception as e:
            print(f"Database update failed: {e}")
        
        time.sleep(1)