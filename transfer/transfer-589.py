"""One-time verified byte transfer. Never execute/build CtrlOne or its installers."""
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import time
import urllib.error
import urllib.request

REPO = 'uquicktechnologies-spec/ctrlone_updates'
BRANCH = 'transfer/msi589-verified-bytes'
BASE = '6a79ae0476a33db705a94000c1fc233cd0b05991'
TREE = 'bd521f2674b64fd18d2fc15c9467938646e4e971'
SOURCE = '68a56c3ca87e6c1cca7dd0dbd6e2c8e53a9797eb'
VERSION, CHUNK = '1.3.589', 4 * 1024 * 1024
MSI, EXE = 'CtrlOne-Setup-UNSIGNED-LAB-v1.3.589.msi', 'CtrlOne-Setup-UNSIGNED-LAB.exe'
FILES = {
    MSI: (29188096, 'ded8d950d7e1e770c767d39b5e441ec37e25a482fe8b0bac0f659b476220dc7b', '33b6e5fe309cc4f862b25831740e41868b6e0f0d'),
    EXE: (38706176, 'febe59f5f6619c9212949806d3753d502fc275738373b6a6cc2c807ca5a47d9e', 'd4f2cf444d845fd2fb7fc482624a4799b94f3839'),
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw): return hashlib.sha256(raw).hexdigest()
def blob(raw): return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
def unique(rows):
    result = {}
    for key, value in rows:
        require(key not in result, 'Duplicate JSON key')
        result[key] = value
    return result


def local(root, name, limit):
    require(re.fullmatch(r'transfer/(?:manifest\.json|README\.md|chunks/[a-z0-9_-]+\.bin)', name), 'Unexpected transfer path')
    path = root / name
    require(path.resolve(strict=True) == path and stat.S_ISREG(path.lstat().st_mode), 'Physical transfer file required')
    with path.open('rb') as stream:
        raw = stream.read(limit + 1)
    require(len(raw) <= limit, 'Transfer file exceeds bound')
    return raw


def reconstruct(root):
    manifest = json.loads(local(root, 'transfer/manifest.json', 128 * 1024), object_pairs_hook=unique)
    require([manifest.get(k) for k in ('schemaVersion', 'version', 'repository', 'branch', 'baseCommit', 'baseTree', 'sourceCommit')]
            == [1, VERSION, REPO, BRANCH, BASE, TREE, SOURCE], 'Manifest identity differs')
    require(len(manifest['files']) == 2 and {r['path'] for r in manifest['files']} == set(FILES), 'Exact MSI and EXE required')
    result, seen = {}, set()
    for row in manifest['files']:
        name, parts, offset = row['path'], [], 0
        require((row['bytes'], row['sha256'], row['gitBlob']) == FILES[name], 'Whole-file pins differ')
        require(len(row['chunks']) == (row['bytes'] + CHUNK - 1) // CHUNK, 'Chunk count differs')
        for part in row['chunks']:
            require(part['path'] not in seen and part['file'] == name and part['offset'] == offset and
                    part['bytes'] == min(CHUNK, row['bytes'] - offset), 'Chunk identity/order differs')
            seen.add(part['path'])
            raw = local(root, part['path'], CHUNK)
            require(len(raw) == part['bytes'] and sha(raw) == part['sha256'] and blob(raw) == part['gitBlob'], 'Chunk bytes differ')
            parts.append(raw)
            offset += len(raw)
        raw = b''.join(parts)
        require((len(raw), sha(raw), blob(raw)) == FILES[name], 'Reconstructed installer differs')
        result[name] = raw
    row = manifest['readme']
    require(row['path'] == 'transfer/README.md' and 0 < row['bytes'] <= 64 * 1024, 'README identity differs')
    raw = local(root, row['path'], 64 * 1024)
    require(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'README bytes differ')
    raw.decode('utf-8')
    return result, raw


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs): raise ValueError('API redirect refused')


class API:
    def __init__(self, token):
        require(bool(token), 'Repository job token required')
        self.token, self.opener = token, urllib.request.build_opener(NoRedirect())

    def __call__(self, method, route, value=None):
        require(route.startswith('/git/') and not any(c in route for c in '\r\n#'), 'Unexpected API route')
        body = None if value is None else json.dumps(value, separators=(',', ':')).encode()
        request = urllib.request.Request('https://api.github.com/repos/' + REPO + route, data=body, method=method,
            headers={'Authorization': 'Bearer ' + self.token, 'Accept': 'application/vnd.github+json',
                     'Content-Type': 'application/json', 'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'CtrlOne-verified-transfer-589'})
        for attempt in range(2 if method != 'PATCH' else 1):
            try:
                with self.opener.open(request, timeout=120) as response:
                    raw = response.read((2 << 20) + 1)
                require(len(raw) <= 2 << 20, 'API response exceeds bound')
                return json.loads(raw, object_pairs_hook=unique)
            except urllib.error.HTTPError as error:
                if error.code not in (429, 500, 502, 503, 504) or method == 'PATCH' or attempt == 1:
                    raise RuntimeError('GitHub API HTTP ' + str(error.code)) from None
            except (urllib.error.URLError, TimeoutError):
                if method == 'PATCH' or attempt == 1: raise RuntimeError('GitHub API transport failed') from None
            time.sleep(2)


def publish(api, files, readme):
    def main():
        value = api('GET', '/git/ref/heads/main')
        require(value['ref'] == 'refs/heads/main' and value['object']['type'] == 'commit', 'Main ref differs')
        return value['object']['sha']
    def entries(tree):
        value = api('GET', '/git/trees/' + tree + '?recursive=1')
        require(value['sha'] == tree and value.get('truncated') is False, 'Complete tree required')
        rows = {r['path']: (r['mode'], r['type'], r['sha']) for r in value['tree']}
        require(len(rows) == len(value['tree']), 'Duplicate tree path')
        return rows
    def tree(base, replacements):
        expected = entries(base) | {name: ('100644', 'blob', key) for name, key in replacements.items()}
        value = api('POST', '/git/trees', {'base_tree': base, 'tree': [
            {'path': name, 'mode': '100644', 'type': 'blob', 'sha': key} for name, key in replacements.items()]})
        require(entries(value['sha']) == expected, 'Tree did not preserve existing files')
        return value['sha']
    def commit(parent, tree_id, message):
        value = api('POST', '/git/commits', {'message': message, 'tree': tree_id, 'parents': [parent]})
        require(value['tree']['sha'] == tree_id and [p['sha'] for p in value['parents']] == [parent], 'Commit identity differs')
        return value['sha']
    def upload(raw):
        value = api('POST', '/git/blobs', {'content': base64.b64encode(raw).decode('ascii'), 'encoding': 'base64'})
        require(value['sha'] == blob(raw), 'Uploaded blob identity differs')
        return value['sha']
    require(main() == BASE and api('GET', '/git/commits/' + BASE)['tree']['sha'] == TREE, 'Main moved; refusing publication')
    original = entries(TREE)
    alias = 'CtrlOne-Setup-UNSIGNED-LAB-v' + VERSION + '.exe'
    require(MSI not in original and alias not in original, 'Immutable version already exists')
    artifacts = {name: upload(raw) for name, raw in files.items()}
    artifacts[alias] = artifacts[EXE]
    artifact_tree = tree(TREE, artifacts)
    artifact_commit = commit(BASE, artifact_tree, 'Add verified CtrlOne 1.3.589 unsigned test installer bytes')
    raw_base = 'https://raw.githubusercontent.com/' + REPO + '/' + artifact_commit + '/'
    feed = {'schemaVersion': 1, 'product': 'CtrlOne Intelligence Ai+', 'channel': 'manual-test', 'buildFlavor': 'unsigned-lab',
            'manualOnly': True, 'architecture': 'x64', 'version': VERSION, 'sourceCommit': SOURCE, 'artifactCommit': artifact_commit,
            'msiUrl': raw_base + MSI, 'sha256': FILES[MSI][1], 'sizeBytes': FILES[MSI][0],
            'setupUrl': raw_base + EXE, 'setupSha256': FILES[EXE][1], 'setupSizeBytes': FILES[EXE][0]}
    metadata = {'latest-test.json': (json.dumps(feed, indent=2) + '\n').encode(), 'README.md': readme,
                'SHA256SUMS.txt': ''.join(FILES[name][1] + '  ' + name + '\n' for name in (MSI, EXE)).encode()}
    catalog_tree = tree(artifact_tree, {name: upload(raw) for name, raw in metadata.items()})
    catalog_commit = commit(artifact_commit, catalog_tree, 'Publish verified CtrlOne 1.3.589 explicit test catalog')
    require(main() == BASE, 'Main moved; refusing ref update')
    try: api('PATCH', '/git/refs/heads/main', {'sha': catalog_commit, 'force': False})
    except RuntimeError:
        require(main() == catalog_commit, 'Ref update unconfirmed; inspect main before retrying')
    require(main() == catalog_commit, 'Published main was not confirmed')
    print(json.dumps({'status': 'PUBLISHED_VERIFIED_589_TEST_BYTES', 'artifactCommit': artifact_commit, 'feedCommit': catalog_commit,
                      'files': {name: {'bytes': pin[0], 'sha256': pin[1], 'gitBlob': pin[2]} for name, pin in FILES.items()}}))


def main():
    require(os.environ.get('GITHUB_REPOSITORY') == REPO and os.environ.get('GITHUB_EVENT_NAME') == 'push' and
            os.environ.get('GITHUB_REF') == 'refs/heads/' + BRANCH, 'Only the fixed repository transfer branch may run')
    files, readme = reconstruct(Path.cwd().resolve())
    publish(API(os.environ.get('GITHUB_TOKEN')), files, readme)


if __name__ == '__main__': main()
