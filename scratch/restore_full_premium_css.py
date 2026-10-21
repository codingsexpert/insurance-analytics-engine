"""
Restore full, flawless, unified stylesheet into src/api/index.html:
1. Complete app layout (.app-layout, .app-sidebar, .app-main, .app-topbar).
2. Navigation groups, nav-item, active state, badges.
3. Panels, KPI cards, charts-grid, form controls, dropzone.
4. Tables, SQL terminal, preset toolbars, toasts.
5. Perfect Dark and Light mode support.
"""

import re

with open('src/api/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Complete, verified, pristine CSS stylesheet
pristine_css = """
    /* ========================================================= */
    /* 1. DESIGN TOKENS (LIGHT & DARK MODE)                      */
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

    * { box-sizing: border-box; margin: 0; padding: 0; }

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

    /* ========================================================= */
    /* 2. APP SHELL LAYOUT: SIDEBAR + TOPBAR + MAIN             */
    /* ========================================================= */
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
      flex-shrink: 0;
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

    /* SIDEBAR NAVIGATION */
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

    /* MAIN APP AREA */
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
    .breadcrumb-root { color: var(--text-muted); }
    .breadcrumb-sep { color: var(--text-subtle); font-size: 0.75rem; }
    .breadcrumb-curr { color: var(--text-main); font-weight: 700; }

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

    /* MAIN CONTENT WRAPPER */
    .app-content {
      flex: 1;
      max-width: 1400px;
      width: 100%;
      margin: 0 auto;
      padding: 1.75rem 2rem;
    }

    .tab-content { display: none; }
    .tab-content.active { display: block; animation: tabSlideUp 0.22s cubic-bezier(0.4, 0, 0.2, 1); }
    @keyframes tabSlideUp {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* ========================================================= */
    /* 3. CARDS, PANELS & GRIDS                                  */
    /* ========================================================= */
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
      background: var(--card-border-subtle);
      color: var(--text-muted);
    }
    [data-theme="dark"] .kpi-chip {
      background: rgba(255, 255, 255, 0.08);
      color: #cbd5e1;
    }
    .kpi-progress-wrap {
      width: 100%;
      height: 4px;
      background: var(--card-border-subtle);
      border-radius: 2px;
      margin-top: 0.75rem;
      overflow: hidden;
    }
    .kpi-progress-bar {
      height: 100%;
      border-radius: 2px;
    }

    /* CHARTS GRID */
    .charts-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(460px, 1fr));
      gap: 1.5rem;
      margin-bottom: 1.75rem;
    }
    .chart-panel {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 1.5rem 1.75rem;
      box-shadow: var(--shadow-card);
      display: flex;
      flex-direction: column;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .chart-panel:hover {
      box-shadow: 0 8px 24px -4px rgba(15, 23, 42, 0.08);
      border-color: var(--card-hover-border);
    }
    .chart-panel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.25rem;
    }
    .chart-panel-title {
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 0.55rem;
    }
    .chart-wrapper {
      position: relative;
      height: 275px;
      width: 100%;
    }

    /* ========================================================= */
    /* 4. FORM CONTROLS & PRESET TOOLBARS                        */
    /* ========================================================= */
    .form-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 1.25rem;
      margin-bottom: 1.5rem;
    }
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

    .form-section-title {
      font-size: 0.78rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--primary);
      margin-bottom: 0.85rem;
      padding-bottom: 0.4rem;
      border-bottom: 1px solid var(--card-border-subtle);
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

    /* PRESETS TOOLBAR */
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

    /* SLIDERS */
    .slider-container { display: flex; flex-direction: column; gap: 6px; }
    .slider-header { display: flex; justify-content: space-between; align-items: center; }
    .slider-val-badge { font-size: 0.82rem; font-weight: 700; color: var(--primary); font-family: var(--font-mono); }
    .dual-range { width: 100%; accent-color: var(--primary); cursor: pointer; height: 6px; border-radius: 4px; }

    /* ========================================================= */
    /* 5. FINTECH DATA TABLES & SQL CONSOLE                     */
    /* ========================================================= */
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
    tbody tr:nth-child(even) { background-color: rgba(248, 250, 252, 0.6); }
    [data-theme="dark"] tbody tr:nth-child(even) { background-color: rgba(255, 255, 255, 0.015); }
    tbody tr:hover { background-color: rgba(99, 102, 241, 0.05) !important; }
    [data-theme="dark"] tbody tr:hover { background-color: rgba(99, 102, 241, 0.12) !important; }

    /* TABLE ACTION BAR */
    .table-action-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.75rem;
      margin-bottom: 0.85rem;
      flex-wrap: wrap;
    }
    .table-search-input {
      font-size: 0.8rem;
      padding: 0.4rem 0.75rem;
      width: 260px;
      border-radius: 7px;
    }
    .btn-export-csv {
      font-size: 0.76rem;
      padding: 0.38rem 0.75rem;
      font-weight: 600;
      border-radius: 7px;
      background: var(--surface);
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      transition: all 0.15s ease;
    }
    .btn-export-csv:hover {
      background: var(--nav-hover-bg);
      color: var(--primary);
      border-color: var(--primary);
    }
    [data-theme="dark"] .btn-export-csv {
      background: #0d1424;
      border-color: rgba(255, 255, 255, 0.1);
      color: #94a3b8;
    }
    [data-theme="dark"] .btn-export-csv:hover {
      background: #152038;
      color: #fff;
      border-color: #818cf8;
    }

    /* DROPZONE */
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

    /* SQL TERMINAL */
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
    .dot { width: 10px; height: 10px; border-radius: 50%; }
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

    .result-container {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1.25rem;
      background: var(--card-border-subtle);
      border-radius: 12px;
      border: 1px solid var(--card-border);
      padding: 1.5rem;
      margin-top: 1.5rem;
    }
    [data-theme="dark"] .result-container {
      background: rgba(255, 255, 255, 0.02);
      border-color: rgba(255, 255, 255, 0.08);
    }
    .result-box {
      display: flex;
      flex-direction: column;
      gap: 0.3rem;
      padding: 1rem 1.2rem;
      background: var(--surface);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      box-shadow: var(--shadow-xs);
    }
    [data-theme="dark"] .result-box {
      background: #111a2e;
      border-color: rgba(255, 255, 255, 0.08);
    }
    .result-title {
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
    }
    .result-val {
      font-size: 1.65rem;
      font-weight: 800;
      color: var(--text-main);
      letter-spacing: -0.025em;
    }
    .tier-badge {
      display: inline-block;
      padding: 0.35rem 0.8rem;
      border-radius: 6px;
      font-weight: 700;
      font-size: 0.82rem;
      background: var(--primary-light);
      color: var(--primary);
      border: 1px solid var(--primary-border);
      width: fit-content;
    }
    .status-pill {
      font-size: 0.75rem;
      padding: 0.35rem 0.8rem;
      border-radius: 8px;
      font-family: var(--font-mono);
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      background: var(--primary-light);
      border: 1px solid var(--primary-border);
      color: var(--primary);
      font-weight: 600;
    }

    /* TOAST NOTIFICATION CONTAINER */
    #toast-container {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 99999;
      display: flex;
      flex-direction: column;
      gap: 10px;
      pointer-events: none;
    }
    .toast {
      pointer-events: auto;
      display: flex;
      align-items: center;
      gap: 12px;
      min-width: 280px;
      max-width: 420px;
      padding: 12px 18px;
      border-radius: 10px;
      font-family: var(--font-main);
      font-size: 0.85rem;
      font-weight: 500;
      color: #ffffff;
      box-shadow: 0 10px 25px -5px rgba(0,0,0,0.25);
      opacity: 0;
      transform: translateY(16px);
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .toast.show { opacity: 1; transform: translateY(0); }
    .toast-success { background: #059669; border-left: 5px solid #34d399; }
    .toast-error { background: #e11d48; border-left: 5px solid #fb7185; }
    .toast-warning { background: #d97706; border-left: 5px solid #fde68a; }
    .toast-info { background: #4f46e5; border-left: 5px solid #a5b4fc; }

    /* AUDIT MODAL */
    .audit-modal-backdrop {
      position: fixed; top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(4px);
      display: flex; align-items: center; justify-content: center;
      z-index: 1000; padding: 2rem;
    }
    .audit-modal-content {
      background: var(--surface); border: 1px solid var(--card-border);
      border-radius: 16px; width: 100%; max-width: 960px; max-height: 90vh;
      display: flex; flex-direction: column; box-shadow: var(--shadow-lg); overflow: hidden;
    }
    .audit-modal-header {
      padding: 1.25rem 1.75rem; border-bottom: 1px solid var(--card-border);
      display: flex; justify-content: space-between; align-items: center; background: var(--bg);
    }
    .audit-modal-body {
      padding: 1.75rem; overflow-y: auto; font-family: var(--font-mono);
      font-size: 0.84rem; line-height: 1.65; color: var(--text-main);
    }
    [data-theme="dark"] .audit-modal-content {
      background: #0e1526;
      border-color: rgba(255, 255, 255, 0.1);
    }
    [data-theme="dark"] .audit-modal-header {
      background: #090e1a;
      border-bottom-color: rgba(255, 255, 255, 0.08);
    }

    /* RESPONSIVE & PRINT */
    @media (max-width: 900px) {
      .app-sidebar { display: none; }
      .app-topbar { padding: 0 1rem; }
      .app-content { padding: 1rem 0.85rem; }
      .charts-grid { grid-template-columns: 1fr; }
    }
    @media print {
      body { background: #fff !important; color: #000 !important; }
      .app-sidebar, .app-topbar, .btn-primary, .btn-outline, .btn-topbar, .btn-export-csv, #toast-container, form button {
        display: none !important;
      }
      .panel, .kpi-card, .chart-panel {
        box-shadow: none !important; border: 1px solid #ddd !important; break-inside: avoid;
      }
      .tab-content { display: block !important; }
      table { width: 100% !important; font-size: 8pt !important; }
      th, td { padding: 4px 6px !important; }
    }
"""

# Replace entire <style> content cleanly
content = re.sub(r'<style>[\s\S]*?</style>', f'<style>{pristine_css}\n  </style>', html, count=1)

with open('src/api/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Restored complete, pristine, rock-solid stylesheet into index.html!")
