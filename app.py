import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Student Dropout Analytics",
    page_icon="🎓",
    layout="wide"
)

# 2. Advanced Premium Dark Theme CSS Injection (With Universal Spacing Fix)
st.markdown("""
    <style>
    /* Dark Theme Core Background & Typography */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    h1, h2, h3, p, label {
        color: #f1f5f9 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Title Customization */
    .main-title {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a78bfa, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    
    /* ADD MARGIN SPACING ON SUBHEADINGS */
    /* Adds explicit top margin padding to separate cards cleanly */
    .section-header {
        margin-top: 35px !important;
        margin-bottom: 15px !important;
    }
    
    /* Modern Glassmorphic Cards for Input Grouping */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
        background-color: #151c2c !important;
        border: 1px solid #243149 !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2) !important;
        margin-bottom: 20px;
    }
    
    /* COMPLETE FIX FOR NUMBER INPUT VISIBILITY */
    div[data-testid="stNumberInput"] div, 
    div[data-testid="stNumberInput"] input,
    div[data-baseweb="input"] {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border-color: #334155 !important;
    }
    
    /* Target increment/decrement step buttons inside number inputs */
    div[data-testid="stNumberInput"] button {
        background-color: #334155 !important;
        color: #f1f5f9 !important;
        border-color: #475569 !important;
    }
    
    /* UNIVERSAL CHROME FIX FOR SELECT BOX / DROPDOWN CONTAINER WHITE BACKGROUNDS */
    div[data-testid="stSelectbox"] div,
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] span,
    .stSelectbox > div > div {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border-color: #334155 !important;
    }
    
    /* Ensure the chevron dropdown icon stands out clearly in white */
    div[data-testid="stSelectbox"] svg {
        fill: #ffffff !important;
    }
    
    /* ---- FIX FOR SLIDER CONTAINER CLIPPING & EXTENSIONS ---- */
    div[data-testid="stSlider"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 14px 18px 18px 18px !important;
    }
    div[data-testid="stSlider"] div[role="slider"] {
        background-color: #8b5cf6 !important;
        border: 2px solid #a78bfa !important;
    }
    div[data-testid="stSlider"] [data-testid="stWidgetLabel"] p,
    div[data-testid="stSlider"] div {
        color: #ffffff !important;
    }
    
    /* High-contrast Action Button */
    button[kind="primary"] {
        background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 12px 0px !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
    }
    button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Load Model Components
@st.cache_resource
def load_model_components():
    model = joblib.load("dropout_model.pkl")
    scaler = joblib.load("scaler.pkl")
    feature_columns = joblib.load("feature_columns.pkl")
    return model, scaler, feature_columns

try:
    model, scaler, feature_columns = load_model_components()
except FileNotFoundError:
    st.error("Model framework components missing! Ensure pipeline pickle files match current active workspace directory.")
    st.stop()

# Header Layout
st.markdown("<h1 class='main-title'>🎓 Student Retention Intelligence Matrix</h1>", unsafe_allow_html=True)
st.write("Calibrate operational academic indicators below to evaluate risk probability factors.")
st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

# Form Wrap for clean organization
with st.form("retention_matrix_form"):
    
    # --- CARD 1: ACADEMIC PERFORMANCES ---
    st.markdown("<h3 class='section-header'>📚 Academic Pillars</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        current_gpa = st.number_input("Current Active GPA", 0.0, 10.0, 6.5)
        previous_gpa = st.number_input("Prior Term GPA", 0.0, 10.0, 6.5)
    with col2:
        attendance = st.slider("Attendance Rate (%)", 0.0, 100.0, 85.0)
        assignment = st.slider("Assignment Compliance (%)", 0.0, 100.0, 75.0)
    with col3:
        failed_subjects = st.number_input("Failed Subject Units", 0, 10, 0)
        previous_backlogs = st.number_input("Cumulative Backlogs", 0, 20, 0)
    with col4:
        participation = st.slider("Class Engagement Rate (%)", 0.0, 100.0, 70.0)
        study_hours = st.number_input("Weekly Self-Study Hours", 0.0, 168.0, 15.0)

    # --- CARD 2: BEHAVIORAL & LOGISTICAL FACTORS ---
    st.markdown("<h3 class='section-header'>⏱️ Engagement & Logistical Risk Metrics</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        lms_logins = st.number_input("LMS Portal Syncs / Week", 0, 200, 15)
        age = st.number_input("Age Counter", 15, 60, 20)
    with col2:
        late_submissions = st.number_input("Tardy Assignment Flags", 0, 50, 1)
    with col3:
        commute = st.number_input("Daily Commute (Minutes)", 0, 240, 30)
    with col4:
        extracurricular = st.number_input("Extracurricular Hours / Wk", 0.0, 100.0, 4.0)

    # --- CARD 3: SOCIAL, FAMILY & ECONOMIC INDEX ---
    st.markdown("<h3 class='section-header'>👤 Household & Welfare Indicators</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        financial_stress = st.slider("Financial Stress Index (1-10)", 1.0, 10.0, 4.0)
    with col2:
        sleep = st.number_input("Average Sleep Hours / Night", 0.0, 24.0, 7.2)
    with col3:
        internet = st.selectbox("Digital Access at Residence", ["Yes", "No"])
        scholarship = st.selectbox("Financially Scholarship Funded", ["Yes", "No"])
    with col4:
        academic_support = st.selectbox("Under Academic Mentorship", ["Yes", "No"])
        parent_education = st.selectbox("Highest Household Degree", ["Undergraduate", "Diploma", "Postgraduate", "School"])

    # Spacing before the button
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    
    # Execution Trigger Button
    submit_button = st.form_submit_button("🔮 Evaluate Retention Probability Vectors", type="primary")

# 4. Result Metrics Layout
if submit_button:
    # Build Input Object Mapping Framework Columns Exactly
    raw_input = pd.DataFrame({
        "Age": [age],
        "Attendance_Percentage": [attendance],
        "Previous_GPA": [previous_gpa],
        "Current_GPA": [current_gpa],
        "Failed_Subjects": [failed_subjects],
        "Assignment_Completion_Percentage": [assignment],
        "Study_Hours_Per_Week": [study_hours],
        "Late_Submissions": [late_submissions],
        "LMS_Logins_Per_Week": [lms_logins],
        "Class_Participation_Percentage": [participation],
        "Previous_Backlogs": [previous_backlogs],
        "Financial_Stress": [financial_stress],
        "Commute_Time_Minutes": [commute],
        "Internet_Access": [internet],
        "Scholarship": [scholarship],
        "Academic_Support": [academic_support],
        "Parent_Education": [parent_education],
        "Extracurricular_Hours_Per_Week": [extracurricular],
        "Sleep_Hours_Per_Night": [sleep]
    })
    
    # Hot-Encoding Execution
    encoded_input = pd.get_dummies(
        raw_input, 
        columns=["Internet_Access", "Scholarship", "Academic_Support", "Parent_Education"], 
        drop_first=True
    )
    encoded_input = encoded_input.reindex(columns=feature_columns, fill_value=0)
    scaled_features = scaler.transform(encoded_input)
    
    # Class Predictions Output Processing
    prediction = model.predict(scaled_features)[0]
    probabilities = model.predict_proba(scaled_features)[0]   # FIXED: Extracted single row slice array from matrix
    confidence = max(probabilities) * 100
    
    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
    out_col1, out_col2 = st.columns(2)
    
    with out_col1:
        st.subheader("🎯 Primary Determination")
        if prediction == "Low":
            st.markdown(
                '<div style="background-color: rgba(40, 167, 69, 0.15); color: #28a745; padding: 25px; '
                'border-radius: 12px; border: 1px solid #28a745; font-size: 22px; font-weight: bold; text-align: center;">'
                '🟢 LOW RISK PROFILE'
                '</div>', 
                unsafe_allow_html=True
            )
        elif prediction == "Medium":
            st.markdown(
                '<div style="background-color: rgba(255, 193, 7, 0.15); color: #ffc107; padding: 25px; '
                'border-radius: 12px; border: 1px solid #ffc107; font-size: 22px; font-weight: bold; text-align: center;">'
                '🟡 MODERATE RISK PROFILE'
                '</div>', 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div style="background-color: rgba(220, 53, 69, 0.15); color: #dc3545; padding: 25px; '
                'border-radius: 12px; border: 1px solid #dc3545; font-size: 22px; font-weight: bold; text-align: center;">'
                '🔴 CRITICAL DROPOUT RISK'
                '</div>', 
                unsafe_allow_html=True
            )
        st.markdown(f"<p style='text-align: center; color: #94a3b8; margin-top: 12px;'>Confidence Index: {confidence:.2f}%</p>", unsafe_allow_html=True)

    with out_col2:
        st.subheader("📊 Probability Metrics Index")
        
        prob_data = pd.DataFrame({
            "Risk Vector": model.classes_,
            "Certainty (%)": probabilities * 100
        }).sort_values(by="Certainty (%)", ascending=True)
        
        # Plotly dark theme chart display setup
        fig = px.bar(
            prob_data,
            x="Certainty (%)",
            y="Risk Vector",
            orientation="h",
            text="Certainty (%)",
            color="Certainty (%)",
            color_continuous_scale="Viridis"
        )
        
        fig.update_traces(
            texttemplate='%{text:.2f}%', 
            textposition='outside',
            textfont=dict(color="#f8fafc", size=12),
            marker_line_color='rgba(0,0,0,0)',
            marker_line_width=0
        )
        
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            xaxis=dict(
                showgrid=True, 
                gridcolor="#1e293b", 
                range=[0, 115], 
                title="", 
                tickfont=dict(color="#94a3b8")
            ),
            yaxis=dict(
                showgrid=False, 
                title="", 
                tickfont=dict(color="#f8fafc", size=13)
            ),
            margin=dict(l=10, r=40, t=10, b=10),
            height=180
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})




    






        
