# hozon.json の shared:true のページを PDF にして AGILE_共有 へ保存（ソースが新しいときだけ書き直す）
import json, os, re, shutil, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.expanduser("~/Library/CloudStorage/GoogleDrive-mm738966m@gmail.com/マイドライブ/AGILE_共有")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
build = open(os.path.join(H, "build.mjs")).read()
src_of = {o: s for s, o in re.findall(r"src: '([^']+)', out: '([^']+)'", build)}
for p in json.load(open(os.path.join(H, "hozon.json")))["pages"]:
    if not p.get("shared"):
        continue
    src = os.path.join(H, src_of[p["out"]])
    name = ("" if p.get("prefix") is False else "(森川)") + p["name"] + ".pdf"
    dst = os.path.join(ROOT, p["folder"], name)
    if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        continue
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    tmp = os.path.join(H, os.path.dirname(p["out"]), "_print.html")   # 画像の相対パスを合わせる
    shutil.copy(src, tmp)
    try:
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=8000",
                        "--print-to-pdf=" + dst, "file://" + tmp], capture_output=True, timeout=120)
    finally:
        os.remove(tmp)
    print("保存:", os.path.relpath(dst, ROOT))
