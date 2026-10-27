set -e
cd /tmp/guide
python3 build_guide.py >/dev/null
NODE_PATH=$(npm root -g) node pdf.js
python3 - <<'PY'
import subprocess,json,re
from pypdf import PdfReader
n=len(PdfReader('guide.pdf').pages)
pages={}
for i in range(1,n+1):
    t=subprocess.run(['pdftotext','-f',str(i),'-l',str(i),'guide.pdf','-'],capture_output=True,text=True).stdout
    for g in re.findall(r'SECTION (\d\d)',t):
        pages.setdefault(str(int(g)),i)
json.dump(pages,open('toc_pages.json','w'));print(n,pages)
PY
