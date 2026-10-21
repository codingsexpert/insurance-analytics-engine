"""
Script to apply comprehensive UI/UX improvements to src/api/index.html:
1. Dark / Light Mode with sleek fintech styling & toggle button.
2. Toast Notification System.
3. 1-Click Executive PDF & Print Export.
4. Dual Sliders & Speedometer Risk Gauge in Rating Engine.
5. Loss Development Triangle Heatmap.
6. Instant Table Search & Row Count Filter.
"""

import re

with open('src/api/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. ADD CSS FOR DARK MODE, TOAST, PRINT, AND SLIDERS
new_css = """
    /* ========================================================= */
    /* UI IMPROVEMENTS: DARK THEME, TOASTS, GAUGE & PRINT STYLES */
    /* ========================================================= */
    
    [data-theme="dark"] {
      --bg: #090d16;
      --surface: #0f172a;
      --card-bg: #141e33;
      --card-border: #1e293b;
      --card-border-subtle: #172554;
      --card-hover-border: #3b82f6;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-subtle: #64748b;
      --primary-light: rgba(99, 102, 241, 0.16);
      --primary-border: #4338ca;
      --emerald-light: rgba(5, 150, 105, 0.16);
      --emerald-border: #047857;
      --amber-light: rgba(217, 119, 6, 0.16);
      --amber-border: #b45309;
      --rose-light: rgba(225, 29, 72, 0.16);
      --rose-border: #be123c;
    }

    [data-theme="dark"] body {
      background-color: var(--bg);
      background-image: 
        radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.08) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(16, 185, 129, 0.06) 0px, transparent 50%);
      color: var(--text-main);
    }

    [data-theme="dark"] header {
      background: rgba(15, 23, 42, 0.92);
      border-bottom-color: rgba(51, 65, 85, 0.7);
    }

    [data-theme="dark"] .tabs-wrapper {
      background: #0f172a;
      border-bottom-color: #1e293b;
    }

    [data-theme="dark"] .tab-btn {
      color: #94a3b8;
    }

    [data-theme="dark"] .tab-btn:hover {
      background: #1e293b;
      color: #f8fafc;
    }

    [data-theme="dark"] .tab-btn.active {
      background: rgba(79, 70, 229, 0.22);
      color: #a5b4fc;
      border-bottom-color: #818cf8;
    }

    [data-theme="dark"] .form-control {
      background: #0b1120;
      border-color: #334155;
      color: #f8fafc;
    }

    [data-theme="dark"] .form-label {
      color: #cbd5e1;
    }

    [data-theme="dark"] .btn-outline,
    [data-theme="dark"] .btn-audit {
      background: #1e293b;
      border-color: #334155;
      color: #e2e8f0;
    }

    [data-theme="dark"] .btn-outline:hover,
    [data-theme="dark"] .btn-audit:hover {
      background: #334155;
      color: #ffffff;
      border-color: #6366f1;
    }

    [data-theme="dark"] table th {
      background: #1e293b;
      color: #cbd5e1;
      border-bottom-color: #334155;
    }

    [data-theme="dark"] table td {
      border-bottom-color: #1e293b;
      color: #cbd5e1;
    }

    [data-theme="dark"] table tbody tr:hover {
      background: rgba(30, 41, 59, 0.5);
    }

    [data-theme="dark"] .result-container {
      background: #0b1120;
      border-color: #1e293b;
    }

    [data-theme="dark"] .result-box {
      background: #141e33;
      border-color: #1e293b;
    }

    [data-theme="dark"] .kpi-card,
    [data-theme="dark"] .panel,
    [data-theme="dark"] .chart-panel {
      background: #141e33;
      border-color: #1e293b;
    }

    [data-theme="dark"] .preset-chip {
      background: #1e293b;
      border-color: #334155;
      color: #94a3b8;
    }

    [data-theme="dark"] .preset-chip:hover {
      background: #334155;
      color: #f8fafc;
    }

    [data-theme="dark"] .audit-modal-content {
      background: #0f172a;
      border-color: #334155;
      color: #f8fafc;
    }

    [data-theme="dark"] .audit-modal-body pre, 
    [data-theme="dark"] .audit-modal-body code {
      background: #0b1120;
      color: #a5b4fc;
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

    /* SPEEDOMETER & RANGE SLIDERS */
    .slider-container {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .slider-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .slider-val-badge {
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--primary);
      font-family: var(--font-mono);
    }
    .dual-range {
      width: 100%;
      accent-color: var(--primary);
      cursor: pointer;
      height: 6px;
      border-radius: 4px;
    }

    /* PRINT STYLES */
    @media print {
      body { background: #fff !important; color: #000 !important; }
      .top-bar, header, .tabs-wrapper, .btn-primary, .btn-outline, .btn-audit, #toast-container, form button {
        display: none !important;
      }
      .panel, .kpi-card, .chart-panel {
        box-shadow: none !important;
        border: 1px solid #ddd !important;
        break-inside: avoid;
        page-break-inside: avoid;
      }
      .tab-content { display: block !important; }
      table { width: 100% !important; font-size: 8pt !important; }
      th, td { padding: 4px 6px !important; }
    }
"""

# Insert new CSS before </style>
content = content.replace('</style>', new_css + '\n  </style>', 1)

# 2. ADD BUTTONS TO HEADER: PDF EXPORT AND THEME TOGGLE
header_buttons = """      <button class="btn-audit" onclick="window.print()" title="Export Executive View to PDF" style="gap: 0.45rem;">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
        Export PDF
      </button>
      <button id="theme-toggle-btn" class="btn-audit" onclick="toggleTheme()" title="Toggle Dark/Light Mode" style="gap: 0.45rem;">
        <span id="theme-icon">🌙</span>
        <span id="theme-text">Dark</span>
      </button>
"""

content = content.replace(
    '<button class="btn-audit" onclick="openAuditModal()">',
    header_buttons + '      <button class="btn-audit" onclick="openAuditModal()">'
)

# 3. ADD TOAST CONTAINER BEFORE </body>
content = content.replace('</body>', '  <div id="toast-container"></div>\n</body>')

# 4. ADD JAVASCRIPT FUNCTIONS: THEME TOGGLE, TOASTS, SLIDER SYNC, TABLE FILTER, GAUGE UPDATE
js_improvements = """
    // ==========================================
    // THEME TOGGLE (DARK / LIGHT MODE)
    // ==========================================
    function initTheme() {
      const savedTheme = localStorage.getItem('actuaria_theme') || 'light';
      setTheme(savedTheme);
    }

    function toggleTheme() {
      const current = document.documentElement.getAttribute('data-theme') || 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      setTheme(next);
      showToast(`Switched to ${next.toUpperCase()} theme`, 'info', 2000);
    }

    function setTheme(theme) {
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('actuaria_theme', theme);
      const icon = document.getElementById('theme-icon');
      const text = document.getElementById('theme-text');
      if (icon && text) {
        if (theme === 'dark') {
          icon.innerText = '☀️';
          text.innerText = 'Light';
        } else {
          icon.innerText = '🌙';
          text.innerText = 'Dark';
        }
      }
    }

    // ==========================================
    // TOAST NOTIFICATION SYSTEM
    // ==========================================
    function showToast(message, type = 'info', duration = 3500) {
      const container = document.getElementById('toast-container');
      if (!container) return;

      const toast = document.createElement('div');
      toast.className = `toast toast-${type}`;
      
      let icon = 'ℹ️';
      if (type === 'success') icon = '✅';
      if (type === 'error') icon = '⚠️';
      if (type === 'warning') icon = '⚡';

      toast.innerHTML = `<span style="font-size:1.1rem;">${icon}</span><span>${message}</span>`;
      container.appendChild(toast);

      setTimeout(() => toast.classList.add('show'), 10);

      setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
      }, duration);
    }

    // Replace window.alert with showToast
    const originalAlert = window.alert;
    window.alert = function(msg) {
      if (msg && msg.toLowerCase().includes('error')) {
        showToast(msg, 'error', 4500);
      } else {
        showToast(msg, 'info', 3500);
      }
    };

    // ==========================================
    // INSTANT TABLE SEARCH & FILTER
    // ==========================================
    function filterTable(tableId, query) {
      const q = (query || '').toLowerCase().trim();
      const table = document.getElementById(tableId);
      if (!table) return;
      const tbody = table.querySelector('tbody');
      if (!tbody) return;
      const rows = tbody.querySelectorAll('tr');
      let matches = 0;

      rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        if (!q || text.includes(q)) {
          row.style.display = '';
          matches++;
        } else {
          row.style.display = 'none';
        }
      });

      const countEl = document.getElementById(`${tableId}-count`);
      if (countEl) {
        countEl.innerText = q ? `Showing ${matches} of ${rows.length} rows` : `${rows.length} total rows`;
      }
    }

    // ==========================================
    // DUAL SLIDER & LIVE RATING CONTROLLER
    // ==========================================
    let liveRatingDebounce = null;

    function syncSlider(sliderId, val) {
      const slider = document.getElementById(sliderId);
      if (slider) slider.value = val;
    }

    function syncInput(inputId, val) {
      const input = document.getElementById(inputId);
      if (input) input.value = val;
    }

    function triggerLiveRating() {
      clearTimeout(liveRatingDebounce);
      liveRatingDebounce = setTimeout(() => {
        calculateQuote(true);
      }, 250);
    }

    function updateRiskGauge(tier) {
      const needle = document.getElementById('gauge-needle');
      const label = document.getElementById('gauge-tier-label');
      if (!needle || !label) return;

      label.innerText = tier;
      let rot = 0; // Center is 0 deg (Tier C)
      let color = '#d97706';

      if (tier.includes('Tier A')) {
        rot = -65;
        color = '#059669';
      } else if (tier.includes('Tier B')) {
        rot = -30;
        color = '#0284c7';
      } else if (tier.includes('Tier C')) {
        rot = 0;
        color = '#d97706';
      } else if (tier.includes('Tier D')) {
        rot = 35;
        color = '#ea580c';
      } else if (tier.includes('Tier E')) {
        rot = 68;
        color = '#e11d48';
      }

      needle.style.transform = `rotate(${rot}deg)`;
      needle.setAttribute('stroke', color);
      label.style.color = color;
    }
"""

content = content.replace('<script>\n    // Indian Currency Formatter Helper', '<script>\n' + js_improvements + '\n    // Indian Currency Formatter Helper')

# 5. INITIALIZE THEME ON DOM LOAD
content = content.replace("window.addEventListener('DOMContentLoaded', () => {", "window.addEventListener('DOMContentLoaded', () => {\n      initTheme();")

# 6. ENHANCE RATING FORM WITH DUAL SLIDERS & GAUGE
# Replace Driver Age group
old_age_group = """            <div class="form-group">
              <label class="form-label">Driver Age (Years)</label>
              <input type="number" id="rate-driver-age" class="form-control" value="23" min="18" max="85" required>
            </div>"""

new_age_group = """            <div class="form-group slider-container">
              <div class="slider-header">
                <label class="form-label">Driver Age</label>
                <span id="rate-driver-age-disp" class="slider-val-badge">23 yrs</span>
              </div>
              <input type="range" id="rate-driver-age-slider" class="dual-range" min="18" max="85" value="23" oninput="syncInput('rate-driver-age', this.value); document.getElementById('rate-driver-age-disp').innerText = this.value + ' yrs'; triggerLiveRating();">
              <input type="number" id="rate-driver-age" class="form-control" value="23" min="18" max="85" style="display:none;" required>
            </div>"""

if old_age_group in content:
    content = content.replace(old_age_group, new_age_group, 1)

# Replace IDV (Vehicle Val) group
old_val_group = """            <div class="form-group">
              <label class="form-label">Insured Declared Value - IDV (₹)</label>
              <input type="number" id="rate-vehicle-val" class="form-control" value="650000" min="50000" step="10000" required>
            </div>"""

new_val_group = """            <div class="form-group slider-container">
              <div class="slider-header">
                <label class="form-label">Insured Declared Value (IDV)</label>
                <span id="rate-vehicle-val-disp" class="slider-val-badge">₹ 6,50,000</span>
              </div>
              <input type="range" id="rate-vehicle-val-slider" class="dual-range" min="50000" max="3000000" step="25000" value="650000" oninput="syncInput('rate-vehicle-val', this.value); document.getElementById('rate-vehicle-val-disp').innerText = formatINR(this.value); triggerLiveRating();">
              <input type="number" id="rate-vehicle-val" class="form-control" value="650000" min="50000" step="10000" style="display:none;" required>
            </div>"""

if old_val_group in content:
    content = content.replace(old_val_group, new_val_group, 1)

# Replace Mileage group
old_mileage_group = """            <div class="form-group">
              <label class="form-label">Annual Mileage (km)</label>
              <input type="number" id="rate-mileage" class="form-control" value="12000" min="2000" step="1000" required>
            </div>"""

new_mileage_group = """            <div class="form-group slider-container">
              <div class="slider-header">
                <label class="form-label">Annual Mileage</label>
                <span id="rate-mileage-disp" class="slider-val-badge">12,000 km</span>
              </div>
              <input type="range" id="rate-mileage-slider" class="dual-range" min="2000" max="40000" step="1000" value="12000" oninput="syncInput('rate-mileage', this.value); document.getElementById('rate-mileage-disp').innerText = Number(this.value).toLocaleString('en-IN') + ' km'; triggerLiveRating();">
              <input type="number" id="rate-mileage" class="form-control" value="12000" min="2000" step="1000" style="display:none;" required>
            </div>"""

if old_mileage_group in content:
    content = content.replace(old_mileage_group, new_mileage_group, 1)

# Add Gauge to Rating Results Box
old_res_tier_box = """          <div class="result-box">
            <span class="result-title">Risk Rating Tier</span>
            <div style="margin-top: 0.35rem;"><span id="res-tier" class="tier-badge">Tier B</span></div>
          </div>"""

new_res_tier_box = """          <div class="result-box" style="align-items: center; justify-content: center; text-align: center;">
            <span class="result-title" style="align-self: flex-start;">Risk Severity Gauge</span>
            <div style="position: relative; width: 130px; height: 75px; margin-top: 5px;">
              <svg viewBox="0 0 100 55" width="100%" height="100%">
                <path d="M 12 50 A 38 38 0 0 1 88 50" fill="none" stroke="var(--card-border)" stroke-width="8" stroke-linecap="round"/>
                <path d="M 12 50 A 38 38 0 0 1 27 22" fill="none" stroke="#059669" stroke-width="8" stroke-linecap="round"/>
                <path d="M 27 22 A 38 38 0 0 1 50 12" fill="none" stroke="#0284c7" stroke-width="8"/>
                <path d="M 50 12 A 38 38 0 0 1 73 22" fill="none" stroke="#d97706" stroke-width="8"/>
                <path d="M 73 22 A 38 38 0 0 1 88 50" fill="none" stroke="#e11d48" stroke-width="8" stroke-linecap="round"/>
                <line id="gauge-needle" x1="50" y1="50" x2="50" y2="18" stroke="#4f46e5" stroke-width="2.5" stroke-linecap="round" style="transform-origin: 50px 50px; transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);"/>
                <circle cx="50" cy="50" r="4.5" fill="#4f46e5"/>
              </svg>
              <div id="gauge-tier-label" style="position: absolute; bottom: 0; width: 100%; text-align: center; font-size: 0.76rem; font-weight: 800; color: var(--primary);">TIER B</div>
            </div>
            <div style="margin-top: 0.2rem;"><span id="res-tier" class="tier-badge">Tier B</span></div>
          </div>"""

if old_res_tier_box in content:
    content = content.replace(old_res_tier_box, new_res_tier_box, 1)

# Hook updateRiskGauge into calculateQuote
content = content.replace(
    "document.getElementById('res-tier').innerText = data.risk_tier;",
    "document.getElementById('res-tier').innerText = data.risk_tier;\n        updateRiskGauge(data.risk_tier);"
)

# 7. ADD INSTANT SEARCH FILTER TO GOLD MARTS TABLE
old_gold_header = """      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">Gold Layer: Actuarial Rating Cell Aggregations</div>
          <button class="btn-outline" onclick="loadGoldMarts()">Refresh Table</button>
        </div>"""

new_gold_header = """      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">Gold Layer: Actuarial Rating Cell Aggregations</div>
          <div style="display: flex; gap: 0.6rem; align-items: center;">
            <input type="text" placeholder="🔍 Search territory, vehicle, age band..." class="form-control" style="font-size: 0.78rem; padding: 0.35rem 0.75rem; width: 260px;" oninput="filterTable('gold-marts-table', this.value)">
            <button class="btn-outline" onclick="loadGoldMarts()">Refresh Table</button>
          </div>
        </div>
        <div style="display:flex; justify-content: flex-end; margin-top: -0.5rem; margin-bottom: 0.75rem;">
          <span id="gold-marts-table-count" style="font-size: 0.75rem; font-weight: 600; color: var(--text-muted);"></span>
        </div>"""

if old_gold_header in content:
    content = content.replace(old_gold_header, new_gold_header, 1)

# Update row count in loadGoldMarts
content = content.replace(
    "rows.slice(0, 50).forEach(r => {",
    "document.getElementById('gold-marts-table-count').innerText = `${rows.length} total rating cells (showing top 50)`;\n        rows.slice(0, 50).forEach(r => {"
)

# 8. ENHANCE LOSS DEVELOPMENT TRIANGLE WITH ACTUARIAL HEATMAP
old_tri_populate = """        rowsTri.forEach(r => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td><strong>AY ${r.accident_year}</strong></td>
            <td>${r.dev_0 ? formatINR(r.dev_0) : '-'}</td>
            <td>${r.dev_1 ? formatINR(r.dev_1) : '-'}</td>
            <td>${r.dev_2 ? formatINR(r.dev_2) : '-'}</td>
            <td>${r.dev_3 ? formatINR(r.dev_3) : '-'}</td>
            <td>${r.dev_4 ? formatINR(r.dev_4) : '-'}</td>
          `;
          tbodyTri.appendChild(tr);
        });"""

new_tri_populate = """        const allVals = [];
        rowsTri.forEach(r => {
          [r.dev_0, r.dev_1, r.dev_2, r.dev_3, r.dev_4].forEach(v => { if (v) allVals.push(v); });
        });
        const maxTriVal = Math.max(...allVals, 1);

        function getHeatBg(val) {
          if (!val) return 'transparent';
          const pct = Math.min(1, Math.max(0.12, val / maxTriVal));
          return `rgba(99, 102, 241, ${(pct * 0.28).toFixed(2)})`;
        }

        rowsTri.forEach(r => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td><strong>AY ${r.accident_year}</strong></td>
            <td style="background:${getHeatBg(r.dev_0)}; font-weight:600;">${r.dev_0 ? formatINR(r.dev_0) : '-'}</td>
            <td style="background:${getHeatBg(r.dev_1)}; font-weight:600;">${r.dev_1 ? formatINR(r.dev_1) : '-'}</td>
            <td style="background:${getHeatBg(r.dev_2)}; font-weight:600;">${r.dev_2 ? formatINR(r.dev_2) : '-'}</td>
            <td style="background:${getHeatBg(r.dev_3)}; font-weight:600;">${r.dev_3 ? formatINR(r.dev_3) : '-'}</td>
            <td style="background:${getHeatBg(r.dev_4)}; font-weight:600;">${r.dev_4 ? formatINR(r.dev_4) : '-'}</td>
          `;
          tbodyTri.appendChild(tr);
        });"""

if old_tri_populate in content:
    content = content.replace(old_tri_populate, new_tri_populate, 1)

# Write upgraded index.html
with open('src/api/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("UI improvements successfully written to src/api/index.html!")
