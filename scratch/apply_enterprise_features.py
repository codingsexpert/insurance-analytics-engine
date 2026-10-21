"""
Implement comprehensive enterprise features:
1. Live What-If Sliders for Stress Testing.
2. Universal 1-Click CSV Export for all data tables.
3. Click-to-Sort for all tables (numeric, currency, percentage, string aware).
4. Universal Search Filters on Geo-Risk & Batch Scored tables.
5. Shimmer Skeleton loaders for clean asynchronous states.
"""

import re

with open('src/api/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. ADD SKELETON & SORTABLE CSS
extra_css = """
    /* SKELETON SHIMMER LOADERS */
    @keyframes shimmerAnim {
      0% { background-position: -200% 0; }
      100% { background-position: 200% 0; }
    }
    .skeleton-bar {
      height: 14px;
      border-radius: 4px;
      background: linear-gradient(90deg, #e2e8f0 25%, #f1f5f9 50%, #e2e8f0 75%);
      background-size: 200% 100%;
      animation: shimmerAnim 1.5s infinite;
      display: inline-block;
      width: 100%;
    }
    [data-theme="dark"] .skeleton-bar {
      background: linear-gradient(90deg, #1e293b 25%, #334155 50%, #1e293b 75%);
      background-size: 200% 100%;
    }

    /* TABLE ACTION BAR (SEARCH + EXPORT) */
    .table-action-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.75rem;
      margin-bottom: 0.85rem;
      flex-wrap: wrap;
    }
    .table-action-left, .table-action-right {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .table-search-input {
      font-size: 0.8rem;
      padding: 0.4rem 0.75rem;
      width: 240px;
      border-radius: 6px;
    }
    .btn-export-csv {
      font-size: 0.76rem;
      padding: 0.35rem 0.7rem;
      font-weight: 600;
      border-radius: 6px;
      background: transparent;
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      transition: all 0.15s ease;
    }
    .btn-export-csv:hover {
      background: var(--surface);
      color: var(--primary);
      border-color: var(--primary);
    }
    [data-theme="dark"] .btn-export-csv {
      border-color: #334155;
      color: #94a3b8;
    }
    [data-theme="dark"] .btn-export-csv:hover {
      background: #1e293b;
      color: #f8fafc;
      border-color: #6366f1;
    }
"""

content = content.replace('/* PRINT STYLES */', extra_css + '\n    /* PRINT STYLES */')

# 2. ENHANCE STRESS TESTING WITH LIVE WHAT-IF SLIDERS
old_stress_form = """        <form id="stress-form" onsubmit="event.preventDefault(); runStressSimulation();">
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">Claim Severity Inflation Shock (%)</label>
              <input type="number" id="stress-sev" class="form-control" value="12" min="-20" max="50" step="1" required>
            </div>
            <div class="form-group">
              <label class="form-label">Catastrophe Frequency Surge (%)</label>
              <input type="number" id="stress-freq" class="form-control" value="15" min="-20" max="100" step="1" required>
            </div>
            <div class="form-group">
              <label class="form-label">Reinsurance Retention Limit / Claim (₹)</label>
              <input type="number" id="stress-ret" class="form-control" value="500000" min="50000" step="50000" required>
            </div>
            <div class="form-group">
              <label class="form-label">Operating Expense Ratio (%)</label>
              <input type="number" id="stress-exp" class="form-control" value="22" min="10" max="40" step="1" required>
            </div>
          </div>
          <button type="submit" class="btn-primary">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
            Execute Stress Simulation
          </button>
        </form>"""

new_stress_form = """        <form id="stress-form" onsubmit="event.preventDefault(); runStressSimulation();">
          <div class="form-grid">
            <div class="form-group slider-container">
              <div class="slider-header">
                <label class="form-label">Severity Inflation Shock</label>
                <span id="stress-sev-disp" class="slider-val-badge">+12%</span>
              </div>
              <input type="range" id="stress-sev-slider" class="dual-range" min="-20" max="50" step="1" value="12" oninput="syncInput('stress-sev', this.value); document.getElementById('stress-sev-disp').innerText = (this.value >= 0 ? '+' : '') + this.value + '%'; triggerLiveStress();">
              <input type="number" id="stress-sev" class="form-control" value="12" min="-20" max="50" step="1" style="display:none;" required>
            </div>

            <div class="form-group slider-container">
              <div class="slider-header">
                <label class="form-label">Catastrophe Frequency Surge</label>
                <span id="stress-freq-disp" class="slider-val-badge">+15%</span>
              </div>
              <input type="range" id="stress-freq-slider" class="dual-range" min="-20" max="100" step="1" value="15" oninput="syncInput('stress-freq', this.value); document.getElementById('stress-freq-disp').innerText = (this.value >= 0 ? '+' : '') + this.value + '%'; triggerLiveStress();">
              <input type="number" id="stress-freq" class="form-control" value="15" min="-20" max="100" step="1" style="display:none;" required>
            </div>

            <div class="form-group slider-container">
              <div class="slider-header">
                <label class="form-label">Reinsurance Retention / Claim</label>
                <span id="stress-ret-disp" class="slider-val-badge">₹ 5,00,000</span>
              </div>
              <input type="range" id="stress-ret-slider" class="dual-range" min="100000" max="2000000" step="50000" value="500000" oninput="syncInput('stress-ret', this.value); document.getElementById('stress-ret-disp').innerText = formatINR(this.value); triggerLiveStress();">
              <input type="number" id="stress-ret" class="form-control" value="500000" min="50000" step="50000" style="display:none;" required>
            </div>

            <div class="form-group">
              <label class="form-label">Operating Expense Ratio (%)</label>
              <input type="number" id="stress-exp" class="form-control" value="22" min="10" max="40" step="1" required oninput="triggerLiveStress();">
            </div>
          </div>
          <button type="submit" class="btn-primary">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
            Execute Stress Simulation
          </button>
        </form>"""

content = content.replace(old_stress_form, new_stress_form)

# 3. ADD CSV EXPORT AND SEARCH TOOLBARS TO TABLES
# A. Gold Marts Table Toolbar
old_gold_header_bar = """        <div class="panel-header">
          <div class="panel-title">Gold Layer: Actuarial Rating Cell Aggregations</div>
          <div style="display: flex; gap: 0.6rem; align-items: center;">
            <input type="text" placeholder="Filter cells by territory, vehicle, age band..." class="form-control" style="font-size: 0.78rem; padding: 0.35rem 0.75rem; width: 260px;" oninput="filterTable('gold-marts-table', this.value)">
            <button class="btn-outline" onclick="loadGoldMarts()">Refresh Table</button>
          </div>
        </div>
        <div style="display:flex; justify-content: flex-end; margin-top: -0.5rem; margin-bottom: 0.75rem;">
          <span id="gold-marts-table-count" style="font-size: 0.75rem; font-weight: 600; color: var(--text-muted);"></span>
        </div>"""

new_gold_header_bar = """        <div class="panel-header">
          <div class="panel-title">Gold Layer: Actuarial Rating Cell Aggregations</div>
          <div style="display: flex; gap: 0.5rem; align-items: center;">
            <button class="btn-export-csv" onclick="exportTableToCSV('gold-marts-table', 'gold_rating_cells.csv')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              Export CSV
            </button>
            <button class="btn-outline" onclick="loadGoldMarts()">Refresh</button>
          </div>
        </div>
        <div class="table-action-bar">
          <input type="text" placeholder="Filter cells by territory, vehicle, age band..." class="form-control table-search-input" oninput="filterTable('gold-marts-table', this.value)">
          <span id="gold-marts-table-count" style="font-size: 0.75rem; font-weight: 600; color: var(--text-muted);"></span>
        </div>"""

content = content.replace(old_gold_header_bar, new_gold_header_bar)

# B. Loss Triangle Table Export
old_tri_header = """        <div class="panel-header">
          <div class="panel-title">Cumulative Paid Loss Development Triangle (₹)</div>
          <button class="btn-outline" onclick="loadReservingData()">Refresh Triangles</button>
        </div>"""

new_tri_header = """        <div class="panel-header">
          <div class="panel-title">Cumulative Paid Loss Development Triangle (₹)</div>
          <div style="display:flex; gap:0.5rem;">
            <button class="btn-export-csv" onclick="exportTableToCSV('triangle-table', 'cumulative_loss_triangle.csv')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              Export CSV
            </button>
            <button class="btn-outline" onclick="loadReservingData()">Refresh</button>
          </div>
        </div>"""

content = content.replace(old_tri_header, new_tri_header)

# C. IBNR Table Export
old_ibnr_header = """        <div class="panel-header">
          <div class="panel-title">Chain Ladder Ultimate Loss & IBNR Reserves Summary (₹)</div>
          <span class="status-pill">IFRS 17 & Solvency II Compliance</span>
        </div>"""

new_ibnr_header = """        <div class="panel-header">
          <div class="panel-title">Chain Ladder Ultimate Loss & IBNR Reserves Summary (₹)</div>
          <div style="display:flex; gap:0.5rem; align-items:center;">
            <button class="btn-export-csv" onclick="exportTableToCSV('ibnr-table', 'ibnr_reserves_summary.csv')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              Export CSV
            </button>
            <span class="status-pill">IFRS 17 Compliance</span>
          </div>
        </div>"""

content = content.replace(old_ibnr_header, new_ibnr_header)

# D. Geo Risk Table Toolbar
old_geo_header = """        <div class="panel-header">
          <div class="panel-title">Geo-Risk Accumulation & Probable Maximum Loss (PML)</div>
          <button class="btn-outline" onclick="loadGeoRiskData()">Refresh Geo Risk</button>
        </div>"""

new_geo_header = """        <div class="panel-header">
          <div class="panel-title">Geo-Risk Accumulation & Probable Maximum Loss (PML)</div>
          <div style="display:flex; gap:0.5rem;">
            <button class="btn-export-csv" onclick="exportTableToCSV('geo-risk-table', 'geo_risk_pml_exposure.csv')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              Export CSV
            </button>
            <button class="btn-outline" onclick="loadGeoRiskData()">Refresh</button>
          </div>
        </div>"""

content = content.replace(old_geo_header, new_geo_header)

# Insert search toolbar above geo-risk-table
content = content.replace(
    '<table id="geo-risk-table">',
    '<div class="table-action-bar"><input type="text" placeholder="Filter territory or exposure metrics..." class="form-control table-search-input" oninput="filterTable(\'geo-risk-table\', this.value)"><span id="geo-risk-table-count" style="font-size:0.75rem; font-weight:600; color:var(--text-muted);"></span></div>\n        <table id="geo-risk-table">'
)

# E. Batch Portfolio Table Export & Search
content = content.replace(
    '<table id="batch-tier-table">',
    '<div class="table-action-bar"><input type="text" placeholder="Filter tier..." class="form-control table-search-input" oninput="filterTable(\'batch-tier-table\', this.value)"><button class="btn-export-csv" onclick="exportTableToCSV(\'batch-tier-table\', \'batch_scored_risk_tiers.csv\')"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg> Export CSV</button></div>\n        <table id="batch-tier-table">'
)

# 4. ADD JS LOGIC FOR:
# - exportTableToCSV(tableId, filename)
# - makeTableSortable(tableId)
# - triggerLiveStress()
# - syncStressSliders()

js_features = """
    // ==========================================
    // CSV EXPORT ENGINE
    // ==========================================
    function exportTableToCSV(tableId, filename = 'actuarial_export.csv') {
      const table = document.getElementById(tableId);
      if (!table) {
        showToast('Table not found', 'error');
        return;
      }
      const rows = Array.from(table.querySelectorAll('tr'));
      const csv = [];

      rows.forEach(row => {
        if (row.style.display === 'none') return;
        const cols = Array.from(row.querySelectorAll('th, td')).map(c => {
          let text = c.innerText.replace(/[▲▼]/g, '').replace(/"/g, '""').trim();
          return `"${text}"`;
        });
        if (cols.length > 0) csv.push(cols.join(','));
      });

      if (csv.length === 0) {
        showToast('No data to export', 'warning');
        return;
      }

      const blob = new Blob([csv.join('\\n')], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showToast(`Exported ${filename}`, 'success');
    }

    // ==========================================
    // CLICK-TO-SORT TABLE COLUMNS
    // ==========================================
    function makeTableSortable(tableId) {
      const table = document.getElementById(tableId);
      if (!table) return;
      const ths = table.querySelectorAll('thead th');
      ths.forEach((th, idx) => {
        th.style.cursor = 'pointer';
        th.style.userSelect = 'none';
        th.title = 'Click to sort';
        th.onclick = () => sortTableByColumn(tableId, idx);
      });
    }

    function sortTableByColumn(tableId, colIdx) {
      const table = document.getElementById(tableId);
      if (!table) return;
      const tbody = table.querySelector('tbody');
      if (!tbody) return;
      const rows = Array.from(tbody.querySelectorAll('tr'));
      if (rows.length <= 1) return;

      const currentDir = table.getAttribute(`data-sort-${colIdx}`) === 'asc' ? 'desc' : 'asc';
      table.setAttribute(`data-sort-${colIdx}`, currentDir);

      const ths = table.querySelectorAll('thead th');
      ths.forEach((h, i) => {
        const base = h.getAttribute('data-base-title') || h.innerText.replace(/[▲▼]/g, '').trim();
        h.setAttribute('data-base-title', base);
        if (i === colIdx) {
          h.innerHTML = `${base} <span style="font-size:0.65rem; opacity:0.8;">${currentDir === 'asc' ? '▲' : '▼'}</span>`;
        } else {
          h.innerHTML = base;
        }
      });

      rows.sort((a, b) => {
        const cellA = a.children[colIdx]?.innerText.replace(/[₹,%]/g, '').trim() || '';
        const cellB = b.children[colIdx]?.innerText.replace(/[₹,%]/g, '').trim() || '';
        const numA = parseFloat(cellA);
        const numB = parseFloat(cellB);

        if (!isNaN(numA) && !isNaN(numB)) {
          return currentDir === 'asc' ? numA - numB : numB - numA;
        }
        return currentDir === 'asc' ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
      });

      rows.forEach(r => tbody.appendChild(r));
    }

    // ==========================================
    // STRESS TESTING WHAT-IF SLIDERS
    // ==========================================
    let stressDebounceTimer = null;

    function triggerLiveStress() {
      clearTimeout(stressDebounceTimer);
      stressDebounceTimer = setTimeout(() => {
        runStressSimulation(true);
      }, 250);
    }

    function syncStressSliders() {
      const sev = document.getElementById('stress-sev')?.value;
      const freq = document.getElementById('stress-freq')?.value;
      const ret = document.getElementById('stress-ret')?.value;

      if (sev !== undefined) {
        syncSlider('stress-sev-slider', sev);
        const disp = document.getElementById('stress-sev-disp');
        if (disp) disp.innerText = (sev >= 0 ? '+' : '') + sev + '%';
      }
      if (freq !== undefined) {
        syncSlider('stress-freq-slider', freq);
        const disp = document.getElementById('stress-freq-disp');
        if (disp) disp.innerText = (freq >= 0 ? '+' : '') + freq + '%';
      }
      if (ret !== undefined) {
        syncSlider('stress-ret-slider', ret);
        const disp = document.getElementById('stress-ret-disp');
        if (disp) disp.innerText = formatINR(ret);
      }
    }
"""

content = content.replace(
    '// ==========================================\n    // INSTANT TABLE SEARCH & FILTER',
    js_features + '\n    // ==========================================\n    // INSTANT TABLE SEARCH & FILTER'
)

# Connect makeTableSortable in DOMContentLoaded & after table loads
content = content.replace(
    "window.addEventListener('DOMContentLoaded', () => {\n      initTheme();\n      syncQuoteSliders();\n      loadSummary();\n      loadGoldMarts();",
    "window.addEventListener('DOMContentLoaded', () => {\n      initTheme();\n      syncQuoteSliders();\n      syncStressSliders();\n      loadSummary();\n      loadGoldMarts();\n      ['gold-marts-table', 'triangle-table', 'ibnr-table', 'geo-risk-table', 'batch-tier-table', 'elasticity-table'].forEach(makeTableSortable);"
)

# Hook syncStressSliders into applyStressPreset
old_stress_preset_fn = """    function applyStressPreset(type) {
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
        document.getElementById('stress-ret').value = 300000;
        document.getElementById('stress-exp').value = 25;
      } else if (type === 'inflation') {
        document.getElementById('stress-sev').value = 25;
        document.getElementById('stress-freq').value = 5;
        document.getElementById('stress-ret').value = 500000;
        document.getElementById('stress-exp').value = 24;
      }
      runStressSimulation();
    }"""

new_stress_preset_fn = """    function applyStressPreset(type) {
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
        document.getElementById('stress-ret').value = 300000;
        document.getElementById('stress-exp').value = 25;
      } else if (type === 'inflation') {
        document.getElementById('stress-sev').value = 25;
        document.getElementById('stress-freq').value = 5;
        document.getElementById('stress-ret').value = 500000;
        document.getElementById('stress-exp').value = 24;
      }
      syncStressSliders();
      runStressSimulation();
    }"""

content = content.replace(old_stress_preset_fn, new_stress_preset_fn)

# Also ensure makeTableSortable is called when data is loaded dynamically
content = content.replace("rows.slice(0, 50).forEach(r => {", "makeTableSortable('gold-marts-table');\n        rows.slice(0, 50).forEach(r => {")
content = content.replace("rowsTri.forEach(r => {", "makeTableSortable('triangle-table');\n        rowsTri.forEach(r => {")
content = content.replace("rowsIbnr.forEach(r => {", "makeTableSortable('ibnr-table');\n        rowsIbnr.forEach(r => {")

with open('src/api/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Enterprise features added cleanly!")
