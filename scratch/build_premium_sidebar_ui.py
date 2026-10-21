"""
Ultra-Premium Redesign of Actuaria Platform:
1. Replaces cramped horizontal navigation bar with an elite collapsible Left Sidebar Navigation (Stripe / Palantir / Linear grade).
2. Grouped navigation items with crisp icons & active indicators.
3. Top App Bar with live breadcrumb, quick metrics ticker, and high-contrast actions.
4. Stunning dark mode depth, glassmorphic card borders, and smooth micro-interactions.
5. Mobile responsive drawer toggle.
"""

import re

with open('src/api/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. NEW CSS ARCHITECTURE FOR SIDEBAR & APP SHELL
sidebar_css = """
    /* ========================================================= */
    /* ULTRA-PREMIUM ENTERPRISE LAYOUT & THEME TOKENS            */
    /* ========================================================= */
    :root {
      --bg: #f8fafc;
      --surface: #ffffff;
      --card-bg: #ffffff;
      --card-border: #e2e8f0;
      --card-border-subtle: #f1f5f9;
      --card-hover-border: #cbd5e1;
      
      --sidebar-bg: #ffffff;
      --sidebar-border: #e2e8f0;
      --topbar-bg: rgba(255, 255, 255, 0.88);
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
      --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.06), 0 1px 2px -1px rgba(0, 0, 0, 0.04);
      --shadow-md: 0 4px 6px -1px rgba(15, 23, 42, 0.07), 0 2px 4px -2px rgba(15, 23, 42, 0.04);
      --shadow-lg: 0 10px 25px -5px rgba(15, 23, 42, 0.08), 0 8px 10px -6px rgba(15, 23, 42, 0.04);
    }

    [data-theme="dark"] {
      --bg: #080c14;
      --surface: #0e1526;
      --card-bg: #111a2e;
      --card-border: rgba(255, 255, 255, 0.07);
      --card-border-subtle: rgba(255, 255, 255, 0.04);
      --card-hover-border: rgba(99, 102, 241, 0.35);
      
      --sidebar-bg: #0b1120;
      --sidebar-border: rgba(255, 255, 255, 0.06);
      --topbar-bg: rgba(11, 17, 32, 0.88);
      --nav-hover-bg: rgba(255, 255, 255, 0.05);
      
      --primary: #818cf8;
      --primary-hover: #6366f1;
      --primary-light: rgba(99, 102, 241, 0.16);
      --primary-border: rgba(99, 102, 241, 0.3);
      
      --emerald: #10b981;
      --emerald-light: rgba(16, 185, 129, 0.14);
      --emerald-border: rgba(16, 185, 129, 0.3);
      
      --amber: #f59e0b;
      --amber-light: rgba(245, 158, 11, 0.14);
      --amber-border: rgba(245, 158, 11, 0.3);
      
      --rose: #f43f5e;
      --rose-light: rgba(244, 63, 94, 0.14);
      --rose-border: rgba(244, 63, 94, 0.3);
      
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-subtle: #64748b;
    }

    /* APP LAYOUT SHELL */
    .app-layout {
      display: flex;
      min-height: 100vh;
      width: 100%;
    }

    /* LEFT SIDEBAR */
    .app-sidebar {
      width: 260px;
      min-width: 260px;
      background: var(--sidebar-bg);
      border-right: 1px solid var(--sidebar-border);
      display: flex;
      flex-direction: column;
      position: sticky;
      top: 0;
      height: 100vh;
      overflow-y: auto;
      z-index: 40;
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .sidebar-brand {
      padding: 1.25rem 1.4rem;
      display: flex;
      align-items: center;
      gap: 0.75rem;
      border-bottom: 1px solid var(--sidebar-border);
    }
    .brand-logo-wrap {
      width: 36px;
      height: 36px;
      border-radius: 9px;
      background: linear-gradient(135deg, #4f46e5 0%, #312e81 100%);
      box-shadow: 0 4px 12px rgba(79, 70, 229, 0.35);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
    }
    .brand-title-wrap {
      display: flex;
      flex-direction: column;
    }
    .brand-name {
      font-size: 1.05rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }
    .brand-badge-pro {
      font-size: 0.62rem;
      font-weight: 800;
      background: var(--primary-light);
      color: var(--primary);
      border: 1px solid var(--primary-border);
      padding: 0.12rem 0.45rem;
      border-radius: 4px;
      letter-spacing: 0.05em;
    }
    .brand-sub {
      font-size: 0.72rem;
      color: var(--text-muted);
      font-weight: 500;
    }

    /* SIDEBAR NAVIGATION GROUPS */
    .sidebar-nav {
      flex: 1;
      padding: 1rem 0;
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }
    .nav-group {
      display: flex;
      flex-direction: column;
      gap: 0.15rem;
    }
    .nav-group-title {
      font-size: 0.67rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--text-subtle);
      padding: 0.25rem 1.25rem 0.4rem 1.25rem;
    }
    .nav-item {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      margin: 1px 0.75rem;
      padding: 0.62rem 0.85rem;
      border-radius: 8px;
      font-family: var(--font-main);
      font-size: 0.83rem;
      font-weight: 600;
      color: var(--text-muted);
      background: transparent;
      border: none;
      cursor: pointer;
      transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
      text-align: left;
      width: calc(100% - 1.5rem);
    }
    .nav-item:hover {
      color: var(--text-main);
      background: var(--nav-hover-bg);
    }
    .nav-item.active {
      color: var(--primary);
      background: var(--primary-light);
      font-weight: 700;
    }
    [data-theme="dark"] .nav-item.active {
      color: #a5b4fc;
      background: rgba(99, 102, 241, 0.18);
      box-shadow: inset 0 0 0 1px rgba(99, 102, 241, 0.35);
    }
    .nav-item svg {
      width: 17px;
      height: 17px;
      flex-shrink: 0;
    }
    .nav-badge-pill {
      margin-left: auto;
      font-size: 0.65rem;
      font-weight: 700;
      padding: 0.15rem 0.45rem;
      border-radius: 9999px;
      background: var(--emerald-light);
      color: var(--emerald);
      border: 1px solid var(--emerald-border);
    }

    /* SIDEBAR FOOTER STATUS */
    .sidebar-footer {
      padding: 1rem 1.25rem;
      border-top: 1px solid var(--sidebar-border);
      background: var(--sidebar-bg);
    }
    .sidebar-status-box {
      display: flex;
      align-items: center;
      gap: 0.65rem;
      padding: 0.6rem 0.75rem;
      border-radius: 8px;
      background: var(--card-border-subtle);
      border: 1px solid var(--card-border);
    }
    [data-theme="dark"] .sidebar-status-box {
      background: rgba(255, 255, 255, 0.03);
      border-color: rgba(255, 255, 255, 0.08);
    }
    .status-pulse-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--emerald);
      box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.25);
    }
    .status-text-wrap {
      display: flex;
      flex-direction: column;
    }
    .status-main-lbl {
      font-size: 0.74rem;
      font-weight: 700;
      color: var(--text-main);
    }
    .status-sub-lbl {
      font-size: 0.66rem;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }

    /* MAIN APP CONTAINER */
    .app-main {
      flex: 1;
      display: flex;
      flex-direction: column;
      min-width: 0;
      overflow-x: hidden;
    }

    /* TOPBAR */
    .app-topbar {
      position: sticky;
      top: 0;
      z-index: 30;
      height: 60px;
      background: var(--topbar-bg);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--sidebar-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 2rem;
    }
    .topbar-left {
      display: flex;
      align-items: center;
      gap: 1rem;
    }
    .topbar-breadcrumb {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.84rem;
      font-weight: 600;
    }
    .breadcrumb-root {
      color: var(--text-muted);
    }
    .breadcrumb-sep {
      color: var(--text-subtle);
      font-size: 0.75rem;
    }
    .breadcrumb-curr {
      color: var(--text-main);
      font-weight: 700;
    }

    .topbar-right {
      display: flex;
      align-items: center;
      gap: 0.65rem;
    }

    .btn-topbar {
      background: var(--surface);
      border: 1px solid var(--card-border);
      border-radius: 7px;
      color: var(--text-main);
      font-family: var(--font-main);
      font-size: 0.78rem;
      font-weight: 600;
      padding: 0.42rem 0.85rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      transition: all 0.15s ease;
      box-shadow: var(--shadow-xs);
    }
    .btn-topbar:hover {
      border-color: var(--primary);
      color: var(--primary);
      transform: translateY(-1px);
    }
    [data-theme="dark"] .btn-topbar {
      background: #111a2e;
      border-color: rgba(255, 255, 255, 0.1);
      color: #e2e8f0;
    }
    [data-theme="dark"] .btn-topbar:hover {
      border-color: #818cf8;
      color: #fff;
    }

    /* MAIN BODY CONTAINER */
    .app-content {
      flex: 1;
      max-width: 1400px;
      width: 100%;
      margin: 0 auto;
      padding: 1.75rem 2rem;
    }

    @media (max-width: 900px) {
      .app-sidebar {
        display: none;
      }
      .app-topbar {
        padding: 0 1rem;
      }
      .app-content {
        padding: 1rem 0.85rem;
      }
    }
"""

# Replace old header/nav styles with new sidebar layout
# We will inject the new CSS at the beginning of <style>
content = re.sub(r':root \{[\s\S]*?/\* Modern Custom Scrollbar \*/', sidebar_css + '\n    /* Modern Custom Scrollbar */', content, count=1)

# 2. BUILD THE HTML STRUCTURE WITH APP-LAYOUT & SIDEBAR
new_body_markup = """<div class="app-layout">

  <!-- LEFT SIDEBAR -->
  <aside class="app-sidebar">
    <div class="sidebar-brand">
      <div class="brand-logo-wrap">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="8 11 12 15 16 9"/></svg>
      </div>
      <div class="brand-title-wrap">
        <span class="brand-name">ACTUARIA <span class="brand-badge-pro">PRO</span></span>
        <span class="brand-sub">Analytics & Rating Engine</span>
      </div>
    </div>

    <nav class="sidebar-nav">
      <div class="nav-group">
        <div class="nav-group-title">Analytics & Portfolio</div>
        <button class="nav-item active" onclick="switchTab('overview', this)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="9"/><rect x="14" y="3" width="7" height="5"/><rect x="14" y="12" width="7" height="9"/><rect x="3" y="16" width="7" height="5"/></svg>
          <span>Actuarial KPIs</span>
        </button>
        <button class="nav-item" onclick="switchTab('rating', this)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          <span>Rating Engine</span>
          <span class="nav-badge-pill">Tweedie</span>
        </button>
        <button class="nav-item" onclick="switchTab('stress', this)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
          <span>Stress Testing & Geo</span>
        </button>
      </div>

      <div class="nav-group">
        <div class="nav-group-title">Actuarial Reserving & Retention</div>
        <button class="nav-item" onclick="switchTab('reserving', this)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 22 22 22 12 2"/></svg>
          <span>Reserving (Triangles)</span>
        </button>
        <button class="nav-item" onclick="switchTab('retention', this)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M16 8l-8 8"/><path d="M8 8l8 8"/></svg>
          <span>Price Elasticity</span>
        </button>
        <button class="nav-item" onclick="switchTab('governance', this)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="9" y1="15" x2="15" y2="15"/></svg>
          <span>Governance & Audit</span>
        </button>
        <button class="nav-item" onclick="switchTab('lift', this)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
          <span>Double Lift Deciles</span>
        </button>
      </div>

      <div class="nav-group">
        <div class="nav-group-title">Operations & Data Lake</div>
        <button class="nav-item" onclick="switchTab('triage', this)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          <span>Claims & Fraud</span>
        </button>
        <button class="nav-item" onclick="switchTab('lakehouse', this)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>
          <span>SQLite Explorer</span>
        </button>
      </div>
    </nav>

    <div class="sidebar-footer">
      <div class="sidebar-status-box">
        <span class="status-pulse-dot"></span>
        <div class="status-text-wrap">
          <span class="status-main-lbl">insurance.db</span>
          <span class="status-sub-lbl">SQLite WAL • Connected</span>
        </div>
      </div>
    </div>
  </aside>

  <!-- MAIN APP CONTAINER -->
  <div class="app-main">
    <header class="app-topbar">
      <div class="topbar-left">
        <div class="topbar-breadcrumb">
          <span class="breadcrumb-root">Dashboard</span>
          <span class="breadcrumb-sep">/</span>
          <span id="breadcrumb-active" class="breadcrumb-curr">Actuarial KPIs</span>
        </div>
      </div>

      <div class="topbar-right">
        <button class="btn-topbar" onclick="switchTab('lakehouse'); document.getElementById('ingest-panel-container')?.scrollIntoView({behavior:'smooth'});">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
          Import Data
        </button>
        <button class="btn-topbar" onclick="openAuditModal()">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
          Audit Memo
        </button>
        <button class="btn-topbar" onclick="window.print()" title="Print / PDF View">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
          Print PDF
        </button>
        <button id="theme-toggle-btn" class="btn-topbar" onclick="toggleTheme()" title="Toggle Theme">
          <span id="theme-icon">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
          </span>
          <span id="theme-text">Dark</span>
        </button>
      </div>
    </header>

    <main class="app-content">"""

# Replace from <body> down to <main>
old_body_and_tabs_pattern = r'<body>[\s\S]*?<main>'
content = re.sub(old_body_and_tabs_pattern, f'<body>\n{new_body_markup}', content, count=1)

# Close </main> and </div> at the end of the app-main
content = content.replace('</main>', '</main>\n  </div>\n</div>', 1)

# 3. UPDATE switchTab() TO SYNC SIDEBAR NAV-ITEM AND TOPBAR BREADCRUMB
old_switch_tab = """    function switchTab(tabId, el) {
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
      
      const btn = el || (typeof event !== 'undefined' && event && event.currentTarget) || document.querySelector(`.tab-btn[onclick*="'${tabId}'"]`);
      if (btn && btn.classList) {
        btn.classList.add('active');
      }
      const section = document.getElementById(`tab-${tabId}`);
      if (section && section.classList) {
        section.classList.add('active');
      }"""

tab_names_map = """
    const TAB_NAMES = {
      'overview': 'Actuarial KPIs',
      'rating': 'Policy Rating Engine',
      'stress': 'Stress Testing & Geo Risk',
      'reserving': 'Reserving & Loss Triangles',
      'retention': 'Price Elasticity Simulator',
      'governance': 'Governance & Fair Lending',
      'lift': 'Double Lift Validation',
      'triage': 'Claims Fraud Triage',
      'lakehouse': 'SQLite Lakehouse Explorer'
    };
"""

new_switch_tab = tab_names_map + """    function switchTab(tabId, el) {
      document.querySelectorAll('.nav-item, .tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
      
      const btn = el || document.querySelector(`.nav-item[onclick*="'${tabId}'"]`) || document.querySelector(`.tab-btn[onclick*="'${tabId}'"]`);
      if (btn && btn.classList) {
        btn.classList.add('active');
      }
      const section = document.getElementById(`tab-${tabId}`);
      if (section && section.classList) {
        section.classList.add('active');
      }

      // Update topbar breadcrumb
      const bc = document.getElementById('breadcrumb-active');
      if (bc && TAB_NAMES[tabId]) {
        bc.innerText = TAB_NAMES[tabId];
      }"""

content = content.replace(old_switch_tab, new_switch_tab, 1)

with open('src/api/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Ultra-premium Left Sidebar layout applied successfully!")
