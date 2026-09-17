import streamlit as st
from datetime import date, time, datetime

from agent import daily_brief, llm_answer
from data import SCENARIO_START, SCENARIO_END


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Executive Productivity Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #f6f8fc;
    }

    .main .block-container {
        max-width: 1280px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3 {
        color: #18254f !important;
        letter-spacing: -0.5px;
    }

    h1 {
        font-size: 2.8rem !important;
        font-weight: 750 !important;
        margin-bottom: 0.15rem !important;
    }

    h2 {
        font-size: 1.9rem !important;
        font-weight: 700 !important;
    }

    h3 {
        font-size: 1.45rem !important;
        font-weight: 700 !important;
    }

    p, span, label, div {
        font-family: Inter, -apple-system, BlinkMacSystemFont,
                     "Segoe UI", sans-serif;
    }


    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #eef2ff 0%,
            #f5f7ff 55%,
            #f8f9fc 100%
        );
        border-right: 1px solid #e2e6f0;
    }

    section[data-testid="stSidebar"] h2 {
        color: #18254f !important;
        font-size: 1.2rem !important;
        margin-bottom: 1.2rem !important;
    }

    section[data-testid="stSidebar"] label {
        color: #475569 !important;
        font-weight: 600 !important;
    }


    /* ---------- HERO ---------- */

    .hero {
        background: linear-gradient(
            135deg,
            #eef2ff 0%,
            #f8f7ff 48%,
            #eef8ff 100%
        );
        border: 1px solid #e2e7f3;
        border-radius: 22px;
        padding: 28px 32px;
        margin-bottom: 30px;
        box-shadow: 0 8px 28px rgba(30, 45, 90, 0.06);
    }

    .hero-title {
        font-size: 2.75rem;
        font-weight: 800;
        color: #18254f;
        line-height: 1.1;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        color: #64748b;
        font-size: 1.02rem;
        margin-bottom: 18px;
    }

    .hero-line {
        height: 4px;
        width: 72px;
        border-radius: 20px;
        background: linear-gradient(
            90deg,
            #5865f2,
            #8b5cf6,
            #38bdf8
        );
    }


    /* ---------- SECTION LABEL ---------- */

    .section-kicker {
        color: #64748b;
        font-size: 0.76rem;
        font-weight: 750;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 5px;
    }


    /* ---------- METRIC CARDS ---------- */

    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e7f0;
        border-radius: 17px;
        padding: 21px 22px;
        min-height: 120px;
        box-shadow: 0 5px 18px rgba(30, 45, 90, 0.055);
        position: relative;
        overflow: hidden;
    }

    .metric-card::before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 5px;
        border-radius: 17px 0 0 17px;
    }

    .metric-blue::before {
        background: #5865f2;
    }

    .metric-purple::before {
        background: #8b5cf6;
    }

    .metric-amber::before {
        background: #f59e0b;
    }

    .metric-red::before {
        background: #ef4444;
    }

    .metric-icon {
        font-size: 1.15rem;
        margin-bottom: 6px;
    }

    .metric-label {
        color: #64748b;
        font-size: 0.82rem;
        font-weight: 650;
        margin-bottom: 4px;
    }

    .metric-value {
        color: #172554;
        font-size: 2rem;
        font-weight: 800;
        line-height: 1;
    }


    /* ---------- CARD CONTENT ---------- */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px !important;
        border-color: #e0e5ef !important;
        background: #ffffff !important;
        box-shadow: 0 4px 16px rgba(30, 45, 90, 0.04);
    }


    /* ---------- STATUS BADGES ---------- */

    .status-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 750;
        letter-spacing: 0.4px;
        margin-right: 7px;
        margin-bottom: 8px;
    }

    .status-overdue {
        background: #fee2e2;
        color: #b91c1c;
    }

    .status-review {
        background: #fef3c7;
        color: #92400e;
    }

    .status-confirmed {
        background: #dcfce7;
        color: #166534;
    }

    .status-waiting {
        background: #ede9fe;
        color: #6d28d9;
    }

    .status-unconfirmed {
        background: #fef3c7;
        color: #92400e;
    }

    .priority-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 750;
        background: #eef2ff;
        color: #4338ca;
        letter-spacing: 0.3px;
    }


    /* ---------- ACTION TITLE ---------- */

    .action-title {
        font-size: 1.04rem;
        font-weight: 750;
        color: #172554;
        margin-bottom: 10px;
    }

    .field-label {
        color: #64748b;
        font-size: 0.76rem;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        margin-bottom: 2px;
    }

    .field-value {
        color: #24324f;
        font-size: 0.94rem;
        font-weight: 600;
    }


    /* ---------- SPECIAL WARNING CARDS ---------- */

    .ownership-note {
        background: #fffbeb;
        border: 1px solid #fde68a;
        border-left: 4px solid #f59e0b;
        border-radius: 10px;
        padding: 13px 15px;
        color: #92400e;
        font-size: 0.87rem;
        line-height: 1.45;
        margin: 10px 0 12px 0;
    }

    .overdue-box {
        background: #fff5f5;
        border: 1px solid #fecaca;
        border-left: 4px solid #ef4444;
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 10px;
    }

    .overdue-title {
        color: #991b1b;
        font-weight: 750;
        font-size: 0.95rem;
    }

    .overdue-status {
        color: #b91c1c;
        font-size: 0.82rem;
        margin-top: 3px;
    }


    /* ---------- ASK THE AGENT ---------- */

    .agent-header {
        background: linear-gradient(
            135deg,
            #eef2ff,
            #f5f3ff
        );
        border: 1px solid #dddff7;
        border-radius: 18px;
        padding: 20px 22px;
        margin-top: 8px;
        margin-bottom: 14px;
    }

    .agent-title {
        font-size: 1.35rem;
        font-weight: 750;
        color: #18254f;
    }

    .agent-description {
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 4px;
    }


    /* ========================================================
       CLICKABLE QUESTION BUTTONS
       ======================================================== */

    .question-buttons {
        margin-top: 4px;
        margin-bottom: 14px;
    }

    .question-buttons div[data-testid="stButton"] > button {
        background: #ffffff !important;
        color: #334155 !important;
        border: 1px solid #dfe4ef !important;
        border-radius: 999px !important;
        padding: 8px 14px !important;
        min-height: 40px !important;
        height: auto !important;
        font-size: 0.80rem !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 7px rgba(30, 45, 90, 0.035) !important;
        transition: all 0.18s ease !important;
        white-space: nowrap !important;
    }

    .question-buttons div[data-testid="stButton"] > button:hover {
        background: #eef2ff !important;
        border-color: #a5b4fc !important;
        color: #3730a3 !important;
        transform: translateY(-1px);
        box-shadow: 0 5px 12px rgba(79, 70, 229, 0.10) !important;
    }

    .question-buttons div[data-testid="stButton"] > button:active {
        transform: translateY(0);
    }


    /* ---------- CHAT ---------- */

    div[data-testid="stChatMessage"] {
        border-radius: 15px;
    }

    div[data-testid="stChatInput"] {
        margin-top: 8px;
    }


    /* ---------- DIVIDER ---------- */

    hr {
        border-color: #e3e7ef !important;
        margin: 34px 0 !important;
    }


    /* ---------- EXPANDER ---------- */

    div[data-testid="stExpander"] {
        border: 1px solid #e2e7ef !important;
        border-radius: 11px !important;
        background: #fafbfe !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR — SCENARIO
# ============================================================

with st.sidebar:
    st.markdown("## Scenario")

    scenario_date = st.date_input(
        "Date",
        value=date(2026, 9, 23),
        min_value=SCENARIO_START,
        max_value=SCENARIO_END,
    )

    scenario_time = st.time_input(
        "Time",
        value=time(9, 0),
    )

    scenario_dt = datetime.combine(
        scenario_date,
        scenario_time
    )


# ============================================================
# GET BRIEF
# ============================================================

brief = daily_brief(scenario_dt)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">Executive Productivity Agent</div>
        <div class="hero-line"></div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DAILY ACTION BRIEF
# ============================================================

st.markdown(
    '<div class="section-kicker">Overview</div>',
    unsafe_allow_html=True,
)

st.header("Daily Action Brief")


# ============================================================
# METRICS
# ============================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        f"""
        <div class="metric-card metric-blue">
            <div class="metric-icon">✓</div>
            <div class="metric-label">MY ACTIONS</div>
            <div class="metric-value">{len(brief["my_actions"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        f"""
        <div class="metric-card metric-purple">
            <div class="metric-icon">◷</div>
            <div class="metric-label">WAITING ON OTHERS</div>
            <div class="metric-value">{len(brief["waiting"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m3:
    st.markdown(
        f"""
        <div class="metric-card metric-amber">
            <div class="metric-icon">!</div>
            <div class="metric-label">UNCLEAR OWNERSHIP</div>
            <div class="metric-value">{len(brief["unclear"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m4:
    st.markdown(
        f"""
        <div class="metric-card metric-red">
            <div class="metric-icon">⚠</div>
            <div class="metric-label">OVERDUE</div>
            <div class="metric-value">{len(brief["overdue"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# HELPER — STATUS BADGE
# ============================================================

def status_badge(status):
    status_lower = status.lower()

    if "overdue" in status_lower:
        return '<span class="status-badge status-overdue">● OVERDUE</span>'

    if "review pending" in status_lower:
        return '<span class="status-badge status-review">● REVIEW PENDING</span>'

    if "review scheduled" in status_lower:
        return '<span class="status-badge status-review">● REVIEW SCHEDULED</span>'

    if "confirmed" in status_lower:
        return '<span class="status-badge status-confirmed">● CONFIRMED</span>'

    if "waiting" in status_lower:
        return '<span class="status-badge status-waiting">● WAITING</span>'

    if "unconfirmed" in status_lower:
        return '<span class="status-badge status-unconfirmed">● OWNER UNCONFIRMED</span>'

    return '<span class="status-badge status-waiting">● PENDING</span>'


# ============================================================
# MY ACTIONS
# ============================================================

st.subheader("My Actions")

if brief["my_actions"]:

    for a in brief["my_actions"]:

        with st.container(border=True):

            st.markdown(
                f'<div class="action-title">{a["title"]}</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                status_badge(a["status"])
                + f'<span class="priority-badge">{a["priority"].upper()} PRIORITY</span>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div style="margin-top:10px;">
                    <div class="field-label">Deadline</div>
                    <div class="field-value">{a["deadline_label"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander("Evidence"):
                for e in a["evidence"]:
                    st.write("• " + e)

else:
    st.info("No current action is classified as mine.")


# ============================================================
# WAITING ON OTHERS
# ============================================================

st.subheader("Waiting on Others")

if brief["waiting"]:

    for a in brief["waiting"]:

        with st.container(border=True):

            st.markdown(
                f'<div class="action-title">{a["title"]}</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<span class="status-badge status-waiting">● WAITING ON OTHERS</span>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div style="margin-top:8px;">
                    <div class="field-label">Waiting on</div>
                    <div class="field-value">{a["waiting_on"]}</div>
                </div>

                <div style="margin-top:11px;">
                    <div class="field-label">Expected</div>
                    <div class="field-value">{a["deadline_label"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div style="margin-top:11px;">
                    <div class="field-label">Status</div>
                    <div class="field-value">{a["status"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander("Evidence"):
                for e in a["evidence"]:
                    st.write("• " + e)

else:
    st.info("No unresolved waiting item.")


# ============================================================
# UNCLEAR OWNERSHIP
# ============================================================

if brief["unclear"]:

    st.subheader("Unclear Ownership")

    for a in brief["unclear"]:

        with st.container(border=True):

            st.markdown(
                f'<div class="action-title">{a["title"]}</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<span class="status-badge status-unconfirmed">● OWNER UNCONFIRMED</span>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div style="margin-top:8px;">
                    <div class="field-label">Deadline</div>
                    <div class="field-value">{a["deadline_label"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <div class="ownership-note">
                    Ownership is not confirmed in the supplied data.
                    The agent does not assign an owner by assumption.
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander("Evidence"):
                for e in a["evidence"]:
                    st.write("• " + e)


# ============================================================
# OVERDUE
# ============================================================

if brief["overdue"]:

    st.subheader("Overdue")

    for a in brief["overdue"]:

        st.markdown(
            f"""
            <div class="overdue-box">
                <div class="overdue-title">
                    ⚠ {a["title"]}
                </div>
                <div class="overdue-status">
                    {a["status"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# ASK THE AGENT
# ============================================================

st.divider()

st.markdown(
    """
    <div class="agent-header">
        <div class="agent-title">🤖 Ask the Agent</div>
        
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CLICKABLE EXAMPLE QUESTIONS
# ============================================================

questions = [
    "What did I promise Raghav?",
    "What is overdue?",
    "What am I waiting on?",
    "What needs action today?",
    "What has unclear ownership?",
]

st.markdown(
    '<div class="section-kicker">Try asking</div>',
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# IMPORTANT:
# These are REAL Streamlit buttons.
# Clicking one immediately runs the corresponding query.
# ------------------------------------------------------------

selected_question = None

st.markdown(
    '<div class="question-buttons">',
    unsafe_allow_html=True,
)

qcols = st.columns(5)

for i, q in enumerate(questions):
    with qcols[i]:
        if st.button(
            q,
            key=f"example_question_{i}",
            use_container_width=True,
        ):
            selected_question = q

st.markdown(
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# CHAT INPUT
# ============================================================

typed_question = st.chat_input(
    "Ask anything about your work..."
)


# ============================================================
# DETERMINE QUESTION
# ============================================================

# If the user clicked an example question, use that.
# Otherwise use whatever they typed in the chat box.

question = selected_question if selected_question else typed_question


# ============================================================
# CHAT RESPONSE
# ============================================================

if question:

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):

        with st.spinner("Analyzing your work..."):

            answer = llm_answer(
                question,
                scenario_dt
            )

        st.markdown(answer)