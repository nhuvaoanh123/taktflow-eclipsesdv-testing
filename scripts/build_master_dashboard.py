#!/usr/bin/env python3
"""
Build a professional consortium-grade master dashboard for all exorcism projects.
Reads _master_data.json and generates exorcism-master-index.html.
"""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE, '_master_data.json')) as f:
    projects = json.load(f)

# Categorize
cats = {}
for p in projects:
    name = p['dir'].replace('exorcism-', '')
    parts = name.split('-')
    cat = parts[0].upper()
    cats.setdefault(cat, []).append(p)

# Sort categories, sort projects within by LOC descending
for c in cats:
    cats[c].sort(key=lambda p: p['loc'], reverse=True)

# Aggregates
total_files = sum(p['files'] for p in projects)
total_loc = sum(p['loc'] for p in projects)
total_funcs = sum(p['funcs'] for p in projects)
total_comm = sum(p['comm'] for p in projects)
total_sm = sum(p['sm'] for p in projects)
total_high_cc = sum(p['high_cc'] for p in projects)
avg_cc_all = round(sum(p['avg_cc'] * p['funcs'] for p in projects if p['funcs']) / total_funcs, 1) if total_funcs else 0

# Language totals across all projects
all_langs = {}
for p in projects:
    for l in p['langs']:
        all_langs[l] = all_langs.get(l, 0) + 1
lang_sorted = sorted(all_langs.items(), key=lambda x: x[1], reverse=True)

# Category descriptions for consortium context
CAT_DESC = {
    'ANKAIOS': 'Lightweight workload orchestrator for automotive ECUs — manages container and process lifecycles in resource-constrained environments.',
    'CHARIOTT': 'Service discovery and intent-based programming model for in-vehicle software components.',
    'ECLIPSE': 'Core Eclipse SDV platform components including KUKSA databroker and Python SDK.',
    'IBEJI': 'In-vehicle digital twin framework — maintains live models of vehicle state and synchronizes with cloud.',
    'KUKSA': 'Vehicle data layer — feeders, providers, and SDK implementations for the central VSS databroker.',
    'LEDA': 'Complete SDV Linux distribution bundling orchestration, data broker, and container runtime.',
    'SCORE': 'Safety-certified middleware — ASIL-rated communication, lifecycle, logging, and OS abstraction layers.',
    'SDV': 'SDV Blueprints — reference application patterns for fleet management, insurance, and ROS integration.',
    'UPROTOCOL': 'Transport-agnostic messaging protocol bridging MQTT, SOME/IP, Zenoh, and gRPC across vehicle domains.',
    'VELOCITAS': 'Vehicle App development SDK and toolchain — templates, model generators, and CLI for rapid prototyping.',
}

def fmt_num(n):
    return f'{n:,}'

def cc_badge(avg):
    if avg <= 3:
        return f'<span class="badge badge-green">{avg}</span>'
    elif avg <= 6:
        return f'<span class="badge badge-yellow">{avg}</span>'
    else:
        return f'<span class="badge badge-red">{avg}</span>'

def lang_tags(langs):
    return ' '.join(f'<span class="tag">{l}</span>' for l in langs)

# Build sidebar nav
sidebar_cats = ''.join(
    f'<a href="#cat-{c.lower()}">{c} ({len(cats[c])})</a>'
    for c in sorted(cats)
)

# Build category sections
cat_sections = []
for c in sorted(cats):
    ps = cats[c]
    cat_loc = sum(p['loc'] for p in ps)
    cat_funcs = sum(p['funcs'] for p in ps)
    cat_files = sum(p['files'] for p in ps)
    desc = CAT_DESC.get(c, '')

    rows = []
    for p in ps:
        rows.append(f'''<tr>
  <td><a href="{p['dir']}/index.html">{p['name']}</a></td>
  <td>{lang_tags(p['langs'])}</td>
  <td class="num-cell">{fmt_num(p['files'])}</td>
  <td class="num-cell">{fmt_num(p['loc'])}</td>
  <td class="num-cell">{fmt_num(p['funcs'])}</td>
  <td>{cc_badge(p['avg_cc'])}</td>
  <td class="num-cell">{p['max_cc']}</td>
  <td class="num-cell">{p['high_cc']}</td>
  <td class="num-cell">{p['comm']}</td>
  <td class="num-cell">{p['sm']}</td>
</tr>''')

    cat_sections.append(f'''
<section id="cat-{c.lower()}" class="cat-section">
  <h2>{c} <span class="cat-count">{len(ps)} projects</span></h2>
  <p class="cat-desc">{desc}</p>
  <div class="cat-stats">
    <div class="mini-stat"><span class="mini-num">{fmt_num(cat_files)}</span><span class="mini-lbl">Files</span></div>
    <div class="mini-stat"><span class="mini-num">{fmt_num(cat_loc)}</span><span class="mini-lbl">LOC</span></div>
    <div class="mini-stat"><span class="mini-num">{fmt_num(cat_funcs)}</span><span class="mini-lbl">Functions</span></div>
  </div>
  <table class="data-table sortable">
    <thead>
      <tr>
        <th>Project</th><th>Languages</th><th>Files</th><th>LOC</th><th>Functions</th>
        <th>Avg CC</th><th>Max CC</th><th>High CC</th><th>Comm</th><th>SM</th>
      </tr>
    </thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>
</section>''')

# Build language breakdown for donut chart data
lang_chart_data = json.dumps([{'lang': l, 'count': c} for l, c in lang_sorted[:12]])

# Category chart data (LOC distribution)
cat_chart_data = json.dumps([{'cat': c, 'loc': sum(p['loc'] for p in cats[c])} for c in sorted(cats)])

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Eclipse SDV — Codebase Intelligence Report</title>
  <style>
:root {{
  --bg: #f5f6f8;
  --sidebar: #0f1419;
  --sidebar-hover: #1a2332;
  --accent: #4f8ef7;
  --accent-light: #e8f0fe;
  --text: #2d3748;
  --text-secondary: #718096;
  --border: #e2e8f0;
  --card: #fff;
  --green: #38a169;
  --yellow: #d69e2e;
  --red: #e53e3e;
  --shadow: 0 1px 3px rgba(0,0,0,.08), 0 1px 2px rgba(0,0,0,.06);
  --shadow-lg: 0 4px 6px rgba(0,0,0,.07), 0 2px 4px rgba(0,0,0,.06);
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
       background: var(--bg); color: var(--text); display: flex; min-height: 100vh;
       font-size: 14px; line-height: 1.6; }}

/* Sidebar */
#sidebar {{
  width: 280px; min-width: 280px; background: var(--sidebar); color: #8899aa;
  position: sticky; top: 0; height: 100vh; overflow-y: auto;
  display: flex; flex-direction: column; z-index: 10;
}}
#sidebar .brand {{
  padding: 24px 20px; border-bottom: 1px solid #1e2d3d;
}}
#sidebar .brand h1 {{
  font-size: 11px; font-weight: 700; text-transform: uppercase;
  letter-spacing: .12em; color: #556677; margin-bottom: 4px;
}}
#sidebar .brand .title {{
  font-size: 16px; font-weight: 700; color: #fff; line-height: 1.3;
}}
#sidebar .brand .subtitle {{
  font-size: 11px; color: #556677; margin-top: 4px;
}}
#sidebar nav {{ padding: 16px 0; flex: 1; }}
#sidebar .nav-group {{ padding: 0 0 8px; }}
#sidebar .nav-label {{
  font-size: 10px; text-transform: uppercase; letter-spacing: .12em;
  color: #445566; padding: 12px 20px 4px; font-weight: 600;
}}
#sidebar a {{
  display: block; padding: 6px 20px; color: #8899aa; text-decoration: none;
  font-size: 13px; border-left: 3px solid transparent; transition: all .15s;
}}
#sidebar a:hover, #sidebar a.active {{
  background: var(--sidebar-hover); color: #fff; border-left-color: var(--accent);
}}
#sidebar .nav-badge {{
  float: right; background: #1e2d3d; color: #667; padding: 1px 7px;
  border-radius: 10px; font-size: 11px;
}}

/* Content */
#content {{ flex: 1; max-width: 1200px; padding: 32px 48px; overflow-x: hidden; }}

/* Hero */
.hero {{
  background: linear-gradient(135deg, #0f1419 0%, #1a2332 50%, #2d3748 100%);
  color: #fff; padding: 48px; border-radius: 16px; margin-bottom: 32px;
  position: relative; overflow: hidden;
}}
.hero::after {{
  content: ''; position: absolute; top: -50%; right: -20%; width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(79,142,247,.15) 0%, transparent 70%);
  pointer-events: none;
}}
.hero h1 {{ font-size: 32px; font-weight: 800; margin-bottom: 8px; position: relative; }}
.hero .tagline {{ color: #8899aa; font-size: 15px; position: relative; }}
.hero .meta {{ margin-top: 16px; display: flex; gap: 24px; flex-wrap: wrap; position: relative; }}
.hero .meta-item {{ font-size: 12px; color: #667788; }}
.hero .meta-item strong {{ color: #aabbcc; }}

/* Stats Grid */
.stats-grid {{
  display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px; margin-bottom: 32px;
}}
.stat-card {{
  background: var(--card); border: 1px solid var(--border); border-radius: 12px;
  padding: 20px; box-shadow: var(--shadow); transition: transform .15s, box-shadow .15s;
}}
.stat-card:hover {{ transform: translateY(-2px); box-shadow: var(--shadow-lg); }}
.stat-card .num {{ font-size: 32px; font-weight: 800; color: var(--accent); line-height: 1; }}
.stat-card .lbl {{ font-size: 12px; color: var(--text-secondary); margin-top: 6px; font-weight: 500; }}
.stat-card .trend {{ font-size: 11px; margin-top: 4px; }}
.stat-card .trend.good {{ color: var(--green); }}
.stat-card .trend.warn {{ color: var(--yellow); }}
.stat-card .trend.bad {{ color: var(--red); }}

/* Section headers */
section {{ margin-bottom: 40px; scroll-margin-top: 24px; }}
section h2 {{
  font-size: 22px; font-weight: 700; color: var(--text);
  padding-bottom: 12px; margin-bottom: 20px;
  border-bottom: 2px solid var(--accent);
  display: flex; align-items: center; gap: 12px;
}}
.cat-count {{
  font-size: 13px; font-weight: 600; background: var(--accent-light);
  color: var(--accent); padding: 2px 10px; border-radius: 12px;
}}
.cat-desc {{
  color: var(--text-secondary); margin-bottom: 16px; font-size: 14px; max-width: 800px;
}}
.cat-stats {{
  display: flex; gap: 24px; margin-bottom: 16px;
}}
.mini-stat {{ display: flex; align-items: baseline; gap: 6px; }}
.mini-num {{ font-size: 18px; font-weight: 700; color: var(--accent); }}
.mini-lbl {{ font-size: 12px; color: var(--text-secondary); }}

/* Tables */
.data-table {{
  width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 16px;
  background: var(--card); border-radius: 8px; overflow: hidden;
  box-shadow: var(--shadow);
}}
.data-table th {{
  background: #f7f8fa; text-align: left; padding: 10px 14px;
  border-bottom: 2px solid var(--border); font-weight: 600; color: var(--text-secondary);
  font-size: 11px; text-transform: uppercase; letter-spacing: .05em;
  cursor: pointer; user-select: none; white-space: nowrap;
}}
.data-table th:hover {{ background: #eef0f4; }}
.data-table th::after {{ content: ' \\2195'; opacity: .3; }}
.data-table td {{ padding: 9px 14px; border-bottom: 1px solid #f0f2f5; }}
.data-table tr:hover td {{ background: #f8fafc; }}
.data-table .num-cell {{ text-align: right; font-variant-numeric: tabular-nums; }}
.data-table a {{ color: var(--accent); text-decoration: none; font-weight: 600; }}
.data-table a:hover {{ text-decoration: underline; }}

/* Badges */
.badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; }}
.badge-green {{ background: #f0fff4; color: var(--green); }}
.badge-yellow {{ background: #fffff0; color: var(--yellow); }}
.badge-red {{ background: #fff5f5; color: var(--red); }}
.badge-blue {{ background: var(--accent-light); color: var(--accent); }}
.tag {{ display: inline-block; background: var(--accent-light); color: #3b82f6;
       border-radius: 4px; padding: 1px 7px; font-size: 11px; font-weight: 500; margin: 1px; }}

/* Search */
.search-bar {{
  position: sticky; top: 0; z-index: 5; background: var(--bg);
  padding: 16px 0; margin-bottom: 16px;
}}
.search-bar input {{
  width: 100%; padding: 12px 16px; border: 1px solid var(--border);
  border-radius: 10px; font-size: 14px; background: var(--card);
  box-shadow: var(--shadow); transition: border-color .15s, box-shadow .15s;
}}
.search-bar input:focus {{
  outline: none; border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(79,142,247,.15);
}}
.search-bar .search-meta {{
  font-size: 12px; color: var(--text-secondary); margin-top: 8px;
}}

/* Charts area */
.charts-grid {{
  display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 32px;
}}
.chart-card {{
  background: var(--card); border: 1px solid var(--border); border-radius: 12px;
  padding: 24px; box-shadow: var(--shadow);
}}
.chart-card h3 {{ font-size: 14px; font-weight: 600; color: var(--text); margin-bottom: 16px; }}
.bar-chart {{ display: flex; flex-direction: column; gap: 8px; }}
.bar-row {{ display: flex; align-items: center; gap: 10px; }}
.bar-label {{ width: 100px; font-size: 12px; color: var(--text-secondary); text-align: right;
              flex-shrink: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.bar-track {{ flex: 1; height: 24px; background: #f0f2f5; border-radius: 6px; overflow: hidden; position: relative; }}
.bar-fill {{ height: 100%; border-radius: 6px; transition: width .6s ease; min-width: 2px; }}
.bar-value {{ position: absolute; right: 8px; top: 50%; transform: translateY(-50%);
              font-size: 11px; font-weight: 600; color: var(--text); }}

/* Ecosystem diagram */
.mermaid {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px;
           padding: 24px; text-align: center; overflow-x: auto; box-shadow: var(--shadow); }}

/* Responsive */
@media (max-width: 1024px) {{
  .charts-grid {{ grid-template-columns: 1fr; }}
}}
@media (max-width: 768px) {{
  body {{ flex-direction: column; }}
  #sidebar {{ width: 100%; height: auto; position: static; }}
  #content {{ padding: 20px; }}
  .hero {{ padding: 24px; }}
  .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
}}
html {{ scroll-behavior: smooth; }}

/* Print */
@media print {{
  #sidebar {{ display: none; }}
  #content {{ max-width: 100%; padding: 0; }}
  .hero {{ background: #1a2332 !important; -webkit-print-color-adjust: exact; }}
  .search-bar {{ display: none; }}
}}

/* Footer */
.footer {{
  text-align: center; padding: 32px; color: var(--text-secondary); font-size: 12px;
  border-top: 1px solid var(--border); margin-top: 32px;
}}
</style>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
</head>
<body>
  <div id="sidebar">
    <div class="brand">
      <h1>Eclipse SDV</h1>
      <div class="title">Codebase Intelligence Report</div>
      <div class="subtitle">{len(projects)} projects &middot; {fmt_num(total_loc)} LOC</div>
    </div>
    <nav>
      <div class="nav-group">
        <div class="nav-label">Overview</div>
        <a href="#dashboard">Executive Summary</a>
        <a href="#charts">Analysis Charts</a>
        <a href="#ecosystem">Ecosystem Map</a>
      </div>
      <div class="nav-group">
        <div class="nav-label">Categories ({len(cats)})</div>
        {sidebar_cats}
      </div>
    </nav>
  </div>

  <div id="content">
    <div class="hero">
      <h1>Eclipse SDV Codebase Intelligence</h1>
      <p class="tagline">Automated static analysis across {len(projects)} Eclipse Software Defined Vehicle repositories</p>
      <div class="meta">
        <div class="meta-item">Analysis scope: <strong>{len(cats)} ecosystems</strong></div>
        <div class="meta-item">Languages: <strong>{len(all_langs)} detected</strong></div>
        <div class="meta-item">Generated: <strong>April 2026</strong></div>
      </div>
    </div>

    <section id="dashboard">
      <h2>Executive Summary</h2>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="num">{len(projects)}</div>
          <div class="lbl">Repositories Analyzed</div>
        </div>
        <div class="stat-card">
          <div class="num">{fmt_num(total_files)}</div>
          <div class="lbl">Source Files</div>
        </div>
        <div class="stat-card">
          <div class="num">{fmt_num(total_loc)}</div>
          <div class="lbl">Lines of Code</div>
        </div>
        <div class="stat-card">
          <div class="num">{fmt_num(total_funcs)}</div>
          <div class="lbl">Functions Analyzed</div>
        </div>
        <div class="stat-card">
          <div class="num">{avg_cc_all}</div>
          <div class="lbl">Weighted Avg Complexity</div>
          <div class="trend good">Below industry threshold (&lt;10)</div>
        </div>
        <div class="stat-card">
          <div class="num">{fmt_num(total_high_cc)}</div>
          <div class="lbl">High-Risk Functions (CC&gt;10)</div>
          <div class="trend {'good' if total_high_cc < 500 else 'warn'}">{round(total_high_cc/total_funcs*100,1)}% of total</div>
        </div>
        <div class="stat-card">
          <div class="num">{total_comm}</div>
          <div class="lbl">Communication Patterns</div>
        </div>
        <div class="stat-card">
          <div class="num">{total_sm}</div>
          <div class="lbl">State Machines</div>
        </div>
      </div>
    </section>

    <section id="charts">
      <h2>Analysis Breakdown</h2>
      <div class="charts-grid">
        <div class="chart-card">
          <h3>LOC by Ecosystem</h3>
          <div class="bar-chart" id="loc-chart"></div>
        </div>
        <div class="chart-card">
          <h3>Language Distribution (by project count)</h3>
          <div class="bar-chart" id="lang-chart"></div>
        </div>
      </div>
    </section>

    <section id="ecosystem">
      <h2>SDV Ecosystem Architecture</h2>
      <div class="mermaid">flowchart TB
    subgraph Vehicle["In-Vehicle Software Stack"]
        direction TB
        KUKSA["KUKSA Databroker\\n(Vehicle Data Layer)\\n53K LOC"]
        Ankaios["Ankaios\\n(Workload Orchestrator)\\n97K LOC"]
        Ibeji["Ibeji\\n(Digital Twin)\\n20K LOC"]
        Chariott["Chariott\\n(Service Discovery)\\n13K LOC"]
        VehicleApps["Velocitas Apps\\n(Vehicle App SDK)\\n38K LOC"]
        SCORE["SCORE\\n(Safety Middleware)\\n781K LOC"]
    end
    subgraph Protocols["Communication Protocols"]
        CAN["CAN Bus"]
        SOMEIP["SOME/IP"]
        uP["uProtocol\\n58K LOC"]
        Zenoh["Zenoh"]
        MQTT["MQTT"]
        gRPC["gRPC"]
    end
    subgraph Cloud["Cloud / Fleet"]
        Freyja["Freyja\\n(Cloud Sync)"]
        Fleet["Fleet Mgmt\\nBlueprints 12K LOC"]
    end
    subgraph Edge["Edge / Distribution"]
        Leda["Leda\\n(SDV Distro)\\n24K LOC"]
    end

    CAN --> KUKSA
    SOMEIP --> KUKSA
    KUKSA --> VehicleApps
    KUKSA --> Ibeji
    Ibeji --> Freyja
    Freyja --> Fleet
    Ankaios --> VehicleApps
    Chariott --> VehicleApps
    uP --> Chariott
    MQTT --> Chariott
    Zenoh --> uP
    gRPC --> KUKSA
    Leda --> KUKSA
    Leda --> Ankaios
    SCORE --> Ankaios</div>
    </section>

    <div class="search-bar">
      <input type="text" id="project-search" placeholder="Search projects by name, language, or category..." />
      <div class="search-meta" id="search-meta">Showing all {len(projects)} projects across {len(cats)} categories</div>
    </div>

    {''.join(cat_sections)}

    <div class="footer">
      Eclipse SDV Codebase Intelligence Report &middot; Generated by Taktflow Systems automated static analysis pipeline<br/>
      {fmt_num(total_loc)} lines of code across {len(projects)} repositories &middot; {fmt_num(total_funcs)} functions &middot; {len(all_langs)} languages
    </div>
  </div>

  <script>
mermaid.initialize({{ startOnLoad: true, theme: 'default', securityLevel: 'loose' }});

// ── Bar Charts ──
const catData = {cat_chart_data};
const langData = {lang_chart_data};
const colors = ['#4f8ef7','#38a169','#d69e2e','#e53e3e','#805ad5','#dd6b20','#319795','#d53f8c','#3182ce','#718096'];

function renderBarChart(containerId, data, labelKey, valueKey, maxVal) {{
  const el = document.getElementById(containerId);
  if (!el) return;
  const max = maxVal || Math.max(...data.map(d => d[valueKey]));
  el.innerHTML = data.map((d, i) => {{
    const pct = Math.round(d[valueKey] / max * 100);
    const color = colors[i % colors.length];
    return '<div class="bar-row">' +
      '<span class="bar-label">' + d[labelKey] + '</span>' +
      '<div class="bar-track"><div class="bar-fill" style="width:' + pct + '%;background:' + color + '"></div>' +
      '<span class="bar-value">' + d[valueKey].toLocaleString() + '</span></div></div>';
  }}).join('');
}}

renderBarChart('loc-chart', catData, 'cat', 'loc');
renderBarChart('lang-chart', langData, 'lang', 'count');

// ── Search / Filter ──
const searchInput = document.getElementById('project-search');
const searchMeta = document.getElementById('search-meta');
const catSections = document.querySelectorAll('.cat-section');

searchInput.addEventListener('input', function() {{
  const q = this.value.toLowerCase().trim();
  let shown = 0;
  let shownCats = 0;
  catSections.forEach(section => {{
    const rows = section.querySelectorAll('tbody tr');
    let catVisible = 0;
    rows.forEach(row => {{
      const text = row.textContent.toLowerCase();
      const match = !q || text.includes(q);
      row.style.display = match ? '' : 'none';
      if (match) catVisible++;
    }});
    section.style.display = catVisible > 0 ? '' : 'none';
    if (catVisible > 0) shownCats++;
    shown += catVisible;
  }});
  searchMeta.textContent = q
    ? 'Showing ' + shown + ' projects matching "' + this.value + '"'
    : 'Showing all {len(projects)} projects across {len(cats)} categories';
}});

// ── Sortable Tables ──
document.querySelectorAll('.data-table.sortable').forEach(table => {{
  const headers = table.querySelectorAll('th');
  headers.forEach((th, i) => {{
    th.addEventListener('click', () => {{
      const tbody = table.querySelector('tbody');
      const rows = Array.from(tbody.querySelectorAll('tr'));
      const asc = th.dataset.sort !== 'asc';
      headers.forEach(h => delete h.dataset.sort);
      th.dataset.sort = asc ? 'asc' : 'desc';
      rows.sort((a, b) => {{
        let av = a.children[i].textContent.trim().replace(/,/g, '');
        let bv = b.children[i].textContent.trim().replace(/,/g, '');
        const an = parseFloat(av), bn = parseFloat(bv);
        if (!isNaN(an) && !isNaN(bn)) return asc ? an - bn : bn - an;
        return asc ? av.localeCompare(bv) : bv.localeCompare(av);
      }});
      rows.forEach(r => tbody.appendChild(r));
    }});
  }});
}});

// ── Active nav highlight ──
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('#sidebar a[href^="#"]');
const observer = new IntersectionObserver(entries => {{
  entries.forEach(e => {{
    if (e.isIntersecting) {{
      navLinks.forEach(l => l.classList.toggle('active',
        l.getAttribute('href') === '#' + e.target.id));
    }}
  }});
}}, {{ threshold: 0.2 }});
sections.forEach(s => observer.observe(s));
</script>
</body>
</html>'''

outpath = os.path.join(BASE, 'exorcism-master-index.html')
with open(outpath, 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Wrote {outpath} ({len(html):,} bytes)')
