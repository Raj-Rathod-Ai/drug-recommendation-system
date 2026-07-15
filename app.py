import streamlit as st
import utils

# Page configuration
st.set_page_config(
    page_title="Personalized Drug Recommendation Assistant",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Styling (Light & Dark theme compatible, responsive premium SaaS layout)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .saas-card {
        background: padding-box;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.15);
        margin-bottom: 2rem;
    }
    
    .progress-wrapper {
        margin-bottom: 2rem;
    }
    .progress-text {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #10B981;
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }
    
    .question-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        color: #1E293B;
    }
    .question-desc {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 2rem;
        transition: all 0.2s ease-in-out;
    }
    
    @media (prefers-color-scheme: dark) {
        .question-title {
            color: #F8FAFC;
        }
        .question-desc {
            color: #94A3B8;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "step" not in st.session_state:
    st.session_state.step = 1

# Answer storage
if "age" not in st.session_state:
    st.session_state.age = int(utils.DEFAULTS['Age'])

if "sex" not in st.session_state:
    st.session_state.sex = "Female"

if "bp" not in st.session_state:
    st.session_state.bp = "Normal"
if "bp_known" not in st.session_state:
    st.session_state.bp_known = True

if "cholesterol" not in st.session_state:
    st.session_state.cholesterol = "Normal"
if "cholesterol_known" not in st.session_state:
    st.session_state.cholesterol_known = True

if "na_to_k" not in st.session_state:
    st.session_state.na_to_k = float(utils.DEFAULTS['Na_to_K'])
if "na_to_k_known" not in st.session_state:
    st.session_state.na_to_k_known = True

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

def reset_wizard():
    st.session_state.step = 1
    st.session_state.age = int(utils.DEFAULTS['Age'])
    st.session_state.sex = "Female"
    st.session_state.bp = "Normal"
    st.session_state.bp_known = True
    st.session_state.cholesterol = "Normal"
    st.session_state.cholesterol_known = True
    st.session_state.na_to_k = float(utils.DEFAULTS['Na_to_K'])
    st.session_state.na_to_k_known = True

st.title("💊 Personalized Medication Advisor")
st.markdown("A patient-friendly assistant that suggests suitable therapies based on health factors.")

TOTAL_STEPS = 6
progress_percentage = int((st.session_state.step - 1) / TOTAL_STEPS * 100)

# Render Progress Bar
st.markdown(f"""
<div class="progress-wrapper">
    <div class="progress-text">
        <span>Question {min(st.session_state.step, TOTAL_STEPS)} of {TOTAL_STEPS}</span>
        <span>{progress_percentage}% Complete</span>
    </div>
</div>
""", unsafe_allow_html=True)
st.progress(progress_percentage / 100.0)

st.markdown('<div class="saas-card">', unsafe_allow_html=True)

if st.session_state.step == 1:
    st.markdown('<div class="question-title">Step 1: Your Age</div>', unsafe_allow_html=True)
    st.markdown('<div class="question-desc">How old are you? (Medication dosages and recommendations adapt based on age bracket)</div>', unsafe_allow_html=True)
    
    age = st.number_input(
        "Age (in years)",
        min_value=int(utils.VALIDATION_LIMITS['Age']['min']),
        max_value=int(utils.VALIDATION_LIMITS['Age']['max']),
        value=st.session_state.age,
        step=1
    )
    st.session_state.age = age
    
    col1, col2 = st.columns([1, 4])
    with col2:
        st.button("Next Question →", on_click=next_step, type="primary")

elif st.session_state.step == 2:
    st.markdown('<div class="question-title">Step 2: Biological Sex</div>', unsafe_allow_html=True)
    st.markdown('<div class="question-desc">What is your biological sex?</div>', unsafe_allow_html=True)
    
    sex = st.selectbox(
        "Biological Sex",
        options=["Female", "Male"],
        index=0 if st.session_state.sex == "Female" else 1
    )
    st.session_state.sex = sex
    
    col1, col2 = st.columns([1, 4])
    with col1:
        st.button("← Back", on_click=prev_step)
    with col2:
        st.button("Next Question →", on_click=next_step, type="primary")

elif st.session_state.step == 3:
    st.markdown('<div class="question-title">Step 3: Blood Pressure Level</div>', unsafe_allow_html=True)
    st.markdown('<div class="question-desc">Do you know your recent blood pressure reading category?</div>', unsafe_allow_html=True)
    
    known = st.checkbox("I know my blood pressure reading", value=st.session_state.bp_known)
    st.session_state.bp_known = known
    
    if known:
        bp = st.selectbox(
            "Blood Pressure Level",
            options=["Normal", "Low", "High"],
            index=["Normal", "Low", "High"].index(st.session_state.bp)
        )
        st.session_state.bp = bp
    else:
        st.info("Using standard medical default baseline: **Normal**")
        st.session_state.bp = "Normal"
        
    col1, col2 = st.columns([1, 4])
    with col1:
        st.button("← Back", on_click=prev_step)
    with col2:
        st.button("Next Question →", on_click=next_step, type="primary")

elif st.session_state.step == 4:
    st.markdown('<div class="question-title">Step 4: Cholesterol Level</div>', unsafe_allow_html=True)
    st.markdown('<div class="question-desc">Do you know your typical cholesterol reading category?</div>', unsafe_allow_html=True)
    
    known = st.checkbox("I know my cholesterol reading", value=st.session_state.cholesterol_known)
    st.session_state.cholesterol_known = known
    
    if known:
        cholesterol = st.selectbox(
            "Cholesterol Level",
            options=["Normal", "High"],
            index=["Normal", "High"].index(st.session_state.cholesterol)
        )
        st.session_state.cholesterol = cholesterol
    else:
        st.info("Using standard medical default baseline: **Normal**")
        st.session_state.cholesterol = "Normal"
        
    col1, col2 = st.columns([1, 4])
    with col1:
        st.button("← Back", on_click=prev_step)
    with col2:
        st.button("Next Question →", on_click=next_step, type="primary")

elif st.session_state.step == 5:
    st.markdown('<div class="question-title">Step 5: Sodium-to-Potassium Ratio</div>', unsafe_allow_html=True)
    st.markdown('<div class="question-desc">Do you know your biological Sodium-to-Potassium Ratio (Na_to_K)?</div>', unsafe_allow_html=True)
    
    known = st.checkbox("I know my Sodium-to-Potassium ratio", value=st.session_state.na_to_k_known)
    st.session_state.na_to_k_known = known
    
    if known:
        na_to_k = st.number_input(
            "Sodium-to-Potassium Ratio (Na_to_K)",
            min_value=utils.VALIDATION_LIMITS['Na_to_K']['min'],
            max_value=utils.VALIDATION_LIMITS['Na_to_K']['max'],
            value=st.session_state.na_to_k if st.session_state.na_to_k is not None else utils.DEFAULTS['Na_to_K'],
            step=utils.VALIDATION_LIMITS['Na_to_K']['step']
        )
        st.session_state.na_to_k = na_to_k
    else:
        st.info(f"Using default median value for medical calculations: **{utils.DEFAULTS['Na_to_K']:.2f}**")
        st.session_state.na_to_k = None
        
    col1, col2 = st.columns([1, 4])
    with col1:
        st.button("← Back", on_click=prev_step)
    with col2:
        st.button("Review Summary →", on_click=next_step, type="primary")

elif st.session_state.step == 6:
    st.markdown('<div class="question-title">Summary of Patient Profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="question-desc">Review details before retrieving recommended medication suggestions.</div>', unsafe_allow_html=True)
    
    show_bp = st.session_state.bp if st.session_state.bp_known else "Unknown (using Normal)"
    show_chol = st.session_state.cholesterol if st.session_state.cholesterol_known else "Unknown (using Normal)"
    show_nak = f"{st.session_state.na_to_k:.2f}" if st.session_state.na_to_k_known else "Unknown (using baseline)"
    
    st.markdown(f"""
    | Medical Indicator | Your Answer |
    | :--- | :--- |
    | **Patient Age** | {st.session_state.age} years |
    | **Biological Sex** | {st.session_state.sex} |
    | **Blood Pressure Level** | {show_bp} |
    | **Cholesterol Level** | {show_chol} |
    | **Sodium-to-Potassium Ratio** | {show_nak} |
    """, unsafe_allow_html=True)
    
    st.write("")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        st.button("← Back", on_click=prev_step)
    with col2:
        predict_clicked = st.button("💊 Determine Best Drug", type="primary")
        
    if predict_clicked:
        try:
            with st.spinner("Analyzing parameters against medical templates..."):
                drug, confidence = utils.predict_drug(
                    st.session_state.age,
                    st.session_state.sex,
                    st.session_state.bp.upper(),
                    st.session_state.cholesterol.upper(),
                    st.session_state.na_to_k
                )
            
            # Map drug codes to patient-friendly names
            friendly_drug = drug.replace("drug", "Medication ")
            
            # Custom styled output
            st.write("")
            st.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.1); border-left: 5px solid #10B981; padding: 1.5rem; border-radius: 8px; margin-top: 1rem;">
                <h4 style="color: #10B981; margin: 0 0 0.5rem 0;">Recommended Treatment Plan</h4>
                <p style="font-size: 2.2rem; font-weight: 700; color: #047857; margin: 0;">{friendly_drug}</p>
                <div style="margin-top: 0.5rem; font-weight: 600; font-size: 1.05rem; color: #065F46;">
                    Confidence Score: {confidence:.1f}%
                </div>
                <p style="font-size: 0.95rem; color: #065F46; margin: 0.5rem 0 0 0; line-height: 1.5;">
                    Based on the patient's demographics, blood pressure profile, cholesterol baseline, and electrolytes ratio, <b>{friendly_drug}</b> is the recommended therapeutic route.
                </p>
                <div style="margin-top: 1rem; padding: 0.5rem; background: rgba(245, 158, 11, 0.1); border: 1px dashed #F59E0B; border-radius: 6px; font-size: 0.85rem; color: #B45309; text-align: center;">
                    ⚠️ DISCLAIMER: This is a decision-support demonstration tool. Consult a qualified physician before taking any medication.
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
        except Exception as e:
            st.error(f"Prediction failed: {e}")
            
    st.write("")
    st.button("🔄 Restart Assessment", on_click=reset_wizard)

st.markdown('</div>', unsafe_allow_html=True)
