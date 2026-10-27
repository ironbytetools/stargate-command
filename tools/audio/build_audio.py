import subprocess, base64, os, sys, json
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
src = os.path.join(root, 'Game Soundtrack')
tracks = [
    ('title', '(Disk 1) 01 - (Main Title) Season 1 - Radim Sebesta (192k).mp3'),
    ('enemy', '(Disk 1) 03 - The Enemy Within (Suite) - Radim Sebesta (192k).mp3'),
    ('emanc', '(Disk 1) 05 - Emancipation (Suite).mp3'),
    ('hathor', '(Disk 1) 09 - Hathor (Suite).mp3'),
    ('credits', '(Disk 1) 12 - (End Credits) - Radim Sebesta (192k).mp3'),
]
work = os.path.expanduser('~/aenc')
os.makedirs(work, exist_ok=True)
data = {}
for key, name in tracks:
    out = os.path.join(work, key + '.mp3')
    if not os.path.exists(out):
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', os.path.join(src, name), '-af', 'loudnorm=I=-18:LRA=11:TP=-1.5', '-ar', '44100', '-ac', '2', '-b:a', '64k', out], check=True)
    data[key] = base64.b64encode(open(out, 'rb').read()).decode()
sfxd = {}
sd = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sfx')
for fn in sorted(os.listdir(sd)):
    if fn.endswith('.mp3'):
        sfxd[fn[:-4]] = base64.b64encode(open(os.path.join(sd, fn), 'rb').read()).decode()
base, dst = sys.argv[1], sys.argv[2]
html = open(base, encoding='utf-8').read()
marker = '<script>\n'
i = html.index(marker)
block = '<script>const AUDIO_DATA=' + json.dumps(data) + ';</script>\n'
html = html[:i] + block + html[i:]
open(dst, 'w', encoding='utf-8').write(html)
print(os.path.getsize(dst))
