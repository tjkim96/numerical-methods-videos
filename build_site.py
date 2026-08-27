# -*- coding: utf-8 -*-
"""
Generates the static ME 2004 (Numerical Methods) course-mirror website
from structured data transcribed from "Canvas Shell Su22.docx".

Run: python build_site.py
Outputs into ./docs (GitHub Pages can serve straight from /docs).
"""
import os, re, html
from urllib.parse import quote

OUT = os.path.join(os.path.dirname(__file__), "docs")
CHANNEL = "https://www.youtube.com/@jaisohnkim"

# Video IDs confirmed directly from the "ME 2004 Videos" YouTube course
# (https://www.youtube.com/playlist?list=PLJjf2IxsyffaHqKUdyABeMzQGthEzYkaT)
KNOWN = {
    "Annually Compounded Interest (1/3)": "OAiG-dX6dcQ",
    "Annually Compounded Interest (2/3)": "dzzYXya9s64",
    "Annually Compounded Interest (3/3)": "PMoi8QR-fDs",
    "Change Maker (1/3)": "pFCVttATL50",
    "Change Maker (2/3)": "pZDU1fHA4OA",
    "Change Maker (3/3)": "OWD5sttUU88",
    "Projectile Velocity (1/2)": "QiqcFKPIwWQ",
    "Projectile Velocity (2/2)": "LXTBGlS3KBM",
    "Repetition Structures (1/3)": "B4xDHuwgyvs",
    "Repetition Structures (2/3)": "1Nbu6rU4VEQ",
    "Repetition Structures (3/3)": "YUBkeC8fchw",
    "Relational Operators (1/2)": "_RPRt4Dxlm8",
    "Relational Operators (2/2)": "Z_kzlvlARck",
    "Logical Operators (1/2)": "lLunlQi5QA8",
    "Logical Operators (2/2)": "2IUnjWjjw1o",
    "If Statements": "nhtbycofPCc",
    "Software Development Process": "9mIsWGLMF4Y",
    "Physical Processes & Mathematical Modeling": "bHg7_d_D0_8",
    "Numerical Errors (1/2)": "b1CFNSR3f40",
    "Numerical Errors (2/2)": "03Lg60MTSdM",
    # Confirmed by Jaisohn (from unconfirmed_videos.md):
    "Tips for Success": "xTyHBlfpBPI",
    "What is ME 2004?": "2wmRbFlLDec",
    "Matrix Terminology Review": "OwTsm3aCQMY",
    "MATLAB Environment, Script Files, and Publishing": "qx6NQAIx7-Y",
    "MATLAB Basics": "mw-zAnGnEsM",
    "The fprintf() Command": "P0X3iDqHYRw",
    "Plotting": "1bgfMs_44NE",
    "Bell Curve": "mWJWb-uBwaU",
    "Hookian Springs": "1RgVqHmqwZo",
    "RLC Circuit": "X4wmyrQUi-8",
    "Manning's Equation": "Q2Qkd1mnGAc",
    "MATLAB Grader Overview": "WHYLlmw4wO8",
    "Function .m Files (1/2)": "uLVJNrlBW5Y",
    "Function .m Files (2/2)": "dxRRl6Yh8-c",
    "Anonymous Functions (1/2)": "qHTfGIqK04k",
    "Anonymous Functions (2/2)": "KRb4Oetbkq4",
    "Lateral Acceleration of a Vehicle (1/2)": "3m1gJ-L7dHo",
    "Lateral Acceleration of a Vehicle (2/2)": "qY0aqMuFT3c",
    "Unit Step Function (1/2)": "G3txcntNZWQ",
    "Unit Step Function (2/2)": "U5Jx2N0ezG4",
    "Linear Algebra Intro": "JJgJZzDawNo",
    "Solving Linear Algebra Problems in MATLAB": "P1NyusxiLEY",
    "Existence and Uniqueness of Solutions": "lI9g9rwwRtg",
    "Rope Tension (1/2)": "MRPWcAlhHAs",
    "Rope Tension (2/2)": "9IkSMr9ivPc",
    "Wheatstone Bridge (1/2)": "THIdS9IW714",
    "Wheatstone Bridge (2/2)": "nZOg15CLsWk",
    "Column Elongation": "Ys1DgXpQgd4",
    "Traffic Network (1/2)": "HgdSAe8tqNs",
    "Traffic Network (2/2)": "A5AvITOu5jE",
    "Matrix Inverse": "xN8TOBw2nGg",
    "Vector/Matrix Norms": "y0AjJeeWoNM",
    "Reactor Concentrations": "OvQBZ7JB49c",
    "Truss (1/2)": "qlB3zagYYR8",
    "Truss (2/2)": "NxTFpE16Fzk",
    "Curve Fitting (1/2)": "nBqCxq3Kp3g",
    "Curve Fitting (2/2)": "7oa-XQ5IK6I",
    "Charles's Law": "ZG2EIxMLyzY",
    "Nonlinear Regression": "NE4zAVloQPI",
    "RC Circuit": "pPDnvHlziQM",
    "Animal Metabolism": "m5b-xEbpuiI",
    "Nonlinear Regression Example 3": "zeHw9t_uHh4",
    "Polynomial Regression Example": "LOUYI84mog0",
    "Linear Interpolation (1/2)": "Yrvch1CEEtk",
    "Linear Interpolation (2/2)": "eV_JDYaW9Jo",
    "Steam Table Interpolation": "pY11wvM5i3o",
    "Root Finding Introduction": "UovsP6ACfJQ",
    "Root Finding: Graphical Method": "wGakH9DmmZU",
    "Bisection Method": "Njyro3rv0XE",
    "Manual Iterations of the Bisection Method": "2Va6bcNQ-6A",
    "MATLAB Implementation of the Bisection Method": "qBZoadV3v2o",
    "Critical Channel Depth": "Zq-jTyxsWqc",
    "Newton-Raphson Method": "Cavm4RduP80",
    "Manual Iterations of the Newton-Raphson Method": "MOineRasURA",
    "MATLAB Implementation of the Newton-Raphson Method": "nW6tkLhBiIQ",
    "ODE Fixed Points": "DbZYXtFMV50",
    "The fzero() Function": "e9SRGH-u_2g",
    "Redlich–Kwong Equation": "2pnTsHo2qSM",
    "Population Study": "aGTYUodsz0g",
    "Moody Diagram (1/2)": "B5aHPHHZWbE",
    "Moody Diagram (2/2)": "SOq6UllvA1c",
    "Numerical Differentiation": "CcDY8I9z2us",
    "Stopping Distances": "-2GGYsdim1A",
    "Vehicle Pitch Rate (1/2)": "IMYsqbV4CEg",
    "Vehicle Pitch Rate (2/2)": "JHtjmvLTGR4",
    "Numerical Differentiation: Step Size Exploration": "e5JsPcfEC9s",
    "Integration Review": "eeW88rkKBD0",
    "Step/Delta Integrals": "bneVK6GBBxE",
    "Pulse Function (1/2)": "PFDM-bwjq-s",
    "Pulse Function (2/2)": "Ta_LFoBSrQ0",
    "Trapezoidal Rule Review": "OuvMKQGCIBc",
    "Trapezoidal Rule Demo": "q9FxdW0tIDE",
    "Shear/Moment Diagrams": "FV_fAFvwKwk",
    "Mechanical Work": "C-6f8klg_n8",
    "Space-Time Diagrams": "CgSjAtgx_Lk",
    "ODEs Introduction": "obpHjzM4vxs",
    "1st Order ODEs Overview": "gA7WfmAiyX0",
    "Sketching Phase Portraits and Anticipated Solutions (1/3)": "dnmNhx7sJ5g",
    "Sketching Phase Portraits and Anticipated Solutions (2/3)": "lSVQUod8QOU",
    "Sketching Phase Portraits and Anticipated Solutions (3/3)": "UGHyO2brTcw",
    "The ode45() Function": "2kaERUM27NM",
    "Skydiver (1/2)": "HkWPMrqjsBU",
    "Skydiver (2/2)": "IIth5JFIlHs",
    "Population Model (1/2)": "KVDGSkkPTMs",
    "Population Model (2/2)": "cmMDewgmtwM",
    "Lumped Thermal Mass (1/2)": "Nn76G7HN3v0",
    "Lumped Thermal Mass (2/2)": "EeeNJ5rEYdE",
}

def video_link(title, note=None):
    """Return (href, is_direct) for a lecture video title."""
    key = title.strip()
    if key in KNOWN:
        return f"https://www.youtube.com/watch?v={KNOWN[key]}", True
    q = quote(title)
    return f"{CHANNEL}/search?query={q}", False

# ---------------------------------------------------------------------------
# Structured schedule data (transcribed from Canvas Shell Su22.docx images).
# Calendar dates and textbook (Vick) readings have been intentionally
# omitted -- only weekday order, topics, readings, and lecture videos remain.
# ---------------------------------------------------------------------------
WEEKS = [
  dict(
    num=1,
    blurb="""The first week of class is dedicated to reviewing MATLAB fundamentals. We're operating under
    the assumption that everyone has at least some prior MATLAB experience. Wednesday's videos introduce
    the course. Thursday's videos contain examples covering various facets of MATLAB (plotting, working
    with vectors, etc.). Friday's videos cover flow control. HW 1 only covers Wednesday's and Thursday's
    videos, but HW 2 (next week) includes Friday's videos.""",
    days=[
      dict(date="Monday", note="No class."),
      dict(date="Tuesday", note="No class (first day of class is Wednesday)"),
      dict(date="Wednesday",
        readings=["Course Introduction, Overview, and Layout", "Homework Formatting and Submission Guidelines",
                   "Plot Formatting Guidelines", "All About MATLAB Grader Workshops", "Debugging Help",
                   "ME 2004 Syllabus and Schedule Su22.pdf",
                   "Crimes Against Matrices", "Attaway Ch 3–3.2"],
        lectures=["Tips for Success", "What is ME 2004?", "Matrix Terminology Review",
                   "MATLAB Environment, Script Files, and Publishing"],
        duration="35:09"),
      dict(date="Thursday",
        readings=["Attaway Ch 1–1.5 (skip 1.4.5)", "Attaway Ch 2 (skip 2.4)", "Attaway Ch 3.3–3.6"],
        lectures=["MATLAB Basics", "The fprintf() Command", "Plotting", "Bell Curve", "Hookian Springs",
                   "RLC Circuit", "Manning's Equation"],
        duration="1:11:45"),
      dict(date="Friday",
        readings=["Attaway Ch 2.4", "Attaway Ch 4 (4.4 optional but highly recommended)", "Attaway Ch 5"],
        lectures=["Relational Operators (1/2)", "Relational Operators (2/2)", "Logical Operators (1/2)",
                   "Logical Operators (2/2)", "If Statements", "Repetition Structures (1/3)",
                   "Repetition Structures (2/3)", "Repetition Structures (3/3)", "MATLAB Grader Overview"],
        duration="1:03:07"),
    ]),
  dict(
    num=2,
    blurb="""This week's content builds on your MATLAB foundation. Monday's videos introduce anonymous
    functions and function .m-files. Wednesday's videos cover the Unit Step Function, arguably one of the
    most important functions in all of engineering — the first two are given by Dr. Brian Vick, a ME
    professor at VT and the godfather of this course. Thursday's lectures take a step back from coding and
    examine the big picture: why mathematical modeling is important and strategies for debugging code.
    Friday's videos cover numerical errors, used extensively starting in Week 4.""",
    days=[
      dict(date="Monday",
        readings=["Attaway Ch 3.7–3.9", "Attaway Ch 6–6.3 (Ch 6.4 optional but highly recommended)",
                   "Attaway 10.2–10.4"],
        lectures=["Function .m Files (1/2)", "Function .m Files (2/2)", "Anonymous Functions (1/2)",
                   "Anonymous Functions (2/2)", "Software Development Process"],
        duration="56:18"),
      dict(date="Tuesday", readings=["N/A"],
        lectures=["Lateral Acceleration of a Vehicle (1/2)", "Lateral Acceleration of a Vehicle (2/2)",
                   "Change Maker (1/3)", "Change Maker (2/3)", "Change Maker (3/3)",
                   "Annually Compounded Interest (1/3)", "Annually Compounded Interest (2/3)",
                   "Annually Compounded Interest (3/3)"],
        duration="1:03:28"),
      dict(date="Wednesday",
        readings=["heaviside() MATLAB documentation",
                   "Heaviside/Unit Step Function (Wikipedia) (optional)"],
        lectures=["Unit Step Function (1/2)", "Unit Step Function (2/2)", "Projectile Velocity (1/2)",
                   "Projectile Velocity (2/2)"],
        duration="1:06:32"),
      dict(date="Thursday",
        readings=["Attaway Ch 6.5", "Techniques for Debugging MATLAB M-files (Columbia).pdf (optional)"],
        lectures=["Physical Processes & Mathematical Modeling"],
        duration="47:14"),
      dict(date="Friday", readings=["Short Webpage on Errors (optional)"],
        lectures=["Numerical Errors (1/2)", "Numerical Errors (2/2)"],
        duration="27:46"),
    ]),
  dict(
    num=3,
    blurb="""This week is dedicated to Linear Algebra — arguably the most important numerical methods
    topic. Monday reviews concepts from a Linear Algebra math course plus introductory examples; Tuesday
    covers more complex examples; Wednesday introduces the Matrix Inverse and Vector/Matrix norms.
    Thursday we switch gears to Curve Fitting, an application of Linear Algebra, and Friday covers
    Nonlinear Regression and 1D Linear Interpolation. The Midterm Exam follows on the next Monday and
    covers everything through this Friday's class.""",
    days=[
      dict(date="Monday", readings=["N/A"],
        lectures=["Linear Algebra Intro", "Solving Linear Algebra Problems in MATLAB",
                   "Existence and Uniqueness of Solutions", "Rope Tension (1/2)", "Rope Tension (2/2)"],
        duration="42:15"),
      dict(date="Tuesday", readings=["N/A"],
        lectures=["Wheatstone Bridge (1/2)", "Wheatstone Bridge (2/2)", "Column Elongation",
                   "Traffic Network (1/2)", "Traffic Network (2/2)"],
        duration="59:01"),
      dict(date="Wednesday", readings=["N/A"],
        lectures=["Matrix Inverse", "Vector/Matrix Norms", "Reactor Concentrations", "Truss (1/2)",
                   "Truss (2/2)"],
        duration="54:26"),
      dict(date="Thursday",
        readings=['Kiusalaas Ch 3.4 (only up to the "Fitting Linear Forms" section)',
                   "MATLAB fit() Documentation", "fit() Postprocessing (read coeffvalues() and plot() docs)"],
        lectures=["Curve Fitting (1/2)", "Curve Fitting (2/2)", "Charles's Law"],
        duration="1:15:32"),
      dict(date="Friday",
        readings=["List of Library Models for Curve/Surface Fitting",
                   'Kiusalaas Ch 3.4 (only the "Fitting Exponential Functions" section)',
                   "Linear Interpolation (Westerink, University of Notre Dame).pdf",
                   "MATLAB interp1() Documentation", "Midterm Exam Guidelines Su22.pdf"],
        lectures=["Nonlinear Regression", "RC Circuit", "Animal Metabolism",
                   "Nonlinear Regression Example 3", "Polynomial Regression Example",
                   "Linear Interpolation (1/2)", "Linear Interpolation (2/2)", "Steam Table Interpolation"],
        duration="53:48"),
    ],
    callout="The Midterm Exam is the following Monday — it covers everything from the first day of class "
            "up to and including this Friday's class."),
  dict(
    num=4,
    blurb="""Last week we learned about Linear Algebra. This week we learn about Nonlinear Algebra, a.k.a.
    Root Finding — how to solve equations that cannot (or cannot easily) be linearized. Tuesday introduces
    the Graphical and Bisection Methods, Wednesday introduces Newton-Raphson, and Thursday introduces
    MATLAB's built-in solver fzero().""",
    callout="The Midterm Exam is Monday! It covers everything through last Friday's class.",
    days=[
      dict(date="Monday", readings=["Midterm Exam Guidelines Su22.pdf"],
        note="No lectures today due to the Midterm Exam. Good luck!"),
      dict(date="Tuesday",
        readings=["Kiusalaas Ch 4–4.3",
                   "Bisection Method Overview and Examples (optional)"],
        lectures=["Root Finding Introduction", "Root Finding: Graphical Method", "Bisection Method",
                   "Manual Iterations of the Bisection Method",
                   "MATLAB Implementation of the Bisection Method", "Critical Channel Depth"],
        duration="42:44"),
      dict(date="Wednesday",
        readings=["Kiusalaas Ch 4.5",
                   "Newton-Raphson Method Overview and Examples (optional)"],
        lectures=["Newton-Raphson Method", "Manual Iterations of the Newton-Raphson Method",
                   "MATLAB Implementation of the Newton-Raphson Method", "ODE Fixed Points"],
        duration="23:24"),
      dict(date="Thursday", readings=["MATLAB fzero() Documentation"],
        lectures=["The fzero() Function", "Redlich–Kwong Equation", "Population Study"],
        duration="25:40"),
      dict(date="Friday", readings=["Moody Chart Wikipedia page (optional)"],
        lectures=["Moody Diagram (1/2)", "Moody Diagram (2/2)"], duration="1:02:16"),
    ]),
  dict(
    num=5,
    blurb="""We switch gears to Numerical Differentiation and Integration. Monday covers Numerical
    Differentiation; Tuesday reviews the Unit Step Function and covers the Unit Pulse and Delta Function;
    Wednesday covers the Trapezoid Rule (and its variants), concluding the Calculus unit. Friday begins the
    final unit of the course: ODEs, starting with 1st order ODEs and sketching phase portraits.""",
    days=[
      dict(date="Monday", readings=["Kiusalaas Ch 5–5.2"],
        lectures=["Numerical Differentiation", "Stopping Distances", "Vehicle Pitch Rate (1/2)",
                   "Vehicle Pitch Rate (2/2)", "Numerical Differentiation: Step Size Exploration"],
        duration="51:59"),
      dict(date="Tuesday", readings=["N/A"],
        lectures=["Integration Review", "Step/Delta Integrals", "Pulse Function (1/2)",
                   "Pulse Function (2/2)"],
        duration="58:06"),
      dict(date="Wednesday",
        readings=['Kiusalaas Ch 6–6.2 (only up to the "Recursive Trapezoidal Rule" section)',
                   "trapz(), cumtrapz(), integral() MATLAB Documentation"],
        lectures=["Trapezoidal Rule Review", "Trapezoidal Rule Demo", "Shear/Moment Diagrams",
                   "Mechanical Work", "Space-Time Diagrams"],
        duration="45:56"),
      dict(date="Thursday", readings=["N/A"], note="No class — work on this week's assignments."),
      dict(date="Friday", readings=["N/A"],
        lectures=["ODEs Introduction", "1st Order ODEs Overview",
                   "Sketching Phase Portraits and Anticipated Solutions (1/3)",
                   "Sketching Phase Portraits and Anticipated Solutions (2/3)",
                   "Sketching Phase Portraits and Anticipated Solutions (3/3)"],
        duration="1:00:03"),
    ]),
  dict(
    num=6,
    blurb="""We finish ODEs on Tuesday, solving them numerically with MATLAB's built-in solver ode45().
    Wednesday and Thursday have no new readings/lectures — use the time to wrap up assignments (all due
    Thursday) and prepare for the Final Exam, administered Friday.""",
    days=[
      dict(date="Monday",
        readings=["ode45() and Summary of ODE Options — MATLAB documentation"],
        lectures=["The ode45() Function", "Skydiver (1/2)", "Skydiver (2/2)", "Population Model (1/2)",
                   "Population Model (2/2)", "Lumped Thermal Mass (1/2)", "Lumped Thermal Mass (2/2)"],
        duration="56:49",
        note="All Monday videos were cancelled that term, but are left here in case you want to watch."),
      dict(date="Tuesday",
        readings=["Kiusalaas Ch 7.1",
                   "A brief introduction to using ode45 in MATLAB (Berkeley).pdf (optional)"],
        note="Lectures cancelled."),
      dict(date="Wednesday", readings=["N/A"], note="No class."),
      dict(date="Thursday", readings=["N/A"], note="No class — all Week 6 assignments due tonight."),
      dict(date="Friday", readings=["Final Exam Guidelines Su22.pdf"],
        note="Final Exam."),
    ]),
]

TOTAL_WEEKS = len(WEEKS)

# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------
def esc(s): return html.escape(s, quote=True)

NAV_LINKS = [("index.html", "Home")] + \
            [(f"week{w['num']}.html", f"Week {w['num']}") for w in WEEKS]

def page_shell(title, active, body, description=""):
    nav_html = "\n".join(
        f'      <a href="{href}" class="{"active" if href == active else ""}">{label}</a>'
        for href, label in NAV_LINKS
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} · Numerical Methods (ME 2004)</title>
<meta name="description" content="{esc(description)}">
<link rel="stylesheet" href="assets/style.css">
<link rel="icon" href="data:,">
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">Numerical&nbsp;Methods <span>· ME 2004 video course</span></a>
    <nav>
{nav_html}
      <a href="{CHANNEL}/videos" target="_blank" rel="noopener">YouTube ↗</a>
    </nav>
  </div>
</header>
<main class="wrap">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <p>Lecture videos by Jaisohn Kim — <a href="{CHANNEL}" target="_blank" rel="noopener">youtube.com/@jaisohnkim</a>.
    This site is an unofficial, learner-facing mirror of the Canvas course shell for
    <em>Engineering Analysis: Numerical Methods</em>, built so anyone can follow the lectures in order.</p>
  </div>
</footer>
</body>
</html>
"""

def render_video_list(titles):
    items = []
    for t in titles:
        href, direct = video_link(t)
        cls = "" if direct else " class=\"search\""
        title_attr = "" if direct else ' title="Opens a search for this exact lecture title on the channel"'
        items.append(f'<li><a href="{href}"{cls}{title_attr} target="_blank" rel="noopener">▶ {esc(t)}</a></li>')
    return "<ul class=\"videos\">\n" + "\n".join(items) + "\n</ul>"

def render_day(day):
    date = day["date"]
    parts = [f'<article class="day">', f'<h3>{esc(date)}</h3>']
    if day.get("note"):
        parts.append(f'<p class="note">{esc(day["note"])}</p>')
    if day.get("readings"):
        parts.append('<div class="col readings"><h4>📚 Readings</h4><ul>')
        for r in day["readings"]:
            parts.append(f'<li>{esc(r)}</li>')
        parts.append('</ul></div>')
    if day.get("lectures"):
        dur = f' <span class="dur">({esc(day["duration"])})</span>' if day.get("duration") else ""
        parts.append(f'<div class="col lectures"><h4>🎬 Lectures{dur}</h4>')
        parts.append(render_video_list(day["lectures"]))
        parts.append('</div>')
    parts.append('</article>')
    return "\n".join(parts)

def render_week(w):
    prev = f'<a href="week{w["num"]-1}.html" class="prevnext">← Week {w["num"]-1}</a>' if w["num"] > 1 else '<span></span>'
    nextw = f'<a href="week{w["num"]+1}.html" class="prevnext">Week {w["num"]+1} →</a>' if w["num"] < TOTAL_WEEKS else '<span></span>'
    callout = f'<p class="callout">⚠️ {esc(w["callout"])}</p>' if w.get("callout") else ""
    days_html = "\n".join(render_day(d) for d in w["days"])
    body = f"""
<div class="weeknav">{prev}<h1>Week {w['num']}</h1>{nextw}</div>
<p class="blurb">{esc(w['blurb']).strip()}</p>
{callout}
<div class="days">
{days_html}
</div>
<div class="weeknav bottom">{prev}{nextw}</div>
"""
    return page_shell(f"Week {w['num']}", f"week{w['num']}.html", body,
                       description=f"Week {w['num']} reading and lecture schedule for ME 2004.")

def render_index():
    cards = []
    for w in WEEKS:
        cards.append(f"""
        <a class="weekcard" href="week{w['num']}.html">
          <h3>Week {w['num']}</h3>
        </a>""")
    body = f"""
<section class="hero">
  <h1>Numerical Methods Video Lectures</h1>
  <p class="lede">This site provides an organized video guide for ME 2004: Engineering Analysis Using Numerical Methods at Virginia Tech.
  Use the outline below to see the recommended viewing sequence and where each video fits within the progression of the course.

The schedule reflects the course as it was taught during a 6-week summer session. More recent versions of ME 2004 may use a different schedule, topic sequence, or set of materials, so current students should follow their instructor's guidance.</p>
  <p>Every lecture links out to Jaisohn's YouTube channel,
     <a href="{CHANNEL}" target="_blank" rel="noopener">@jaisohnkim</a>, which hosts the full video library
     of MATLAB and numerical-methods tutorials.</p>
</section>

<section>
  <h2>How to use this site</h2>
  <ol class="howto">
    <li>For each day, do the listed <strong>Readings</strong> first, then watch the <strong>lectures</strong>
        in order. Most videos are split into short sequences.</li>
    <li>The schedule is a suggestion, not a strict deadline. Pace yourself across the week.</li>
  </ol>
</section>

<section>
  <h2>Course schedule</h2>
  <div class="weekgrid">
    {''.join(cards)}
  </div>
</section>


"""
    return page_shell("Home", "index.html", body,
                       description="An unofficial mirror of the ME 2004 Numerical Methods Canvas course "
                                    "shell, organized week by week with links to every lecture video.")

CSS = """
:root{
  --ink:#1c2430; --muted:#5b6672; --line:#e3e7ec; --bg:#fbfbfc; --panel:#ffffff;
  --accent:#8b2f2f; --accent-ink:#6e2424; --focus:#2e5aac;
  --radius:10px;
  font-size:16px;
}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;}
body{
  background:var(--bg); color:var(--ink);
  font-family:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;
  line-height:1.6;
}
.wrap{max-width:900px;margin:0 auto;padding:0 20px;}
a{color:var(--accent-ink);}
a:hover{color:var(--accent);}

.site-header{border-bottom:1px solid var(--line); background:var(--panel);}
.site-header .wrap{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;padding:14px 20px;gap:10px;}
.brand{font-weight:700;font-size:1.15rem;text-decoration:none;color:var(--ink);}
.brand span{font-weight:400;color:var(--muted);font-size:0.85rem;}
nav{display:flex;flex-wrap:wrap;gap:4px 14px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:0.92rem;}
nav a{text-decoration:none;color:var(--muted);padding:4px 2px;border-bottom:2px solid transparent;}
nav a.active{color:var(--ink);border-bottom-color:var(--accent);font-weight:600;}
nav a:hover{color:var(--ink);}

main{padding:36px 20px 60px;}

.hero h1{font-size:2rem;margin-bottom:0.4em;}
.hero .lede{font-size:1.08rem;color:var(--ink);}

h1{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;letter-spacing:-0.01em;}
h2{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:1.35rem;margin-top:2.2em;border-bottom:1px solid var(--line);padding-bottom:0.3em;}
h3{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}

.howto{padding-left:1.2em;}
.howto li{margin-bottom:0.4em;}

.weekgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-top:1em;}
.weekcard{display:block;background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);
  padding:16px 18px;text-decoration:none;color:var(--ink);transition:border-color .15s, transform .15s;}
.weekcard:hover{border-color:var(--accent);transform:translateY(-1px);}
.weekcard h3{margin:0;font-size:1.1rem;color:var(--accent-ink);}

.weeknav{display:flex;align-items:baseline;justify-content:space-between;gap:12px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;flex-wrap:wrap;}
.weeknav h1{margin:0;font-size:1.6rem;flex:1;text-align:center;}
.weeknav.bottom{margin-top:2.5em;padding-top:1em;border-top:1px solid var(--line);}
.prevnext{text-decoration:none;font-weight:600;white-space:nowrap;}

.blurb{margin-top:1.2em;}
.callout{background:#fbeeea;border:1px solid #e7c6bc;color:var(--accent-ink);border-radius:var(--radius);padding:10px 14px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:0.95rem;}

.days{margin-top:1.5em;display:flex;flex-direction:column;gap:18px;}
.day{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:16px 20px;}
.day h3{margin:0 0 10px;font-size:1.1rem;color:var(--accent-ink);}
.day .note{font-style:italic;color:var(--muted);margin:0.2em 0;}
.day .col{margin-top:10px;}
.day .col h4{margin:0 0 6px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:0.85rem;text-transform:uppercase;letter-spacing:0.04em;color:var(--muted);}
.day .col h4 .dur{text-transform:none;letter-spacing:normal;font-weight:400;}
.day ul{margin:0;padding-left:1.3em;}
.day .readings li{color:#333;}
.videos{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:4px;}
.videos li a{text-decoration:none;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:0.96rem;}
.videos li a.search{color:var(--focus);}
.videos li a.search::after{content:" (search)";font-size:0.78em;color:var(--muted);}

.site-footer{border-top:1px solid var(--line);margin-top:40px;padding:22px 0;color:var(--muted);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:0.85rem;}
"""

def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    with open(os.path.join(OUT, "assets", "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_index())
    for w in WEEKS:
        with open(os.path.join(OUT, f"week{w['num']}.html"), "w", encoding="utf-8") as f:
            f.write(render_week(w))
    print("Built", 1 + len(WEEKS), "HTML pages into", OUT)

if __name__ == "__main__":
    main()
