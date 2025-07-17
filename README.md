# AI Email Offer Chatbot

This project reads listing-agent emails, calculates a **60% offer** based on a property's Zestimate (or the asking price), and sends the offer back automatically.  
The logic lives in an **n8n** workflow; Zestimate lookups are served by a lightweight **Flask** microservice.

---

## Quick Start (Docker Compose)

> Docker Compose spins up both the API (port `5001`) and n8n (port `5678`) with one command.

1. **Clone the repo** and switch to the project folder.

2. **Create an `.env`** file in the root (it can be empty).  
   To enable live Zestimate data, add your RapidAPI key:

   ```env
   RAPIDAPI_KEY=YOUR_RAPIDAPI_KEY_HERE
   ```

3. **Start everything**

   ```bash
   docker compose up --build
   ```

4. **Open your browser**

   | URL                      | Purpose            | Default credentials             |
   | ------------------------ | ------------------ | ------------------------------- |
   | `http://localhost:5001/` | Flask health check | n/a                             |
   | `http://localhost:5678/` | n8n UI             | user: `admin`, pass: `changeme` |

5. **Import** `n8n/EmailOfferWorkflow.json` in the n8n UI and connect your Gmail account for both trigger and send nodes.

6. **Send a test email**

   ```
   Subject: Property Inquiry: 123 Main St
   Body:
   Address: 123 Main St
   Price: $550,000
   ```

   The bot replies with a 60% offer.

---

## Local Development (No Docker)

```bash
# 1. Set up Python environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. (Optional) enable live Zestimate key
cp .env.example .env
# Edit .env and add: RAPIDAPI_KEY=...

# 3. Run Flask API
python api/api.py
```

Spin up n8n separately:

```bash
docker run -d --name n8n \
  -p 5678:5678 \
  -v $HOME/.n8n:/home/node/.n8n \
  n8nio/n8n
```

---

## Running Tests

```bash
pytest
```

`tests/test_api.py` verifies that `/zestimate` returns a valid response.

---

## Project Structure

```
api/                    Flask microservice
n8n/                    Workflow JSON
tests/                  Basic pytest suite
Dockerfile              API container image
docker-compose.yml      One-command stack
requirements.txt        Python dependencies
.env.example            Env-var template
LICENSE                 MIT license
SETUP_PAID_SERVICES.md  RapidAPI & Gmail notes
```

---

## Security & Production Notes

* **Change** the n8n basic-auth credentials in `docker-compose.yml` before going live.
* Set Gmail quotas or use a G Suite account if you expect high traffic.
* Consider adding a database or log store for long-term tracking or persistence.

---

MIT License – see `LICENSE` for details.
git add README.md
