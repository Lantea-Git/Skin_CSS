import re
import os
import fnmatch

js_file = "ui_2023_jvc_js.js"

# === Motif des fichiers CSS Stylus
pattern = "*JVC*Stylus_*.css"
matches = [f for f in os.listdir('.') if fnmatch.fnmatch(f, pattern)]

if matches:
    css_file = max(matches, key=os.path.getmtime)  # Le plus récent
else:
    css_file = "ui_2023_jvc.user.css"  # Autre logique

# === Lecture du CSS
with open(css_file, "r", encoding="utf-8") as f:
    css_content = f.read()

# === Métadonnées
version = re.search(r"@version\s+([0-9.]+)", css_content).group(1)
description = re.search(r"@description\s+([^.]+)", css_content).group(1)
auteur = re.search(r"@author\s+(.+)", css_content).group(1)

# === Nettoyage : en-têtes UserStyle + @-moz-document
css_cleaned = re.sub(r"/\*\s*==UserStyle==[\s\S]*?==/UserStyle==\s*\*/", "", css_content)
css_cleaned = re.sub(r"@-moz-document\s+domain\([^)]+\)\s*{", "", css_cleaned).strip()
if css_cleaned.endswith("}"):
    css_cleaned = css_cleaned[:-1].strip()

#virer VAR-*
lines = css_cleaned.splitlines()
result = []
i = 0
while i < len(lines):
    # Supprimer VCSS-START + la ligne suivante
    if lines[i].strip() == "/* VCSS-START */":
        i += 2  # saute START + la ligne après
        continue

    # Supprimer la ligne juste avant VCSS-END + la ligne VCSS-END elle-même
    if lines[i].strip() == "/* VCSS-END */":
        if result:
            result.pop()  # retire la ligne précédente
        i += 1  # saute la ligne VCSS-END
        continue

    result.append(lines[i])
    i += 1

css_cleaned = "\n".join(result)


css_lines = css_cleaned.splitlines()
if css_lines:
    css_lines[0] = '    ' + css_lines[0]
css_cleaned = "\n".join(css_lines)

# === Génération du UserScript JS
js_header = f"""// ==UserScript==
// @name         UI_2023_JVC_JS
// @namespace    UI_2023_JVC_JS
// @version      {version}
// @description  {description} (JS).
// @author       {auteur}
// @match        *://www.jeuxvideo.com/*
// @grant        GM_addStyle
// @icon         https://images.emojiterra.com/google/noto-emoji/unicode-16.0/color/128px/1f7e7.png
// @license      CC0-1.0
// @run-at       document-start
// ==/UserScript==

/* SKIN CSS : https://userstyles.world/style/17542/ */
"""

js_content = js_header + '\nGM_addStyle(`\n\n' + css_cleaned + '\n`);\n'

with open(js_file, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"✅ JS généré : {js_file}")