# Suas - IoT Intelligent Alarm
---

## Project Overview
A full-stack IoT Alarm that uses a monitoring system to enforce users waking up in the morning by continously sounding an alarm until the user physically gets out of their bed. Developed for ICA-1 IoT Development, 3rd Year, Dundalk Institute of Technology.

Users can set their alarm schedule in a web application & PWA. The system will also track time in bed and time out of bed across mutiple days/weeks creating data that the user can access. This could also be used as a tool to improve sleep habits. When the alarm goes off and the user gets out of bed they may want to get back into bed if the alarm stops, if this occurs and the pressure mat senses pressure after the alarm goes off after a certain time window the alarm will go off again.
## Tech Stack

Frontend: FastAPI template

Backend: FastAPI

Database: MySQL

Cloud: AWS

## Hardware

Raspberry Pi

Normally Open(NO) Pressure Mat Switch

Touchscreen

Buzzer or Speaker for Custom Alarm Sounds

## Potential Addon Features

Potentially creating a secondary device with a step motor to open blinds. When the alarm goes off it could trigger the blinds to open assisting the user in waking up and exposing them to daylight. If this feature was to be incopirated I would also need a stepper motor and create something to house the motor. Another consideration is if the motor would be controlled wirelessly or with wired. If it where wired it may cause potential issues.




