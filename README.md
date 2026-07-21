# 🛡️ ScamShield AI — Rapid Response & Scam Triage Agent

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini%202.5-4285F4.svg)](https://ai.google.dev/)
[![Groq](https://img.shields.io/badge/LLM-Groq%20Llama%203-f36e00.svg)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**ScamShield AI** is an intelligent, real-time cybersecurity triage engine designed to help users identify, evaluate, and mitigate online fraud, phishing emails, smishing SMS, and financial social engineering attacks in seconds.

Powered by **Google Gemini** and **Groq** LLMs coupled with **Pydantic** structured schema validation, ScamShield AI delivers high-precision risk scoring, red flag analysis, and immediate step-by-step containment strategies.

---

## 🌟 Key Features

- 🚨 **Instant Threat Triage:** Classifies incoming messages into `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW` threat levels.
- ⏱️ **Urgency & Risk Scoring:** Quantifies risk on a strict 1–10 scale based on psychological manipulation cues (urgency, fear, greed, isolation).
- 🚩 **Red Flag Extraction:** Identifies specific indicators of fraud (spoofed URLs, impersonation patterns, pressure tactics, unverified payment links).
- 📋 **Automated Incident Response Plan:** Generates custom containment action items (e.g., card freezing, password resetting, reporting portals).
- 🏢 **Escalation & Official Reporting:** Links directly to bank anti-fraud desks and cybercrime reporting channels.
- 🔒 **Privacy & Safety First:** Zero persistence of sensitive personal data; designed for rapid client-side inspection.

---

## 🏗️ System Architecture

```text
┌─────────────────────────┐
│     User Input (UI)     │  <-- Raw SMS / Phishing Email / Message
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Streamlit Frontend App  │  <-- app.py (Session state, environment checks)
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Agent Triage Engine   │  <-- Gemini 2.5 / Groq Llama 3 with Pydantic Schema
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Structured Scam Analysis│  <-- Threat Level, Urgency Score, Red Flags, Action Plan
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Response Dashboard (UI) │  <-- Visual threat badges, actionable guidance, export
└─────────────────────────┘

