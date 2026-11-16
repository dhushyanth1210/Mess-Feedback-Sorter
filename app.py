"""Mess Feedback Sorter | Streamlit interface.

Run: streamlit run app.py
Uses the existing main.py classify(), manual_review(), apply_safety_net().
Stores new UI submissions in ui_feedback.db; never edits the console reports.
"""
import csv
import io
import os
import re
import sqlite3
import uuid
import unicodedata
from collections import Counter
from datetime import datetime
from html import escape
from pathlib import Path

import streamlit as st
import main as sorter

ROOT = Path(__file__).resolve().parent
DB = ROOT / "ui_feedback.db"
MEALS = ["Breakfast", "Lunch", "Snacks", "Dinner"]
CATEGORIES = ["taste", "hygiene", "quantity", "timing", "other"]

st.set_page_config(page_title="Messly | Mess Feedback Sorter", page_icon="🍽️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""

<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
:root{--ink:#143b29;--sub:#607b6a;--line:#dceee0;--green:#168448;--lime:#a4e44f;--bg:#f6fbf7}
html,body,[class*="css"],.stApp{font-family:'DM Sans',sans-serif}
.stApp{background:radial-gradient(ellipse at 95% 6%,#e6f9da 0%,transparent 29%),radial-gradient(ellipse at 2% 60%,#eaf8ed 0%,transparent 35%),var(--bg);color:var(--ink)}
.block-container{max-width:1300px;padding:1.1rem 2.5rem 4rem}
header[data-testid="stHeader"]{background:transparent}
#MainMenu,footer{visibility:hidden}
h1,h2,h3{font-family:'Plus Jakarta Sans',sans-serif!important;letter-spacing:-.045em;color:var(--ink)}
[data-testid="stForm"]{background:#fff;border:1px solid #cde8d3;border-radius:24px;padding:27px 29px;box-shadow:0 16px 48px rgba(17,105,56,.07);animation:rise .55s ease both}
[data-testid="stVerticalBlockBorderWrapper"]{border-color:#dceee0!important;border-radius:20px!important;background:#fff}
.stButton>button,.stFormSubmitButton>button,.stDownloadButton>button{border-radius:13px!important;font-weight:700!important;min-height:46px;transition:transform .18s ease,box-shadow .18s ease,background .18s ease}
.stButton>button:hover,.stFormSubmitButton>button:hover,.stDownloadButton>button:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(21,125,63,.15)}
.stButton>button[kind="primary"],.stFormSubmitButton>button[kind="primary"]{background:linear-gradient(105deg,#75c90b,#008b4a)!important;border-color:#168448!important;color:white!important}
.stButton>button:hover,.stFormSubmitButton>button:hover{border-color:#168448!important}
.stTextArea textarea,.stTextInput input,[data-baseweb="select"]>div{border-radius:13px!important;border-color:#d8e8dc!important;background:#fbfefb!important}
.stTextArea textarea:focus,.stTextInput input:focus{border-color:#4dbb70!important;box-shadow:0 0 0 3px rgba(52,173,92,.12)!important}
[data-testid="stMetric"]{background:linear-gradient(140deg,#fff,#f2fbf4);padding:22px;border:1px solid var(--line);border-radius:19px;box-shadow:0 8px 24px rgba(17,105,56,.045);transition:transform .2s}
[data-testid="stMetric"]:hover{transform:translateY(-3px)}
[data-testid="stMetricLabel"]{font-weight:700;color:#63816c}
[data-testid="stMetricValue"]{font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;color:#145c35}
[data-testid="stDataFrame"]{border-radius:16px;overflow:hidden}
.brand{display:flex;align-items:center;gap:11px;padding:9px 0 18px}
.brand-icon{display:inline-flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#e1f9c4,#b8edc7);color:#075f30;border:1px solid #c9e9cc;border-radius:14px;width:47px;height:47px;font-size:26px;box-shadow:0 6px 18px rgba(48,142,72,.1)}
.brand-name{font:800 25px 'Plus Jakarta Sans',sans-serif;letter-spacing:-.055em;color:#103e27}
.brand-name span{color:#73c920}
.brand-tag{color:#779383;font-size:10px;letter-spacing:.12em;font-weight:700;margin-top:1px}
.hero{position:relative;overflow:hidden;background:linear-gradient(115deg,#effaf0 0%,#f9fdf9 56%,#d9f5c5 100%);border:1px solid #d5ecd5;border-radius:28px;padding:43px 47px;margin:13px 0 28px;color:#163e2a;min-height:265px;box-shadow:0 16px 45px rgba(17,105,56,.055);animation:rise .55s ease both}
.hero:after{content:'✦';position:absolute;width:260px;height:260px;border:45px solid rgba(124,209,61,.13);border-radius:50%;right:-70px;top:-125px;color:#70be34;font-size:40px;text-align:center;pointer-events:none}
.hero-label{display:inline-block;background:#e0f4df;border-radius:40px;padding:8px 14px;font-size:11px;letter-spacing:.09em;font-weight:800;color:#177a42;text-transform:uppercase;margin-bottom:18px}
.hero h1{font-size:clamp(31px,4vw,52px);line-height:1.16;letter-spacing:-.055em;color:#123d29;margin:0 0 15px;max-width:780px}
.hero h1 em{font-style:normal;color:#50ad22}
.hero p{font-size:15px;line-height:1.75;color:#557565;max-width:650px;margin:0}
.hero-chips{display:flex;flex-wrap:wrap;gap:9px;margin-top:22px}
.hero-chip{display:inline-flex;align-items:center;gap:7px;background:#fff;border:1px solid #dcebdc;border-radius:12px;padding:10px 12px;font-size:12px;font-weight:700;color:#225c38;box-shadow:0 5px 15px rgba(10,90,42,.035)}
.eyebrow{font-size:11px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#168448;margin-bottom:9px}
.section-head{font:800 23px 'Plus Jakarta Sans',sans-serif;letter-spacing:-.05em;color:#163e2a;margin:7px 0 6px}
.section-sub{color:#698573;font-size:13px;margin-bottom:19px;line-height:1.65}
.feature{background:#fff;border:1px solid #deeddf;border-radius:18px;padding:20px 22px;margin-bottom:12px;box-shadow:0 5px 20px rgba(20,85,40,.03);transition:transform .2s,box-shadow .2s;animation:rise .6s ease both}
.feature:hover{transform:translateY(-4px);box-shadow:0 12px 28px rgba(20,85,40,.09)}
.feature-index{display:inline-flex;align-items:center;justify-content:center;background:#e7f8db;color:#248b37;font-weight:800;border-radius:11px;width:36px;height:36px;margin-right:9px}
.feature-title{font-size:14px;font-weight:800;color:#163e2a}
.feature-desc{font-size:12px;color:#718778;line-height:1.6;margin:7px 0 0 45px}
.mini-tag{display:inline-block;padding:7px 12px;border-radius:20px;background:#e6f7e9;color:#247d46;font-weight:700;font-size:11px;margin:4px 4px 0 0}
.note{background:#eaf8e9;border:1px solid #ccebcf;border-radius:14px;padding:16px 18px;color:#346b48;font-size:12px;line-height:1.75}
.success-panel{border:1px solid #a9e7b9;background:#eafbf0;border-radius:16px;padding:18px 21px;color:#166138;line-height:1.85;margin-top:16px;animation:rise .35s ease}
.warning-panel{border:1px solid #ffe0a1;background:#fff9ec;border-radius:15px;padding:17px 20px;color:#7e5b15;line-height:1.8;margin-top:16px}
.small-title{font:800 15px 'Plus Jakarta Sans',sans-serif;color:#163e2a;margin-bottom:10px}
.divider{border-top:1px solid #deebdf;margin:20px 0}
.footer{border-top:1px solid #dcebdd;padding:25px 0 0;text-align:center;color:#789481;font-size:11px;margin-top:45px}
@keyframes rise{from{opacity:0;transform:translateY(13px)}to{opacity:1;transform:translateY(0)}}
@media(max-width:700px){.block-container{padding:1rem 1rem 3rem}.hero{padding:27px 23px;min-height:220px}.hero h1{font-size:32px}.hero:after{opacity:.35}[data-testid="stForm"]{padding:18px}.brand-name{font-size:21px}.hero-chip{font-size:10px}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
</style>
""", unsafe_allow_html=True)


def connect():
    conn = sqlite3.connect(DB, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS feedback (
        id TEXT PRIMARY KEY, date TEXT NOT NULL, meal TEXT NOT NULL,
        comment TEXT NOT NULL, language TEXT NOT NULL,
        category TEXT NOT NULL, sentiment TEXT NOT NULL,
        urgent INTEGER NOT NULL, summary TEXT NOT NULL,
        status TEXT NOT NULL, priority TEXT NOT NULL,
        reason TEXT NOT NULL DEFAULT ''
    )""")
    conn.commit()
    return conn


def save_record(record):
    with connect() as conn:
        conn.execute("""INSERT INTO feedback
          (id,date,meal,comment,language,category,sentiment,urgent,summary,status,priority,reason)
          VALUES (:id,:date,:meal,:comment,:language,:category,:sentiment,:urgent,:summary,:status,:priority,:reason)""", record)


def update_status(record_id, status):
    with connect() as conn:
        conn.execute("UPDATE feedback SET status=? WHERE id=?", (status, record_id))


def get_records():
    with connect() as conn:
        local = [dict(r) for r in conn.execute("SELECT * FROM feedback ORDER BY date DESC")]
    # Existing console results are displayed read-only, not copied or modified.
    original = ROOT / "results.csv"
    if original.exists():
        try:
            with original.open(encoding="utf-8-sig", newline="") as f:
                for r in csv.DictReader(f):
                    is_urgent = str(r.get("urgent", "")).strip().lower() in ("true", "1", "yes")
                    manual = r.get("review_status", "") == "needs_manual_review"
                    local.append({
                        "id": "CSV-" + str(r.get("id", "")), "date": r.get("date", ""),
                        "meal": r.get("meal", ""), "comment": r.get("comment", ""),
                        "language": "—", "category": r.get("category", "other"),
                        "sentiment": r.get("sentiment", "neutral"), "urgent": int(is_urgent),
                        "summary": r.get("summary", ""),
                        "status": "Needs Review" if manual else "Accepted",
                        "priority": "Critical" if is_urgent else "Normal", "reason": "",
                    })
        except (OSError, UnicodeError, csv.Error):
            st.warning("Existing results.csv could not be read. New UI submissions are still available.")
    return local


def validate(text):
    text = text.strip()
    if not text:
        return "Please write your feedback before submitting."
    letters = re.findall(r"[^\W\d_]", text, re.UNICODE)
    if len(letters) < 3:
        return "Please enter meaningful feedback, not just numbers or symbols."
    # Allow Unicode letters/combining marks (including Tamil), digits, whitespace,
    # and ordinary sentence punctuation. Reject unwanted symbols before calling the API.
    allowed_punctuation = set(".,!?;:'\"()-")
    for char in text:
        category = unicodedata.category(char)
        if not (category[0] in "LMN" or char.isspace() or char in allowed_punctuation):
            return "Please remove unwanted special characters from your feedback."
    normalized = re.sub(r"[^\w]", "", text.lower(), flags=re.UNICODE)
    if normalized in {"asdf", "asdfgh", "asdfghjkl", "qwerty", "qwertyuiop", "zxcv", "zxcvbn", "abcabc", "testtest"}:
        return "This looks like random text. Please describe your mess experience."
    words = re.findall(r"[^\W\d_]+", text.lower(), re.UNICODE)
    # Reject combinations of known keyboard-mashing tokens without blocking
    # legitimate English, Tamil or Tanglish spelling variations.
    random_words = {
        "asdf", "asdfgh", "asdfghjkl", "qwerty", "qwertyuiop",
        "zxcv", "zxcvbn", "abcabc", "testtest",
    }
    if words and all(word in random_words for word in words):
        return "This looks like random text. Please describe your mess experience."
    if len(words) > 1 and words[-1] in {"because", "but", "and", "the", "was", "is", "are", "romba"}:
        return "Your feedback seems unfinished. Please complete your sentence."
    # Meaning/relevance cannot be guaranteed by regex. Ambiguous text is left to the classifier/reviewer.
    return None


def priority_for(category, sentiment, urgent):
    if urgent:
        return "Critical"
    if sentiment == "positive":
        return "Normal"
    return {"hygiene": "High", "taste": "Medium", "quantity": "Medium", "timing": "Low"}.get(category, "Normal")


def classify_feedback(meal, language, comment):
    record = {
        "id": "MF-" + uuid.uuid4().hex[:10].upper(),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "meal": meal, "comment": comment.strip(), "language": language,
        "category": "other", "sentiment": "neutral", "urgent": 0,
        "summary": "Awaiting review", "status": "Needs Review",
        "priority": "Normal", "reason": "",
    }
    try:
        result = sorter.classify(comment)
        if result is None:
            record["reason"] = "Automatic classification was unavailable."
        else:
            result = sorter.apply_safety_net(comment, dict(result)) or result
            record.update(
                category=str(result.get("category", "other")).lower(),
                sentiment=str(result.get("sentiment", "neutral")).lower(),
                urgent=int(bool(result.get("urgent", False))),
                summary=str(result.get("summary", "")),
                status="Accepted",
            )
            record["priority"] = priority_for(record["category"], record["sentiment"], record["urgent"])
    except Exception:
        # Do not expose API keys, configuration, or exception details in the UI.
        record["reason"] = "The classifier is currently unavailable."
    save_record(record)
    return record


if "page" not in st.session_state:
    st.session_state.page = "Student Portal"
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "admin_access" not in st.session_state:
    st.session_state.admin_access = False

brand, student_nav, admin_nav = st.columns([5, 1.35, 1.35], vertical_alignment="center")
with brand:
    logo_file = ROOT / "messly_logo.png"
    if logo_file.is_file():
        st.image(str(logo_file), width=190)
    else:
        st.markdown('<div class="brand"><span class="brand-icon">🍽</span><div><div class="brand-name">Mess<span>ly</span></div><div class="brand-tag">MESS FEEDBACK SORTER</div></div></div>', unsafe_allow_html=True)
with student_nav:
    if st.button("Student Portal", use_container_width=True, type="primary" if st.session_state.page == "Student Portal" else "secondary"):
        st.session_state.page = "Student Portal"
        st.rerun()
with admin_nav:
    if st.button("Admin Area", use_container_width=True, type="primary" if st.session_state.page != "Student Portal" else "secondary"):
        st.session_state.page = "Admin Dashboard"
        st.rerun()

if st.session_state.page == "Student Portal":
    st.markdown('''<div class="hero"><div class="hero-label">✦ CIT HOSTEL MESS</div><h1>Your Voice,<br><em>Better Food!</em></h1><p>Share your mess experience, help us spot issues early, and make our food better, together.</p><div class="hero-chips"><span class="hero-chip">⚡ AI-Powered Sorting</span><span class="hero-chip">🛡 Health Risk Detection</span><span class="hero-chip">▥ Clear Reports</span></div></div>''', unsafe_allow_html=True)
    left, right = st.columns([1.7, 1], gap="large")
    with left:
        st.markdown('<div class="eyebrow">SHARE YOUR EXPERIENCE</div><div class="section-head">Tell us how it went.</div><div class="section-sub">Just a few details. No complicated forms, no pressure.</div>', unsafe_allow_html=True)
        with st.form("feedback_form", clear_on_submit=True):
            meal = st.selectbox("Which meal are you reviewing?", MEALS)
            language = st.selectbox("Preferred language", ["English", "Tamil", "Tanglish"])
            comment = st.text_area("Your feedback", height=180, placeholder="Example: Inniku lunch la rice konjam cold ah irundhuchu...", help="You can write in English, Tamil or Tanglish. Spelling mistakes are okay.")
            st.caption("We welcome genuine feedback. Please avoid random or unrelated messages.")
            submit = st.form_submit_button("Submit my feedback  →", type="primary", use_container_width=True)
        if submit:
            error = validate(comment)
            if error:
                st.error(error)
                st.session_state.last_result = None
            else:
                with st.spinner("Checking your feedback..."):
                    st.session_state.last_result = classify_feedback(meal, language, comment)
        if st.session_state.last_result:
            r = st.session_state.last_result
            if r["status"] == "Accepted":
                st.markdown(f'<div class="success-panel"><b>✓ Feedback received successfully</b><div>Category: {escape(r["category"].title())} &nbsp; · &nbsp; Sentiment: {escape(r["sentiment"].title())}</div><div>Reference: {escape(r["id"])}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="warning-panel"><b>Feedback received for manual review</b><div>Reference: {escape(r["id"])}</div></div>', unsafe_allow_html=True)
            st.session_state.last_result = None
    with right:
        st.markdown('<div class="eyebrow">SIMPLE & TRANSPARENT</div><div class="section-head">How it works</div><div class="section-sub">Three easy steps to make your voice count.</div>', unsafe_allow_html=True)
        for num, title, description in [
            ("01", "Pick your meal", "Choose the meal you want to share feedback about."),
            ("02", "Write in your own words", "English, Tamil or Tanglish — spelling mistakes are fine."),
            ("03", "We sort and review", "Feedback is categorized and food safety issues are highlighted."),
        ]:
            st.markdown(f'<div class="feature"><span class="feature-index">{num}</span><span class="feature-title">{title}</span><div class="feature-desc">{description}</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="note"><b>What can you report?</b><br>Food taste, cleanliness, portion sizes, serving delays and other mess-related experiences.</div>', unsafe_allow_html=True)
        st.markdown('<div style="margin-top:17px"><span class="mini-tag">Taste</span><span class="mini-tag">Hygiene</span><span class="mini-tag">Quantity</span><span class="mini-tag">Timing</span><span class="mini-tag">Other</span></div>', unsafe_allow_html=True)

else:
    admin_password = os.environ.get("MESS_ADMIN_PASSWORD", "").strip()
    if not admin_password:
        st.markdown('<div class="hero"><div class="hero-label">ADMIN AREA</div><h1>Secure access required.</h1><p>Set an admin password in your local environment to view student feedback and reports.</p></div>', unsafe_allow_html=True)
        st.info("Set MESS_ADMIN_PASSWORD in your .env file and restart Streamlit. Never put the password in app.py or GitHub.")
    elif not st.session_state.admin_access:
        st.markdown('<div class="hero"><div class="hero-label">MESS MANAGEMENT</div><h1>Welcome back, admin.</h1><p>Sign in to monitor feedback, review concerns and see insights.</p></div>', unsafe_allow_html=True)
        _, mid, _ = st.columns([1, 1.1, 1])
        with mid:
            with st.form("admin_auth"):
                password = st.text_input("Admin password", type="password")
                if st.form_submit_button("Unlock dashboard", type="primary", use_container_width=True):
                    import hmac
                    if hmac.compare_digest(password, admin_password):
                        st.session_state.admin_access = True
                        st.rerun()
                    else:
                        st.error("Incorrect password.")
    else:
        st.markdown('<div class="hero"><div class="hero-label">MESS MANAGEMENT · ANALYTICS</div><h1>Your feedback, organized.</h1><p>Spot patterns, monitor urgent concerns and manage student submissions in one place.</p></div>', unsafe_allow_html=True)
        records = get_records()
        total = len(records)
        accepted = sum(r["status"] == "Accepted" for r in records)
        review = sum(r["status"] == "Needs Review" for r in records)
        urgent = sum(bool(r["urgent"]) for r in records)
        negative = sum(r["sentiment"] == "negative" for r in records if r["status"] == "Accepted")
        metrics = st.columns(5)
        for col, title, value in zip(metrics, ["Total feedback", "Accepted", "Needs review", "Urgent alerts", "Negative %"], [total, accepted, review, urgent, f"{(negative / accepted * 100):.0f}%" if accepted else "0%"]):
            with col:
                st.metric(title, value)
        st.write("")
        st.markdown('<div class="section-head">Feedback insights</div><div class="section-sub">Live totals from local submissions and existing console results.</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2, gap="large")
        with c1:
            st.markdown("**Categories**")
            counts = Counter(r["category"] for r in records if r["status"] == "Accepted")
            st.bar_chart({"Count": {k.title(): counts.get(k, 0) for k in CATEGORIES}}, color="#168448")
        with c2:
            st.markdown("**Sentiment**")
            sentiments = Counter(r["sentiment"] for r in records if r["status"] == "Accepted")
            st.bar_chart({"Count": {k.title(): sentiments.get(k, 0) for k in ["positive", "negative", "neutral"]}}, color="#75c936")
        st.markdown('<div class="section-head">Feedback management</div><div class="section-sub">Search and filter feedback. Existing CSV records are read-only.</div>', unsafe_allow_html=True)
        qcol, catcol, statuscol, prioritycol = st.columns([2, 1, 1.2, 1])
        with qcol:
            query = st.text_input("Search", placeholder="Search comments or summaries...")
        with catcol:
            cat = st.selectbox("Category", ["All"] + CATEGORIES)
        with statuscol:
            status = st.selectbox("Status", ["All", "Accepted", "Needs Review", "Rejected"])
        with prioritycol:
            prio = st.selectbox("Priority", ["All", "Critical", "High", "Medium", "Low", "Normal"])
        filtered = [r for r in records if (not query or query.casefold() in (r["comment"] + " " + r["summary"]).casefold()) and (cat == "All" or r["category"] == cat) and (status == "All" or r["status"] == status) and (prio == "All" or r["priority"] == prio)]
        if filtered:
            st.dataframe([{k: ("Yes" if r[k] else "No") if k == "urgent" else r[k] for k in ["date", "meal", "comment", "category", "sentiment", "urgent", "priority", "status"]} for r in filtered], hide_index=True, use_container_width=True)
            st.markdown("**Review individual feedback**")
            for r in filtered[:60]:
                with st.expander(f'{"⚠️ " if r["urgent"] else ""}{r["meal"]} · {r["status"]} · {r["comment"][:85]}'):
                    st.write(r["comment"])
                    st.caption(f'ID: {r["id"]} | Category: {r["category"]} | Sentiment: {r["sentiment"]} | Priority: {r["priority"]}')
                    st.write("**Summary:**", r["summary"])
                    if r["reason"]:
                        st.info(r["reason"])
                    if not r["id"].startswith("CSV-"):
                        buttons = st.columns(3)
                        for col, new_status, label in zip(buttons, ["Accepted", "Rejected", "Needs Review"], ["Accept", "Reject", "Manual review"]):
                            with col:
                                if st.button(label, key=f'{r["id"]}-{new_status}', use_container_width=True, disabled=r["status"] == new_status):
                                    update_status(r["id"], new_status)
                                    st.rerun()
        else:
            st.info("No feedback matches these filters.")
        buffer = io.StringIO()
        columns = ["id", "date", "meal", "comment", "language", "category", "sentiment", "urgent", "summary", "status", "priority", "reason"]
        writer = csv.DictWriter(buffer, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(filtered)
        st.download_button("↓ Export filtered CSV", buffer.getvalue().encode("utf-8-sig"), "mess_feedback_export.csv", "text/csv")
        st.write("")
        if st.button("Sign out of admin"):
            st.session_state.admin_access = False
            st.session_state.page = "Student Portal"
            st.rerun()

st.markdown('<div class="footer">MESSLY · MESS FEEDBACK SORTER &nbsp; | &nbsp; Turning student feedback into smarter mess decisions</div>', unsafe_allow_html=True)
