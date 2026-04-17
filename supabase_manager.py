from supabase import create_client, Client
from langchain.tools import tool
import os

# Ye keys aapko Supabase dashboard se milengi
url = "https://xrahpiybqbizvbyoayyz.supabase.co"
key = "sb_publishable_9Lj977gXORQ1JvzNdHZ8cQ_vxe4Tk9y"
supabase: Client = create_client(url, key)

def save_lead_to_db(name, email, query):
    try:
        data = {
            "user_name": name,
            "user_email": email,
            "user_query": query
        }
        # 'leads' naam ki table mein data insert karna
        response = supabase.table("leads").insert(data).execute()
        return "Success! Data saved to Supabase."
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def save_customer_lead(name: str, email: str, query: str) -> str:
    """
    Saves the customer's contact information (name, email, and their requirement)
    into the database when they are interested in our services.
    """
    try:
        # Check karein ke supabase client sahi se initialized hai
        data = {"user_name": name, "user_email": email, "user_query": query}
        supabase.table("leads").insert(data).execute()
        return "Successfully saved the lead to the database."
        response = supabase.table("leads").insert(data).execute()
        print("FULL RESPONSE:", response)
    except Exception as e:
        return f"Error saving lead: {e}"
