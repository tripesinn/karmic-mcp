---
name: Karmic Gochara
description: Real-time astrological transit calculations with Swiss Ephemeris
category: wellness
keywords: ["astrology", "wellness", "predictions", "natal chart", "transits"]
---

# Karmic Gochara

Real-time astrological analysis powered by Swiss Ephemeris. Get personalized natal chart readings and transit predictions using the Doctrine Évolutive Synthétique framework — a sophisticated blend of Jyotish, Western astrology, and psychological insight.

## Features

- **Real-time Calculations** — Swiss Ephemeris-backed precision (not hallucinated)
- **Personalized Analysis** — Natal chart interpretation based on your birth data
- **Doctrine Évolutive Synthétique** — Proprietary astrological framework combining multiple traditions
- **Offline-Capable** — Works with Gemma-4-E4B on Pixel 9+ without cloud dependencies
- **Multi-language** — Responses in English and French

## How It Works

Karmic Gochara MCP (Model Context Protocol) server connects to Gemma-4-E4B on your device. It calculates:

1. **Natal Chart** — Your birth planets, nodes, and sensitive points
2. **Current Transits** — Where planets are today relative to your chart
3. **Doctrine Reading** — Astrological interpretation in the Doctrine Évolutive Synthétique system

The MCP server handles all calculations and data; Gemma provides natural language interpretation locally on your device.

## Requirements

- **Device** — Pixel 8 Pro or Pixel 9+ with Gemma-4-E2B-it or E4B-it
- **Connection** — Internet for MCP server communication (or local server for offline)
- **Optional** — Run your own local MCP server for fully offline use

## Setup

### Via Edge Gallery

1. Open Edge Gallery on your Pixel
2. Go to **Agent Skills** → **Load skill from URL**
3. Paste: `https://api.karmicgochara.app`
4. Or use GitHub directly: `https://github.com/tripesinn/karmic-mcp`

### Local Deployment

For fully offline use, deploy the MCP server locally:
```bash
git clone https://github.com/tripesinn/karmic-mcp
cd karmic-mcp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py
```

## Usage Examples

**Ask Gemma:**

- "What are my astrological transits today?"
- "Analyze my natal chart for 31/10/1974 8h25 Athis-Mons"
- "What does the Moon opposition mean for me right now?"

**Response includes:**
- ROM/Dharma (Ketu/Rahu) — past-life patterns vs. soul direction
- Porte Invisible → Porte Visible — unconscious blocks → conscious stage
- Épreuve Lilith — friction points and transformation
- Alternative de Conscience — actionable insight

## Documentation

- **GitHub Repository** — https://github.com/tripesinn/karmic-mcp
- **MCP Server URL** — https://api.karmicgochara.app
- **Doctrine Framework** — See README.md for full methodology

## Support

For issues or feature requests, open an issue on GitHub:
https://github.com/tripesinn/karmic-mcp/issues

---

**Status:** ✅ Production-ready | **License:** MIT | **Language:** EN/FR