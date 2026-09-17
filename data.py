from datetime import date, time, datetime

PEOPLE = {
    "Arjun Malhotra": {"role": "VP Sales", "email": "arjun.malhotra@veridian-corp.example"},
    "Neha Kapoor": {"role": "Marketing Lead", "email": "neha.kapoor@veridian-corp.example"},
    "Raghav Sethi": {"role": "Ops Manager", "email": "raghav.sethi@veridian-corp.example"},
    "Divya Rao": {"role": "Finance", "email": "divya.rao@veridian-corp.example"},
    "Priya Nair": {"role": "Meridian Logistics (external client)", "email": "priya.nair@meridianlogistics.example"},
    "Facilities": {"role": "Internal distribution list", "email": "facilities@veridian-corp.example"},
}

SCENARIO_START = date(2026, 9, 21)
SCENARIO_END = date(2026, 9, 25)

MEETING = {
    "title": "Leadership Sync",
    "date": "2026-09-21",
    "time": "09:00–09:35",
    "attendees": ["Arjun Malhotra", "Neha Kapoor", "Raghav Sethi", "Divya Rao"],
    "statements": [
        ("Arjun", "Let's keep this quick. Neha, where are we on the Q3 campaign deck?"),
        ("Neha", "Draft is 80% done. I'll send it to Arjun for review by Wednesday."),
        ("Arjun", "Good. Also, remind me — I told Raghav I'd send him the updated vendor list. I'll get that to him by end of day tomorrow."),
        ("Raghav", "Appreciated. Separately, the Mumbai office renewal paperwork needs someone to sign off this week. Not sure whose desk that's on right now."),
        ("Divya", "I think that's supposed to be Facilities, but I haven't seen anyone pick it up."),
        ("Arjun", "Okay, flag it, don't assume."),
        ("Arjun", "Divya, can you also pull the July expense variance report before Thursday's board prep?"),
        ("Divya", "Yes, I'll have it ready Wednesday evening."),
        ("Arjun", "One more thing — client call with Meridian Logistics got pushed. I need to reconfirm the new time with their team myself."),
        ("Neha", "Also, just a reminder, the campaign deck review — I said Wednesday, but realistically Thursday morning is safer."),
        ("Arjun", "Noted. Let's close here."),
    ],
}

CALENDARS = {
    "Arjun Malhotra": [
        ("2026-09-21", "09:00", "09:35", "Leadership Sync"),
        ("2026-09-21", "14:00", "14:30", "1:1 with Neha"),
        ("2026-09-21", "16:00", "17:00", "Blocked"),
        ("2026-09-22", "11:00", "12:00", "Internal Budget Review"),
        ("2026-09-22", "15:00", "15:30", "Blocked"),
        ("2026-09-23", "15:00", "15:30", "Call — Meridian Logistics"),
        ("2026-09-23", "18:00", "18:15", "Blocked"),
        ("2026-09-24", "09:00", "10:00", "Board Prep Session"),
        ("2026-09-24", "16:00", "17:00", "Hiring Panel — Sales Associate"),
        ("2026-09-25", "10:00", "10:30", "Facilities Check-in"),
        ("2026-09-25", "13:00", "14:00", "Blocked"),
    ],
    "Neha Kapoor": [
        ("2026-09-21", "10:00", "11:00", "Blocked"),
        ("2026-09-21", "14:00", "14:30", "1:1 with Arjun"),
        ("2026-09-22", "13:00", "14:00", "Campaign Vendor Call"),
        ("2026-09-23", "10:00", "10:30", "Deck Prep"),
        ("2026-09-23", "13:00", "15:00", "Blocked"),
        ("2026-09-24", "09:30", "10:00", "Deck Review with Arjun"),
        ("2026-09-25", "11:00", "12:00", "Blocked"),
    ],
    "Raghav Sethi": [
        ("2026-09-21", "09:00", "09:35", "Leadership Sync"),
        ("2026-09-21", "13:00", "14:00", "Blocked"),
        ("2026-09-22", "11:00", "12:00", "Internal Budget Review"),
        ("2026-09-22", "15:30", "16:00", "Ops Standup"),
        ("2026-09-23", "09:00", "11:00", "Blocked"),
        ("2026-09-24", "14:00", "15:00", "Blocked"),
        ("2026-09-25", "10:00", "10:30", "Facilities Check-in"),
        ("2026-09-25", "15:00", "16:00", "Blocked"),
    ],
    "Divya Rao": [
        ("2026-09-21", "14:30", "15:00", "Budget Prep"),
        ("2026-09-21", "16:00", "17:00", "Blocked"),
        ("2026-09-22", "09:00", "09:15", "Quick Call with Arjun"),
        ("2026-09-22", "11:00", "12:00", "Internal Budget Review"),
        ("2026-09-23", "13:00", "14:00", "Blocked"),
        ("2026-09-24", "09:00", "10:00", "Board Prep Session"),
        ("2026-09-24", "14:00", "15:00", "Blocked"),
        ("2026-09-25", "10:00", "11:00", "Blocked"),
    ],
}

EMAIL_THREADS = {
    "Vendor List": [
        ("2026-09-21 09:50", "Raghav Sethi", "Arjun Malhotra", "Following up from the sync — can you send the updated vendor list today?"),
        ("2026-09-21 17:40", "Arjun Malhotra", "Raghav Sethi", "Running behind, will send first thing tomorrow morning instead."),
        ("2026-09-22 09:15", "Raghav Sethi", "Arjun Malhotra", "No worries, whenever you get a chance today works."),
        ("2026-09-22 18:30", "Arjun Malhotra", "Raghav Sethi", "Sorry, got pulled into board prep — will send by tomorrow (Wednesday) morning for sure."),
        ("2026-09-23 08:45", "Raghav Sethi", "Arjun Malhotra", "Just checking — still good for this morning?"),
    ],
    "Q3 Campaign Deck": [
        ("2026-09-21 11:00", "Neha Kapoor", "Arjun Malhotra", "Deck's coming together, still targeting Wednesday for your review."),
        ("2026-09-22 16:15", "Neha Kapoor", "Arjun Malhotra", "Heads up — shifting the review to Thursday morning instead of Wednesday, need one more day on the data slides."),
        ("2026-09-23 10:00", "Arjun Malhotra", "Neha Kapoor", "Understood, Thursday morning works. What time exactly?"),
        ("2026-09-23 10:20", "Neha Kapoor", "Arjun Malhotra", "Let's say 9:30 AM Thursday, before your board prep block."),
        ("2026-09-24 08:00", "Neha Kapoor", "Arjun Malhotra", "Deck is ready, attaching the draft ahead of our 9:30 review."),
    ],
    "Call Reschedule": [
        ("2026-09-21 13:00", "Priya Nair", "Arjun Malhotra", "Our scheduled call this week got bumped from our side — can you propose a new time? We're flexible Tuesday–Thursday afternoons."),
        ("2026-09-22 15:00", "Arjun Malhotra", "Priya Nair", "Apologies for the delay — how about Wednesday 3:00 PM?"),
        ("2026-09-22 17:45", "Priya Nair", "Arjun Malhotra", "Wednesday 3 PM works on our end, confirmed."),
        ("2026-09-23 13:30", "Priya Nair", "Arjun Malhotra", "Quick check — still on for 3 PM today?"),
        ("2026-09-23 14:00", "Arjun Malhotra", "Priya Nair", "Yes, confirmed, see you at 3."),
    ],
    "Expense Variance Report": [
        ("2026-09-21 14:30", "Divya Rao", "Arjun Malhotra", "Starting on the July variance numbers, targeting Thursday morning for board prep as discussed."),
        ("2026-09-22 09:00", "Arjun Malhotra", "Divya Rao", "Actually, can I get it by Wednesday evening instead? Want time to review before Thursday."),
        ("2026-09-22 09:40", "Divya Rao", "Arjun Malhotra", "Wednesday evening is tight but doable, I'll prioritize it."),
        ("2026-09-23 18:00", "Divya Rao", "Arjun Malhotra", "Report attached, sent as promised."),
        ("2026-09-23 18:10", "Arjun Malhotra", "Divya Rao", "Got it, thank you — exactly what I needed before tomorrow."),
    ],
    "Mumbai Office Lease Renewal": [
        ("2026-09-21 10:15", "Facilities", "All Staff", "Reminder: the Mumbai office lease renewal requires an authorized signature by Friday, 25 September."),
        ("2026-09-22 11:00", "Raghav Sethi", "Arjun Malhotra, Divya Rao", "Following up from the sync — has anyone confirmed who's signing off on the Mumbai renewal? Don't think it's been assigned."),
        ("2026-09-23 09:30", "Divya Rao", "Raghav Sethi, Arjun Malhotra", "Not on my end — I believe this typically sits with Facilities directly, not us."),
        ("2026-09-24 16:00", "Facilities", "All Staff", "Second reminder: signature is still pending. Deadline is Friday, 25 September, end of day."),
        ("2026-09-24 16:45", "Raghav Sethi", "Arjun Malhotra", "This is now one day out and still unowned — can you confirm who's handling it?"),
    ],
}

VOICE_NOTES = [
    ("2026-09-21 18:40", "Voice Note 1", "Quick note to self — need to get Raghav that vendor list, I think I said today but it might slip to tomorrow morning, remind me. Also still haven't heard back on the Mumbai lease thing, someone needs to own that, I don't think it's me."),
    ("2026-09-23 08:15", "Voice Note 2", "Reminder — expense variance report from Divya needs to be in my hands by Wednesday evening, not Thursday, I want time to go through it before board prep. Also Meridian call — I owe Priya a time, need to lock that in today."),
]

# The five underlying actions represented repeatedly across the source material.
ACTIONS = [
    {
        "id": "vendor_list",
        "title": "Send updated vendor list to Raghav",
        "short": "Updated vendor list",
        "owner": "Arjun Malhotra",
        "waiting_on": None,
        "stakeholder": "Raghav Sethi",
        "deadline": datetime(2026, 9, 23, 10, 0),
        "deadline_label": "Wednesday morning",
        "status_base": "pending",
        "category": "my_action",
        "priority": "High",
        "sources": ["Leadership Sync", "Vendor List emails", "Voice Note 1"],
        "evidence": [
            "Leadership Sync: Arjun said he would send Raghav the updated vendor list.",
            "Vendor List email: Arjun moved the commitment to Wednesday morning.",
            "Voice Note 1: Arjun reminded himself to get Raghav the vendor list.",
            "Vendor List email: Raghav followed up Wednesday at 8:45 AM."
        ],
    },
    {
        "id": "campaign_deck",
        "title": "Review Q3 campaign deck",
        "short": "Q3 Campaign Deck",
        "owner": "Arjun Malhotra",
        "waiting_on": "Neha Kapoor",
        "stakeholder": "Neha Kapoor",
        "deadline": datetime(2026, 9, 24, 9, 30),
        "deadline_label": "Thursday 9:30 AM",
        "status_base": "waiting_on_others",
        "category": "waiting",
        "priority": "Medium",
        "sources": ["Leadership Sync", "Q3 Campaign Deck emails", "Neha calendar"],
        "evidence": [
            "Leadership Sync: Neha said the deck was 80% done and would send it for review.",
            "Q3 Campaign Deck email: review moved to Thursday morning.",
            "Q3 Campaign Deck email: Neha confirmed 9:30 AM Thursday.",
            "Neha calendar: Deck Review with Arjun is scheduled Thursday 9:30–10:00 AM."
        ],
    },
    {
        "id": "expense_report",
        "title": "Review July expense variance report",
        "short": "July expense variance report",
        "owner": "Arjun Malhotra",
        "waiting_on": "Divya Rao",
        "stakeholder": "Divya Rao",
        "deadline": datetime(2026, 9, 24, 9, 0),
        "deadline_label": "Before Thursday board prep",
        "status_base": "received",
        "category": "my_action",
        "priority": "High",
        "sources": ["Leadership Sync", "Expense Variance Report emails", "Voice Note 2", "Arjun calendar"],
        "evidence": [
            "Leadership Sync: Arjun asked Divya for the July expense variance report before Thursday board prep.",
            "Email: Arjun requested Wednesday evening delivery so he had time to review.",
            "Email: Divya sent the report Wednesday at 6:00 PM.",
            "Voice Note 2: Arjun said he wanted time to go through it before board prep."
        ],
    },
    {
        "id": "meridian_call",
        "title": "Reconfirm/attend Meridian Logistics call",
        "short": "Meridian Logistics call",
        "owner": "Arjun Malhotra",
        "waiting_on": None,
        "stakeholder": "Priya Nair",
        "deadline": datetime(2026, 9, 23, 15, 0),
        "deadline_label": "Wednesday 3:00 PM",
        "status_base": "confirmed",
        "category": "my_action",
        "priority": "High",
        "sources": ["Leadership Sync", "Call Reschedule emails", "Arjun calendar", "Voice Note 2"],
        "evidence": [
            "Leadership Sync: Arjun said he needed to reconfirm the new time himself.",
            "Call Reschedule email: Wednesday 3:00 PM was proposed and confirmed.",
            "Call Reschedule email: Arjun reconfirmed at 2:00 PM Wednesday.",
            "Arjun calendar: Call — Meridian Logistics, Wednesday 3:00–3:30 PM."
        ],
    },
    {
        "id": "mumbai_lease",
        "title": "Resolve ownership/sign-off for Mumbai office lease renewal",
        "short": "Mumbai office lease renewal",
        "owner": None,
        "waiting_on": None,
        "stakeholder": "Facilities / Raghav Sethi / Divya Rao",
        "deadline": datetime(2026, 9, 25, 17, 0),
        "deadline_label": "Friday 25 Sep, EOD",
        "status_base": "pending",
        "category": "unclear_ownership",
        "priority": "High",
        "sources": ["Leadership Sync", "Mumbai Office Lease Renewal emails"],
        "evidence": [
            "Leadership Sync: Raghav said someone needs to sign off this week and ownership was unclear.",
            "Leadership Sync: Divya believed it was Facilities, but Arjun explicitly said to flag it and not assume.",
            "Email: Raghav said no one had confirmed who was signing off.",
            "Email: Divya said she believed it typically sits with Facilities.",
            "Latest email: Raghav said it was still unowned and asked Arjun to confirm who is handling it."
        ],
    },
]
