# Executive Productivity Agent

An intelligent productivity assistant that converts fragmented workplace communication into a structured view of commitments, actions, dependencies, deadlines, and ownership.

The prototype is designed around a simple question:

> **What do I need to know and act on today?**

It processes the supplied workplace data pack and consolidates repeated mentions of the same commitment into actionable items.

---

## Overview

In a typical work environment, important commitments can be scattered across meetings, emails, calendars, and voice notes. This makes it difficult to track:

- What I committed to
- What is waiting on someone else
- What is overdue
- Who owns an unresolved task
- What needs attention today

The **Executive Productivity Agent** addresses this by transforming fragmented information into a single, actionable productivity view.

---

## Key Features

### 1. Commitment Identification

Identifies commitments made by the user from the supplied workplace data.

### 2. My Actions

Separates tasks that require action from the user.

### 3. Waiting on Others

Identifies tasks where the user is waiting for another person or dependency before proceeding.

### 4. Deadline Detection

Tracks deadlines associated with commitments and identifies upcoming or overdue items.

### 5. Deduplication

Combines repeated mentions of the same commitment across different sources into a single normalized action.

### 6. Unclear Ownership Detection

Flags items where ownership is not explicitly established instead of making assumptions.

### 7. Daily Action Brief

Provides a concise summary of:

- Actions requiring attention
- Waiting items
- Unclear ownership
- Today's priorities
- Overdue commitments

### 8. Natural-Language Questions

Allows users to ask questions about their commitments and work context using natural language.

Example questions:

- What did I promise Raghav?
- What is overdue?
- What am I waiting on?
- What needs action today?
- What has unclear ownership?

---

## How It Works

The application follows a structured processing pipeline:

```text
Workplace Data
      │
      ├── Emails
      ├── Meeting Information
      ├── Calendar Information
      └── Voice Notes
              │
              ▼
       Data Normalization
              │
              ▼
     Commitment Identification
              │
              ▼
          Deduplication
              │
              ▼
       Action Classification
              │
       ┌──────┼─────────────┐
       ▼      ▼             ▼
  My Actions  Waiting on    Unclear
              Others        Ownership
       │
       ▼
   Deadline & Status Detection
       │
       ▼
    Daily Action Brief
       │
       ▼
    Natural-Language Q&A