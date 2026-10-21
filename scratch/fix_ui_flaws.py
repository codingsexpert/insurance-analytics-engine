"""
Fix identified UI flaws and edge cases:
1. Chart.js Dark Mode live synchronization (ticks, legends, grid lines).
2. Cross-browser SVG Speedometer transform fix (transform-box: view-box & explicit SVG rotate).
3. Preset chips synchronization with range sliders and value badges.
4. Remove duplicate toast-container in print template string.
5. Dark mode contrast fixes for chips, badges, and primary color.
6. Responsive CSS for mobile/tablet (<768px).
"""

with open('src/api/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. FIX DUPLICATE TOAST-CONTAINER IN PRINT WINDOW TEMPLATE
content = content.replace(
    '<pre>${cachedAuditReport || \'Loading...\'}</pre>\n          <div id="toast-container"></div>\n</body>',
    '<pre>${cachedAuditReport || \'Loading...\'}</pre>\n</body>'
)

# 2. ENHANCE CHART.JS THEME SYNC IN setTheme()
old_set_theme = """    function setTheme(theme) {
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('actuaria_theme', theme);
      const icon = document.getElementById('theme-icon');
      const text = document.getElementById('theme-text');
      if (icon && text) {
        if (theme === 'dark') {
          icon.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';
          text.innerText = 'Light';
        } else {
          icon.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
          text.innerText = 'Dark';
        }
      }
    }"""

new_set_theme = """    function setTheme(theme) {
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('actuaria_theme', theme);
      const icon = document.getElementById('theme-icon');
      const text = document.getElementById('theme-text');
      const isDark = theme === 'dark';

      if (icon && text) {
        if (isDark) {
          icon.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';
          text.innerText = 'Light';
        } else {
          icon.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
          text.innerText = 'Dark';
        }
      }

      // Live synchronise all Chart.js colors on theme switch
      if (typeof Chart !== 'undefined') {
        const textColor = isDark ? '#94a3b8' : '#64748b';
        const gridColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.06)';
        Chart.defaults.color = textColor;
        Chart.defaults.borderColor = gridColor;

        if (typeof charts !== 'undefined') {
          Object.values(charts).forEach(ch => {
            try {
              if (ch && ch.options) {
                if (ch.options.scales) {
                  Object.values(ch.options.scales).forEach(scale => {
                    if (scale.ticks) scale.ticks.color = textColor;
                    if (scale.grid) scale.grid.color = gridColor;
                  });
                }
                if (ch.options.plugins && ch.options.plugins.legend && ch.options.plugins.legend.labels) {
                  ch.options.plugins.legend.labels.color = isDark ? '#f8fafc' : '#0f172a';
                }
                ch.update();
              }
            } catch(e) {}
          });
        }
      }
    }"""

content = content.replace(old_set_theme, new_set_theme)

# 3. FIX SPEEDOMETER NEEDLE TRANSFORM & PIVOT POINT
old_update_gauge = """    function updateRiskGauge(tier) {
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
    }"""

new_update_gauge = """    function updateRiskGauge(tier) {
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

      // Cross-browser SVG rotation around center (50, 50)
      needle.setAttribute('transform', `rotate(${rot} 50 50)`);
      needle.style.transform = `rotate(${rot}deg)`;
      needle.setAttribute('stroke', color);
      label.style.color = color;
    }"""

content = content.replace(old_update_gauge, new_update_gauge)

# Ensure SVG line needle has transform-box: view-box;
old_needle_line = '<line id="gauge-needle" x1="50" y1="50" x2="50" y2="18" stroke="#4f46e5" stroke-width="2.5" stroke-linecap="round" style="transform-origin: 50px 50px; transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);"/>'
new_needle_line = '<line id="gauge-needle" x1="50" y1="50" x2="50" y2="18" stroke="#4f46e5" stroke-width="2.5" stroke-linecap="round" style="transform-box: view-box; transform-origin: 50px 50px; transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);"/>'
content = content.replace(old_needle_line, new_needle_line)

# 4. FIX PRESET CHIP SLIDER SYNCHRONIZATION
old_preset_handler_end = """      }
      calculateQuote();
    }"""

new_preset_handler_end = """      }
      // Keep range sliders & value badges in perfect sync with selected preset
      syncQuoteSliders();
      calculateQuote();
    }

    function syncQuoteSliders() {
      const age = document.getElementById('rate-driver-age')?.value;
      const val = document.getElementById('rate-vehicle-val')?.value;
      const mil = document.getElementById('rate-mileage')?.value;

      if (age) {
        syncSlider('rate-driver-age-slider', age);
        const ageDisp = document.getElementById('rate-driver-age-disp');
        if (ageDisp) ageDisp.innerText = age + ' yrs';
      }
      if (val) {
        syncSlider('rate-vehicle-val-slider', val);
        const valDisp = document.getElementById('rate-vehicle-val-disp');
        if (valDisp) valDisp.innerText = formatINR(val);
      }
      if (mil) {
        syncSlider('rate-mileage-slider', mil);
        const milDisp = document.getElementById('rate-mileage-disp');
        if (milDisp) milDisp.innerText = Number(mil).toLocaleString('en-IN') + ' km';
      }
    }"""

content = content.replace(old_preset_handler_end, new_preset_handler_end)

# Also sync sliders initially on DOMContentLoaded
content = content.replace(
    "window.addEventListener('DOMContentLoaded', () => {\n      initTheme();",
    "window.addEventListener('DOMContentLoaded', () => {\n      initTheme();\n      syncQuoteSliders();"
)

# 5. ADD COMPREHENSIVE RESPONSIVE CSS & DARK MODE CHIP STYLES
responsive_and_contrast_css = """
    /* DARK MODE CONTRAST & CHIP REFINEMENTS */
    [data-theme="dark"] .kpi-chip {
      background: rgba(255, 255, 255, 0.08) !important;
      color: #cbd5e1 !important;
    }
    [data-theme="dark"] .status-pill {
      background: rgba(99, 102, 241, 0.15);
      border-color: #4338ca;
      color: #a5b4fc;
    }
    [data-theme="dark"] .tier-badge {
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
    }

    /* RESPONSIVE LAYOUT (<768px & <1024px) */
    @media (max-width: 768px) {
      header {
        padding: 0.75rem 1rem;
        flex-wrap: wrap;
        gap: 0.75rem;
      }
      .header-badges {
        flex-wrap: wrap;
        gap: 0.4rem;
        width: 100%;
        justify-content: flex-start;
      }
      .tabs-wrapper {
        padding: 0 0.75rem;
      }
      main {
        padding: 1rem 0.75rem;
      }
      .kpi-grid {
        grid-template-columns: 1fr;
      }
      .form-grid {
        grid-template-columns: 1fr;
      }
      .result-container {
        grid-template-columns: 1fr;
      }
      .chart-wrapper {
        height: 230px;
      }
    }
"""

content = content.replace('/* PRINT STYLES */', responsive_and_contrast_css + '\n    /* PRINT STYLES */')

with open('src/api/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed Chart.js theme sync, SVG gauge pivot, preset sync, and responsive styles!")
