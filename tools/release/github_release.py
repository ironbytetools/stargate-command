import json
import os
import sys
import urllib.request

repo = 'ironbytetools/stargate-command'
tag, title, notes_file = sys.argv[1:4]
assets = sys.argv[4:]
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
token = open(os.path.join(root, '.release-token')).read().strip()
head = {'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'sgc-release'}


def call(url, data=None, extra=None, method=None):
    h = dict(head)
    h.update(extra or {})
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read().decode())


body = json.dumps({'tag_name': tag, 'name': title, 'body': open(notes_file, encoding='utf-8').read(), 'draft': False, 'prerelease': False}).encode()
rel = call('https://api.github.com/repos/' + repo + '/releases', body, {'Content-Type': 'application/json'})
print('release', rel['html_url'])
up = rel['upload_url'].split('{')[0]
for a in assets:
    name = os.path.basename(a)
    ctype = 'application/pdf' if name.endswith('.pdf') else 'application/zip' if name.endswith('.zip') else 'text/html'
    try:
        res = call(up + '?name=' + name, open(a, 'rb').read(), {'Content-Type': ctype})
        print('asset', res['name'], res['size'])
    except Exception as e:
        print('asset not uploaded', name, e)
