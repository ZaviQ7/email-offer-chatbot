# Integrating Paid Services

## RapidAPI Zillow (live Zestimate data)

1. Sign up at https://rapidapi.com
2. Subscribe to the "Zillow‑com" API (free tier gives 100 calls/month).
3. Copy your `X-RapidAPI-Key`.
4. Create `.env` in the project root:

   ```
   RAPIDAPI_KEY=PASTE_YOUR_KEY_HERE
   ```

5. Restart `api/api.py` (the Flask service reads the key at startup).

n8n continues to call `http://host.docker.internal:5001/zestimate`—no changes needed.

## Gmail API costs

Using n8n’s built‑in Gmail node is free. Google enforces daily sending quotas; upgrade to a G Suite account if you expect high volume.

## Scaling Up

* **Render/Railway:** free web service for the Flask API (auto‑deploy from GitHub).
* **n8n Cloud:** 30‑day trial, pay‑as‑you‑go after that. Or self‑host on Render.

Make sure environment variables (`RAPIDAPI_KEY`, etc.) are set on the hosting provider.
