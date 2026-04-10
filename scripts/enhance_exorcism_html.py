#!/usr/bin/env python3
"""
Enhance all exorcism per-project index.html files:
1. Inject interactive Callgraph Viewer (Mermaid)
2. Inject CFG Explorer (dropdown + Mermaid render)
3. Add sidebar nav entries for the new sections

Data is INLINED as JSON variables in <script> tags so the pages
work from file:// without any HTTP server.
"""
import os
import json
import glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Sidebar nav entries to add
NAV_ENTRIES = '''  <a href="#callgraph-viewer">7. Call Graph</a>
  <a href="#cfg-explorer">8. CFG Explorer</a>'''


def build_inject_block(data_dir):
    """Build the full injection block with inlined data for one project."""

    # Load callgraph
    cg_path = os.path.join(data_dir, 'callgraph.json')
    callgraph = []
    if os.path.exists(cg_path):
        try:
            with open(cg_path, encoding='utf-8') as f:
                callgraph = json.load(f)
        except Exception:
            pass

    # Load metrics
    met_path = os.path.join(data_dir, 'metrics.json')
    metrics = []
    if os.path.exists(met_path):
        try:
            with open(met_path, encoding='utf-8') as f:
                metrics = json.load(f)
        except Exception:
            pass

    # Load all CFG files
    cfg_dir = os.path.join(data_dir, 'cfg')
    cfgs = {}
    if os.path.isdir(cfg_dir):
        for cfgfile in glob.glob(os.path.join(cfg_dir, '*.json')):
            key = os.path.splitext(os.path.basename(cfgfile))[0]
            try:
                with open(cfgfile, encoding='utf-8') as f:
                    cfgs[key] = json.load(f)
            except Exception:
                pass

    cg_json = json.dumps(callgraph, separators=(',', ':'))
    met_json = json.dumps(metrics, separators=(',', ':'))
    cfgs_json = json.dumps(cfgs, separators=(',', ':'))

    return f'''
<!-- ═══ Interactive Callgraph & CFG Explorer (injected) ═══ -->
<style>
#callgraph-viewer .mermaid-wrap {{
  background: var(--card); border: 1px solid var(--border); border-radius: 8px;
  padding: 20px; overflow-x: auto; margin-bottom: 16px; min-height: 200px;
}}
#cfg-explorer select {{
  padding: 8px 12px; border: 1px solid var(--border); border-radius: 6px;
  font-size: 13px; min-width: 300px; margin-right: 12px; background: #fff;
}}
#cfg-explorer .cfg-render {{
  background: var(--card); border: 1px solid var(--border); border-radius: 8px;
  padding: 20px; overflow-x: auto; margin-top: 16px; min-height: 150px;
}}
#cfg-explorer .cfg-meta {{
  display: flex; gap: 16px; margin-top: 12px; flex-wrap: wrap;
}}
#cfg-explorer .cfg-meta .stat-card {{ min-width: 100px; }}
.callgraph-controls {{ margin-bottom: 16px; display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }}
.callgraph-controls input {{
  padding: 8px 12px; border: 1px solid var(--border); border-radius: 6px;
  font-size: 13px; min-width: 250px;
}}
.no-data {{ color: #999; font-style: italic; padding: 20px; }}
</style>

<script>
(function() {{
  var __CALLGRAPH__ = {cg_json};
  var __METRICS__ = {met_json};
  var __CFGS__ = {cfgs_json};

  // ── Callgraph Viewer ──
  var cgSection = document.getElementById('callgraph-viewer');
  if (cgSection) {{
    var data = __CALLGRAPH__;
    var wrap = cgSection.querySelector('.mermaid-wrap');
    if (!data || data.length === 0) {{
      wrap.innerHTML = '<p class="no-data">No call relationships found in this project.</p>';
    }} else {{
      // Reject strings with quotes, braces, parens, slashes, spaces
      function isSafeName(s) {{ return /^[a-zA-Z_][a-zA-Z0-9_.]*$/.test(s); }}

      // Normalize: strip class/module prefix — "Foo.bar" → "bar", "bar" → "bar"
      function normName(s) {{
        var i = s.lastIndexOf('.');
        return i >= 0 ? s.substring(i + 1) : s;
      }}

      // Build normalized call graph: caller → [callee, ...] using bare function names
      // This merges "Foo.bar" targets with "bar" callers so edges connect properly
      var callerSet = {{}};  // bare name → true (functions that appear as callers)
      data.forEach(function(d) {{
        var fn = d["function"];
        if (isSafeName(fn)) callerSet[fn] = true;
      }});

      // Count how many unique callees each caller has
      var callCounts = {{}};
      data.forEach(function(d) {{
        var fn = d["function"];
        if (!isSafeName(fn)) return;
        var targets = {{}};
        (d.calls || []).forEach(function(c) {{
          if (!isSafeName(c)) return;
          var norm = normName(c);
          // Only count if the normalized target is also a known caller (real function)
          if (callerSet[norm]) targets[norm] = true;
        }});
        var targetList = Object.keys(targets);
        callCounts[fn] = (callCounts[fn] || 0) + targetList.length;
        targetList.forEach(function(t) {{ callCounts[t] = callCounts[t] || 0; }});
      }});

      var topFuncs = Object.keys(callCounts)
        .sort(function(a,b) {{ return (callCounts[b]||0) - (callCounts[a]||0); }})
        .slice(0, 50);
      var topSet = {{}};
      topFuncs.forEach(function(f) {{ topSet[f] = true; }});

      var lines = ['flowchart LR'];
      var nodeIds = {{}};
      var idCounter = 0;
      var edgeSet = {{}};

      data.forEach(function(d) {{
        var fn = d["function"];
        if (!topSet[fn]) return;
        (d.calls || []).forEach(function(c) {{
          if (!isSafeName(c)) return;
          var tgt = normName(c);
          if (!topSet[tgt] || tgt === fn) return;  // skip self-loops
          if (nodeIds[fn] === undefined) nodeIds[fn] = idCounter++;
          if (nodeIds[tgt] === undefined) nodeIds[tgt] = idCounter++;
          var srcId = 'N' + nodeIds[fn];
          var tgtId = 'N' + nodeIds[tgt];
          var key = srcId + '>' + tgtId;
          if (!edgeSet[key]) {{
            edgeSet[key] = true;
            lines.push('  ' + srcId + ' --> ' + tgtId);
          }}
        }});
      }});

      // Add node labels (bare function names, safe for Mermaid)
      Object.keys(nodeIds).forEach(function(name) {{
        var short = name.length > 28 ? name.slice(0,25) + '...' : name;
        lines.push('  N' + nodeIds[name] + '["' + short + '"]');
      }});

      var nodeCount = Object.keys(nodeIds).length;
      var edgeCount = Object.keys(edgeSet).length;
      if (nodeCount < 2) {{
        wrap.innerHTML = '<p class="no-data">Not enough inter-function calls to visualize.</p>';
      }} else {{
        var mermaidCode = lines.join('\\n');
        wrap.innerHTML = '';
        var div = document.createElement('div');
        div.className = 'mermaid';
        div.textContent = mermaidCode;
        wrap.appendChild(div);
        try {{
          if (window.mermaid) mermaid.init(undefined, div);
        }} catch(e) {{
          wrap.innerHTML = '<p class="no-data">Diagram too complex to render inline (' + nodeCount + ' nodes, ' + edgeCount + ' edges). Try opening in a Mermaid live editor.</p>';
        }}
      }}

      // Populate datalist with node names for autocomplete
      var datalist = document.getElementById('cg-suggestions');
      if (datalist) {{
        Object.keys(nodeIds).sort().forEach(function(name) {{
          var opt = document.createElement('option');
          opt.value = name;
          datalist.appendChild(opt);
        }});
      }}

      var searchInput = cgSection.querySelector('.cg-search');
      if (searchInput) {{
        searchInput.addEventListener('input', function() {{
          var q = this.value.toLowerCase().trim();
          wrap.querySelectorAll('.node').forEach(function(n) {{
            var txt = (n.textContent || '').toLowerCase();
            n.style.opacity = (!q || txt.indexOf(q) >= 0) ? '1' : '0.15';
          }});
        }});
      }}
    }}
  }}

  // ── CFG Explorer ──
  var cfgSection = document.getElementById('cfg-explorer');
  if (cfgSection) {{
    var select = cfgSection.querySelector('#cfg-select');
    var renderArea = cfgSection.querySelector('.cfg-render');
    var metaArea = cfgSection.querySelector('.cfg-meta');
    var metrics = __METRICS__;
    var cfgData = __CFGS__;

    var withCfg = metrics.filter(function(m) {{ return m.cyclomatic_complexity > 3; }});
    if (withCfg.length === 0) {{
      select.innerHTML = '<option>No complex functions (all CC \\u2264 3)</option>';
    }} else {{
      withCfg.sort(function(a,b) {{ return b.cyclomatic_complexity - a.cyclomatic_complexity; }});
      select.innerHTML = '<option value="">\\u2014 Select a function to visualize \\u2014</option>';
      withCfg.forEach(function(m) {{
        var opt = document.createElement('option');
        opt.value = m["function"] + '_' + m.start_line;
        opt.textContent = m["function"] + ' (CC=' + m.cyclomatic_complexity + ', ' + m.file + ':' + m.start_line + ')';
        select.appendChild(opt);
      }});

      select.addEventListener('change', function() {{
        if (!this.value) {{ renderArea.innerHTML = ''; metaArea.innerHTML = ''; return; }}
        var cfg = cfgData[this.value];
        if (!cfg) {{
          renderArea.innerHTML = '<p class="no-data">CFG data not found for this function.</p>';
          metaArea.innerHTML = '';
          return;
        }}
        var lines = ['flowchart TD'];
        cfg.nodes.forEach(function(n) {{
          var lbl = (n.label || 'node').replace(/"/g, "'");
          lines.push('  N' + n.id + '["' + lbl + '<br/>L' + n.line + '"]');
        }});
        cfg.edges.forEach(function(e) {{
          var arrow = e.label ? '-->|' + e.label + '|' : '-->';
          lines.push('  N' + e.from + ' ' + arrow + ' N' + e.to);
        }});
        cfg.nodes.forEach(function(n) {{
          if (n.label && n.label.indexOf('entry') === 0) lines.push('  style N' + n.id + ' fill:#d4edda,stroke:#28a745');
          if (n.label && n.label.indexOf('exit') === 0) lines.push('  style N' + n.id + ' fill:#f8d7da,stroke:#dc3545');
          if (n.label && n.label.indexOf('if') === 0) lines.push('  style N' + n.id + ' fill:#fff3cd,stroke:#ffc107');
        }});

        renderArea.innerHTML = '';
        var div = document.createElement('div');
        div.className = 'mermaid';
        div.textContent = lines.join('\\n');
        renderArea.appendChild(div);
        if (window.mermaid) mermaid.init(undefined, div);

        var selMetric = null;
        for (var i = 0; i < withCfg.length; i++) {{
          if ((withCfg[i]["function"] + '_' + withCfg[i].start_line) === select.value) {{
            selMetric = withCfg[i]; break;
          }}
        }}
        if (selMetric) {{
          metaArea.innerHTML =
            '<div class="stat-card"><div class="num">' + selMetric.cyclomatic_complexity + '</div><div class="lbl">Complexity</div></div>' +
            '<div class="stat-card"><div class="num">' + selMetric.nesting_depth + '</div><div class="lbl">Max Nesting</div></div>' +
            '<div class="stat-card"><div class="num">' + selMetric.loc + '</div><div class="lbl">Lines</div></div>' +
            '<div class="stat-card"><div class="num">' + selMetric.param_count + '</div><div class="lbl">Parameters</div></div>';
        }}
      }});
    }}
  }}
}})();
</script>
'''


CONTENT_SECTIONS = '''
<section id="callgraph-viewer">
  <h2>7. Interactive Call Graph</h2>
  <p>Function call relationships visualized from static analysis. Top 50 most-connected functions.</p>
  <div class="callgraph-controls">
    <input type="text" class="cg-search" list="cg-suggestions" placeholder="Highlight a function..." autocomplete="off" />
    <datalist id="cg-suggestions"></datalist>
  </div>
  <div class="mermaid-wrap">
    <p class="no-data">Loading call graph...</p>
  </div>
</section>

<section id="cfg-explorer">
  <h2>8. Control Flow Graph Explorer</h2>
  <p>Select a function to visualize its control flow. Only functions with cyclomatic complexity &gt; 3 have CFGs.</p>
  <select id="cfg-select"><option>Loading...</option></select>
  <div class="cfg-meta"></div>
  <div class="cfg-render"></div>
</section>
'''


def strip_old_injection(html):
    """Remove previous fetch-based injection if present."""
    # Remove the old injected CSS+JS block
    marker = '<!-- ═══ Interactive Callgraph & CFG Explorer (injected) ═══ -->'
    idx = html.find(marker)
    if idx >= 0:
        # Find the end: it's before </body>
        end_marker = '\n</body>'
        end_idx = html.find(end_marker, idx)
        if end_idx > idx:
            html = html[:idx] + html[end_idx:]

    # Remove the old content sections (callgraph-viewer and cfg-explorer)
    for section_id in ['callgraph-viewer', 'cfg-explorer']:
        start_tag = f'<section id="{section_id}">'
        idx = html.find(start_tag)
        if idx >= 0:
            end_tag = '</section>'
            end_idx = html.find(end_tag, idx)
            if end_idx > idx:
                # Remove including any leading newlines
                start = idx
                while start > 0 and html[start-1] == '\n':
                    start -= 1
                html = html[:start] + html[end_idx + len(end_tag):]

    # Remove old nav entries
    for nav_line in ['  <a href="#callgraph-viewer">7. Call Graph</a>\n',
                     '  <a href="#cfg-explorer">8. CFG Explorer</a>\n']:
        html = html.replace(nav_line, '')

    return html


def patch_html(filepath):
    """Patch a single exorcism index.html with inlined interactive viewers."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Strip any old injection first
    html = strip_old_injection(html)

    # Determine _data dir
    data_dir = os.path.join(os.path.dirname(filepath), '_data')
    if not os.path.isdir(data_dir):
        return False

    # Build the inject block with inlined data
    inject_block = build_inject_block(data_dir)

    # 1. Add nav entries before </nav>
    html = html.replace('</nav>', NAV_ENTRIES + '\n</nav>', 1)

    # 2. Add content sections before the closing </div> + <script>
    html = html.replace('</div>\n  <script>', CONTENT_SECTIONS + '\n</div>\n  <script>', 1)

    # 3. Add the inlined JS + CSS before </body>
    html = html.replace('</body>', inject_block + '\n</body>', 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return True


def main():
    pattern = os.path.join(BASE, 'exorcism-*', 'index.html')
    files = glob.glob(pattern)
    patched = 0
    errors = 0
    for f in sorted(files):
        try:
            if patch_html(f):
                patched += 1
        except Exception as e:
            print(f"ERROR: {f}: {e}")
            errors += 1
    print(f"Patched {patched} files, {errors} errors")


if __name__ == '__main__':
    main()
