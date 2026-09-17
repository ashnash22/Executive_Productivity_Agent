import streamlit as st
from datetime import date, time, datetime

from agent import daily_brief, llm_answer
from data import SCENARIO_START, SCENARIO_END


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Executive Productivity Agent",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    .stApp { background: #f7f8fc; }

    .main .block-container {
        max-width: 1420px;
        padding-top: 1.25rem;
        padding-bottom: 3.5rem;
    }

    h1, h2, h3 {
        color: #172554 !important;
        letter-spacing: -0.4px;
    }

    p, span, label, div {
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background: #fbfbfe;
        border-right: 1px solid #e4e7ef;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 4px 4px 17px;
        border-bottom: 1px solid #e8eaf1;
        margin-bottom: 16px;
    }

    .brand-icon {
        width: 34px;
        height: 34px;
        border-radius: 10px;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
    }

    .brand-title {
        color: #172554;
        font-size: .9rem;
        font-weight: 800;
        line-height: 1.1;
    }

    .brand-subtitle {
        color: #94a3b8;
        font-size: .66rem;
        margin-top: 3px;
    }

    .nav-label {
        color: #94a3b8;
        font-size: .66rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin: 14px 4px 7px;
    }

    .nav-item {
        color: #64748b;
        font-size: .81rem;
        font-weight: 650;
        padding: 8px 10px;
        border-radius: 9px;
        margin-bottom: 3px;
    }

    .nav-item-active {
        background: #eef2ff;
        color: #3730a3;
        font-weight: 750;
    }

    .scenario-box {
        background: #f8f9ff;
        border: 1px solid #e3e7f2;
        border-radius: 13px;
        padding: 12px;
        margin-top: 15px;
    }

    /* TOP BAR */
    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 13px;
    }

    .eyebrow {
        color: #64748b;
        font-size: .7rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }

    .date-pill {
        background: #fff;
        border: 1px solid #e1e5ee;
        color: #475569;
        border-radius: 999px;
        padding: 6px 11px;
        font-size: .72rem;
        font-weight: 650;
    }

    /* HERO */
    .hero {
        background: linear-gradient(115deg, #eef2ff, #f8f7ff 55%, #edf8ff);
        border: 1px solid #e0e5f1;
        border-radius: 19px;
        padding: 24px 28px 22px;
        margin-bottom: 18px;
        box-shadow: 0 7px 24px rgba(30,45,90,.045);
    }

    .hero-kicker {
        color: #6366f1;
        font-size: .68rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.15px;
        margin-bottom: 7px;
    }

    .hero-title {
        color: #172554;
        font-size: 2.15rem;
        font-weight: 850;
        line-height: 1.12;
        margin-bottom: 9px;
    }

    .hero-context {
        color: #64748b;
        font-size: .8rem;
        line-height: 1.45;
    }

    .hero-line {
        width: 74px;
        height: 4px;
        border-radius: 999px;
        background: linear-gradient(90deg, #4f46e5, #7c3aed, #38bdf8);
        margin-top: 14px;
    }

    /* SECTIONS */
    .section-kicker {
        color: #94a3b8;
        font-size: .66rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.25px;
        margin-bottom: 3px;
    }

    .section-title {
        color: #172554;
        font-size: 1.28rem;
        font-weight: 820;
        margin-bottom: 11px;
    }

    /* METRICS */
    .metric-card {
        background: #fff;
        border: 1px solid #e1e5ee;
        border-radius: 14px;
        min-height: 101px;
        padding: 15px 17px;
        box-shadow: 0 4px 15px rgba(30,45,90,.045);
        position: relative;
        overflow: hidden;
    }

    .metric-card:before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
    }

    .metric-blue:before { background: #4f46e5; }
    .metric-purple:before { background: #7c3aed; }
    .metric-amber:before { background: #f59e0b; }
    .metric-red:before { background: #ef4444; }

    .metric-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }

    .metric-label {
        color: #64748b;
        font-size: .67rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: .75px;
    }

    .metric-icon {
        width: 27px;
        height: 27px;
        border-radius: 8px;
        background: #f1f5f9;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: .8rem;
    }

    .metric-value {
        color: #172554;
        font-size: 1.75rem;
        font-weight: 850;
        line-height: 1;
    }

    /* PRIORITY */
    .priority-banner {
        background: linear-gradient(100deg, #171d4d, #24276a);
        border-radius: 14px;
        padding: 13px 17px;
        color: #fff;
        margin: 15px 0 22px;
        box-shadow: 0 8px 22px rgba(24,37,84,.12);
    }

    .priority-label {
        color: #c7d2fe;
        font-size: .63rem;
        font-weight: 850;
        text-transform: uppercase;
        letter-spacing: 1.1px;
        margin-bottom: 3px;
    }

    .priority-title {
        font-size: .92rem;
        font-weight: 780;
    }

    .priority-meta {
        color: #cbd5e1;
        font-size: .69rem;
        margin-top: 2px;
    }

    /* CARDS */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 13px !important;
        border-color: #e1e5ee !important;
        background: #fff !important;
        box-shadow: 0 3px 13px rgba(30,45,90,.035);
    }

    .action-title {
        color: #172554;
        font-size: .91rem;
        font-weight: 800;
        line-height: 1.35;
        margin-bottom: 7px;
    }

    .field-label {
        color: #94a3b8;
        font-size: .61rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: .75px;
        margin-bottom: 2px;
    }

    .field-value {
        color: #334155;
        font-size: .75rem;
        font-weight: 650;
    }

    .badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 999px;
        font-size: .61rem;
        font-weight: 800;
        letter-spacing: .25px;
        margin-right: 4px;
        margin-bottom: 7px;
    }

    .badge-overdue { background: #fee2e2; color: #b91c1c; }
    .badge-review { background: #fef3c7; color: #92400e; }
    .badge-confirmed { background: #dcfce7; color: #166534; }
    .badge-waiting { background: #ede9fe; color: #6d28d9; }
    .badge-owner { background: #fff7ed; color: #c2410c; }
    .badge-priority { background: #eef2ff; color: #4338ca; }

    .ownership-note {
        background: #fffbeb;
        border: 1px solid #fde68a;
        border-left: 3px solid #f59e0b;
        border-radius: 8px;
        padding: 8px 10px;
        color: #92400e;
        font-size: .7rem;
        line-height: 1.4;
        margin-top: 8px;
    }

    .overdue-box {
        background: #fff7f7;
        border: 1px solid #fecaca;
        border-left: 3px solid #ef4444;
        border-radius: 9px;
        padding: 10px 12px;
        margin-bottom: 7px;
    }

    .overdue-title {
        color: #991b1b;
        font-size: .78rem;
        font-weight: 800;
    }

    .overdue-status {
        color: #b91c1c;
        font-size: .68rem;
        margin-top: 2px;
    }

    div[data-testid="stExpander"] {
        border: 1px solid #e8ebf2 !important;
        border-radius: 8px !important;
        background: #fafbfe !important;
        margin-top: 8px;
    }

    /* QUESTIONS */
    .question-buttons div[data-testid="stButton"] > button {
        background: #fff !important;
        color: #475569 !important;
        border: 1px solid #e0e5ee !important;
        border-radius: 999px !important;
        min-height: 36px !important;
        padding: 5px 10px !important;
        font-size: .69rem !important;
        font-weight: 700 !important;
        box-shadow: none !important;
    }

    .question-buttons div[data-testid="stButton"] > button:hover {
        background: #eef2ff !important;
        border-color: #a5b4fc !important;
        color: #3730a3 !important;
    }

    .agent-header {
        background: #fff;
        border: 1px solid #e1e5ee;
        border-radius: 14px;
        padding: 13px 16px;
        margin-top: 7px;
        margin-bottom: 10px;
    }

    .agent-title {
        color: #172554;
        font-size: 1rem;
        font-weight: 800;
    }

    div[data-testid="stChatMessage"] { border-radius: 12px; }

    hr {
        border-color: #e5e7ef !important;
        margin: 25px 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">◈</div>
            <div>
                <div class="brand-title">Executive Productivity</div>
                <div class="brand-subtitle">Action intelligence workspace</div>
            </div>
        </div>

        <div class="nav-label">Workspace</div>
        <div class="nav-item nav-item-active">▦ &nbsp; Daily Brief</div>
        <div class="nav-item">✓ &nbsp; My Actions</div>
        <div class="nav-item">◷ &nbsp; Waiting on Others</div>
        <div class="nav-item">! &nbsp; Unclear Ownership</div>
        <div class="nav-item">⚠ &nbsp; Overdue</div>
        <div class="nav-item">⌕ &nbsp; Ask the Agent</div>

        <div class="nav-label">Scenario</div>
        """,
        unsafe_allow_html=True,
    )

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

    scenario_dt = datetime.combine(scenario_date, scenario_time)

    st.markdown(
        f"""
        <div class="scenario-box">
            <div style="color:#172554;font-size:.77rem;font-weight:800;margin-bottom:8px;">
                Scenario context
            </div>
            <div class="field-label">Selected date</div>
            <div class="field-value">{scenario_date.strftime("%d %b %Y")}</div>
            <div style="height:6px;"></div>
            <div class="field-label">Scenario time</div>
            <div class="field-value">{scenario_time.strftime("%I:%M %p")}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# GET BRIEF
# ============================================================

brief = daily_brief(scenario_dt)


# ============================================================
# TOP BAR
# ============================================================

st.markdown(
    f"""
    <div class="topbar">
        <div class="eyebrow">Executive Productivity Agent</div>
        <div class="date-pill">
            Scenario · {scenario_date.strftime("%d %b %Y")} · {scenario_time.strftime("%I:%M %p")}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">Daily command center</div>
        <div class="hero-title">What do I need to know and act on today?</div>
        <div class="hero-line"></div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# METRICS
# ============================================================

st.markdown(
    '<div class="section-kicker">Today at a glance</div>',
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4, gap="medium")

with m1:
    st.markdown(
        f"""
        <div class="metric-card metric-blue">
            <div class="metric-top">
                <div class="metric-label">My Actions</div>
                <div class="metric-icon">✓</div>
            </div>
            <div class="metric-value">{len(brief["my_actions"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        f"""
        <div class="metric-card metric-purple">
            <div class="metric-top">
                <div class="metric-label">Waiting on Others</div>
                <div class="metric-icon">◷</div>
            </div>
            <div class="metric-value">{len(brief["waiting"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m3:
    st.markdown(
        f"""
        <div class="metric-card metric-amber">
            <div class="metric-top">
                <div class="metric-label">Unclear Ownership</div>
                <div class="metric-icon">!</div>
            </div>
            <div class="metric-value">{len(brief["unclear"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m4:
    st.markdown(
        f"""
        <div class="metric-card metric-red">
            <div class="metric-top">
                <div class="metric-label">Overdue</div>
                <div class="metric-icon">⚠</div>
            </div>
            <div class="metric-value">{len(brief["overdue"])}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PRIORITY BANNER
# ============================================================

if brief["overdue"]:
    priority_action = brief["overdue"][0]
    priority_text = priority_action["title"]
    priority_meta = priority_action["status"]
elif brief["my_actions"]:
    priority_action = brief["my_actions"][0]
    priority_text = priority_action["title"]
    priority_meta = f'Due {priority_action["deadline_label"]}'
elif brief["unclear"]:
    priority_action = brief["unclear"][0]
    priority_text = priority_action["title"]
    priority_meta = "Ownership needs confirmation"
else:
    priority_text = "No immediate priority detected"
    priority_meta = "Review the daily brief for the latest context."

st.markdown(
    f"""
    <div class="priority-banner">
        <div class="priority-label">Immediate priority</div>
        <div class="priority-title">{priority_text}</div>
        <div class="priority-meta">{priority_meta}</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def status_badge(status):
    status_lower = status.lower()

    if "overdue" in status_lower:
        return '<span class="badge badge-overdue">● OVERDUE</span>'
    if "review pending" in status_lower:
        return '<span class="badge badge-review">● REVIEW PENDING</span>'
    if "review scheduled" in status_lower:
        return '<span class="badge badge-review">● REVIEW SCHEDULED</span>'
    if "confirmed" in status_lower:
        return '<span class="badge badge-confirmed">● CONFIRMED</span>'
    if "waiting" in status_lower:
        return '<span class="badge badge-waiting">● WAITING</span>'
    if "unconfirmed" in status_lower:
        return '<span class="badge badge-owner">● OWNER UNCONFIRMED</span>'

    return '<span class="badge badge-waiting">● PENDING</span>'


def render_action_card(action, waiting=False, unclear=False):
    with st.container(border=True):
        st.markdown(
            f'<div class="action-title">{action["title"]}</div>',
            unsafe_allow_html=True,
        )

        if unclear:
            badges = (
                '<span class="badge badge-owner">● OWNER UNCONFIRMED</span>'
                + f'<span class="badge badge-priority">{action["priority"].upper()} PRIORITY</span>'
            )
        elif waiting:
            badges = '<span class="badge badge-waiting">● WAITING ON OTHERS</span>'
        else:
            badges = (
                status_badge(action["status"])
                + f'<span class="badge badge-priority">{action["priority"].upper()} PRIORITY</span>'
            )

        st.markdown(badges, unsafe_allow_html=True)

        c1, c2 = st.columns(2)

        with c1:
            st.markdown(
                f"""
                <div class="field-label">Deadline</div>
                <div class="field-value">{action["deadline_label"]}</div>
                """,
                unsafe_allow_html=True,
            )

        with c2:
            if waiting:
                st.markdown(
                    f"""
                    <div class="field-label">Waiting on</div>
                    <div class="field-value">{action["waiting_on"]}</div>
                    """,
                    unsafe_allow_html=True,
                )
            elif unclear:
                st.markdown(
                    """
                    <div class="field-label">Owner</div>
                    <div class="field-value">Not established</div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
                    <div class="field-label">Owner</div>
                    <div class="field-value">Arjun</div>
                    """,
                    unsafe_allow_html=True,
                )

        if waiting:
            st.markdown(
                f"""
                <div style="margin-top:8px;">
                    <div class="field-label">Status</div>
                    <div class="field-value">{action["status"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if unclear:
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
            for evidence in action["evidence"]:
                st.write("• " + evidence)


# ============================================================
# MAIN WORKSPACE
# ============================================================

left, right = st.columns([1.65, 1], gap="large")

with left:
    st.markdown(
        '<div class="section-kicker">Requires your attention</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-title">My Actions</div>',
        unsafe_allow_html=True,
    )

    if brief["my_actions"]:
        for action in brief["my_actions"]:
            render_action_card(action)
    else:
        st.info("No current action is classified as mine.")

with right:
    st.markdown(
        '<div class="section-kicker">Needs clarification</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-title">Unclear Ownership</div>',
        unsafe_allow_html=True,
    )

    if brief["unclear"]:
        for action in brief["unclear"]:
            render_action_card(action, unclear=True)
    else:
        st.success("No unresolved ownership issue.")


# ============================================================
# WAITING ON OTHERS
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="section-kicker">Dependencies</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-title">Waiting on Others</div>',
    unsafe_allow_html=True,
)

if brief["waiting"]:
    wait_cols = st.columns(min(3, len(brief["waiting"])), gap="medium")

    for i, action in enumerate(brief["waiting"]):
        with wait_cols[i % len(wait_cols)]:
            render_action_card(action, waiting=True)
else:
    st.info("No unresolved waiting item.")


# ============================================================
# OVERDUE
# ============================================================

if brief["overdue"]:
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-kicker">Risk</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-title">Overdue Commitments</div>',
        unsafe_allow_html=True,
    )

    overdue_cols = st.columns(min(2, len(brief["overdue"])), gap="medium")

    for i, action in enumerate(brief["overdue"]):
        with overdue_cols[i % len(overdue_cols)]:
            st.markdown(
                f"""
                <div class="overdue-box">
                    <div class="overdue-title">⚠ {action["title"]}</div>
                    <div class="overdue-status">{action["status"]}</div>
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
        <div class="agent-title">◈ Ask the Agent</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-kicker">Quick questions</div>',
    unsafe_allow_html=True,
)

questions = [
    "What did I promise Raghav?",
    "What is overdue?",
    "What am I waiting on?",
    "What needs action today?",
    "What has unclear ownership?",
]

selected_question = None

st.markdown('<div class="question-buttons">', unsafe_allow_html=True)

qcols = st.columns(5)

for i, question_text in enumerate(questions):
    with qcols[i]:
        if st.button(
            question_text,
            key=f"example_question_{i}",
            use_container_width=True,
        ):
            selected_question = question_text

st.markdown("</div>", unsafe_allow_html=True)

typed_question = st.chat_input("Ask anything about your work...")
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
