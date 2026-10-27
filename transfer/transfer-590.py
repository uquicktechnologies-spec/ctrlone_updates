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
BRANCH = 'transfer/msi590-verified-bytes'
BASE = 'be744eacedec5c0d82b958b3546810660ece8ccf'
TREE = '7406f0d10a1915b6b76865b7428626d29a62fd2f'
SOURCE = '0a8435d6091e2b23a631b3488a8e5d4686ba9718'
SOURCE_TREE = 'aec9459b7f1267908c4e2dca6fce72e5ba92d573'
QA_SHA256 = '821c183ba1be0ced1793f236cff2758228a05ecb2a7410a0cd6d0da12d93fd3c'
ROOT_REVIEWED_QA = True
README_PIN = (6569, '6363e49649da57d016be38de4d7c17d3f69e550d4c4e03a1c1e825d7cb19c303')
VERSION, CHUNK = '1.3.590', 4 * 1024 * 1024
MSI, EXE = 'CtrlOne-Setup-UNSIGNED-LAB-v1.3.590.msi', 'CtrlOne-Setup-UNSIGNED-LAB.exe'
FILES = {'CtrlOne-Setup-UNSIGNED-LAB-v1.3.590.msi': (29229056, '4edfa4ce26b3e91cef9be707257408fc81aa989df94c4c6701d18be48e73be83', '9c6e7d6677d9249b2d12fb4d516460df96cc4acc'), 'CtrlOne-Setup-UNSIGNED-LAB.exe': (38794240, 'a94170b8f731018bdfd8b325024622494fbd5f394367cdcc314e39f6f4aa4617', 'e4104a7a96306f66e862a306604f4323c2122588')}


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


def validate_pins():
    require(ROOT_REVIEWED_QA is True and re.fullmatch('[a-f0-9]{40}', SOURCE) and
            re.fullmatch('[a-f0-9]{40}', SOURCE_TREE) and re.fullmatch('[a-f0-9]{64}', QA_SHA256),
            'Final root-reviewed package QA is not bound; preparation only')
    require(isinstance(README_PIN, (list, tuple)) and len(README_PIN) == 2 and type(README_PIN[0]) is int and
            0 < README_PIN[0] <= 64 * 1024 and re.fullmatch('[a-f0-9]{64}', README_PIN[1]), 'Root-reviewed README pin required')
    require(re.fullmatch('[a-f0-9]{40}', BASE) and re.fullmatch('[a-f0-9]{40}', TREE), 'Exact public baseline required')
    require(isinstance(FILES, dict) and set(FILES) == {MSI, EXE}, 'Exact verified MSI/EXE pins required')
    for pin in FILES.values():
        require(isinstance(pin, (list, tuple)) and len(pin) == 3 and type(pin[0]) is int and 0 < pin[0] < 100 * 1024 * 1024 and
                re.fullmatch('[a-f0-9]{64}', pin[1]) and re.fullmatch('[a-f0-9]{40}', pin[2]), 'Complete package pins required')


def local(root, name, limit):
    require(re.fullmatch(r'transfer/(?:manifest\.json|README\.md|chunks/[a-z0-9_-]+\.bin)', name), 'Unexpected transfer path')
    path = root / name
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        require(not stat.S_ISLNK(info.st_mode) and not getattr(info, 'st_file_attributes', 0) & 0x400, 'Reparse transfer path refused')
    require(path.resolve(strict=True) == path and stat.S_ISREG(path.lstat().st_mode), 'Physical transfer file required')
    with path.open('rb') as stream:
        raw = stream.read(limit + 1)
    require(len(raw) <= limit, 'Transfer file exceeds bound')
    return raw


def reconstruct(root):
    validate_pins()
    manifest = json.loads(local(root, 'transfer/manifest.json', 128 * 1024), object_pairs_hook=unique)
    require([manifest.get(k) for k in ('schemaVersion', 'version', 'repository', 'branch', 'baseCommit', 'baseTree', 'sourceCommit')]
            == [1, VERSION, REPO, BRANCH, BASE, TREE, SOURCE], 'Manifest identity differs')
    require(manifest.get('sourceTree') == SOURCE_TREE and manifest.get('packageQASha256') == QA_SHA256,
            'Manifest final source/package QA differs')
    require(len(manifest['files']) == 2 and {r['path'] for r in manifest['files']} == set(FILES), 'Exact MSI and EXE required')
    result, seen = {}, set()
    for row in manifest['files']:
        name, parts, offset = row['path'], [], 0
        require((row['bytes'], row['sha256'], row['gitBlob']) == tuple(FILES[name]), 'Whole-file pins differ')
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
        require((len(raw), sha(raw), blob(raw)) == tuple(FILES[name]), 'Reconstructed installer differs')
        result[name] = raw
    row = manifest['readme']
    require(row['path'] == 'transfer/README.md' and 0 < row['bytes'] <= 64 * 1024, 'README identity differs')
    require((row['bytes'], row['sha256']) == tuple(README_PIN), 'Root-reviewed README differs')
    raw = local(root, row['path'], 64 * 1024)
    require(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'README bytes differ')
    raw.decode('utf-8')
    return result, raw


def build_feed(artifact_commit):
    validate_pins()
    require(re.fullmatch('[a-f0-9]{40}', artifact_commit), 'Exact artifact commit required')
    raw_base = 'https://raw.githubusercontent.com/' + REPO + '/' + artifact_commit + '/'
    # Exactly the current native ManualTestRelease fields: its decoder rejects
    # unknown fields. Test download information never grants signed install authority.
    return {'schemaVersion': 1, 'product': 'CtrlOne Intelligence Ai+', 'channel': 'manual-test', 'buildFlavor': 'unsigned-lab',
            'manualOnly': True, 'architecture': 'x64', 'version': VERSION, 'sourceCommit': SOURCE, 'artifactCommit': artifact_commit,
            'msiUrl': raw_base + MSI, 'sha256': FILES[MSI][1], 'sizeBytes': FILES[MSI][0],
            'setupUrl': raw_base + EXE, 'setupSha256': FILES[EXE][1], 'setupSizeBytes': FILES[EXE][0]}


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
                     'Content-Type': 'application/json', 'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'CtrlOne-verified-transfer-590'})
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
    validate_pins()
    require(set(files) == set(FILES) and all((len(raw), sha(raw), blob(raw)) == tuple(FILES[name])
            for name, raw in files.items()), 'Pre-upload package bytes differ')
    require((len(readme), sha(readme)) == tuple(README_PIN), 'Pre-upload README differs')
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
    artifact_commit = commit(BASE, artifact_tree, 'Add verified CtrlOne 1.3.590 unsigned test installer bytes')
    feed = build_feed(artifact_commit)
    metadata = {'latest-test.json': (json.dumps(feed, indent=2) + '\n').encode(), 'README.md': readme,
                'SHA256SUMS.txt': ''.join(FILES[name][1] + '  ' + name + '\n' for name in (MSI, EXE)).encode()}
    catalog_tree = tree(artifact_tree, {name: upload(raw) for name, raw in metadata.items()})
    catalog_commit = commit(artifact_commit, catalog_tree, 'Publish verified CtrlOne 1.3.590 explicit test catalog')
    require(main() == BASE, 'Main moved; refusing ref update')
    try: api('PATCH', '/git/refs/heads/main', {'sha': catalog_commit, 'force': False})
    except RuntimeError:
        require(main() == catalog_commit, 'Ref update unconfirmed; inspect main before retrying')
    require(main() == catalog_commit, 'Published main was not confirmed')
    print(json.dumps({'status': 'PUBLISHED_VERIFIED_590_TEST_BYTES', 'artifactCommit': artifact_commit, 'feedCommit': catalog_commit,
                      'sourceCommit': SOURCE, 'sourceTree': SOURCE_TREE, 'packageQASha256': QA_SHA256,
                      'files': {name: {'bytes': pin[0], 'sha256': pin[1], 'gitBlob': pin[2]} for name, pin in FILES.items()}}))


def main():
    validate_pins()
    require(os.environ.get('GITHUB_REPOSITORY') == REPO and os.environ.get('GITHUB_EVENT_NAME') == 'push' and
            os.environ.get('GITHUB_REF') == 'refs/heads/' + BRANCH, 'Only the fixed repository transfer branch may run')
    files, readme = reconstruct(Path.cwd().resolve())
    publish(API(os.environ.get('GITHUB_TOKEN')), files, readme)


if __name__ == '__main__': main()
