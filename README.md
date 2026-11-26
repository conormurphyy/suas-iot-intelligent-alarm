# Suas — IoT Intelligent Alarm

**Course:** ICA-1 IoT Development — 3rd Year, BSc (Hons) in Computing in Software Development, Dundalk Institute of Technology  
**Author:** Conor Murphy

---

## Overview

**Suas** (*Irish for "up"*) is a full-stack IoT smart alarm system designed to ensure users physically get out of bed in the morning. Rather than providing a snooze button on a phone screen, Suas pairs a cloud-hosted scheduling web application with a Raspberry Pi wired to an under-mattress pressure mat and buzzer. When a scheduled alarm triggers, the buzzer sounds continuously while weight is detected on the bed and only stops once the user physically steps off the mat.

---

## System Architecture

```text
+-------------------+        HTTPS         +----------------------------------------+
|  Web Browser /    | -------------------> |  AWS EC2 (Docker Compose)              |
|  Mobile PWA       |                      |  - Nginx + Cloudflare (suas.tech)      |
+-------------------+                      |  - FastAPI + Jinja2 Web App            |
                                           |  - SQLite Database + APScheduler       |
                                           |  - Eclipse Mosquitto MQTT Broker :1883 |
                                           +-------------------+--------------------+
                                                               |
                                                               | MQTT (alarm/trigger)
                                                               v
                                           +----------------------------------------+
                                           |  Raspberry Pi                          |
                                           |  - hardware/main.py (paho-mqtt)        |
                                           |  - NO Pressure Mat Switch (GPIO 17)    |
                                           |  - PWM Buzzer (GPIO 18)                |
                                           +----------------------------------------+
```

1. **Schedule:** A logged-in user creates, edits, or deletes alarms from the `/schedule` web interface.
2. **Persist & Queue:** FastAPI stores alarms in SQLite via SQLAlchemy and registers jobs in `APScheduler` (reloading active alarms automatically on server startup).
3. **Trigger:** At the scheduled time, `APScheduler` publishes `"on"` to the `alarm/trigger` MQTT topic via Eclipse Mosquitto.
4. **Enforce Wake-Up:** The Raspberry Pi receives the `alarm/trigger` message, sounds the PWM buzzer while the pressure mat switch is closed (user in bed), and stops the alarm once pressure is released (user out of bed).

---

## Features

- **User Authentication & Profiles:** Registration, login, logout, profile updates, and password changes secured with `bcrypt` password hashing and `PyJWT` tokens (`HttpOnly` cookies + OAuth2 `/api/users/token` endpoint).
- **Alarm Management Dashboard:** Overview dashboard with live clock, active alarm counts, next scheduled alarm card, and full CRUD alarm scheduling UI.
- **Cloud-to-Edge MQTT Messaging:** Authenticated Eclipse Mosquitto broker decoupling the AWS cloud backend from the local Raspberry Pi hardware.
- **Physical Pressure-Mat Enforcement:** `gpiozero` hardware loop monitoring bed occupancy in real time.
- **Automated Database Backups:** Rolling SQLite backup script (`scripts/backup_database.py`) with 14-day retention.

---

## Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Python 3.14, FastAPI, Uvicorn, APScheduler, Pydantic Settings |
| **Frontend** | Server-rendered HTML5, Jinja2 Templates, Gentelella v4 CSS/JS |
| **Database** | SQLite with SQLAlchemy ORM |
| **Authentication** | PyJWT (`HS256`) & `bcrypt` |
| **Messaging** | MQTT (Eclipse Mosquitto broker & `paho-mqtt` client) |
| **Hardware** | Raspberry Pi, `gpiozero` (`Button` & `PWMOutputDevice`) |
| **Deployment** | Docker & Docker Compose on AWS EC2, Nginx reverse proxy, Cloudflare HTTPS |

---

## Hardware Components

| Component | Description / Pin |
| :--- | :--- |
| **Raspberry Pi** | Runs the standalone MQTT + GPIO client (`hardware/main.py`) |
| **Normally Open (NO) Pressure Mat** | Connected to **GPIO 17** (`pull_up=True`) to detect whether the user is in bed |
| **Piezo Buzzer** | Connected to **GPIO 18** (`PWMOutputDevice`, 500 Hz) to sound the alarm |
| **Touchscreen / Display** *(optional)* | Local access to the web dashboard |

---

## Project Structure

```text
suas-iot-intelligent-alarm/
├── api/
│   ├── routes/
│   │   ├── alarm.py             # /api/alarms CRUD endpoints + scheduler hooks
│   │   ├── pages.py             # Jinja2 HTML routes (overview, schedule, profile, auth)
│   │   ├── readings.py          # /api/readings endpoints for sensor records
│   │   └── users.py             # /api/users CRUD + OAuth2 /token and /me endpoints
│   ├── services/
│   │   ├── alarm_scheduler.py   # APScheduler job management & alarm trigger
│   │   └── mqtt_client.py       # FastAPI MQTT client publishing to alarm/trigger
│   ├── auth.py                  # bcrypt hashing & JWT creation/verification
│   ├── config.py                # Environment settings (SECRET_KEY, token expiry)
│   ├── database.py              # SQLite engine & SQLAlchemy session dependency
│   ├── main.py                  # FastAPI entry point, static mounts & lifespan
│   ├── models.py                # SQLAlchemy models (User, Alarm, PressureMatReading)
│   ├── schemas.py               # Pydantic request/response schemas
│   └── pyproject.toml           # Python dependencies managed with uv
├── frontend/
│   ├── media/                   # User media assets
│   ├── static/                  # Stylesheets, icons, images & dashboard clock JS
│   └── templates/               # Jinja2 layouts and pages (index, schedule, profile, login, register)
├── hardware/
│   ├── main.py                  # Raspberry Pi MQTT subscriber + pressure mat/buzzer loop
│   ├── pressure_mat.py          # Standalone pressure mat test script
│   ├── alarm_buzzer.py          # Standalone buzzer test script
│   └── alarm_controller.py      # Local alarm controller helper
├── mosquitto/
│   └── config/mosquitto.conf    # Mosquitto broker listener & authentication config
├── scripts/
│   └── backup_database.py       # Automated SQLite backup script (14-day retention)
├── Dockerfile                   # FastAPI container build using uv
└── docker-compose.yml           # Multi-container stack (FastAPI API + Mosquitto)
```

---

## Setup & Running

### 1. Environment Variables

Copy `.env.example` to `.env` in the project root and set strong credentials:

```env
SECRET_KEY=replace-with-a-strong-random-secret
ACCESS_TOKEN_EXPIRE_MINUTES=60

MQTT_USERNAME=suas_user
MQTT_PASSWORD=replace-with-mqtt-password
```

Generate a Mosquitto password file matching `MQTT_USERNAME` and `MQTT_PASSWORD` at `mosquitto/config/passwordfile`, and ensure an empty SQLite file exists at `data/alarm.db` before first container startup:

```bash
mkdir -p data
touch data/alarm.db
```

### 2. Run Cloud Stack with Docker Compose (AWS EC2 / Local)

```bash
docker compose up -d --build
```

- **Web App & API:** `http://127.0.0.1:8000` (proxied via Nginx/Cloudflare in production)
- **Interactive API Docs:** `http://127.0.0.1:8000/docs`
- **MQTT Broker:** TCP port `1883` (ensure port `1883` is open to the Raspberry Pi in the EC2 Security Group)

### 3. Local Backend Development (Without Docker)

From the `api/` directory using [uv](https://docs.astral.sh/uv/):

```bash
cd api
uv sync
PYTHONPATH=.. uv run uvicorn api.main:app --reload --port 8000
```

### 4. Run the Raspberry Pi Client

On the Raspberry Pi, install `gpiozero`, `lgpio` (for Raspberry Pi 5), and `paho-mqtt`, then export the broker credentials and start `hardware/main.py`:

```bash
export MQTT_HOST="your-ec2-ip-or-domain"
export MQTT_USERNAME="suas_user"
export MQTT_PASSWORD="your-mqtt-password"

python3 hardware/main.py
```

---

## Potential Future Enhancements

- **Return-to-Bed Re-Trigger Window:** Keep monitoring the pressure mat for a configurable grace window after the alarm stops so the buzzer re-activates if the user gets back into bed.
- **Sleep Habit Logging:** Publish in-bed and out-of-bed timestamps from the Raspberry Pi over MQTT to populate historical sleep insights.
- **Custom Alarm Audio:** Play custom MP3 alarm tones through a speaker via `hardware/alarm_audio.py`.
- **Automated Smart Blinds:** Trigger a secondary wireless stepper-motor unit when the alarm fires to open bedroom blinds and expose the user to natural daylight.

---

## AI Usage Declaration

All AI assistance used during development is documented in [AI_CHAT_LOG.md](AI_CHAT_LOG.md).
