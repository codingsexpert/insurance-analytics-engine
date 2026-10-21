"""
Clean up src/api/index.html:
1. Remove all emojis (🌙, ☀️, 🔍, ✅, ⚠️, ⚡) and replace with clean SVGs or text.
2. Remove top-bar clutter.
3. Streamline header titles and button labels.
4. Replace long wordy panel-desc paragraphs with crisp, minimal 1-line labels.
5. Keep UI clean, minimal, and enterprise-grade.
"""

import re

with open('src/api/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. REMOVE TOP-BAR FROM CSS AND HTML
# Remove top-bar CSS
content = re.sub(r'/\* Top Bar Announcement & System Status \*/[\s\S]*?\.top-bar strong \{ color: #f8fafc; font-weight: 600; \}', '', content)
# Remove top-bar HTML
content = re.sub(r'<!-- Top Announcement & System Status Bar -->[\s\S]*?<!-- Header -->', '<!-- Header -->', content)

# 2. CLEAN UP HEADER HTML (Minimalist, No Emojis, Clean SVGs)
old_header_pattern = r'<header>[\s\S]*?</header>'

sun_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'
moon_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'

new_header = f"""<header>
    <div class="brand">
      <div class="brand-logo">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="8 11 12 15 16 9"/></svg>
      </div>
      <div>
        <div class="brand-title">Actuaria <span class="brand-badge">Engine</span></div>
        <div class="brand-subtitle">Insurance Analytics & Rating Platform</div>
      </div>
    </div>
    <div class="header-badges">
      <button class="btn-audit" onclick="switchTab('lakehouse'); document.getElementById('ingest-panel-container')?.scrollIntoView({{behavior:'smooth'}});">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
        Import Data
      </button>
      <button class="btn-audit" onclick="openAuditModal()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
        Audit Memo
      </button>
      <button class="btn-audit" onclick="window.print()" title="Print / Export PDF">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
        Print PDF
      </button>
      <button id="theme-toggle-btn" class="btn-audit" onclick="toggleTheme()" title="Toggle Theme">
        <span id="theme-icon">{moon_svg}</span>
        <span id="theme-text">Dark</span>
      </button>
      <div class="status-pill">
        <span class="status-dot"></span>
        <span>SQLite Ready</span>
      </div>
    </div>
  </header>"""

content = re.sub(old_header_pattern, new_header, content)

# 3. CLEAN UP SEARCH PLACEHOLDERS (NO EMOJI)
content = content.replace('placeholder="🔍 Search territory, vehicle, age band..."', 'placeholder="Filter cells by territory, vehicle, age band..."')

# 4. CLEAN UP TOASTS JAVASCRIPT (SVGs, NO EMOJIS)
old_toast_logic = """      let icon = 'ℹ️';
      if (type === 'success') icon = '✅';
      if (type === 'error') icon = '⚠️';
      if (type === 'warning') icon = '⚡';

      toast.innerHTML = `<span style="font-size:1.1rem;">${icon}</span><span>${message}</span>`;"""

new_toast_logic = """      let iconSvg = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>';
      if (type === 'success') {
        iconSvg = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>';
      } else if (type === 'error') {
        iconSvg = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>';
      } else if (type === 'warning') {
        iconSvg = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>';
      }

      toast.innerHTML = `<span style="display:inline-flex; align-items:center;">${iconSvg}</span><span>${message}</span>`;"""

content = content.replace(old_toast_logic, new_toast_logic)

# 5. CLEAN UP THEME JS (NO EMOJIS IN INNERTEXT)
old_theme_set = """        if (theme === 'dark') {
          icon.innerText = '☀️';
          text.innerText = 'Light';
        } else {
          icon.innerText = '🌙';
          text.innerText = 'Dark';
        }"""

new_theme_set = f"""        if (theme === 'dark') {{
          icon.innerHTML = '{sun_svg}';
          text.innerText = 'Light';
        }} else {{
          icon.innerHTML = '{moon_svg}';
          text.innerText = 'Dark';
        }}"""

content = content.replace(old_theme_set, new_theme_set)

# 6. STREAMLINE WORDY PANEL DESCRIPTIONS (.panel-desc) TO CLEAN 1-LINERS
replacements = [
    # Gold layer
    (
        r'<p class="panel-desc">\s*Aggregated by Territory, Driver Age Band, and Vehicle Type in SQLite[\s\S]*?<\/p>',
        '<p class="panel-desc">Rating cell empirical frequency, severity, and loss cost aggregations.</p>'
    ),
    # Rating quote
    (
        r'<p class="panel-desc">\s*Specify driver and vehicle risk parameters to instantaneously calculate[\s\S]*?<\/p>',
        '<p class="panel-desc">Calculate expected frequency, severity, and pure premium quote.</p>'
    ),
    # Batch scoring
    (
        r'<p class="panel-desc">\s*Executes automated batch inference across unrated in-force book policies[\s\S]*?<\/p>',
        '<p class="panel-desc">Batch risk tier segmentation and projected Gross Written Premium.</p>'
    ),
    # Stress test
    (
        r'<p class="panel-desc">\s*Simulate inflation shocks on claim severity, weather-induced frequency surges[\s\S]*?<\/p>',
        '<p class="panel-desc">Inflation shock, storm surge, and reinsurance capital stress testing.</p>'
    ),
    # Geo risk
    (
        r'<p class="panel-desc">\s*Total Insured Value \(TIV in ₹\) exposure concentration across territories[\s\S]*?<\/p>',
        '<p class="panel-desc">Total Insured Value exposure concentration and 1-in-100 / 1-in-250 Yr PML.</p>'
    ),
    # Reserving triangle
    (
        r'<p class="panel-desc">\s*Accident Year \(AY\) vs Development Year \(Dev 0-4\) cumulative paid loss evolution[\s\S]*?<\/p>',
        '<p class="panel-desc">Accident Year cumulative loss emergence matrix.</p>'
    ),
    # IBNR summary
    (
        r'<p class="panel-desc">\s*Applies age-to-age Link Ratios \(LDF\) and Cumulative Development Factors[\s\S]*?<\/p>',
        '<p class="panel-desc">Chain Ladder link ratios (LDF) and estimated IBNR reserves.</p>'
    ),
    # Price elasticity
    (
        r'<p class="panel-desc">\s*Test renewal pricing scenarios for individual policies in ₹ to evaluate[\s\S]*?<\/p>',
        '<p class="panel-desc">Logistic churn sensitivity and renewal conversion projection.</p>'
    ),
    # Portfolio renewal
    (
        r'<p class="panel-desc">\s*Simulates the tradeoff between price change %, policyholder retention rate[\s\S]*?<\/p>',
        '<p class="panel-desc">Retention trade-off curves across price change spectrum.</p>'
    ),
    # Relativities
    (
        r'<p class="panel-desc">\s*Multiplicative relativities exported for IRDAI \/ State DOI Regulatory Rate Filing[\s\S]*?<\/p>',
        '<p class="panel-desc">Published rating relativities and multipliers.</p>'
    ),
    # Fair lending
    (
        r'<p class="panel-desc">\s*Audits rating tier distribution across demographic groups to ensure[\s\S]*?<\/p>',
        '<p class="panel-desc">Four-Fifths (80%) Rule Disparate Impact Ratio audit.</p>'
    ),
    # Claims fraud
    (
        r'<p class="panel-desc">\s*Evaluates incoming First Notice of Loss \(FNOL\) claims in ₹ for suspicious patterns[\s\S]*?<\/p>',
        '<p class="panel-desc">First Notice of Loss triage and automated SIU routing.</p>'
    ),
    # Custom CSV
    (
        r'<p class="panel-desc">\s*Upload custom policy book or claims loss run data\. Automatically validates columns[\s\S]*?<\/p>',
        '<p class="panel-desc">Ingest policy or claims datasets into local lakehouse.</p>'
    ),
    # Double lift
    (
        r'<p class="panel-desc">\s*Evaluates risk segmentation across 10 deciles of predicted risk in ₹[\s\S]*?<\/p>',
        '<p class="panel-desc">Model risk discrimination across 10 deciles.</p>'
    ),
]

for pat, repl in replacements:
    content = re.sub(pat, repl, content)

with open('src/api/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Cleaned up emojis, top-bar, and text bloat successfully!")
