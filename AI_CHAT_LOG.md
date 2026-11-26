# AI Chat Log

**Project:** SUAS IoT Intelligent Alarm
**Course:** ICA-1 IoT Development — 3rd Year, Dundalk Institute of Technology

Record of AI tools used during the development of this project.
Cline sessions used model **DeepSeek V4 Pro** (DeepSeek provider).

| Date | Tool | Summary | Branch |
|------|------|---------|--------|
| 2026-11-09 | Cline | Generated the frontend HTML pages (home/dashboard, profile, alarm schedule) reusing the existing Bootstrap template and styling | FastAPI_Dev |
| 2026-11-10 | Cline | Reviewed the API for errors | Hardware_Dev |
| 2026-11-10 | Cline | Debugged a 404 (Not Found) error causing a blank white page on load | Frontend_Dev |
| 2026-11-12 | Cline | Advised on what still needed to be implemented to complete the alarm application | Development |
| 2026-11-25 | Cline | Documented all Cline AI usage in `AI_CHAT_LOG.md` | FastAPI_Dev |
| 2026-11-25 | Cline | Fixed foundation issues: resolved `.gitignore` merge conflict, fixed Schedule page Edit/Delete buttons, wired live data into the Overview dashboard | FastAPI_Dev |
| 2026-11-25 | Antigravity (Gemini / Claude) | Added a minimal MQTT publisher (`api/services/mqtt_client.py`) started/stopped in the FastAPI lifespan; the alarm scheduler now publishes `on` to `alarm/trigger` instead of calling hardware code directly. Exposed Mosquitto port 1883 and passed MQTT credentials via environment variables in `docker-compose.yml` | FastAPI_Dev |
| 2026-11-25 | Antigravity (Gemini / Claude) | Removed unused `/analytics` navigation links; implemented simple JWT cookie authentication (`PyJWT`) and `bcrypt` password hashing (`api/services/auth.py`, `api/routes/auth.py`); built `login.html` and `register.html` reusing the existing Gentelella template; wired authenticated profile update and password change routes; enforced per-user ownership on alarms/users and added automated tests (`api/tests/test_auth_and_app.py`) | FastAPI_Dev |
| 2026-11-26 | Antigravity (Gemini) | Simplified custom frontend JavaScript: reduced `frontend/static/js/alarm-ui.js` to only the dashboard clock, simplified the alarm CRUD script in `schedule.html`, and switched `profile.html` to standard HTML form submissions | FastAPI_Dev |
| Not recorded | ChatGPT | https://chatgpt.com/share/6af35913-d410-83ed-a8f1-b7621ba5dc3d | — |

## Declaration

I declare that the AI tools listed above were used in the development of this
project as described, and that all AI-generated content was reviewed and adapted
by the developer before being committed to the project.

**Name:** Conor Murphy
**Date:** 2026-11-25

