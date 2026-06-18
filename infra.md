# Documentation Technique — Infrastructure Ymmo

## 1. Présentation du projet

**Ymmo** est un groupe immobilier implanté en France avec :
- 1 siège social à Aix-en-Provence (~30 postes)
- 12 agences réparties sur le territoire national (~5 postes par agence)

---

## 2. Schéma d'architecture réseau

```
                        INTERNET
                            |
                       [Pare-feu]
                            |
                      [Routeur Siège]
                     /      |       \
              [Switch]   [DMZ]    [VPN IPSec]
             /   |   \      |          |
          [AD] [Web] [BDD] [Srv]   [Agences x12]
          
Siège — Aix-en-Provence
┌─────────────────────────────────────────────────────┐
│  DMZ                                                │
│  ┌──────────────┐  ┌──────────────┐                │
│  │ Serveur Web  │  │ Serveur BDD  │                │
│  │ (Flask/Nginx)│  │ (PostgreSQL) │                │
│  └──────────────┘  └──────────────┘                │
│                                                     │
│  LAN Interne                                        │
│  ┌──────────────┐  ┌──────────────┐                │
│  │ Windows      │  │ Serveur de   │                │
│  │ Server (AD)  │  │ fichiers/NAS │                │
│  └──────────────┘  └──────────────┘                │
│                                                     │
│  Postes : Direction / Commercial / RH / IT (~30)    │
└─────────────────────────────────────────────────────┘
          |
    [VPN IPSec Site-à-Site]
          |
┌─────────────────────┐
│ Agence (x12)        │
│ ┌─────────────────┐ │
│ │ Routeur/Pare-feu│ │
│ │ Switch          │ │
│ │ 5 postes        │ │
│ │ 1 imprimante    │ │
│ └─────────────────┘ │
└─────────────────────┘
```

---

## 3. Plan d'adressage IP

### Siège — Aix-en-Provence

| Réseau | Plage IP | Masque | Passerelle | Usage |
|--------|----------|--------|------------|-------|
| LAN Siège | 192.168.1.0/24 | 255.255.255.0 | 192.168.1.1 | Postes utilisateurs |
| DMZ | 192.168.2.0/24 | 255.255.255.0 | 192.168.2.1 | Serveurs exposés |
| Gestion | 192.168.3.0/24 | 255.255.255.0 | 192.168.3.1 | Administration IT |

### Serveurs Siège

| Serveur | IP fixe | Rôle |
|---------|---------|------|
| Windows Server (AD/DNS/DHCP) | 192.168.1.10 | Contrôleur de domaine |
| Serveur Web (Nginx + Flask) | 192.168.2.10 | Application Ymmo |
| Serveur BDD (PostgreSQL) | 192.168.2.11 | Base de données |
| Serveur de fichiers (NAS) | 192.168.1.11 | Stockage partagé |
| Routeur/Pare-feu | 192.168.1.1 | Passerelle principale |

### Agences (x12)

| Agence | Réseau | Plage IP | Tunnel VPN |
|--------|--------|----------|------------|
| Agence 01 — Paris | 10.1.1.0/24 | 10.1.1.1 - 10.1.1.254 | 10.0.0.1/30 |
| Agence 02 — Lyon | 10.1.2.0/24 | 10.1.2.1 - 10.1.2.254 | 10.0.0.5/30 |
| Agence 03 — Marseille | 10.1.3.0/24 | 10.1.3.1 - 10.1.3.254 | 10.0.0.9/30 |
| Agence 04 — Bordeaux | 10.1.4.0/24 | 10.1.4.1 - 10.1.4.254 | 10.0.0.13/30 |
| Agence 05 — Toulouse | 10.1.5.0/24 | 10.1.5.1 - 10.1.5.254 | 10.0.0.17/30 |
| Agence 06 — Nice | 10.1.6.0/24 | 10.1.6.1 - 10.1.6.254 | 10.0.0.21/30 |
| Agence 07 — Nantes | 10.1.7.0/24 | 10.1.7.1 - 10.1.7.254 | 10.0.0.25/30 |
| Agence 08 — Strasbourg | 10.1.8.0/24 | 10.1.8.1 - 10.1.8.254 | 10.0.0.29/30 |
| Agence 09 — Montpellier | 10.1.9.0/24 | 10.1.9.1 - 10.1.9.254 | 10.0.0.33/30 |
| Agence 10 — Lille | 10.1.10.0/24 | 10.1.10.1 - 10.1.10.254 | 10.0.0.37/30 |
| Agence 11 — Rennes | 10.1.11.0/24 | 10.1.11.1 - 10.1.11.254 | 10.0.0.41/30 |
| Agence 12 — Grenoble | 10.1.12.0/24 | 10.1.12.1 - 10.1.12.254 | 10.0.0.45/30 |

---

## 4. Configuration VPN IPSec Site-à-Site

```
Phase 1 (IKE) :
  - Algorithme de chiffrement : AES-256
  - Algorithme de hachage    : SHA-256
  - Groupe DH                : Group 14 (2048 bits)
  - Durée de vie SA          : 86400 secondes

Phase 2 (IPSec) :
  - Protocole                : ESP
  - Chiffrement              : AES-256
  - Authentification         : SHA-256
  - Mode                     : Tunnel
  - Durée de vie SA          : 3600 secondes
```

---

## 5. Active Directory & GPO

### Structure de l'annuaire

```
ymmo.local
├── OU=Siege
│   ├── OU=Direction
│   ├── OU=Commercial
│   ├── OU=Communication_Marketing
│   ├── OU=Administratif_RH_Juridique
│   └── OU=IT_Support
└── OU=Agences
    ├── OU=Agence_Paris
    ├── OU=Agence_Lyon
    └── ... (x12)
```

### GPO principales

| GPO | Cible | Description |
|-----|-------|-------------|
| GPO-MotDePasse | Tous | Longueur min 12 car., complexité obligatoire, expiration 90 jours |
| GPO-Firewall | Tous | Activation du pare-feu Windows, blocage ports inutiles |
| GPO-Verrouillage | Tous | Verrouillage après 5 tentatives échouées |
| GPO-MiseAJour | Tous | Mises à jour automatiques via WSUS |
| GPO-Restriction | Commerciaux | Blocage installation de logiciels |
| GPO-Bureau | Tous | Fond d'écran, raccourcis standardisés |

---

## 6. Matrice des droits d'accès

| Dossier partagé | Direction | Commercial | Com. & Marketing | Admin RH | IT Support |
|----------------|-----------|------------|------------------|----------|------------|
| Direction | Lecture/Écriture | Interdit | Interdit | Interdit | Interdit |
| Commercial | Lecture | Lecture/Écriture | Lecture | Interdit | Interdit |
| Communication | Lecture | Lecture | Lecture/Écriture | Interdit | Interdit |
| Administratif RH | Lecture | Interdit | Interdit | Lecture/Écriture | Interdit |
| IT et Support | Interdit | Interdit | Interdit | Interdit | Lecture/Écriture |

---

## 7. Politique de sécurité réseau

### Pare-feu (règles principales)

| Règle | Source | Destination | Port | Action |
|-------|--------|-------------|------|--------|
| HTTP/HTTPS public | Internet | DMZ Web | 80, 443 | Autoriser |
| BDD interne | DMZ Web | DMZ BDD | 5432 | Autoriser |
| VPN IPSec | Agences | Siège | 500, 4500 | Autoriser |
| AD/DNS interne | LAN | AD Server | 53, 389, 636 | Autoriser |
| SSH admin | IT only | Serveurs | 22 | Autoriser |
| Tout le reste | * | * | * | Bloquer |

### Segmentation réseau
- DMZ isolée du LAN interne par pare-feu
- Serveur BDD non accessible depuis Internet
- VLAN par département au siège
- Trafic inter-agences chiffré via VPN IPSec

---

## 8. Plan de sauvegarde

| Données | Fréquence | Type | Rétention | Destination |
|---------|-----------|------|-----------|-------------|
| Base de données | Quotidienne | Incrémentielle | 30 jours | NAS + Cloud |
| Base de données | Hebdomadaire | Complète | 3 mois | NAS + Cloud |
| Serveur de fichiers | Quotidienne | Incrémentielle | 30 jours | NAS |
| Serveur de fichiers | Hebdomadaire | Complète | 6 mois | Cloud |
| AD (sysvol/ntds) | Quotidienne | Complète | 1 mois | NAS |
| Config réseau | Mensuelle | Complète | 1 an | NAS |

**Règle 3-2-1 :** 3 copies, 2 supports différents, 1 hors site (cloud)

---

## 9. Solution Cloud proposée — Azure

| Service Azure | Usage | Justification |
|--------------|-------|---------------|
| Azure Virtual Machines | Hébergement app en production | Scalabilité, haute disponibilité |
| Azure SQL Database | BDD managée | Sauvegardes automatiques, réplication |
| Azure Blob Storage | Stockage photos annonces | Pas cher, CDN intégré |
| Azure Active Directory | SSO + MFA | Intégration AD on-premise |
| Azure Backup | Sauvegarde hors site | Conformité règle 3-2-1 |
| Azure VPN Gateway | Extension VPN vers cloud | Continuité si siège inaccessible |

**Coût estimé mensuel :** ~350-500 €/mois

---

## 10. Liste du matériel & budgétisation

### Siège

| Matériel | Quantité | Prix unitaire | Total |
|----------|----------|---------------|-------|
| Serveur Dell PowerEdge R540 | 2 | 3 500 € | 7 000 € |
| Switch manageable 48 ports | 2 | 800 € | 1 600 € |
| Pare-feu Fortinet FortiGate 100F | 1 | 2 500 € | 2 500 € |
| Routeur Cisco ISR 4321 | 1 | 1 800 € | 1 800 € |
| NAS Synology RS1221+ | 1 | 1 200 € | 1 200 € |
| Postes de travail | 30 | 900 € | 27 000 € |
| Imprimante réseau | 1 | 400 € | 400 € |
| **Sous-total Siège** | | | **41 500 €** |

### Par agence (x12)

| Matériel | Quantité | Prix unitaire | Total |
|----------|----------|---------------|-------|
| Routeur VPN (Cisco ISR 1100) | 1 | 600 € | 600 € |
| Switch 8 ports | 1 | 150 € | 150 € |
| Postes de travail | 5 | 900 € | 4 500 € |
| Imprimante réseau | 1 | 300 € | 300 € |
| **Sous-total par agence** | | | **5 550 €** |

### Total infrastructure

| Poste | Coût |
|-------|------|
| Siège | 41 500 € |
| 12 agences (12 × 5 550 €) | 66 600 € |
| Licences Windows Server (2 srv) | 3 200 € |
| Licences Windows 11 Pro (30+60) | 8 100 € |
| Microsoft 365 Business (90 users) | 1 620 €/an |
| Azure Cloud (1 an) | 4 800 €/an |
| **TOTAL** | **~125 820 €** |

---

## 11. Guide de déploiement (résumé)

### Étape 1 — Siège
1. Installer Windows Server 2022 sur les 2 serveurs
2. Configurer le contrôleur de domaine (AD DS, DNS, DHCP)
3. Joindre les postes au domaine `ymmo.local`
4. Appliquer les GPO
5. Configurer le pare-feu et les VLANs
6. Déployer l'application Ymmo sur le serveur web

### Étape 2 — Agences
1. Configurer le routeur VPN avec les paramètres IPSec
2. Tester le tunnel VPN vers le siège
3. Joindre les postes au domaine via VPN
4. Vérifier l'accès à l'application web

### Étape 3 — Cloud
1. Créer l'environnement Azure
2. Configurer Azure VPN Gateway
3. Tester la réplication BDD
4. Configurer les sauvegardes automatiques

---

## 12. Plan de supervision

| Outil | Usage |
|-------|-------|
| Zabbix | Supervision réseau et serveurs (CPU, RAM, disque) |
| Grafana | Tableaux de bord visuels |
| Windows Event Viewer | Logs AD et événements sécurité |
| Azure Monitor | Supervision cloud |

**Alertes configurées :**
- CPU > 85% pendant 5 min → alerte email
- Espace disque < 10% → alerte email
- Tunnel VPN down → alerte SMS
- Tentatives de connexion échouées > 10 → alerte sécurité