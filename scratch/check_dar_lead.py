import json

with open('data/research_leads.json', 'r', encoding='utf-8') as f:
    leads = json.load(f)

for lead in leads:
    if 'dar' in lead.get('lead_id', '').lower() or 'sheikh' in lead.get('lead_id', '').lower() or 'aligarh' in lead.get('publisher_or_archive', '').lower():
        print(f"Lead ID: {lead['lead_id']}")
        print(f"Title: {lead['title']}")
        print(f"Authors: {lead['authors_or_institution']}")
        print(f"Status: {lead.get('status')}")
        print(f"Notes: {lead.get('verification_notes', '')[:200]}")

