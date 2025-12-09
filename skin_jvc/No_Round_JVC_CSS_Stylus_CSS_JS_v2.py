import re
import os
import fnmatch

js_file = "ui_2023_jvc_js.js"

# === Motif des fichiers CSS Stylus
pattern = "*JVC*Stylus_*.css"
version_file = []
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, pattern):
        version_file.append(file)

if version_file:
    css_file = max(version_file, key=os.path.getmtime)  # Le plus récent
else:
    css_file = "ui_2023_jvc.user.css"  # Autre logique

# === Lecture du CSS
with open(css_file, "r", encoding="utf-8") as file:
    css_content = file.read()

# === Get Métadonnées
version = re.search(r"@version\s+([0-9.]+)", css_content).group(1)
description = re.search(r"@description\s+([^.]+)", css_content).group(1)
auteur = re.search(r"@author\s+(.+)", css_content).group(1)

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

# === Nettoyage : en-têtes UserStyle + @-moz-document
css_content = re.sub(r"/\*\s*==UserStyle==[\s\S]*?==/UserStyle==\s*\*/\n?", "", css_content) #Entete
css_content = re.sub(r"@-moz-document\s+domain\([^)]+\)\s*{", "", css_content) #moz 
css_content = re.sub(r"}\s*$", "", css_content) #fin accolade css

# vire VCSS-START + la ligne suivante
css_content = re.sub(r"[^\n]*\/\* VCSS-START \*\/[^\n]*\n[^\n]*\n?", "", css_content)
# vire la ligne juste avant VCSS-END + VCSS-END
css_content = re.sub(r"[^\n]*\n\s*/\* VCSS-END \*/\n?", "", css_content)

# vire VCSS-NO-START et le contenue
css_content = re.sub(r"\s*/\* VCSS-NO-START \*/[\s\S]*?/\* VCSS-NO-END \*/", "", css_content)

js_content = js_header + '\nGM_addStyle(`' + css_content + '\n`);\n'

with open(js_file, "w", encoding="utf-8") as file:
    file.write(js_content)

print(f"✅ JS généré : {js_file}")