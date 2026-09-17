from datetime import datetime, date, time, timedelta
import re
from data import ACTIONS, EMAIL_THREADS, MEETING, VOICE_NOTES, CALENDARS

def action_status(action, scenario_dt):
    """Resolve status using only supplied evidence + scenario date."""
    base = action["status_base"]

    if action["id"] == "expense_report":
        if scenario_dt >= datetime(2026, 9, 23, 18, 0):
            return "received — review pending"
        return "waiting for report"

    if action["id"] == "meridian_call":
        if scenario_dt >= datetime(2026, 9, 23, 15, 30):
            return "confirmed / call completed in scenario"

        if scenario_dt >= datetime(2026, 9, 23, 14, 0):
            return "confirmed"

        return "awaiting reconfirmation"

    if action["id"] == "campaign_deck":
        if scenario_dt >= datetime(2026, 9, 24, 8, 0):
            return "received — review scheduled"
        return "waiting on Neha"

    if action["id"] == "vendor_list":
        if scenario_dt >= datetime(2026, 9, 23, 10, 0):
            return "overdue / no completion evidence"
        return "pending"

    if action["id"] == "mumbai_lease":
        return "pending — ownership unconfirmed"

    return base

def enrich_actions(scenario_dt):
    results = []
    for a in ACTIONS:
        x = dict(a)
        x["status"] = action_status(a, scenario_dt)
        x["days_until"] = (a["deadline"].date() - scenario_dt.date()).days
        x["overdue"] = scenario_dt > a["deadline"] and a["id"] not in {"expense_report", "meridian_call", "campaign_deck"}
        if a["id"] == "vendor_list" and scenario_dt >= a["deadline"]:
            x["overdue"] = True
        x["urgent"] = (0 <= x["days_until"] <= 1) or x["overdue"] or a["priority"] == "High"
        results.append(x)
    return results

def source_text(action_id):
    a = next(x for x in ACTIONS if x["id"] == action_id)
    return "\n".join(f"• {e}" for e in a["evidence"])

def daily_brief(scenario_dt):
    actions = enrich_actions(scenario_dt)
    my_actions = [a for a in actions if a["category"] == "my_action"]
    waiting = [a for a in actions if a["category"] == "waiting"]
    unclear = [a for a in actions if a["category"] == "unclear_ownership"]

    today = []
    for a in actions:
        if a["deadline"].date() == scenario_dt.date():
            today.append(a)
    # Include the lease because its deadline is imminent even before Friday.
    if any(a["id"] == "mumbai_lease" for a in unclear) and scenario_dt.date() in {
        date(2026, 9, 24), date(2026, 9, 25)
    }:
        today += [a for a in unclear if a not in today]

    overdue = [a for a in actions if a["overdue"]]

    return {
        "actions": actions,
        "my_actions": my_actions,
        "waiting": waiting,
        "unclear": unclear,
        "today": today,
        "overdue": overdue,
    }

def format_action(a):
    owner = a["owner"] if a["owner"] else "UNCONFIRMED"
    wait = f"Waiting on: {a['waiting_on']}" if a["waiting_on"] else ""
    return (
        f"**{a['title']}**\n\n"
        f"- Owner: {owner}\n"
        f"- Deadline: {a['deadline_label']}\n"
        f"- Status: {a['status']}\n"
        f"- Priority: {a['priority']}\n"
        + (f"- {wait}\n" if wait else "")
    )

def local_answer(question, scenario_dt):
    """Grounded Q&A without requiring an external API."""
    q = question.lower().strip()
    actions = enrich_actions(scenario_dt)

    if any(k in q for k in ["raghav", "vendor list"]):
        a = next(x for x in actions if x["id"] == "vendor_list")
        return (
            f"### What you promised Raghav\n\n"
            f"You promised to **send the updated vendor list to Raghav Sethi**.\n\n"
            f"**Latest commitment:** Wednesday morning.\n\n"
            f"**Current status:** {a['status']}.\n\n"
            f"Raghav followed up at 8:45 AM Wednesday asking whether it was still on track.\n\n"
            f"**Evidence**\n{source_text('vendor_list')}"
        )

    if any(k in q for k in ["waiting", "wait on", "others"]):
        rows = []
        for a in actions:
            if a["category"] == "waiting":
                rows.append(
                    f"- **{a['title']}** — waiting on {a['waiting_on']}; expected {a['deadline_label']}."
                )
        # The report is a waiting item only before delivery.
        exp = next(x for x in actions if x["id"] == "expense_report")
        if "waiting" in exp["status"]:
            rows.append(f"- **{exp['title']}** — waiting on Divya Rao; expected Wednesday evening.")
        if not rows:
            rows.append("- No unresolved external dependency is currently shown in the supplied data.")
        return "### What am I waiting on?\n\n" + "\n".join(rows)

    if any(k in q for k in ["unclear", "unowned", "ownership", "owner"]):
        a = next(x for x in actions if x["id"] == "mumbai_lease")
        return (
            "### Unclear ownership\n\n"
            "**Mumbai Office Lease Renewal** has no confirmed owner in the source data.\n\n"
            "Divya believes it typically sits with Facilities, but Arjun explicitly said **not to assume**. "
            "Raghav's latest message says it is still unowned and asks Arjun to confirm who is handling it.\n\n"
            f"**Deadline:** {a['deadline_label']}\n\n"
            f"**Evidence**\n{source_text('mumbai_lease')}"
        )

    if any(k in q for k in ["overdue", "late"]):
        overdue = [a for a in actions if a["overdue"]]
        if not overdue:
            return "### Overdue\n\nNo item is classified as overdue for the selected scenario date/time."
        return "### Overdue\n\n" + "\n".join(
            f"- **{a['title']}** — {a['status']}" for a in overdue
        )

    if any(k in q for k in ["today", "action", "do"]):
        brief = daily_brief(scenario_dt)
        if not brief["today"]:
            return "### Action today\n\nNo deadline falls exactly on the selected scenario date."
        return "### Action today\n\n" + "\n".join(
            f"- **{a['title']}** — {a['status']} — deadline {a['deadline_label']}."
            for a in brief["today"]
        )

    if "campaign" in q or "deck" in q:
        a = next(x for x in actions if x["id"] == "campaign_deck")
        return (
            f"### Q3 Campaign Deck\n\n"
            f"Neha Kapoor is preparing the deck and Arjun needs to review it.\n\n"
            f"**Review:** Thursday, 24 Sep at 9:30 AM.\n\n"
            f"**Status:** {a['status']}.\n\n"
            f"**Evidence**\n{source_text('campaign_deck')}"
        )

    if "expense" in q or "variance" in q:
        a = next(x for x in actions if x["id"] == "expense_report")
        return (
            f"### July Expense Variance Report\n\n"
            f"Divya Rao was asked to provide it before Thursday board prep. "
            f"Arjun moved the requested delivery to Wednesday evening so he could review it.\n\n"
            f"**Status:** {a['status']}.\n\n"
            f"**Evidence**\n{source_text('expense_report')}"
        )

    if "meridian" in q or "priya" in q or "call" in q:
        a = next(x for x in actions if x["id"] == "meridian_call")
        return (
            f"### Meridian Logistics\n\n"
            f"The call is confirmed for **Wednesday, 23 Sep, 3:00–3:30 PM**.\n\n"
            f"Priya confirmed the time and Arjun reconfirmed it at 2:00 PM Wednesday.\n\n"
            f"**Status:** {a['status']}."
        )

    return (
        "I can answer questions grounded in the supplied assignment data. "
        "Try: **What did I promise Raghav?**, **What needs action today?**, "
        "**What am I waiting on?**, **What is overdue?**, or **What has unclear ownership?**"
    )

def llm_answer(question, scenario_dt, api_key=None):
    """Optional LLM layer. Facts supplied to the model are restricted to the local data."""
    if not api_key:
        return local_answer(question, scenario_dt)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        context = []
        for a in enrich_actions(scenario_dt):
            context.append({
                "title": a["title"],
                "owner": a["owner"],
                "waiting_on": a["waiting_on"],
                "deadline": a["deadline"].isoformat(),
                "deadline_label": a["deadline_label"],
                "status": a["status"],
                "category": a["category"],
                "priority": a["priority"],
                "evidence": a["evidence"],
            })
        prompt = f"""You are an executive productivity agent for Arjun Malhotra, VP Sales.
Answer only from the supplied structured evidence below. Never invent an owner, date,
commitment, or status. If ownership is uncertain, explicitly say it is unconfirmed.
Scenario date/time: {scenario_dt.isoformat()}

DATA:
{context}

USER QUESTION:
{question}

Give a concise answer with the relevant action, deadline, status, and evidence when useful."""
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "You are a grounded enterprise productivity agent."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
        return response.choices[0].message.content
    except Exception as e:
        return local_answer(question, scenario_dt) + f"\n\n*LLM mode unavailable; local grounded mode used.*"
