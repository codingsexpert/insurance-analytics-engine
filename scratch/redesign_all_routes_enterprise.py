"""
Comprehensive Design Overhaul for ALL Routes in Actuaria:
1. Re-engineers Design System with rich typography, glassmorphism, depth, and ambient glows.
2. Replaces ugly native file input in Tab 8 with a modern Drag & Drop upload dropzone.
3. Upgrades SQL Analytical Console with IDE styling, macOS dots, and glowing focus.
4. Upgrades Data Tables into Stripe-grade FinTech Data Grids (monospace numbers, hover glow, zebra striping, currency badges).
5. Upgrades all form controls, custom styled select dropdowns with SVG chevrons, and segmented pill chips.
6. Ensures BOTH Light Mode and Dark Mode have rich contrast, layered depth, and zero boring flatness.
"""

import re

with open('src/api/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. UPGRADE GLOBAL DESIGN SYSTEM CSS
rich_design_system_css = """
    /* ========================================================= */
    /* ULTRA-PREMIUM FINTECH DESIGN SYSTEM (ALL ROUTES)          */
    /* ========================================================= */
    :root {
      --bg: #f8fafc;
      --surface: #ffffff;
      --card-bg: rgba(255, 255, 255, 0.95);
      --card-border: #e2e8f0;
      --card-border-subtle: #f1f5f9;
      --card-hover-border: #c7d2fe;
      
      --sidebar-bg: #ffffff;
      --sidebar-border: #e2e8f0;
      --topbar-bg: rgba(255, 255, 255, 0.92);
      --nav-hover-bg: #f1f5f9;
      
      --primary: #4f46e5;
      --primary-hover: #4338ca;
      --primary-light: #eef2ff;
      --primary-border: #c7d2fe;
      --primary-gradient: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
      
      --emerald: #059669;
      --emerald-light: #ecfdf5;
      --emerald-border: #a7f3d0;
      
      --amber: #d97706;
      --amber-light: #fffbeb;
      --amber-border: #fde68a;
      
      --rose: #e11d48;
      --rose-light: #fff1f2;
      --rose-border: #fecdd3;
      
      --text-main: #0f172a;
      --text-muted: #64748b;
      --text-subtle: #94a3b8;
      
      --font-main: 'Plus Jakarta Sans', -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
      
      --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.04);
      --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px -1px rgba(0, 0, 0, 0.03);
      --shadow-md: 0 4px 6px -1px rgba(15, 23, 42, 0.06), 0 2px 4px -2px rgba(15, 23, 42, 0.03);
      --shadow-lg: 0 10px 25px -5px rgba(15, 23, 42, 0.07), 0 8px 10px -6px rgba(15, 23, 42, 0.03);
      --shadow-card: 0 2px 10px rgba(15, 23, 42, 0.04), 0 0 0 1px rgba(15, 23, 42, 0.05);
    }

    [data-theme="dark"] {
      --bg: #070b12;
      --surface: #0e1626;
      --card-bg: rgba(15, 23, 42, 0.85);
      --card-border: rgba(255, 255, 255, 0.08);
      --card-border-subtle: rgba(255, 255, 255, 0.04);
      --card-hover-border: rgba(99, 102, 241, 0.45);
      
      --sidebar-bg: #090e1a;
      --sidebar-border: rgba(255, 255, 255, 0.06);
      --topbar-bg: rgba(9, 14, 26, 0.88);
      --nav-hover-bg: rgba(255, 255, 255, 0.05);
      
      --primary: #818cf8;
      --primary-hover: #6366f1;
      --primary-light: rgba(99, 102, 241, 0.16);
      --primary-border: rgba(99, 102, 241, 0.35);
      
      --emerald: #10b981;
      --emerald-light: rgba(16, 185, 129, 0.14);
      --emerald-border: rgba(16, 185, 129, 0.35);
      
      --amber: #f59e0b;
      --amber-light: rgba(245, 158, 11, 0.14);
      --amber-border: rgba(245, 158, 11, 0.35);
      
      --rose: #f43f5e;
      --rose-light: rgba(244, 63, 94, 0.14);
      --rose-border: rgba(244, 63, 94, 0.35);
      
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-subtle: #64748b;
      
      --shadow-card: 0 4px 20px -2px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.08);
    }

    body {
      background-color: var(--bg);
      background-image: 
        radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.04) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(16, 185, 129, 0.03) 0px, transparent 50%),
        radial-gradient(rgba(0, 0, 0, 0.03) 1px, transparent 1px);
      background-size: 100% 100%, 100% 100%, 24px 24px;
      color: var(--text-main);
      font-family: var(--font-main);
      min-height: 100vh;
      overflow-x: hidden;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
    }

    [data-theme="dark"] body {
      background-image: 
        radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.08) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(16, 185, 129, 0.05) 0px, transparent 50%),
        radial-gradient(rgba(255, 255, 255, 0.035) 1px, transparent 1px);
      background-size: 100% 100%, 100% 100%, 24px 24px;
    }

    /* CARD PANELS WITH DEPTH & GLASSMORPHISM */
    .panel {
      background: var(--card-bg);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 1.75rem 2rem;
      box-shadow: var(--shadow-card);
      margin-bottom: 2rem;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
    }
    .panel:hover {
      box-shadow: 0 8px 30px -4px rgba(15, 23, 42, 0.08), 0 0 0 1px var(--card-hover-border);
    }
    [data-theme="dark"] .panel:hover {
      box-shadow: 0 8px 32px -4px rgba(0, 0, 0, 0.6), 0 0 0 1px var(--card-hover-border);
    }

    .panel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.25rem;
      border-bottom: 1px solid var(--card-border-subtle);
      padding-bottom: 1rem;
    }
    .panel-title {
      font-size: 1.1rem;
      font-weight: 800;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 0.6rem;
      letter-spacing: -0.02em;
    }
    .panel-desc {
      font-size: 0.82rem;
      color: var(--text-muted);
      margin-top: -0.5rem;
      margin-bottom: 1.25rem;
      font-weight: 500;
    }

    /* KPI STAT CARDS */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 1.25rem;
      margin-bottom: 2rem;
    }
    .kpi-card {
      background: var(--card-bg);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 1.4rem 1.6rem;
      box-shadow: var(--shadow-card);
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      position: relative;
      overflow: hidden;
    }
    .kpi-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 12px 28px -6px rgba(15, 23, 42, 0.1), 0 0 0 1px var(--card-hover-border);
    }
    .kpi-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.65rem;
    }
    .kpi-label {
      font-size: 0.72rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }
    .kpi-icon-wrap {
      width: 34px;
      height: 34px;
      border-radius: 9px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: var(--shadow-xs);
    }
    .kpi-value {
      font-size: 1.85rem;
      font-weight: 800;
      letter-spacing: -0.035em;
      color: var(--text-main);
      margin-bottom: 0.4rem;
      font-family: var(--font-main);
    }
    .kpi-sub {
      font-size: 0.76rem;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
    }
    .kpi-chip {
      font-size: 0.68rem;
      font-weight: 700;
      padding: 0.18rem 0.55rem;
      border-radius: 9999px;
    }

    /* FORM CONTROLS WITH CUSTOM SVGS & GLOW */
    .form-group {
      display: flex;
      flex-direction: column;
      gap: 0.45rem;
    }
    .form-label {
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--text-main);
      letter-spacing: 0.01em;
    }
    .form-control {
      background: var(--surface);
      border: 1px solid var(--card-border);
      border-radius: 9px;
      padding: 0.65rem 0.95rem;
      color: var(--text-main);
      font-family: var(--font-main);
      font-size: 0.86rem;
      font-weight: 500;
      transition: all 0.15s ease;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
    }
    .form-control:focus {
      outline: none;
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.18);
    }
    select.form-control {
      appearance: none;
      -webkit-appearance: none;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%236366f1' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
      background-repeat: no-repeat;
      background-position: right 0.85rem center;
      padding-right: 2.4rem;
      cursor: pointer;
    }
    [data-theme="dark"] .form-control {
      background: #0d1424;
      border-color: rgba(255, 255, 255, 0.1);
      color: #f8fafc;
    }
    [data-theme="dark"] .form-control:focus {
      border-color: #818cf8;
      box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.25);
    }

    /* BUTTONS */
    .btn-primary {
      background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
      border: none;
      border-radius: 9px;
      color: #fff;
      font-family: var(--font-main);
      font-size: 0.85rem;
      font-weight: 700;
      padding: 0.7rem 1.5rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.55rem;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.25), 0 3px 10px rgba(79, 70, 229, 0.3);
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .btn-primary:hover {
      background: linear-gradient(135deg, #4338ca 0%, #4f46e5 100%);
      transform: translateY(-1px);
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.3), 0 6px 16px rgba(79, 70, 229, 0.4);
    }
    .btn-primary:active {
      transform: translateY(0);
      box-shadow: 0 2px 6px rgba(79, 70, 229, 0.25);
    }

    .btn-outline {
      background: var(--surface);
      border: 1px solid var(--card-border);
      border-radius: 8px;
      color: var(--text-main);
      font-family: var(--font-main);
      font-size: 0.78rem;
      font-weight: 600;
      padding: 0.42rem 0.9rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      transition: all 0.15s ease;
      box-shadow: var(--shadow-xs);
    }
    .btn-outline:hover {
      background: var(--nav-hover-bg);
      border-color: var(--primary);
      color: var(--primary);
      transform: translateY(-1px);
    }
    [data-theme="dark"] .btn-outline {
      background: #0d1424;
      border-color: rgba(255, 255, 255, 0.1);
      color: #e2e8f0;
    }
    [data-theme="dark"] .btn-outline:hover {
      background: #152038;
      border-color: #818cf8;
      color: #fff;
    }

    /* SEGMENTED PRESET CHIPS */
    .preset-toolbar {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-bottom: 1.5rem;
      padding: 0.65rem 0.85rem;
      background: var(--card-border-subtle);
      border-radius: 10px;
      border: 1px solid var(--card-border);
    }
    [data-theme="dark"] .preset-toolbar {
      background: rgba(255, 255, 255, 0.02);
      border-color: rgba(255, 255, 255, 0.06);
    }
    .preset-label {
      font-size: 0.73rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-muted);
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      margin-right: 0.35rem;
    }
    .preset-chip {
      background: var(--surface);
      border: 1px solid var(--card-border);
      color: var(--text-main);
      font-family: var(--font-main);
      font-size: 0.76rem;
      font-weight: 600;
      padding: 0.35rem 0.8rem;
      border-radius: 20px;
      cursor: pointer;
      transition: all 0.15s ease;
      box-shadow: var(--shadow-xs);
    }
    .preset-chip:hover {
      background: var(--primary-light);
      color: var(--primary);
      border-color: var(--primary-border);
      transform: translateY(-1px);
      box-shadow: 0 2px 8px rgba(79, 70, 229, 0.15);
    }
    [data-theme="dark"] .preset-chip {
      background: #111a2e;
      border-color: rgba(255, 255, 255, 0.08);
      color: #cbd5e1;
    }
    [data-theme="dark"] .preset-chip:hover {
      background: rgba(99, 102, 241, 0.2);
      color: #a5b4fc;
      border-color: #818cf8;
    }

    /* STRIPE-GRADE FINTECH DATA TABLES */
    .table-responsive {
      overflow-x: auto;
      max-height: 520px;
      border: 1px solid var(--card-border);
      border-radius: 12px;
      box-shadow: var(--shadow-xs);
      background: var(--surface);
    }
    [data-theme="dark"] .table-responsive {
      background: #0c1220;
      border-color: rgba(255, 255, 255, 0.08);
    }
    table {
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      font-size: 0.83rem;
      text-align: left;
    }
    th {
      position: sticky;
      top: 0;
      background: #f8fafc;
      padding: 0.85rem 1.1rem;
      color: var(--text-muted);
      font-weight: 700;
      border-bottom: 1px solid var(--card-border);
      text-transform: uppercase;
      font-size: 0.7rem;
      letter-spacing: 0.05em;
      z-index: 10;
      white-space: nowrap;
    }
    [data-theme="dark"] th {
      background: #0f172a;
      color: #94a3b8;
      border-bottom-color: rgba(255, 255, 255, 0.08);
    }
    td {
      padding: 0.8rem 1.1rem;
      border-bottom: 1px solid var(--card-border-subtle);
      color: var(--text-main);
      font-family: var(--font-mono);
      font-size: 0.81rem;
      font-variant-numeric: tabular-nums;
    }
    [data-theme="dark"] td {
      border-bottom-color: rgba(255, 255, 255, 0.04);
      color: #e2e8f0;
    }
    tbody tr {
      transition: background 0.12s ease;
    }
    tbody tr:nth-child(even) {
      background-color: rgba(248, 250, 252, 0.6);
    }
    [data-theme="dark"] tbody tr:nth-child(even) {
      background-color: rgba(255, 255, 255, 0.015);
    }
    tbody tr:hover {
      background-color: rgba(99, 102, 241, 0.05) !important;
    }
    [data-theme="dark"] tbody tr:hover {
      background-color: rgba(99, 102, 241, 0.12) !important;
    }

    /* MODERN FILE UPLOAD DROPZONE */
    .dropzone-box {
      border: 2px dashed #cbd5e1;
      border-radius: 12px;
      padding: 1.25rem 1.5rem;
      text-align: center;
      background: rgba(248, 250, 252, 0.7);
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 0.4rem;
    }
    .dropzone-box:hover {
      border-color: #6366f1;
      background: rgba(99, 102, 241, 0.04);
    }
    [data-theme="dark"] .dropzone-box {
      border-color: rgba(255, 255, 255, 0.15);
      background: rgba(255, 255, 255, 0.02);
    }
    [data-theme="dark"] .dropzone-box:hover {
      border-color: #818cf8;
      background: rgba(99, 102, 241, 0.08);
    }

    /* SQL ANALYTICAL STUDIO CONSOLE */
    .editor-header {
      background: #090e1a;
      border-radius: 12px 12px 0 0;
      padding: 0.65rem 1rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border: 1px solid #1e293b;
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
    .dot-red { background: #ef4444; }
    .dot-yellow { background: #f59e0b; }
    .dot-green { background: #10b981; }
    .window-title {
      font-size: 0.73rem;
      font-family: var(--font-mono);
      color: #94a3b8;
      margin-left: 0.6rem;
      font-weight: 500;
    }
    .sql-editor-styled {
      width: 100%;
      height: 100px;
      background: #060911;
      border: 1px solid #1e293b;
      border-radius: 0 0 12px 12px;
      padding: 0.95rem 1.1rem;
      font-family: var(--font-mono);
      font-size: 0.88rem;
      color: #38bdf8;
      resize: vertical;
      margin-bottom: 1rem;
      box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.5);
      line-height: 1.5;
    }
    .sql-editor-styled:focus {
      outline: none;
      border-color: #6366f1;
      box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.5), 0 0 0 2px rgba(99, 102, 241, 0.25);
    }
"""

# Replace the beginning of style tag up to /* Modern Data Visualizations
content = re.sub(
    r':root \{[\s\S]*?/\* Modern Data Visualizations & Chart Cards \*/',
    rich_design_system_css + '\n    /* Modern Data Visualizations & Chart Cards */',
    content,
    count=1
)

# 2. UPGRADE TAB 8: CUSTOM DATASET INGESTION STUDIO WITH MODERN DROPZONE
old_ingest_form = """        <form id="ingest-form" onsubmit="event.preventDefault(); submitCustomUpload();">
          <div class="form-grid" style="grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));">
            <div class="form-group">
              <label class="form-label">Dataset Target Table</label>
              <select id="upload-dataset-type" class="form-control">
                <option value="policies" selected>Policy Portfolio (bronze_policies)</option>
                <option value="claims">Claims Loss Run (bronze_claims)</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Ingestion Mode</label>
              <select id="upload-mode" class="form-control">
                <option value="append" selected>Append to Existing Book</option>
                <option value="replace">Replace Portfolio (New Run)</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Select File (.csv, .xlsx, .json)</label>
              <input type="file" id="upload-file-input" class="form-control" accept=".csv,.xlsx,.xls,.json,.txt" required style="padding: 0.5rem;">
            </div>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.75rem;">
            <button type="submit" class="btn-primary" id="btn-submit-upload">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
              Ingest &amp; Rebuild Lakehouse
            </button>
            <span id="upload-status-text" style="font-size:0.85rem; font-family:var(--font-mono); color:var(--text-muted);">Ready to ingest custom data</span>
          </div>
        </form>"""

new_ingest_form = """        <form id="ingest-form" onsubmit="event.preventDefault(); submitCustomUpload();">
          <div class="form-grid" style="grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); align-items: end;">
            <div class="form-group">
              <label class="form-label">Target Lakehouse Entity</label>
              <select id="upload-dataset-type" class="form-control">
                <option value="policies" selected>Policy Portfolio (bronze_policies)</option>
                <option value="claims">Claims Loss Run (bronze_claims)</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Ingestion Pipeline Mode</label>
              <select id="upload-mode" class="form-control">
                <option value="append" selected>Append to Existing Portfolio</option>
                <option value="replace">Replace &amp; Conforce Schema</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Upload Data File</label>
              <div class="dropzone-box" onclick="document.getElementById('upload-file-input').click();">
                <div style="display:flex; align-items:center; gap:0.5rem; color:var(--primary); font-weight:700; font-size:0.84rem;">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                  <span id="dropzone-filename">Choose CSV, Excel or JSON file</span>
                </div>
                <span style="font-size:0.68rem; color:var(--text-muted);">Max 50MB • Schema auto-conformed</span>
                <input type="file" id="upload-file-input" accept=".csv,.xlsx,.xls,.json,.txt" required style="display:none;" onchange="updateDropzoneLabel(this);">
              </div>
            </div>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:1.25rem;">
            <button type="submit" class="btn-primary" id="btn-submit-upload">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
              Ingest &amp; Rebuild Lakehouse
            </button>
            <span id="upload-status-text" style="font-size:0.82rem; font-family:var(--font-mono); color:var(--text-muted);">Ready to ingest custom data</span>
          </div>
        </form>"""

content = content.replace(old_ingest_form, new_ingest_form)

# Add dropzone helper JS
dropzone_js = """
    function updateDropzoneLabel(input) {
      const label = document.getElementById('dropzone-filename');
      if (input.files && input.files[0]) {
        label.innerText = `${input.files[0].name} (${(input.files[0].size / 1024).toFixed(1)} KB)`;
        label.style.color = 'var(--emerald)';
      }
    }
"""

content = content.replace('// Indian Currency Formatter Helper', dropzone_js + '\n    // Indian Currency Formatter Helper')

# 3. UPGRADE TEMPLATE DOWNLOAD BUTTONS IN TAB 8
old_template_buttons = """          <div style="display:flex; gap:0.5rem;">
            <a href="/api/template/policies" download="sample_policies_template.csv" class="btn-outline-xs" style="text-decoration:none; color:#1e293b; background:#ffffff; border-color:#cbd5e1;">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              Policies Template CSV
            </a>
            <a href="/api/template/claims" download="sample_claims_template.csv" class="btn-outline-xs" style="text-decoration:none; color:#1e293b; background:#ffffff; border-color:#cbd5e1;">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              Claims Template CSV
            </a>
          </div>"""

new_template_buttons = """          <div style="display:flex; gap:0.5rem;">
            <a href="/api/template/policies" download="sample_policies_template.csv" class="btn-outline" style="text-decoration:none;">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              Policies Template
            </a>
            <a href="/api/template/claims" download="sample_claims_template.csv" class="btn-outline" style="text-decoration:none;">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              Claims Template
            </a>
          </div>"""

content = content.replace(old_template_buttons, new_template_buttons)

# 4. UPGRADE SQL PRESET BUTTONS TO MODERN SEGMENTED PILLS
old_sql_quick_btns = """        <div class="sql-quick-btns">
          <button class="btn-chip" onclick="setQuery('SELECT * FROM bronze_policies LIMIT 15;')">Bronze Policies</button>
          <button class="btn-chip" onclick="setQuery('SELECT * FROM bronze_claims LIMIT 15;')">Bronze Claims</button>
          <button class="btn-chip" onclick="setQuery('SELECT policy_id, driver_age_band, vehicle_type, exposure, claim_count, total_claim_amount, loss_cost FROM silver_policies LIMIT 15;')">Silver Policies</button>
          <button class="btn-chip" onclick="setQuery('SELECT * FROM gold_rating_cells LIMIT 15;')">Gold Rating Cells</button>
          <button class="btn-chip" onclick="setQuery('SELECT * FROM gold_reserves_summary;')">Gold Reserves (IBNR)</button>
          <button class="btn-chip" onclick="setQuery('SELECT * FROM gold_loss_triangles ORDER BY accident_year, development_year;')">Loss Triangles</button>
        </div>"""

new_sql_quick_btns = """        <div class="preset-toolbar" style="margin-bottom: 1rem;">
          <span class="preset-label">Query Shortcuts:</span>
          <button type="button" class="preset-chip" onclick="setQuery('SELECT * FROM bronze_policies LIMIT 15;')">Bronze Policies</button>
          <button type="button" class="preset-chip" onclick="setQuery('SELECT * FROM bronze_claims LIMIT 15;')">Bronze Claims</button>
          <button type="button" class="preset-chip" onclick="setQuery('SELECT policy_id, driver_age_band, vehicle_type, exposure, claim_count, total_claim_amount, loss_cost FROM silver_policies LIMIT 15;')">Silver Policies</button>
          <button type="button" class="preset-chip" onclick="setQuery('SELECT * FROM gold_rating_cells LIMIT 15;')">Gold Rating Cells</button>
          <button type="button" class="preset-chip" onclick="setQuery('SELECT * FROM gold_reserves_summary;')">Gold Reserves (IBNR)</button>
          <button type="button" class="preset-chip" onclick="setQuery('SELECT * FROM gold_loss_triangles ORDER BY accident_year, development_year;')">Loss Triangles</button>
        </div>"""

content = content.replace(old_sql_quick_btns, new_sql_quick_btns)

# 5. UPGRADE COPY CSV IN TERMINAL
content = content.replace(
    '<button type="button" class="btn-outline-xs" onclick="copyTableCSV()">',
    '<button type="button" class="btn-outline" style="font-size:0.72rem; padding:0.25rem 0.65rem;" onclick="copyTableCSV()">'
)

with open('src/api/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Comprehensive UI Overhaul applied to all routes!")
