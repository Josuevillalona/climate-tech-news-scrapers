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
        # Remove any non-numeric characters left (except the decimal point)
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
        print("Checking for a new deal to process...")
        
        res = supabase.table('deals').select('*').eq('status', 'NEW').limit(1).execute()
        
        if not res.data:
            print("Queue is empty. No new deals to process. Exiting.")
            break

        deal = res.data[0]
        deal_id = deal['id']
        context = deal['raw_text_content']
        
        print(f"--- Processing Deal ID: {deal_id}, Title: {deal['company_name']} ---")

        # STAGE 1: CLASSIFY ARTICLE TYPE
        print("\nStage 1: Classifying article type...")
        type_labels = ["company funding announcement", "general business news", "market analysis", "opinion piece"]
        type_classification = classifier(context[:2000], type_labels, multi_label=False)
        
        top_type_label = type_classification['labels'][0]
        top_type_score = type_classification['scores'][0]
        print(f"  -> Top Type Classification: '{top_type_label}' (Confidence: {top_type_score:.2f})")
        
        if top_type_label != "company funding announcement" or top_type_score < 0.8:
            print("  -> Result: Article is not a clear funding announcement. Marking as irrelevant.")
            supabase.table('deals').update({'status': 'IRRELEVANT_TYPE'}).eq('id', deal_id).execute()
        else:
            print("  -> Result: Article is a funding announcement. Proceeding to Stage 2.")
            
            # STAGE 2: CLASSIFY SECTOR
            print("\nStage 2: Classifying company sector...")
            sector_labels = [
                "Climate Tech - Carbon & Emissions", "Climate Tech - Sustainable Agriculture", "Climate Tech - Energy & Grid",
                "Climate Tech - Circular Economy", "Climate Tech - Electric Mobility", "General B2B Software", "Fintech", "Crypto", "Consumer App", "Robotics & AI"
            ]
            sector_classification = classifier(context, sector_labels, multi_label=False)
            
            top_sector = sector_classification['labels'][0]
            top_sector_score = sector_classification['scores'][0]
            print(f"  -> Top Sector Classification: '{top_sector}' (Confidence: {top_sector_score:.2f})")

            if "Climate Tech" not in top_sector:
                print("  -> Result: Sector is not Climate Tech. Marking as irrelevant.")
                supabase.table('deals').update({'status': 'IRRELEVANT_SECTOR', 'climate_sub_sector': top_sector}).eq('id', deal_id).execute()
            else:
                print("  -> Result: Sector is Climate Tech. Proceeding to final extraction.")
                
                # STAGE 3: EXTRACT DETAILS
                print("\nStage 3: Extracting funding details...")
                questions = {
                    "funding_amount_str": "From the text, what is the total funding amount raised?",
                    "funding_stage": "Based on the text, what is the funding stage, such as Seed, Series A, or Series B?",
                    "lead_investors": "From the text, identify the lead investment firm or venture capital fund.",
                    "other_investors": "Which other firms, funds, or angel investors participated in the round?"
                }
                
                results = {}
                for key, question in questions.items():
                    result = qa_pipeline(question=question, context=context)
                    if result['score'] > 0.1: # Confidence threshold
                        results[key] = result['answer']
                
                numeric_amount = clean_funding_amount(results.get('funding_amount_str'))

                update_data = {
                    'climate_sub_sector': top_sector,
                    'amount_raised': numeric_amount,
                    'funding_amount_str': results.get('funding_amount_str'),
                    'funding_stage': results.get('funding_stage'),
                    'lead_investors': results.get('lead_investors'),
                    'other_investors': results.get('other_investors'),
                    'status': 'PROCESSED_AI'
                }

                print("\nUpdating database with extracted info...")
                try:
                    update_data_cleaned = {k: v for k, v in update_data.items() if v is not None}
                    data, count = supabase.table('deals').update(update_data_cleaned).eq('id', deal_id).execute()
                    print("Database update successful.")
                except Exception as e:
                    print(f"Database update failed: {e}")
        
        time.sleep(1)
