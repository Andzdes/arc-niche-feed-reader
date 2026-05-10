# arc-niche-feed-reader

> **Status:** Development / API Review Request  
> **App Type:** Script (Personal Use / Read-Only)

## 📌 Project Overview

`arc-niche-feed-reader` is a lightweight, read-only Command Line Interface (CLI) application built with Python. 

**Benefit for Redditors:** It provides a streamlined, text-based interface for navigating complex technical discussions in niche communities. By reducing visual overhead, it allows for more efficient information retrieval and troubleshooting.

**Why not Devvit?** The project requires a standalone local CLI for a private desktop workflow, which is not supported by the on-platform, server-side UI environment of Devvit.

### 🛡️ API Compliance & Respect
This tool is designed with strict constraints to ensure zero negative impact on Reddit's infrastructure:
- **Read-Only Scope:** The app operates purely in `read_only` mode using the `read` scope via PRAW. It does not require user OAuth, and cannot post, comment, upvote, or modify user data.
- **No Data Storage/Hoarding:** NO data is stored, archived, or exported. Content (titles and metadata) is fetched for immediate on-screen display in volatile memory (RAM) and then discarded.
- **Low Intensity:** Operates at a very low request volume (typically 5-10 requests per minute), driven entirely by manual user CLI prompts.
- **PRAW Integration:** Uses the official `praw` library, which automatically handles and respects Reddit's API rate limits and HTTP `429` responses.

---

## 🚀 Features
- **Distraction-Free Terminal UI:** Uses the `rich` library for formatted tables with clickable permalinks.
- **Targeted Communities:** Designed for browsing niche technical subreddits (e.g., `r/crm`, `r/SaaS`, `r/softwaredevelopment`, `r/cadcam`).
- **Keyword Filtering:** Keyword-based filtering of new posts for efficient browsing of specific topics.

---

## 📂 Repository Structure
```
arc-niche-feed-reader/
├── reddit_niche_reader.py   # Main application
├── requirements.txt         # Python dependencies
├── .env.example             # Template for API credentials
├── .gitignore               # Prevents secrets and logs from being committed
└── README.md
```

---

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- Active Reddit Developer Application (Script type)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Copy the provided template and fill in your Reddit API credentials:
```bash
cp .env.example .env
```
Then edit `.env` with your values:
```env
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=windows:arc-niche-feed-reader:v1.0.0 (by /u/your_username)
```

### 3. Run
```bash
python reddit_niche_reader.py
```
You will be prompted to enter a target subreddit and an optional keyword filter. Type `q` to exit.

---

## 📄 License
This project is for personal, educational use only.
