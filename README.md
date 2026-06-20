# 🌌 Karmic Gochara MCP Server

> Real-time astrological transit calculations and synthetic evolutionary doctrine readings, exposed via the **Model Context Protocol (MCP)** for Google AI Edge Gallery.

[![Status](https://img.shields.io/badge/status-production-brightgreen)](https://github.com/tripesinn/karmic-mcp)
[![MCP](https://img.shields.io/badge/protocol-MCP-blue)](https://modelcontextprotocol.io/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Made with](https://img.shields.io/badge/made%20with-Gemma--4--E4B--it-orange)](https://huggingface.co/unsloth/gemma-4-E4B-it-UD-MLX-4bit)
[![Local](https://img.shields.io/badge/runs-100%25_local-success)](#-acknowledgments)

**Live endpoint:** `http://34.163.125.49:8000`
**Schema discovery:** `http://34.163.125.49:8000/mcp/discovery`

---

## ⚡ Quick Start

Test the live endpoint in 10 seconds:

```bash
# 1. Health check
curl http://34.163.125.49:8000/health
# → {"status":"ok","service":"karmic-lite-mcp-server"}

# 2. Get planetary transits for a date of birth
curl "http://34.163.125.49:8000/transits/today?dob=1990-05-15"
# → {"date":"1990-05-15","planet_positions":{"sun":"...","moon":"..."}}

# 3. Request a doctrine reading
curl -X POST "http://34.163.125.49:8000/doctrine/reading?dob=1990-05-15&birth_time=14:30" \
  -H "Content-Type: application/json" -d '{}'
# → {"reading":"...","input_details":{"dob":"...","birth_time":"..."}}
```

---

## 🎯 What is this?

The **Karmic Gochara MCP Server** is a lightweight FastAPI microservice that exposes astrological calculations through the **Model Context Protocol (MCP)**, making them directly callable by on-device LLMs like **Gemma-4-E4B-it** running inside Google AI Edge Gallery on Pixel devices.

It currently ships **3 MCP tools** (designed to stay within the context window of small local models):

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| `get_natal_chart` | Birth chart positions | `dob`, `birth_time`, `birth_place` | Sun, Moon, Ascendant, planets, nodes |
| `get_transits_today` | Current planetary aspects | `natal_data`, `tz` | Aspect list, intensity score, dominant planet |
| `get_doctrine_reading` | Synthetic evolutionary reading | `natal_data`, `transits_data`, `question?` | JSON with 4 doctrinal pillars + insight |

---

## 🛠️ Architecture

```
┌─────────────────────┐         HTTP/MCP          ┌──────────────────────────┐
│  Pixel 9 + Edge     │  ──────────────────────►  │  FastAPI MCP Server      │
│  Gallery + Gemma-4  │  ◄──────────────────────  │  (GCP e2-small, Paris)   │
└─────────────────────┘                           └──────────────────────────┘
                                                          │
                                                          ▼
                                                  ┌──────────────────┐
                                                  │  pyswisseph      │
                                                  │  geopy           │
                                                  │  (Swiss Ephemeris│
                                                  │   ephemerides)   │
                                                  └──────────────────┘
```

**Stack:** Python 3.10 · FastAPI 0.104 · Pydantic 2.5 · Uvicorn 0.27 · pyswisseph 2.10 · geopy 2.4

---

## 🚀 Local Development

### Prerequisites
- Python 3.10+
- Git

### Setup

```bash
# Clone
git clone https://github.com/tripesinn/karmic-mcp.git
cd karmic-mcp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python server.py
# → Server runs on http://0.0.0.0:8000
```

### Test locally

```bash
bash test_client.sh
```

Expected output:
```
✅ PASS: Health check returned HTTP 200.
✅ PASS: Transits endpoint returned structured data.
✅ PASS: Doctrine reading endpoint returned structured data.
🚀 MISSION SUCCESS: Local API Validation Complete.
```

---

## ☁️ Deployment (GCP Compute Engine)

This server runs on a **GCP e2-small** instance (Ubuntu 22.04, europe-west9-a) as a systemd service.

### Deploy from scratch

```bash
# 1. SSH into your VM
gcloud compute config-ssh  # one-time setup
ssh dev-vm

# 2. Install Python venv system package
sudo apt install -y python3.10-venv python3-pip

# 3. Clone the repo
cd ~ && git clone https://github.com/tripesinn/karmic-mcp.git
cd karmic-mcp

# 4. Setup venv + install deps
python3 -m venv venv
source venv/bin/activate
./venv/bin/python -m ensurepip --default-pip
./venv/bin/pip install -r requirements.txt

# 5. Create systemd service
sudo tee /etc/systemd/system/karmic-mcp.service > /dev/null <<EOF
[Unit]
Description=Karmic Gochara MCP Server
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/home/$USER/karmic-mcp
ExecStart=/home/$USER/karmic-mcp/venv/bin/uvicorn server:app --host 0.0.0.0 --port 8000
Restart=on-failure
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# 6. Enable + start
sudo systemctl daemon-reload
sudo systemctl enable karmic-mcp
sudo systemctl start karmic-mcp

# 7. Open firewall (run from local machine, not the VM)
gcloud compute firewall-rules create allow-karmic-mcp-8000 \
  --project=karmic-gochara-cloud \
  --direction=INGRESS --action=ALLOW --rules=tcp:8000 \
  --source-ranges=0.0.0.0/0 --target-tags=http-server

gcloud compute instances add-tags dev-vm \
  --tags=http-server --zone=europe-west9-a
```

### Useful maintenance commands

```bash
# Status
sudo systemctl status karmic-mcp

# Live logs
sudo journalctl -u karmic-mcp -f

# Restart after code update
cd ~/karmic-mcp && git pull && sudo systemctl restart karmic-mcp
```

---

## 📱 Edge Gallery Integration

To register this server with **Google AI Edge Gallery**:

1. Open Edge Gallery on your Pixel device
2. Go to **Settings → MCP Servers**
3. Tap **Add custom server**
4. Enter:
   - **Server URL:** `http://34.163.125.49:8000`
   - **Schema URL:** `http://34.163.125.49:8000/mcp/discovery`
5. Save and test by asking Gemma:
   > *"Using the Karmic Gochara MCP server, give me today's planetary transits for someone born on 1990-05-15 at 14:30."*

The 3 MCP tools will become available to Gemma automatically via schema discovery.

---

## 📁 Project Structure

```
karmic-mcp/
├── server.py              # FastAPI app + MCP endpoints
├── requirements.txt       # Python dependencies
├── test_client.sh         # Local validation script
├── .gitignore             # Excludes venv/, __pycache__/, etc.
├── README.md              # This file
└── README.fr.md           # Version française
```

---

## 🌍 Endpoints Reference

| Endpoint | Method | Description | Response time |
|----------|--------|-------------|---------------|
| `/health` | GET | Service health check | <10 ms |
| `/mcp/discovery` | GET | MCP schema for client auto-config | <50 ms |
| `/transits/today?dob=YYYY-MM-DD` | GET | Planetary transits for a DOB | <500 ms |
| `/doctrine/reading?dob=...&birth_time=...` | POST | Synthetic doctrine reading | <2 s |

---

## 🤝 Contributing

Pull requests welcome. For major changes, open an issue first to discuss what you'd like to change.

---

## 📄 License

[MIT](LICENSE)

---

## ✨ Acknowledgments

- **Swiss Ephemeris** for the astronomical calculation engine
- **Google AI Edge Gallery** for the on-device LLM runtime
- **Model Context Protocol** for the standard MCP spec

---

*Built with ❤️ by Jero · [@siderealAstro13](https://github.com/siderealAstro13) · Karmic Gochara Project*

🤖 *Code generated with [Gemma-4-E4B-it](https://huggingface.co/unsloth/gemma-4-E4B-it-UD-MLX-4bit) running locally via [oMLX](https://github.com/jero87/omlx) on a Mac Mini M4 (16GB RAM), orchestrated by [Hermes Agent](https://hermes-agent.nousresearch.com). 100% local, 0 cloud calls during development.*
