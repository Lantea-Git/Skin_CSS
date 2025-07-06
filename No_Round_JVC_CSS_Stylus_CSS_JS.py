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

# === Suite

with open(css_file, "r", encoding="utf-8") as f:
    css_content = f.read()

#version
match = re.search(r"@version\s+([0-9.]+)", css_content)
version = match.group(1)

#description
match = re.search(r"@description\s+(.+)", css_content)
description = match.group(1)

#auteur
match = re.search(r"@author\s+(.+)", css_content)
auteur = match.group(1)

css_cleaned = re.sub(r"/\*\s*==UserStyle==[\s\S]*?==/UserStyle==\s*\*/", "", css_content)
css_cleaned = re.sub(r"@-moz-document\s+domain\([^)]+\)\s*{", "", css_cleaned).strip()
if css_cleaned.endswith("}"):
    css_cleaned = css_cleaned[:-1].strip()

css_cleaned = re.sub(
    r'^ *if\s*\(.*?\)\s*\{\n((?:.*?\n)*?)^\s*\}',
    lambda m: re.sub(r'^\s{4}', '', m.group(1), flags=re.MULTILINE).rstrip(),
    css_cleaned,
    flags=re.MULTILINE
)

css_lines = css_cleaned.splitlines()
if css_lines:
    css_lines[0] = '    ' + css_lines[0]
css_cleaned = "\n".join(css_lines)

js_header = f"""// ==UserScript==
// @name         UI_2023_JVC_JS
// @namespace    UI_2023_JVC_JS
// @version      {version}
// @description  {description}
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
