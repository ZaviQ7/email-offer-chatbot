import os
import logging
import requests
from flask import Flask, request, jsonify

# ── Logging setup ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(name)s ‑ %(message)s",
)
logger = logging.getLogger("zestimate-api")
# ─────────────────────────────────────────────────────────────────────────────

app = Flask(__name__)

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
ZILLOW_HOST = "zillow-com1.p.rapidapi.com"


def get_zestimate_from_rapidapi(address: str):
    """Return a Zestimate via RapidAPI or None on failure."""
    if not RAPIDAPI_KEY:
        return None

    url = f"https://{ZILLOW_HOST}/propertyExtendedSearch"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": ZILLOW_HOST,
    }
    params = {"location": address}

    try:
        res = requests.get(url, headers=headers, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()

        if isinstance(data, dict) and data.get("properties"):
            zestimate = data["properties"][0].get("zestimate")
            if zestimate:
                return float(zestimate)
    except Exception as exc:
        logger.warning("RapidAPI Zillow call failed: %s", exc)

    return None


@app.get("/")
def health():
    """Simple health check."""
    return "Zestimate API running", 200


@app.post("/zestimate")
def zestimate():
    """POST { 'address': '123 Main St' } → { 'address': '…', 'zestimate': 500000 }"""
    payload = request.get_json(force=True)
    address = (payload or {}).get("address", "").strip()

    if not address:
        return jsonify({"error": "address field required"}), 400

    value = get_zestimate_from_rapidapi(address) or 500_000.0
    return jsonify({"address": address, "zestimate": value})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
