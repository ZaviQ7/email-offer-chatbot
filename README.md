# AI Email Offer Chatbot

A lightweight system that reads listing-agent emails, calculates a 60% offer based on the property's Zestimate (or the asking price), and replies automatically. The logic lives in an n8n workflow; Zestimate look‑ups are provided by a small Flask micro‑service.

## Quick start

1. **Clone & install**

   ```bash
   python -m venv venv
   # Windows: venv\Scripts\activate
   # mac/linux: source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **(Optional) enable live Zestimate look‑ups**

   ```bash
   cp .env.example .env
   # edit .env and add your RAPIDAPI_KEY
   ```

3. **Run the API**

   ```bash
   python api/api.py
   ```

4. **Run n8n**

   ```bash
   docker run -d --name n8n \
     -p 5678:5678 \
     -v $HOME/.n8n:/home/node/.n8n \
     n8nio/n8n
   ```

5. **Import** `n8n/EmailOfferWorkflow.json` in the n8n UI (http://localhost:5678).  
   Wire up Gmail credentials for both nodes.  

6. **Test**

   Send yourself an email:

   ```
   Subject: Property Inquiry: 123 Main St
   Body:
   Address: 123 Main St
   Price: $550,000
   ```

   The bot replies with a 60% offer.

## Directory layout

```
api/                  Flask micro‑service
n8n/                  Workflow JSON
requirements.txt      Python deps
.env.example          Put RAPIDAPI_KEY here
README.md             This file
SETUP_PAID_SERVICES.md Extra notes for paid APIs
```
