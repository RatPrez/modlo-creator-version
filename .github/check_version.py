import json
import re
import sys

SEMVER = re.compile(r'^\d+\.\d+\.\d+$')
DATE = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def fail(msg):
    print(f'version.json: {msg}')
    sys.exit(1)


def key(v):
    return tuple(int(x) for x in v.split('.'))


with open(sys.argv[1], encoding='utf-8') as f:
    try:
        doc = json.load(f)
    except json.JSONDecodeError as e:
        fail(f'not valid JSON: {e}')

if not isinstance(doc, dict):
    fail('the top level must be an object')
latest = doc.get('latest')
if not isinstance(latest, str) or not SEMVER.match(latest):
    fail('"latest" must be a version like "1.2.3"')
url = doc.get('download_url')
if not isinstance(url, str) or not url.startswith('https://'):
    fail('"download_url" must be an https:// address')
log = doc.get('changelog')
if not isinstance(log, list) or not log:
    fail('"changelog" must be a list with at least one entry')
prev = None
for i, e in enumerate(log):
    if not isinstance(e, dict):
        fail(f'changelog entry {i + 1} must be an object')
    v = e.get('version')
    if not isinstance(v, str) or not SEMVER.match(v):
        fail(f'changelog entry {i + 1}: "version" must be like "1.2.3"')
    if not isinstance(e.get('date'), str) or not DATE.match(e['date']):
        fail(f'changelog {v}: "date" must be like "2026-10-16"')
    ch = e.get('changes')
    if not isinstance(ch, list) or not ch or not all(isinstance(c, str) and c.strip() for c in ch):
        fail(f'changelog {v}: "changes" must be a list of non-empty strings')
    if prev is not None and key(v) >= key(prev):
        fail(f'changelog {v} must be older than {prev} above it (newest first)')
    prev = v
if log[0]['version'] != latest:
    fail(f'"latest" is {latest} but the first changelog entry is {log[0]["version"]}')
print(f'ok: latest {latest}, {len(log)} changelog entries')
