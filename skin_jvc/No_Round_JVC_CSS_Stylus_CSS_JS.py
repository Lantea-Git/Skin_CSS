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



# === Nettoyage : en-têtes UserStyle + @-moz-document
css_content = re.sub(r"/\*\s*==UserStyle==[\s\S]*?==/UserStyle==\s*\*/\n?", "", css_content) #Entete
# css_content = re.sub(r"@-moz-document\s+domain\([^)]+\)\s*{", "", css_content) #moz 
# css_content = re.sub(r"}\s*$", "", css_content) #fin accolade css


css_result_split = []
in_remove_block = False

for line in css_content.splitlines(True):
    stripped = line.strip()

    # JSCSS-DEL-BLOCK-START - JSCSS-DEL-BLOCK-END block supprime
    if "JSCSS-DEL-BLOCK-START" in stripped:
        in_remove_block = True
        continue
    if "JSCSS-DEL-BLOCK-END" in stripped:
        in_remove_block = False
        continue
    if in_remove_block:
        continue

    # JSCSS-DEL-LINE dans JSCSS
    if "JSCSS-DEL-LINE" in stripped:
        continue

    # Ajout des lignes normales ou internes au bloc UNCOMMENT
    css_result_split.append(line)
css_content = "".join(css_result_split)


# === Génération du UserScript JS
js_header = f"""// ==UserScript==
// @name         UI_2023_JVC_JS
// @namespace    UI_2023_JVC_JS
// @version      {version}
// @description  {description} (JS).
// @author       {auteur}
// @match        *://www.jeuxvideo.com/*
// @grant        none
// @icon         https://images.emojiterra.com/google/noto-emoji/unicode-16.0/color/128px/1f7e7.png
// @license      CC0-1.0
// @run-at       document-start
// ==/UserScript==

/* SKIN CSS : https://userstyles.world/style/17542/ */
"""


js_content = js_header + f"""
const style = document.createElement("style");
style.textContent = `
{css_content}
`;
document.head.append(style);
"""

with open(js_file, "w", encoding="utf-8") as file:
    file.write(js_content)

print(f"✅ JS généré : {js_file}")
