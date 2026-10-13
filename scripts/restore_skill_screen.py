import os

base_dir = r"C:\Users\fury6\OneDrive\Python_Backend_Academy"
canon_path = os.path.join(base_dir, "design_mockups/canonical_pro_screen_benchmark.html")
academy_path = os.path.join(base_dir, "academy.html")
assemble_path = os.path.join(base_dir, "scripts/assemble_academy.py")

with open(canon_path, "r", encoding="utf-8") as f:
    canon_text = f.read()

# 1. Extract CSS
css_start_marker = "/* ================= CLEAN ECHELON TOPBAR & JEWEL DOTS NECKLACE ================= */"
css_end_marker = "/* ================= 3D TACTILE BUTTONS & CODDY AESTHETICS ================= */"

s_css = canon_text.find(css_start_marker)
e_css = canon_text.find(css_end_marker, s_css)
if s_css == -1 or e_css == -1:
    raise ValueError("CSS markers not found in canon")
canon_css = canon_text[s_css:e_css]

# 2. Extract buildTaskSpecDetails and viewPythonSkill
spec_start_marker = "function buildTaskSpecDetails(tObj){"
fn_end_marker = "\nfunction viewCardsHub(){"

s_spec = canon_text.find(spec_start_marker)
e_fn = canon_text.find(fn_end_marker, s_spec)
if s_spec == -1 or e_fn == -1:
    raise ValueError("buildTaskSpecDetails or viewCardsHub not found in canon")
canon_spec_and_fn = canon_text[s_spec:e_fn]

# Ensure Socratic hint label matches test_e2e_dom.js assert ('Сократовская наводка (2/4)')
old_scaffold_label = 'Уровень скаффолдинга: <strong>${pySkillViewState.hintLevel} / ${socraticHints.length}</strong>'
new_scaffold_label = '💡 Сократовская наводка (${pySkillViewState.hintLevel}/${socraticHints.length})'
if old_scaffold_label in canon_spec_and_fn:
    canon_spec_and_fn = canon_spec_and_fn.replace(old_scaffold_label, new_scaffold_label)
    print("Updated scaffold label for Socratic hint")

# 3. Extract pse click handler
pse_code = """  const pse = e.target.closest('[data-py-select-exam]');
  if(pse){
    const unitId = pse.getAttribute('data-py-select-exam');
    const tr = getTrackForSkill(pySkillViewState.sid || '1.1.1');
    location.hash = '#' + tr.routePrefix + '/unittest/' + unitId;
    return;
  }
"""

def patch_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # A. Inject CSS
    if css_start_marker not in content:
        if css_end_marker in content:
            content = content.replace(css_end_marker, canon_css + css_end_marker, 1)
            print(f"[{filepath}] CSS injected")
        else:
            print(f"[{filepath}] WARNING: css_end_marker not found")
    else:
        curr_s = content.find(css_start_marker)
        curr_e = content.find(css_end_marker, curr_s)
        if curr_s != -1 and curr_e != -1:
            content = content[:curr_s] + canon_css + content[curr_e:]
            print(f"[{filepath}] CSS updated")

    # B. Replace buildTaskSpecDetails + viewPythonSkill
    if spec_start_marker in content:
        f_s = content.find(spec_start_marker)
    else:
        f_s = content.find("function viewPythonSkill(sid){")

    f_e = content.find(fn_end_marker, f_s)
    if f_s != -1 and f_e != -1:
        content = content[:f_s] + canon_spec_and_fn + content[f_e:]
        print(f"[{filepath}] buildTaskSpecDetails + viewPythonSkill placed")
    else:
        print(f"[{filepath}] WARNING: function markers not found")

    # C. Inject pse click handler if not present
    if "data-py-select-exam" not in content:
        psk_marker = "const psk = e.target.closest('[data-py-select-k]');"
        if psk_marker in content:
            content = content.replace(psk_marker, pse_code + "\n  " + psk_marker, 1)
            print(f"[{filepath}] pse click handler injected")
    else:
        print(f"[{filepath}] pse click handler already present")

    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

patch_file(academy_path)
patch_file(assemble_path)

print("Restoration script completed successfully!")
