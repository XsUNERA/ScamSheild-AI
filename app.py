import json
import os
import time
from typing import List
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field
import streamlit as st

# 1. Load environment variables
load_dotenv()

# 2. Page Config
st.set_page_config(
    page_title="ScamShield AI - Rapid Response",
    page_icon="🛡️",
    layout="wide"
)

# --- UNIFIED PYDANTIC SCHEMA ---

class CompleteScamAnalysisSchema(BaseModel):
    threat_level: str = Field(
        description="Threat level classification: 'HIGH', 'MEDIUM', 'LOW', or 'SAFE'"
    )
    urgency_score: int = Field(
        description="Urgency score from 1 (Low) to 10 (Critical Emergency)"
    )
    scam_category: str = Field(
        description="Category e.g., Banking Fraud, Phishing, Tech Support, Romance, Ransomware, Safe"
    )
    immediate_assessment: str = Field(
        description="Concise 1-2 sentence executive assessment of the threat"
    )
    step_by_step_plan: List[str] = Field(
        description="Ordered list of immediate steps the user must take right now"
    )
    red_flags: List[str] = Field(
        description="Key fraud indicators identified in the situation"
    )
    critical_warnings: List[str] = Field(
        description="Crucial 'DO NOTs' (e.g., Do not share OTP, Do not click links)"
    )
    reporting_resources: List[str] = Field(
        description="Relevant authorities, banks, or incident reporting portals"
    )


# --- GROQ ENGINE FUNCTION ---

def analyze_scam_incident_groq(user_input: str):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("⚠️ GROQ_API_KEY missing! Add it to your .env file.")
        st.stop()

    client = Groq(api_key=api_key)

    # Prompt with embedded JSON schema requirement
    schema_json = json.dumps(CompleteScamAnalysisSchema.model_json_schema(), indent=2)

    prompt = f"""
    You are an expert Cybersecurity Triage & Emergency Incident Coordinator.
    Analyze the following situation, assess risk level, identify red flags, and formulate an immediate containment action plan.

    User Situation:
    "{user_input}"

    You MUST respond STRICTLY with a valid JSON object matching this schema structure:
    {schema_json}
    """

    # Call Groq with Llama 3.3 70B
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a specialized Cybersecurity Incident AI. You always output strict JSON matching the user's requested schema.",
            },
            {"role": "user", "content": prompt},
        ],
        model="openai/gpt-oss-20b",
        response_format={"type": "json_object"},
        temperature=0.1,
    )

    # Parse JSON directly into Pydantic
    raw_json = response.choices[0].message.content
    return CompleteScamAnalysisSchema.model_validate_json(raw_json)


# --- UI LAYOUT ---

st.title("🛡️ ScamShield AI (Powered by Groq ⚡)")
st.caption("AI-Powered Emergency Scam Triage & Rapid Incident Response System")

with st.sidebar:
    st.header("⚙️ System Status")
    has_key = bool(os.getenv("GROQ_API_KEY"))
    st.write(f"**Groq API Status:** {'✅ Ready' if has_key else '❌ Key Missing'}")

    st.markdown("---")
    demo_mode = st.toggle("🧪 Demo Mode (Offline)", value=False)
    if demo_mode:
        st.info("Demo Mode Active: Instant mock responses without API calls.")

    st.markdown("---")
    st.markdown("""
    ### ⚡ Engine Specs
    - **Provider:** Groq LPU Accelerator
    - **Model:** `openai/gpt-oss-20b`
    - **Response Time:** Sub-second execution
    """)

    if st.button("🔄 Reset App"):
        st.rerun()

st.subheader("Paste suspicious message, link, or describe what happened:")
user_text = st.text_area(
    "Message Input",
    placeholder="e.g., Received an SMS claiming my account was suspended with a link to restore access...",
    height=140,
    label_visibility="collapsed",
)

col1, _ = st.columns([1, 3])
with col1:
    submit_btn = st.button("🚨 Analyze Threat", type="primary", use_container_width=True)

if submit_btn:
    if not user_text.strip():
        st.warning("Please enter a description or paste a message before analyzing.")
    else:
        with st.spinner("⚡ Groq is analyzing threat and generating action plan..."):
            try:
                if demo_mode:
                    time.sleep(0.5)
                    analysis = CompleteScamAnalysisSchema(
                        threat_level="HIGH",
                        urgency_score=9,
                        scam_category="Banking Fraud / Smishing",
                        immediate_assessment="High-risk phishing attempt attempting to harvest banking credentials via SMS link.",
                        step_by_step_plan=[
                            "Do NOT click the link provided in the SMS.",
                            "Block the sender phone number immediately.",
                            "Contact bank customer service directly via their official number."
                        ],
                        red_flags=["Suspicious shortened URL", "Urgency pressure tactics", "Unknown sender number"],
                        critical_warnings=["Do not share OTPs", "Never type passwords into linked pages"],
                        reporting_resources=["Official Bank Fraud Hotline", "FTC ReportFraud"]
                    )
                else:
                    analysis = analyze_scam_incident_groq(user_text)

                st.markdown("---")

                # Metrics Summary Banner
                m1, m2, m3 = st.columns(3)
                level_formatting = {
                    "HIGH": "🔴 HIGH THREAT",
                    "MEDIUM": "🟠 MEDIUM THREAT",
                    "LOW": "🟡 LOW THREAT",
                    "SAFE": "🟢 SAFE / LIKELY LEGIT",
                }

                m1.metric("Threat Level", level_formatting.get(analysis.threat_level.upper(), analysis.threat_level))
                m2.metric("Urgency Score", f"{analysis.urgency_score} / 10")
                m3.metric("Scam Category", analysis.scam_category)

                st.info(f"**Executive Summary:** {analysis.immediate_assessment}")

                st.markdown("---")

                # Actionable Results Layout
                col_left, col_right = st.columns([3, 2])

                with col_left:
                    st.subheader("📋 Step-by-Step Action Plan")
                    for idx, step in enumerate(analysis.step_by_step_plan, 1):
                        st.markdown(f"**{idx}.** {step}")

                    st.markdown("---")
                    st.subheader("🏢 Reporting & Help Portals")
                    for portal in analysis.reporting_resources:
                        st.markdown(f"- {portal}")

                with col_right:
                    st.subheader("⚠️ Critical Warnings")
                    for warning in analysis.critical_warnings:
                        st.error(f"🛑 {warning}")

                    st.subheader("🚩 Detected Red Flags")
                    for flag in analysis.red_flags:
                        st.warning(f"• {flag}")

            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
