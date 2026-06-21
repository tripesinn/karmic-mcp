---
name: MCP Deployment Stack
description: Procedural guide for deploying a Model Context Protocol (MCP) server from source code to a public, secure endpoint via Cloudflare/GCP.
category: wellness
keywords: ["astrology", "wellness", "predictions", "natal chart", "transits", "mcp", "cloudflare"]
---

# 🚀 MCP Deployment Stack (Optimisé)

Ce skill est un guide procédural pour le déploiement de serveurs Model Context Protocol (MCP) de zéro à une API publique et sécurisée sur GCP, en passant par Cloudflare Tunnel.

## 🎯 Résolution du Problème Edge Gallery (CRITIQUE)

Pour que l'Agent (Edge Gallery) retrouve le Skill, la méthode la plus fiable est de **servir le markdown via GitHub**, pas directement via l'API.

**Méthode recommandée :**
Utilisez le lien GitHub du dépôt source (`https://github.com/tripesinn/karmic-mcp`) dans Edge Gallery. L'agent peut lire le `SKILL.md` directement, ce qui garantit la stabilité.

**Méthode de secours :**
Si GitHub n'est pas disponible, le serveur FastAPI doit servir le fichier `SKILL.md` via un endpoint `/SKILL.md`.

## ⚙️ Workflow Complet (Le cycle de vie du produit)

Le déploiement réussi dépend de ces phases :

1. **Code Base** (GCP VM) : Implémentation du serveur MCP en local.
2. **Infrastructure** (Cloudflare) : Configuration du tunnel (`config.yml`).
3. **Public Access** (GCP/Cloudflare) : Mise à jour du firewall GCP.
4. **Skillization** : Documentation du processus.

## 🔑 Maintenance Critique : Cloudflare Origin Certificate

Le tunnel nécessite un certificat d'origine (`cert.pem`) pour valider la connexion.

**Action Requise (Si le tunnel échoue) :**
1. Obtenir `cert.pem` de Cloudflare.
2. Placer le fichier sur la VM.
3. Mettre à jour le fichier `~/.cloudflared/config.yml` pour spécifier le chemin via l'option `origincertPath`.

## ⚡️ Workflow de Démarrage (Simplifié)

**Sur la VM GCP (dev-vm) :**

1. **Démarrage du service :** `sudo systemctl restart karmic-mcp`
2. **Démarrage du tunnel :** `cloudflared tunnel run karmic-mcp` (Note : `sudo` n'est plus nécessaire).
3. **Validation (Local) :** `curl -s http://localhost:8000/health` (Doit retourner `200`)
4. **Validation (Public) :** `curl -s -o /dev/null -w "%{http_code} %{time_total}s\n" https://api.karmicgochara.app/health` (Doit retourner `200`)

## 💡 Exemples d'Utilisation

Ce skill sert de documentation de référence pour le processus de livraison de services MCP, de la conception au déploiement Cloudflare.

**Déploiement :**
1. Cloner le repo source : `git clone https://github.com/tripesinn/karmic-mcp`
2. Configurer et lancer le service.
3. Configurer le tunnel Cloudflare.
---
