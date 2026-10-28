"""Prepared signed artifact transfer. No product, installer, DLL or build execution.

This template refuses operation until final QA, package, metadata and fresh
public baseline pins are bound by the separate reviewed preparation command.
It never changes a feed or an existing repository path.
"""
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
BRANCH = 'transfer/signed593-reviewed-artifacts'
VERSION = '1.3.593'
SOURCE = 'b35d4a68b7827e6485f4379afb47660af9d520ee'
SOURCE_TREE = 'da0c6f4ad0ab25fbffcdcd7b4bb092a7f3698cd8'
REVIEWED_HEAD = '849096285e82fe55dd5c90f73f2fd40261406e97'
THUMBPRINT = 'D42CAA418BFE1A1B402577DC8D7C34E80BB4DE8A'
PUBLISHER = 'UQuick Technologies India Limited'
BASE = 'ca3f0971bf52db216de6698fe643a9f86b4c3400'
TREE = '0e29a85f6d67199fc19c01c29b150dd7f929253d'
QA_SHA256 = 'de079af2bff41862a936515a5cc907b89cd412060aa1480892b28a22a95117ea'
SIGNATURES_SHA256 = 'db623de7d87e89825b2dc235754c6e1a4cda8b7b5eebaf0685d39ea90e2ab89a'
SOURCE_ADMISSION_SHA256 = '9fe3007366c47e29f1c159fa8b29c59a43a150b4bdbba5b27442325078bc2ff4'
ROOT_REVIEWED_QA = True
FILES = {'CtrlOne-Setup-v1.3.593.msi': (29372416, '9b4228ba8fae1c354fd1fbb2e3ae6431007a381d6fe83ff0c5026bad56164bc4', '43fc577f368fe8601f8470dc5c0b5efb8bd85d97'), 'CtrlOne-Setup-v1.3.593.exe': (32854528, '4cefb7c7fc4042ea5b9ea7b49c308703967084d7677fbde6e57ced8bce843471', '9136c70ce258842ab3709c35f2262ba890a091d4')}
README_PIN = (1244, '835d13c67d17c9558ada65d7165ae18e52703dc812e14c8fdd13a518bf0e6baa')
MSI = 'CtrlOne-Setup-v1.3.593.msi'
EXE = 'CtrlOne-Setup-v1.3.593.exe'
README = 'CtrlOne-v1.3.593-README.md'
SUMS = 'CtrlOne-v1.3.593-SHA256SUMS.txt'
CATALOG = 'CtrlOne-v1.3.593-artifacts.json'
TARGETS = {MSI, EXE, README, SUMS, CATALOG}
PROTECTED = {'latest.json', 'latest-test.json', 'downloads.json', 'latest-manual-signed.json', 'README.md', 'SHA256SUMS.txt', 'CtrlOne-Setup-UNSIGNED-LAB.exe'}
CHUNK = 4 * 1024 * 1024


def require(ok, message):
    if not ok: raise ValueError(message)


def sha(raw): return hashlib.sha256(raw).hexdigest()
def blob(raw): return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
def encode(value): return (json.dumps(value, indent=2) + '\n').encode()
def hex40(value): return type(value) is str and re.fullmatch('[a-f0-9]{40}', value)
def hex64(value): return type(value) is str and re.fullmatch('[a-f0-9]{64}', value)


def unique(rows):
    value = {}
    for key, item in rows:
        require(key not in value, 'Duplicate JSON key refused')
        value[key] = item
    return value


def validate_pins():
    require(ROOT_REVIEWED_QA is True and all(hex40(key) for key in (BASE, TREE, SOURCE, SOURCE_TREE, REVIEWED_HEAD)) and
            all(hex64(key) for key in (QA_SHA256, SIGNATURES_SHA256, SOURCE_ADMISSION_SHA256)),
            'Final reviewed production QA and fresh public baseline are unbound; preparation only')
    require(isinstance(FILES, dict) and set(FILES) == {MSI, EXE}, 'Exact versioned signed MSI/EXE required')
    for pin in FILES.values():
        require(isinstance(pin, (list, tuple)) and len(pin) == 3 and type(pin[0]) is int and 0 < pin[0] < 100 * 1024 * 1024 and
                hex64(pin[1]) and hex40(pin[2]), 'Complete actual signed-file pins required')
    require(isinstance(README_PIN, (list, tuple)) and len(README_PIN) == 2 and type(README_PIN[0]) is int and
            0 < README_PIN[0] <= 65536 and hex64(README_PIN[1]), 'Reviewed versioned README pin required')
    require(not TARGETS & PROTECTED, 'A protected feed or existing alias cannot be a target')


def local(root, name, cap):
    require(re.fullmatch(r'transfer/(?:manifest\.json|README\.md|chunks/(?:msi|exe)-[0-9]{3}\.bin)', name), 'Unexpected transfer path')
    path = root / name
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        require(not stat.S_ISLNK(info.st_mode) and not getattr(info, 'st_file_attributes', 0) & 0x400, 'Reparse transfer input refused')
    require(path.resolve(strict=True) == path and stat.S_ISREG(path.lstat().st_mode), 'Ordinary physical transfer file required')
    with path.open('rb') as stream: raw = stream.read(cap + 1)
    require(len(raw) <= cap, 'Transfer input exceeds bound')
    return raw


def reconstruct(root):
    validate_pins()
    manifest = json.loads(local(root, 'transfer/manifest.json', 131072).decode('utf-8'), object_pairs_hook=unique)
    expected = {'schemaVersion': 1, 'version': VERSION, 'repository': REPO, 'branch': BRANCH,
                'baseCommit': BASE, 'baseTree': TREE, 'sourceCommit': SOURCE, 'sourceTree': SOURCE_TREE,
                'reviewedHead': REVIEWED_HEAD, 'packageQASha256': QA_SHA256, 'signaturesSha256': SIGNATURES_SHA256,
                'sourceAdmissionSha256': SOURCE_ADMISSION_SHA256,
                'certificateThumbprint': THUMBPRINT, 'publisher': PUBLISHER}
    require(all(type(manifest.get(key)) is type(value) and manifest[key] == value for key, value in expected.items()), 'Manifest authority differs')
    require(set(manifest) == set(expected) | {'files', 'readme'}, 'Unexpected manifest fields')
    require(type(manifest['files']) is list and len(manifest['files']) == 2 and {row['path'] for row in manifest['files']} == set(FILES), 'Exact versioned artifacts required')
    result, seen = {}, set()
    for row in manifest['files']:
        name, offset, parts = row['path'], 0, []
        require((row['bytes'], row['sha256'], row['gitBlob']) == tuple(FILES[name]) and type(row['bytes']) is int, 'Whole artifact pins differ')
        require(len(row['chunks']) == (row['bytes'] + CHUNK - 1) // CHUNK, 'Chunk count differs')
        prefix = 'msi' if name == MSI else 'exe'
        for index, part in enumerate(row['chunks']):
            expected_path = 'transfer/chunks/' + prefix + '-' + str(index).zfill(3) + '.bin'
            require(part['path'] == expected_path and part['path'] not in seen and part['file'] == name and
                    type(part['offset']) is int and part['offset'] == offset and type(part['bytes']) is int and
                    part['bytes'] == min(CHUNK, row['bytes'] - offset), 'Chunk identity/order/size differs')
            seen.add(part['path'])
            raw = local(root, part['path'], CHUNK)
            require(len(raw) == part['bytes'] and sha(raw) == part['sha256'] and blob(raw) == part['gitBlob'], 'Chunk digest differs')
            parts.append(raw); offset += len(raw)
        raw = b''.join(parts)
        require((len(raw), sha(raw), blob(raw)) == tuple(FILES[name]), 'Reconstructed signed artifact differs')
        result[name] = raw
    row = manifest['readme']
    require(row['path'] == 'transfer/README.md' and (row['bytes'], row['sha256']) == tuple(README_PIN), 'README authority differs')
    readme = local(root, row['path'], 65536)
    require((len(readme), sha(readme)) == tuple(README_PIN), 'README bytes differ')
    readme.decode('utf-8')
    return result, readme


def build_catalog(artifact_commit):
    validate_pins(); require(hex40(artifact_commit), 'Immutable artifact commit required')
    prefix = 'https://raw.githubusercontent.com/' + REPO + '/' + artifact_commit + '/'
    return {'schemaVersion': 1, 'product': 'CtrlOne Intelligence Ai+', 'version': VERSION,
            'kind': 'signed-installer-artifact-catalog', 'automaticUpdateFeed': False,
            'sourceCommit': SOURCE, 'sourceTree': SOURCE_TREE, 'reviewedHead': REVIEWED_HEAD,
            'artifactCommit': artifact_commit, 'packageQASha256': QA_SHA256, 'signaturesSha256': SIGNATURES_SHA256,
            'sourceAdmissionSha256': SOURCE_ADMISSION_SHA256,
            'publisher': PUBLISHER, 'certificateThumbprint': THUMBPRINT, 'publisherAndTimestampVerified': True,
            'runtimeAndUpgradeAcceptance': 'NOT_RUN', 'releaseAccepted': False,
            'files': [{'name': name, 'url': prefix + name, 'bytes': FILES[name][0], 'sha256': FILES[name][1], 'gitBlob': FILES[name][2]}
                      for name in (MSI, EXE)]}


def metadata(artifact_commit, readme):
    require((len(readme), sha(readme)) == tuple(README_PIN), 'Reviewed metadata README changed')
    return {README: readme, SUMS: ''.join(FILES[name][1] + '  ' + name + '\n' for name in (MSI, EXE)).encode(),
            CATALOG: encode(build_catalog(artifact_commit))}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs): raise ValueError('GitHub API redirect refused')


class API:
    def __init__(self, token):
        require(bool(token), 'Repository job token required')
        self.token, self.opener = token, urllib.request.build_opener(NoRedirect())

    def __call__(self, method, route, value=None):
        require(route.startswith('/git/') and not any(c in route for c in '\r\n#'), 'Unexpected Git Data API route')
        require(method in ('GET', 'POST', 'PATCH'), 'Unexpected API method')
        body = None if value is None else json.dumps(value, separators=(',', ':')).encode()
        request = urllib.request.Request('https://api.github.com/repos/' + REPO + route, data=body, method=method,
            headers={'Authorization': 'Bearer ' + self.token, 'Accept': 'application/vnd.github+json',
                     'Content-Type': 'application/json', 'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'CtrlOne-signed-artifact-transfer-593'})
        for attempt in range(1 if method == 'PATCH' else 2):
            try:
                with self.opener.open(request, timeout=120) as response: raw = response.read((2 << 20) + 1)
                require(len(raw) <= 2 << 20, 'API response exceeds bound')
                return json.loads(raw.decode('utf-8'), object_pairs_hook=unique)
            except urllib.error.HTTPError as error:
                if error.code not in (429, 500, 502, 503, 504) or method == 'PATCH' or attempt == 1:
                    raise RuntimeError('GitHub API HTTP ' + str(error.code)) from None
            except (urllib.error.URLError, TimeoutError):
                if method == 'PATCH' or attempt == 1: raise RuntimeError('GitHub API transport failed') from None
            time.sleep(2)


def publish(api, files, readme):
    validate_pins()
    require(set(files) == set(FILES) and all((len(raw), sha(raw), blob(raw)) == tuple(FILES[name]) for name, raw in files.items()), 'Pre-upload artifact bytes differ')
    require((len(readme), sha(readme)) == tuple(README_PIN), 'Pre-upload README differs')
    def main():
        value = api('GET', '/git/ref/heads/main')
        require(value['ref'] == 'refs/heads/main' and value['object']['type'] == 'commit' and hex40(value['object']['sha']), 'Main ref differs')
        return value['object']['sha']
    def entries(tree):
        value = api('GET', '/git/trees/' + tree + '?recursive=1')
        require(value['sha'] == tree and value.get('truncated') is False and type(value['tree']) is list, 'Complete Git tree required')
        rows = {row['path']: (row['mode'], row['type'], row['sha']) for row in value['tree']}
        require(len(rows) == len(value['tree']), 'Duplicate Git tree path')
        return rows
    def tree(base, additions):
        original = entries(base)
        require(set(additions) <= TARGETS and not set(additions) & set(original), 'Immutable versioned target exists')
        expected = original | {name: ('100644', 'blob', key) for name, key in additions.items()}
        value = api('POST', '/git/trees', {'base_tree': base, 'tree': [
            {'path': name, 'mode': '100644', 'type': 'blob', 'sha': key} for name, key in additions.items()]})
        require(hex40(value['sha']) and entries(value['sha']) == expected, 'Tree changed an unrelated existing path')
        return value['sha']
    def commit(parent, tree_id, message):
        value = api('POST', '/git/commits', {'message': message, 'tree': tree_id, 'parents': [parent]})
        require(hex40(value['sha']) and value['tree']['sha'] == tree_id and [p['sha'] for p in value['parents']] == [parent], 'Commit lineage differs')
        return value['sha']
    def upload(raw):
        value = api('POST', '/git/blobs', {'content': base64.b64encode(raw).decode('ascii'), 'encoding': 'base64'})
        require(value['sha'] == blob(raw), 'Uploaded Git blob differs')
        return value['sha']
    require(main() == BASE and api('GET', '/git/commits/' + BASE)['tree']['sha'] == TREE, 'Main moved; obtain a fresh reviewed baseline')
    original = entries(TREE)
    require(not TARGETS & set(original), 'Immutable versioned path already exists')
    artifact_tree = tree(TREE, {name: upload(files[name]) for name in (MSI, EXE)})
    artifact_commit = commit(BASE, artifact_tree, 'Add verified signed CtrlOne 1.3.593 installer artifacts')
    meta = metadata(artifact_commit, readme)
    catalog_tree = tree(artifact_tree, {name: upload(raw) for name, raw in meta.items()})
    catalog_commit = commit(artifact_commit, catalog_tree, 'Add immutable CtrlOne 1.3.593 artifact documentation; preserve all update feeds')
    final = entries(catalog_tree)
    require({key: final[key] for key in original} == original and set(final) - set(original) == TARGETS, 'Publication plan changed existing files')
    require(main() == BASE, 'Main moved; refusing the ref update')
    try: api('PATCH', '/git/refs/heads/main', {'sha': catalog_commit, 'force': False})
    except RuntimeError:
        require(main() == catalog_commit, 'Ref result unconfirmed; inspect main before any retry')
    require(main() == catalog_commit, 'Published main was not confirmed')
    result = {'status': 'PUBLISHED_VERIFIED_SIGNED_593_ARTIFACTS_ONLY', 'repository': REPO, 'version': VERSION,
              'baseCommit': BASE, 'baseTree': TREE, 'artifactCommit': artifact_commit, 'artifactTree': artifact_tree,
              'catalogCommit': catalog_commit, 'catalogTree': catalog_tree, 'sourceCommit': SOURCE, 'sourceTree': SOURCE_TREE,
              'packageQASha256': QA_SHA256, 'signaturesSha256': SIGNATURES_SHA256,
              'sourceAdmissionSha256': SOURCE_ADMISSION_SHA256,
              'files': {name: {'bytes': pin[0], 'sha256': pin[1], 'gitBlob': pin[2]} for name, pin in FILES.items()},
              'newPaths': {name: final[name][2] for name in sorted(TARGETS)},
              'feedsChanged': False, 'unrelatedExistingFilesChanged': False, 'installerExecuted': False,
              'runtimeAndUpgradeAcceptance': 'NOT_RUN', 'customerAutomaticUpdatePublished': False}
    return result


def rollback_plan(receipt, current_head, current_tree, readme):
    """Return a review-only fast-forward rollback plan; never issue API writes."""
    validate_pins()
    require(receipt.get('status') == 'PUBLISHED_VERIFIED_SIGNED_593_ARTIFACTS_ONLY' and receipt.get('baseCommit') == BASE and
            receipt.get('baseTree') == TREE and receipt.get('sourceCommit') == SOURCE and receipt.get('sourceTree') == SOURCE_TREE and
            receipt.get('packageQASha256') == QA_SHA256 and receipt.get('signaturesSha256') == SIGNATURES_SHA256 and
            receipt.get('sourceAdmissionSha256') == SOURCE_ADMISSION_SHA256 and receipt.get('feedsChanged') is False,
            'Rollback receipt is not this bound publication')
    require(current_head == receipt.get('catalogCommit') and current_tree == receipt.get('catalogTree') and hex40(current_head) and hex40(current_tree),
            'Main moved after publication; automatic rollback planning refused')
    require(hex40(receipt.get('artifactCommit')), 'Rollback immutable artifact commit differs')
    expected_paths = {name: blob(raw) for name, raw in metadata(receipt['artifactCommit'], readme).items()} | {name: pin[2] for name, pin in FILES.items()}
    require(receipt.get('newPaths') == expected_paths, 'Rollback path/blob inventory differs')
    return {'status': 'REVIEW_ONLY_NO_MUTATION', 'expectedCurrentHead': current_head, 'parentOfNewRollbackCommit': current_head,
            'desiredTree': TREE, 'removeOnlyPaths': receipt['newPaths'], 'forceRefUpdate': False,
            'preserveCommitHistoryAndImmutableArtifactUrls': True, 'requiresFreshTreeAndRefVerification': True,
            'executed': False}


def main():
    validate_pins()
    require(os.environ.get('GITHUB_REPOSITORY') == REPO and os.environ.get('GITHUB_EVENT_NAME') == 'push' and
            os.environ.get('GITHUB_REF') == 'refs/heads/' + BRANCH and hex40(os.environ.get('GITHUB_SHA')),
            'Only the fixed checked-out repository push branch may run')
    files, readme = reconstruct(Path.cwd().resolve())
    print(json.dumps(publish(API(os.environ.get('GITHUB_TOKEN')), files, readme)))


if __name__ == '__main__': main()
