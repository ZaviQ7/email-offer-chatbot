import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Optional: RapidAPI Zillow key. Leave blank to use the stub value.
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
ZILLOW_HOST = "zillow-com1.p.rapidapi.com"

def get_zestimate_from_rapidapi(address: str):
    """Fetch zestimate via RapidAPI; returns float or None."""
    if not RAPIDAPI_KEY:
        return None
    url = f"https://{ZILLOW_HOST}/propertyExtendedSearch"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": ZILLOW_HOST,
    }
    params = {"location": address}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict) and data.get("properties"):
            zestimate = data["properties"][0].get("zestimate")
            if zestimate:
                return float(zestimate)
    except Exception as exc:
        app.logger.error(f"RapidAPI call failed: {exc}")
    return None

@app.route("/zestimate", methods=["POST"])
def zestimate():
    """Return {{address, zestimate}} JSON."""
    payload = request.get_json(force=True)
    address = (payload or {}).get("address", "").strip()
    if not address:
        return jsonify({"error": "address field required"}), 400
    zestimate_value = get_zestimate_from_rapidapi(address)
    if zestimate_value is None:
        zestimate_value = 500_000.0  # fallback stub
    return jsonify({"address": address, "zestimate": zestimate_value})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
