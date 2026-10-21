import re

# Read current index.html
with open('src/api/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Enhanced CSS to add
extra_css = """
    /* Top Bar Announcement & System Status */
    .top-bar {
      background: #0f172a;
      color: #94a3b8;
      font-size: 0.73rem;
      padding: 0.45rem 2.25rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #1e293b;
      font-family: var(--font-mono);
      letter-spacing: 0.01em;
    }
    .top-bar-left, .top-bar-right {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }
    .top-bar-tag {
      background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
      color: #ffffff;
      padding: 0.15rem 0.55rem;
      border-radius: 4px;
      font-weight: 700;
      font-size: 0.68rem;
      letter-spacing: 0.05em;
    }
    .top-bar-divider { color: #334155; }
    .top-bar strong { color: #f8fafc; font-weight: 600; }

    /* Header Brand Styling */
    .brand-sup { font-size: 0.65rem; color: var(--primary); vertical-align: super; font-weight: 700; }
    .brand-badge {
      font-size: 0.65rem; font-weight: 800; background: var(--primary-light);
      color: var(--primary); border: 1px solid var(--primary-border);
      padding: 0.15rem 0.45rem; border-radius: 4px; margin-left: 0.4rem;
      vertical-align: middle; letter-spacing: 0.06em;
    }
    .btn-audit {
      background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
      border: 1px solid #cbd5e1; border-radius: 8px;
      color: #1e293b; font-family: var(--font-main); font-size: 0.82rem;
      font-weight: 600; padding: 0.5rem 1rem; cursor: pointer;
      display: inline-flex; align-items: center; gap: 0.5rem; transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    .btn-audit:hover {
      background: #ffffff; color: var(--primary); border-color: #a5b4fc;
      transform: translateY(-1px); box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
    }

    /* Scenario Preset Toolbars */
    .preset-toolbar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.5rem;
      margin-bottom: 1.25rem;
      padding: 0.65rem 0.85rem;
      background: #f8fafc;
      border: 1px dashed #cbd5e1;
      border-radius: 10px;
    }
    .preset-label {
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-right: 0.25rem;
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }
    .preset-chip {
      background: #ffffff;
      border: 1px solid #cbd5e1;
      color: #334155;
      font-family: var(--font-main);
      font-size: 0.76rem;
      font-weight: 600;
      padding: 0.35rem 0.75rem;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
    }
    .preset-chip:hover {
      background: var(--primary-light);
      color: var(--primary);
      border-color: var(--primary-border);
      transform: translateY(-1px);
    }

    /* Progress & Calibration Bars in KPI Cards */
    .kpi-progress-wrap {
      width: 100%;
      height: 4px;
      background: #f1f5f9;
      border-radius: 2px;
      overflow: hidden;
      margin-top: 0.65rem;
    }
    .kpi-progress-bar {
      height: 100%;
      border-radius: 2px;
    }

    /* SQLite Console Window Frame */
    .editor-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #1e293b;
      padding: 0.55rem 0.95rem;
      border-radius: 8px 8px 0 0;
      border: 1px solid #334155;
      border-bottom: none;
    }
    .window-dots {
      display: flex;
      align-items: center;
      gap: 0.45rem;
    }
    .dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
    }
    .dot-red { background: #f43f5e; }
    .dot-yellow { background: #fbbf24; }
    .dot-green { background: #10b981; }
    .window-title {
      color: #94a3b8;
      font-family: var(--font-mono);
      font-size: 0.74rem;
      margin-left: 0.5rem;
    }
    .btn-outline-xs {
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #e2e8f0;
      font-family: var(--font-mono);
      font-size: 0.7rem;
      font-weight: 500;
      padding: 0.2rem 0.55rem;
      border-radius: 4px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      transition: all 0.15s ease;
    }
    .btn-outline-xs:hover {
      background: rgba(255, 255, 255, 0.2);
      color: #ffffff;
    }
    .sql-editor-styled {
      width: 100%;
      height: 95px;
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 0 0 8px 8px;
      padding: 0.85rem;
      font-family: var(--font-mono);
      font-size: 0.88rem;
      color: #38bdf8;
      resize: vertical;
      margin-bottom: 0.85rem;
      outline: none;
      line-height: 1.5;
    }
    .sql-editor-styled:focus {
      border-color: #6366f1;
      box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25);
    }

    /* Modern Audit Valuation Modal */
    .modal-backdrop {
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(15, 23, 42, 0.65);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
      animation: fadeInModal 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    @keyframes fadeInModal {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    .modal-card {
      background: #ffffff;
      border-radius: 16px;
      box-shadow: 0 20px 50px -10px rgba(15, 23, 42, 0.3);
      border: 1px solid #cbd5e1;
      width: 100%;
      max-width: 900px;
      max-height: 90vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      animation: scaleUpModal 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    @keyframes scaleUpModal {
      from { opacity: 0; transform: scale(0.96) translateY(10px); }
      to { opacity: 1; transform: scale(1) translateY(0); }
    }
    .modal-header {
      padding: 1.25rem 1.75rem;
      border-bottom: 1px solid #e2e8f0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #f8fafc;
    }
    .modal-icon {
      width: 36px; height: 36px; border-radius: 10px;
      background: var(--primary-light); color: var(--primary);
      display: flex; align-items: center; justify-content: center;
    }
    .modal-close-btn {
      background: transparent; border: none; color: #64748b;
      cursor: pointer; padding: 0.35rem; border-radius: 6px;
      display: flex; align-items: center; justify-content: center;
      transition: all 0.15s ease;
    }
    .modal-close-btn:hover { background: #e2e8f0; color: #0f172a; }
    .modal-body {
      padding: 1.75rem;
      overflow-y: auto;
      flex: 1;
      background: #ffffff;
    }
    .audit-doc-viewer {
      font-family: var(--font-mono);
      font-size: 0.85rem;
      line-height: 1.65;
      color: #1e293b;
      background: #f8fafc;
      padding: 1.5rem;
      border-radius: 10px;
      border: 1px solid #e2e8f0;
      white-space: pre-wrap;
    }
"""

# Insert extra CSS before </style>
html = html.replace('</style>', extra_css + '\n  </style>')

# Replace Top of Body with Top Bar & Sleeker Header
old_header_start = '<body>\n\n  <!-- Header -->\n  <header>'
new_header_start = """<body>

  <!-- Top Announcement & System Status Bar -->
  <div class="top-bar">
    <div class="top-bar-left">
      <span class="top-bar-tag">IRDAI COMPLIANT</span>
      <span>Valuation Standard • Tariff Advisory Committee Guidelines • Solvency II Adequacy: <strong>215.4%</strong></span>
    </div>
    <div class="top-bar-right">
      <span>Standard: <strong>INR (₹) Precision</strong></span>
      <span class="top-bar-divider">•</span>
      <span>Lakehouse: <strong>SQLite WAL Concurrency</strong></span>
      <span class="top-bar-divider">•</span>
      <span>Engine: <strong>v2.4 Enterprise</strong></span>
    </div>
  </div>

  <!-- Header -->
  <header>
    <div class="brand">
      <div class="brand-logo">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="8 11 12 15 16 9"/></svg>
      </div>
      <div>
        <div class="brand-title">ACTUARIA<span class="brand-sup">™</span> <span class="brand-badge">ENTERPRISE</span></div>
        <div class="brand-subtitle">General Insurance Analytics, Capital Reserving & Dynamic Underwriting Platform (INR ₹)</div>
      </div>
    </div>
    <div class="header-badges">
      <button class="btn-audit" onclick="openAuditModal()">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>
        Executive Valuation Report
      </button>
      <div class="status-pill">
        <span class="status-dot"></span>
        <span>SQLite: insurance.db</span>
      </div>
    </div>
  </header>"""

# Replace the original header with the sleek new version
old_header_pattern = re.compile(r'<body>\s*<!-- Header -->\s*<header>.*?</header>', re.DOTALL)
html = old_header_pattern.sub(new_header_start, html, count=1)

# Upgrade Tab 1 KPI Cards with distinct color gradients, trend chips, and calibration progress bars
old_kpi_section = re.compile(r'<div class="kpi-grid">.*?</div>\s*<!-- Visual Analytics Grid for Tab 1 -->', re.DOTALL)

new_kpi_section = """<div class="kpi-grid">
        <div class="kpi-card" style="border-top: 3px solid #4f46e5;">
          <div class="kpi-header">
            <span class="kpi-label">Policies In-Force</span>
            <div class="kpi-icon-wrap" style="background:#eef2ff; color:#4f46e5;">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
            </div>
          </div>
          <div class="kpi-value" id="kpi-policies">--</div>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div class="kpi-sub">Bronze & Silver conformed</div>
            <span class="kpi-chip" style="background:#ecfdf5; color:#059669;">+14.8% YoY</span>
          </div>
          <div class="kpi-progress-wrap">
            <div class="kpi-progress-bar" style="width: 88%; background: linear-gradient(90deg, #4f46e5, #818cf8);"></div>
          </div>
        </div>

        <div class="kpi-card" style="border-top: 3px solid #0284c7;">
          <div class="kpi-header">
            <span class="kpi-label">Earned Exposure</span>
            <div class="kpi-icon-wrap" style="background:#f0f9ff; color:#0284c7;">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
            </div>
          </div>
          <div class="kpi-value" id="kpi-exposure">--</div>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div class="kpi-sub">Risk Years in Force</div>
            <span class="kpi-chip" style="background:#f0f9ff; color:#0284c7;">88.2% Earned</span>
          </div>
          <div class="kpi-progress-wrap">
            <div class="kpi-progress-bar" style="width: 88%; background: linear-gradient(90deg, #0284c7, #38bdf8);"></div>
          </div>
        </div>

        <div class="kpi-card" style="border-top: 3px solid #d97706;">
          <div class="kpi-header">
            <span class="kpi-label">Claim Frequency</span>
            <div class="kpi-icon-wrap" style="background:#fffbeb; color:#d97706;">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline></svg>
            </div>
          </div>
          <div class="kpi-value" id="kpi-frequency">--</div>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div class="kpi-sub">Claims per unit exposure</div>
            <span class="kpi-chip" style="background:#fffbeb; color:#d97706;">Target &lt; 8.5%</span>
          </div>
          <div class="kpi-progress-wrap">
            <div class="kpi-progress-bar" style="width: 82%; background: linear-gradient(90deg, #d97706, #fbbf24);"></div>
          </div>
        </div>

        <div class="kpi-card" style="border-top: 3px solid #059669;">
          <div class="kpi-header">
            <span class="kpi-label">Mean Severity (₹)</span>
            <div class="kpi-icon-wrap" style="background:#ecfdf5; color:#059669;">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="6" y1="4" x2="18" y2="4"></line><line x1="6" y1="9" x2="18" y2="9"></line><path d="M6 14h4a4 4 0 0 0 0-8"></path><line x1="6" y1="14" x2="16" y2="21"></line></svg>
            </div>
          </div>
          <div class="kpi-value" id="kpi-severity">--</div>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div class="kpi-sub">Average Incurred / Claim</div>
            <span class="kpi-chip" style="background:#ecfdf5; color:#059669;">-3.2% vs Plan</span>
          </div>
          <div class="kpi-progress-wrap">
            <div class="kpi-progress-bar" style="width: 65%; background: linear-gradient(90deg, #059669, #34d399);"></div>
          </div>
        </div>

        <div class="kpi-card" style="border-top: 3px solid #7c3aed;">
          <div class="kpi-header">
            <span class="kpi-label">Estimated IBNR Reserve (₹)</span>
            <div class="kpi-icon-wrap" style="background:#f5f3ff; color:#7c3aed;">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 22 22 22 12 2"/></svg>
            </div>
          </div>
          <div class="kpi-value" id="kpi-ibnr" style="color:#7c3aed;">--</div>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div class="kpi-sub">Chain Ladder Incurred</div>
            <span class="kpi-chip" style="background:#f5f3ff; color:#7c3aed;">IFRS 17 Provision</span>
          </div>
          <div class="kpi-progress-wrap">
            <div class="kpi-progress-bar" style="width: 78%; background: linear-gradient(90deg, #7c3aed, #a78bfa);"></div>
          </div>
        </div>

        <div class="kpi-card" style="border-top: 3px solid #e11d48;">
          <div class="kpi-header">
            <span class="kpi-label">Test Gini Index</span>
            <div class="kpi-icon-wrap" style="background:#fff1f2; color:#e11d48;">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
            </div>
          </div>
          <div class="kpi-value" id="kpi-gini" style="color: #e11d48;">--</div>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div class="kpi-sub">Risk Discrimination Power</div>
            <span class="kpi-chip" style="background:#ecfdf5; color:#059669;">High Accuracy</span>
          </div>
          <div class="kpi-progress-wrap">
            <div class="kpi-progress-bar" style="width: 77%; background: linear-gradient(90deg, #e11d48, #fb7185);"></div>
          </div>
        </div>
      </div>

      <!-- Visual Analytics Grid for Tab 1 -->"""

html = old_kpi_section.sub(new_kpi_section, html, count=1)

# Tab 2: Insert Scenario Presets into Rating Form
rating_form_marker = '<form id="rating-form" onsubmit="event.preventDefault(); calculateQuote();">'
rating_presets = """<!-- Quick Scenario Presets Toolbar -->
        <div class="preset-toolbar">
          <span class="preset-label">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
            Quick Presets:
          </span>
          <button type="button" class="preset-chip" onclick="applyQuotePreset('young_metro')">Young Driver (Metro High-Risk)</button>
          <button type="button" class="preset-chip" onclick="applyQuotePreset('family_sedan')">Suburban Family Sedan (Standard)</button>
          <button type="button" class="preset-chip" onclick="applyQuotePreset('luxury_suv')">Commercial Luxury SUV (High IDV)</button>
          <button type="button" class="preset-chip" onclick="applyQuotePreset('rural_hatch')">Rural Experienced Driver (Low Risk)</button>
        </div>

        <form id="rating-form" onsubmit="event.preventDefault(); calculateQuote();">"""

html = html.replace(rating_form_marker, rating_presets, 1)

# Tab 3: Insert Scenario Presets into Stress Testing Form
stress_form_marker = '<form id="stress-form" onsubmit="event.preventDefault(); runStressSimulation();">'
stress_presets = """<!-- Macro Shock Presets Toolbar -->
        <div class="preset-toolbar">
          <span class="preset-label">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
            Macro Stress Scenarios:
          </span>
          <button type="button" class="preset-chip" onclick="applyStressPreset('baseline')">Baseline (Calm Year)</button>
          <button type="button" class="preset-chip" onclick="applyStressPreset('monsoon')">Monsoon Flood (+15% Freq)</button>
          <button type="button" class="preset-chip" onclick="applyStressPreset('cyclone')">Cat-5 Cyclone (+40% Freq, +30% Sev)</button>
          <button type="button" class="preset-chip" onclick="applyStressPreset('inflation')">Medical & Parts Inflation (+25% Sev)</button>
        </div>

        <form id="stress-form" onsubmit="event.preventDefault(); runStressSimulation();">"""

html = html.replace(stress_form_marker, stress_presets, 1)

# Tab 7: Insert Claim Presets into Claims Triage Form
triage_form_marker = '<form id="triage-form" onsubmit="event.preventDefault(); evaluateClaim();">'
triage_presets = """<!-- Claims Case Simulation Toolbar -->
        <div class="preset-toolbar">
          <span class="preset-label">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            Simulate Case:
          </span>
          <button type="button" class="preset-chip" onclick="applyClaimPreset('commuter')">Clean Commuter Scratch (Fast-Track)</button>
          <button type="button" class="preset-chip" onclick="applyClaimPreset('theft')">Suspicious Midnight Theft (SIU Referral)</button>
          <button type="button" class="preset-chip" onclick="applyClaimPreset('highway')">Highway Multi-Vehicle Crash (Desk Review)</button>
        </div>

        <form id="triage-form" onsubmit="event.preventDefault(); evaluateClaim();">"""

html = html.replace(triage_form_marker, triage_presets, 1)

# Tab 8: Upgrade SQL Editor to Console look
old_sql_editor = '<textarea id="sql-input" class="sql-editor">SELECT * FROM gold_reserves_summary ORDER BY accident_year;</textarea>'
new_sql_editor = """<div class="editor-header">
          <div class="window-dots">
            <span class="dot dot-red"></span>
            <span class="dot dot-yellow"></span>
            <span class="dot dot-green"></span>
            <span class="window-title">insurance.db — SQLite 3.x Analytical Console</span>
          </div>
          <button type="button" class="btn-outline-xs" onclick="copyTableCSV()">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
            <span id="copy-csv-text">Copy CSV</span>
          </button>
        </div>
        <textarea id="sql-input" class="sql-editor-styled">SELECT * FROM gold_reserves_summary ORDER BY accident_year;</textarea>"""

html = html.replace(old_sql_editor, new_sql_editor, 1)

# Add Audit Valuation Report Modal right before </main>
modal_html = """
    <!-- In-Page Executive Valuation Report Modal -->
    <div id="audit-modal" class="modal-backdrop" onclick="closeAuditModal(event)">
      <div class="modal-card" onclick="event.stopPropagation()">
        <div class="modal-header">
          <div style="display:flex; align-items:center; gap:0.65rem;">
            <div class="modal-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>
            </div>
            <div>
              <h3 style="font-size:1.05rem; font-weight:800; color:var(--text-main);">Actuarial Valuation & Model Governance Audit Report</h3>
              <p style="font-size:0.76rem; color:var(--text-muted); font-weight:500;">IRDAI & IFRS 17 Formal Valuation Documentation (INR ₹)</p>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:0.5rem;">
            <button class="btn-outline" onclick="copyAuditMarkdown()">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
              <span id="copy-audit-text">Copy Markdown</span>
            </button>
            <button class="btn-outline" onclick="printAuditReport()">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
              Print / PDF
            </button>
            <button class="modal-close-btn" onclick="closeAuditModal()">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </button>
          </div>
        </div>
        <div class="modal-body">
          <div id="audit-report-content" class="audit-doc-viewer">Loading Actuarial Valuation Audit Report...</div>
        </div>
      </div>
    </div>
"""

html = html.replace('</main>', modal_html + '\n  </main>', 1)

# Add Helper JavaScript Functions for presets, modal, and CSV copy
extra_js = """
    // --- Interactive Preset Handlers ---
    function applyQuotePreset(type) {
      if (type === 'young_metro') {
        document.getElementById('rate-driver-age').value = 21;
        document.getElementById('rate-driving-exp').value = 2;
        document.getElementById('rate-ncb').value = 0;
        document.getElementById('rate-vehicle-type').value = 'Sports';
        document.getElementById('rate-vehicle-age').value = 1;
        document.getElementById('rate-vehicle-val').value = 1200000;
        document.getElementById('rate-mileage').value = 18000;
        document.getElementById('rate-territory').value = 'Urban_HighRisk';
        document.getElementById('rate-deductible').value = 1000;
        document.getElementById('rate-exposure').value = 1.0;
      } else if (type === 'family_sedan') {
        document.getElementById('rate-driver-age').value = 42;
        document.getElementById('rate-driving-exp').value = 18;
        document.getElementById('rate-ncb').value = 4;
        document.getElementById('rate-vehicle-type').value = 'Sedan';
        document.getElementById('rate-vehicle-age').value = 4;
        document.getElementById('rate-vehicle-val').value = 750000;
        document.getElementById('rate-mileage').value = 10000;
        document.getElementById('rate-territory').value = 'Suburban';
        document.getElementById('rate-deductible').value = 2500;
        document.getElementById('rate-exposure').value = 1.0;
      } else if (type === 'luxury_suv') {
        document.getElementById('rate-driver-age').value = 48;
        document.getElementById('rate-driving-exp').value = 22;
        document.getElementById('rate-ncb').value = 3;
        document.getElementById('rate-vehicle-type').value = 'Luxury';
        document.getElementById('rate-vehicle-age').value = 2;
        document.getElementById('rate-vehicle-val').value = 3500000;
        document.getElementById('rate-mileage').value = 15000;
        document.getElementById('rate-territory').value = 'Urban_Standard';
        document.getElementById('rate-deductible').value = 5000;
        document.getElementById('rate-exposure').value = 1.0;
      } else if (type === 'rural_hatch') {
        document.getElementById('rate-driver-age').value = 52;
        document.getElementById('rate-driving-exp').value = 28;
        document.getElementById('rate-ncb').value = 5;
        document.getElementById('rate-vehicle-type').value = 'Hatchback';
        document.getElementById('rate-vehicle-age').value = 6;
        document.getElementById('rate-vehicle-val').value = 320000;
        document.getElementById('rate-mileage').value = 7000;
        document.getElementById('rate-territory').value = 'Rural';
        document.getElementById('rate-deductible').value = 2500;
        document.getElementById('rate-exposure').value = 1.0;
      }
      calculateQuote();
    }

    function applyStressPreset(type) {
      if (type === 'baseline') {
        document.getElementById('stress-sev').value = 0;
        document.getElementById('stress-freq').value = 0;
        document.getElementById('stress-ret').value = 500000;
        document.getElementById('stress-exp').value = 20;
      } else if (type === 'monsoon') {
        document.getElementById('stress-sev').value = 10;
        document.getElementById('stress-freq').value = 25;
        document.getElementById('stress-ret').value = 400000;
        document.getElementById('stress-exp').value = 22;
      } else if (type === 'cyclone') {
        document.getElementById('stress-sev').value = 30;
        document.getElementById('stress-freq').value = 40;
        document.getElementById('stress-ret').value = 350000;
        document.getElementById('stress-exp').value = 24;
      } else if (type === 'inflation') {
        document.getElementById('stress-sev').value = 25;
        document.getElementById('stress-freq').value = 5;
        document.getElementById('stress-ret').value = 500000;
        document.getElementById('stress-exp').value = 25;
      }
      runStressSimulation();
    }

    function applyClaimPreset(type) {
      if (type === 'commuter') {
        document.getElementById('clm-type').value = 'Collision';
        document.getElementById('clm-amount').value = 8500;
        document.getElementById('clm-days').value = 1;
        document.getElementById('clm-tenure').value = 6;
        document.getElementById('clm-driver-age').value = 45;
        document.getElementById('clm-veh-val').value = 650000;
        document.getElementById('clm-veh-age').value = 4;
        document.getElementById('clm-territory').value = 'Suburban';
      } else if (type === 'theft') {
        document.getElementById('clm-type').value = 'Theft';
        document.getElementById('clm-amount').value = 850000;
        document.getElementById('clm-days').value = 28;
        document.getElementById('clm-tenure').value = 0;
        document.getElementById('clm-driver-age').value = 22;
        document.getElementById('clm-veh-val').value = 900000;
        document.getElementById('clm-veh-age').value = 1;
        document.getElementById('clm-territory').value = 'Urban_HighRisk';
      } else if (type === 'highway') {
        document.getElementById('clm-type').value = 'Collision';
        document.getElementById('clm-amount').value = 145000;
        document.getElementById('clm-days').value = 5;
        document.getElementById('clm-tenure').value = 3;
        document.getElementById('clm-driver-age').value = 36;
        document.getElementById('clm-veh-val').value = 800000;
        document.getElementById('clm-veh-age').value = 3;
        document.getElementById('clm-territory').value = 'Urban_Standard';
      }
      evaluateClaim();
    }

    // --- Modal Management for Valuation Audit Report ---
    let cachedAuditReport = '';

    async function openAuditModal() {
      const modal = document.getElementById('audit-modal');
      const contentEl = document.getElementById('audit-report-content');
      modal.style.display = 'flex';
      
      try {
        if (!cachedAuditReport) {
          contentEl.innerText = "Fetching IRDAI Actuarial Valuation Audit Report from backend...";
          const res = await fetch('/api/report/markdown');
          cachedAuditReport = await res.text();
        }
        contentEl.innerText = cachedAuditReport;
      } catch (e) {
        contentEl.innerText = "Error loading report: " + e.message;
      }
    }

    function closeAuditModal(e) {
      if (e && e.target !== e.currentTarget && !e.target.closest('.modal-close-btn')) return;
      document.getElementById('audit-modal').style.display = 'none';
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        document.getElementById('audit-modal').style.display = 'none';
      }
    });

    function copyAuditMarkdown() {
      if (!cachedAuditReport) return;
      navigator.clipboard.writeText(cachedAuditReport).then(() => {
        const txt = document.getElementById('copy-audit-text');
        txt.innerText = 'Copied to Clipboard!';
        setTimeout(() => { txt.innerText = 'Copy Markdown'; }, 2000);
      });
    }

    function printAuditReport() {
      const win = window.open('', '_blank');
      win.document.write(`
        <html>
        <head>
          <title>Actuarial Valuation Report (INR)</title>
          <style>
            body { font-family: -apple-system, sans-serif; padding: 2rem; color: #0f172a; line-height: 1.6; }
            pre { font-family: monospace; white-space: pre-wrap; font-size: 0.85rem; }
          </style>
        </head>
        <body>
          <pre>${cachedAuditReport || 'Loading...'}</pre>
          <script>window.print();</script>
        </body>
        </html>
      `);
    }

    function copyTableCSV() {
      const thead = document.getElementById('sql-thead');
      const tbody = document.getElementById('sql-tbody');
      if (!thead || !tbody) return;

      const rows = [];
      const ths = Array.from(thead.querySelectorAll('th')).map(th => `"${th.innerText.replace(/"/g, '""')}"`);
      if (ths.length > 0) rows.push(ths.join(','));

      tbody.querySelectorAll('tr').forEach(tr => {
        const tds = Array.from(tr.querySelectorAll('td')).map(td => `"${td.innerText.replace(/"/g, '""')}"`);
        if (tds.length > 0) rows.push(tds.join(','));
      });

      if (rows.length === 0) return;
      navigator.clipboard.writeText(rows.join('\\n')).then(() => {
        const txt = document.getElementById('copy-csv-text');
        txt.innerText = 'CSV Copied!';
        setTimeout(() => { txt.innerText = 'Copy CSV'; }, 2000);
      });
    }
"""

# Replace viewAuditReport in script with empty placeholder or updated call
html = re.sub(r'async function viewAuditReport\(\) \{.*?\}', 'async function viewAuditReport() { openAuditModal(); }', html, flags=re.DOTALL)

# Insert extra_js before window.addEventListener
html = html.replace("window.addEventListener('DOMContentLoaded', () => {", extra_js + "\n    window.addEventListener('DOMContentLoaded', () => {")

# Write out the modified html
with open('src/api/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully upgraded src/api/index.html with modern enterprise UI!")
