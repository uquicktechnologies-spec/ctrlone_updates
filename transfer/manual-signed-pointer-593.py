"""Separate explicit-check pointer preparation/publication; no installer execution.

The template is inert until complete actual public593 byte verification and a
fresh root-reviewed lease are supplied. It never writes automatic-update feeds.
"""
import argparse
import ast
import base64
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import sys
import urllib.request

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = 'uquicktechnologies-spec/ctrlone_updates'
VERSION = '1.3.593'
BRANCH = 'transfer/manual-signed593-reviewed-pointer'
POINTER = 'latest-manual-signed.json'
BASE = '2960173524dd86398ee303c8de180eeabc8f1f9d'
TREE = 'c4eec0dcd78cf0f70933d630059af67194a015eb'
PREVIOUS = '216a2b48d761ab4042dd35708a1f5fef2aa0ec20'
PUBLISHER_SHA256 = 'fa93b1c69309c9f7c6552dd1332019d10878a47b7c612188cacca37027883fbd'
PUBLICATION_SHA256 = 'e4a9a7c0445a2956d7c5fbc29bb7a66b80728810b5b5827e51db1369b499aff1'
VERIFICATION_SHA256 = '34178135d541dba0245bcaab52c5c15d471c82c104a64f1e8ffae634d84af15e'
POINTER_PIN = (366, '9e32cde61d5dfe747370c0d79a214fb72845764ff1319886e1c729ea27d7df58', '0c466546aa4b3b5cb0067e294e0f14a6597a33ba')
ROOT_REVIEWED_PUBLIC_BYTES = True


def require(ok, message):
    if not ok: raise ValueError(message)


def sha(raw): return hashlib.sha256(raw).hexdigest()
def blob(raw): return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
def encode(value): return (json.dumps(value, indent=2) + '\n').encode()
def hex40(value): return type(value) is str and bool(re.fullmatch('[a-f0-9]{40}', value))
def hex64(value): return type(value) is str and bool(re.fullmatch('[a-f0-9]{64}', value))


def unique(rows):
    value = {}
    for name, item in rows:
        require(name not in value, 'Duplicate JSON key refused'); value[name] = item
    return value


def read(path, cap=131072):
    path = Path(path).absolute()
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        require(not stat.S_ISLNK(info.st_mode) and not getattr(info, 'st_file_attributes', 0) & 0x400, 'Reparse/alias input refused')
    require(path.resolve(strict=True) == path and path.is_file(), 'Ordinary physical input required')
    with path.open('rb') as stream: raw = stream.read(cap + 1)
    require(len(raw) <= cap, 'Input exceeds bound'); return raw


def pinned(path, expected, cap=131072):
    require(hex64(expected), 'Externally reviewed exact digest required')
    raw = read(path, cap); require(sha(raw) == expected, 'Reviewed evidence changed'); return raw


def load_publisher(path, expected):
    pinned(path, expected, 65536)
    spec = importlib.util.spec_from_file_location('reviewed_signed593_artifact_publisher', path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    module.validate_pins()
    require(module.REPO == REPO and module.VERSION == VERSION, 'Current593 frozen artifact publisher required')
    return module


def parse_pointer(raw):
    require(len(raw) <= 8192, 'Pointer exceeds native reader bound')
    value = json.loads(raw.decode('utf-8'), object_pairs_hook=unique)
    keys = {'schemaVersion','product','kind','manualOnly','automaticUpdateFeed','version','catalogCommit','catalogSha256','catalogSizeBytes'}
    require(type(value) is dict and set(value) == keys and type(value['schemaVersion']) is int and value['schemaVersion'] == 1 and
            value['product'] == 'CtrlOne Intelligence Ai+' and value['kind'] == 'signed-manual-download-pointer' and
            value['manualOnly'] is True and value['automaticUpdateFeed'] is False and value['version'] == VERSION and
            hex40(value['catalogCommit']) and hex64(value['catalogSha256']) and type(value['catalogSizeBytes']) is int and
            0 < value['catalogSizeBytes'] <= 65536, 'Pointer differs from strict nine-field native schema')
    return value


def checked_evidence(module, publication, verification, readme, verified_directory=None):
    module.validate_pins()
    require(publication.get('status') == 'PUBLISHED_VERIFIED_SIGNED_593_ARTIFACTS_ONLY' and publication.get('repository') == REPO and
            publication.get('version') == VERSION and all(publication.get(key) == getattr(module, attr) for key, attr in (
                ('sourceCommit','SOURCE'),('sourceTree','SOURCE_TREE'),('packageQASha256','QA_SHA256'),
                ('signaturesSha256','SIGNATURES_SHA256'),('sourceAdmissionSha256','SOURCE_ADMISSION_SHA256'))) and
            all(publication.get(key) is False for key in ('feedsChanged','unrelatedExistingFilesChanged','installerExecuted','customerAutomaticUpdatePublished')) and
            publication.get('runtimeAndUpgradeAcceptance') == 'NOT_RUN', 'Current published593 artifact receipt required')
    artifact, catalog = publication.get('artifactCommit'), publication.get('catalogCommit')
    require(hex40(artifact) and hex40(catalog) and hex40(publication.get('catalogTree')), 'Immutable public artifact/catalog identity required')
    require((len(readme),sha(readme)) == tuple(module.README_PIN), 'Reviewed versioned README differs')
    metadata = module.metadata(artifact,readme)
    files = {name:{'bytes':pin[0],'sha256':pin[1],'gitBlob':pin[2]} for name,pin in module.FILES.items()}
    expected_paths = {name:blob(raw) for name,raw in metadata.items()} | {name:pin[2] for name,pin in module.FILES.items()}
    require(publication.get('files') == files and publication.get('newPaths') == expected_paths, 'Published exact five-path plan differs')
    prefix = 'https://raw.githubusercontent.com/'+REPO+'/'
    expected_metadata = [{'url':prefix+catalog+'/'+name,'bytes':len(raw),'sha256':sha(raw),'gitBlob':blob(raw)} for name,raw in metadata.items()]
    expected_downloads = [{'url':prefix+artifact+'/'+name,**files[name]} for name in (module.MSI,module.EXE)]
    require(verification.get('status') == 'PASS_PUBLIC_SIGNED_593_IMMUTABLE_ARTIFACT_BYTES_ONLY' and
            verification.get('artifactCommit') == artifact and verification.get('catalogCommit') == catalog and
            all(verification.get(key) == publication.get(key) for key in ('sourceCommit','sourceTree','packageQASha256','signaturesSha256','sourceAdmissionSha256')) and
            verification.get('metadata') == expected_metadata and verification.get('downloads') == expected_downloads and
            verification.get('method') == 'Complete non-overlapping strict206/Content-Range reads; whole-file SHA256 and Git blob SHA1' and
            verification.get('installerExecuted') is False and verification.get('feedsReadOrChanged') is False and
            verification.get('runtimeAndUpgradeAcceptance') == 'NOT_RUN' and verification.get('customerAutomaticUpdatePublished') is False,
            'Complete reviewed immutable public593 bytes must pass before manual-pointer preparation')
    if verified_directory is not None:
        directory = Path(verified_directory)
        for name,raw in metadata.items(): require(read(directory/name,65536) == raw, 'Verified local public metadata changed')
        for name,pin in module.FILES.items():
            raw = read(directory/name,100*1024*1024-1)
            require((len(raw),sha(raw),blob(raw)) == tuple(pin), 'Complete verified local public installer changed')
    catalog_raw = metadata[module.CATALOG]
    pointer = {'schemaVersion':1,'product':'CtrlOne Intelligence Ai+','kind':'signed-manual-download-pointer',
               'manualOnly':True,'automaticUpdateFeed':False,'version':VERSION,'catalogCommit':catalog,
               'catalogSha256':sha(catalog_raw),'catalogSizeBytes':len(catalog_raw)}
    raw = encode(pointer); require(parse_pointer(raw) == pointer,'Pointer schema changed'); return raw


def validate_pins():
    require(ROOT_REVIEWED_PUBLIC_BYTES is True and hex40(BASE) and hex40(TREE) and
            (PREVIOUS == 'absent' or hex40(PREVIOUS)) and all(hex64(key) for key in (PUBLISHER_SHA256,PUBLICATION_SHA256,VERIFICATION_SHA256)) and
            isinstance(POINTER_PIN,(tuple,list)) and len(POINTER_PIN) == 3 and type(POINTER_PIN[0]) is int and
            0 < POINTER_PIN[0] <= 8192 and hex64(POINTER_PIN[1]) and hex40(POINTER_PIN[2]),
            'Actual full public verification and fresh pointer lease remain unbound')


def reconstruct(root):
    validate_pins(); root = Path(root)
    module = load_publisher(root/'transfer/frozen-signed-artifacts593.py',PUBLISHER_SHA256)
    publication = json.loads(pinned(root/'transfer/artifact-publication.json',PUBLICATION_SHA256).decode('utf-8'),object_pairs_hook=unique)
    verification = json.loads(pinned(root/'transfer/artifact-verification.json',VERIFICATION_SHA256).decode('utf-8'),object_pairs_hook=unique)
    readme = read(root/'transfer/versioned-README.md',65536)
    expected = checked_evidence(module,publication,verification,readme)
    raw = read(root/'transfer/pointer.json',8192)
    require(raw == expected and (len(raw),sha(raw),blob(raw)) == tuple(POINTER_PIN), 'Frozen strict pointer bytes changed')
    return module,raw


def prepare(frozen_publisher, frozen_publisher_sha256, publication_receipt, publication_receipt_sha256,
            public_verification, public_verification_sha256, readme, output, base_commit, base_tree, previous_pointer_blob,
            reviewed=False):
    require(reviewed is True and hex40(base_commit) and hex40(base_tree) and
            (previous_pointer_blob == 'absent' or hex40(previous_pointer_blob)), 'Root review of complete public bytes and fresh pointer lease required')
    module = load_publisher(frozen_publisher,frozen_publisher_sha256)
    pub_raw = pinned(publication_receipt,publication_receipt_sha256)
    verification_raw = pinned(public_verification,public_verification_sha256)
    publication=json.loads(pub_raw.decode('utf-8'),object_pairs_hook=unique)
    verification=json.loads(verification_raw.decode('utf-8'),object_pairs_hook=unique)
    readme_raw=read(readme,65536)
    pointer=checked_evidence(module,publication,verification,readme_raw,Path(public_verification).absolute().parent)
    script=read(HERE/'manual-signed-pointer-593.py',65536).decode('utf-8')
    replacements={"BASE = '__FRESH_POINTER_BASE_COMMIT_UNBOUND__'":'BASE = '+repr(base_commit),
      "TREE = '__FRESH_POINTER_BASE_TREE_UNBOUND__'":'TREE = '+repr(base_tree),
      "PREVIOUS = '__PREVIOUS_POINTER_BLOB_OR_ABSENT_UNBOUND__'":'PREVIOUS = '+repr(previous_pointer_blob),
      "PUBLISHER_SHA256 = '__ACTUAL_FROZEN_PUBLISHER_SHA256_UNBOUND__'":'PUBLISHER_SHA256 = '+repr(frozen_publisher_sha256),
      "PUBLICATION_SHA256 = '__ACTUAL_PUBLICATION_RECEIPT_SHA256_UNBOUND__'":'PUBLICATION_SHA256 = '+repr(publication_receipt_sha256),
      "VERIFICATION_SHA256 = '__ACTUAL_FULL_PUBLIC_VERIFICATION_SHA256_UNBOUND__'":'VERIFICATION_SHA256 = '+repr(public_verification_sha256),
      "POINTER_PIN = '__ACTUAL_STRICT_POINTER_PIN_UNBOUND__'":'POINTER_PIN = '+repr((len(pointer),sha(pointer),blob(pointer))),
      'ROOT_REVIEWED_PUBLIC_BYTES = False':'ROOT_REVIEWED_PUBLIC_BYTES = True'}
    for old,new in replacements.items():
        require(script.split('def prepare(',1)[0].count(old)==1,'Pointer template binding changed');script=script.replace(old,new,1)
    ast.parse(script)
    output=Path(output).absolute();plan_path=output.parent/(output.name+'-git-write-plan.json')
    for ancestor in (output.parent,*output.parent.parents):
        info=ancestor.lstat();require(not stat.S_ISLNK(info.st_mode) and not getattr(info,'st_file_attributes',0)&0x400,'Reparse output directory refused')
    require(output.parent.is_dir() and output.parent.resolve()==output.parent and not output.exists() and not plan_path.exists() and not plan_path.is_symlink(),'Preserve prior frozen pointer transport and write plan')
    output.mkdir();(output/'transfer').mkdir();(output/'.github/workflows').mkdir(parents=True)
    values={'transfer/manual-signed-pointer-593.py':script.encode(),
      'transfer/frozen-signed-artifacts593.py':pinned(frozen_publisher,frozen_publisher_sha256,65536),
      'transfer/artifact-publication.json':pub_raw,'transfer/artifact-verification.json':verification_raw,
      'transfer/versioned-README.md':readme_raw,'transfer/pointer.json':pointer,
      '.github/workflows/manual-signed-pointer-593.yml':read(HERE/'manual-signed-pointer-593.yml',65536)}
    entries=[]
    for name,raw in values.items():
        (output/name).write_bytes(raw);entries.append({'path':name,'localPath':str(output/name),'bytes':len(raw),'sha256':sha(raw),'gitBlob':blob(raw)})
    result={'status':'PREPARED_MANUAL_SIGNED593_POINTER_ONLY','repository':REPO,'branch':BRANCH,'baseCommit':base_commit,'baseTree':base_tree,
      'previousPointerBlob':previous_pointer_blob,'pointer':parse_pointer(pointer),'files':entries,'published':False,'workflowTriggered':False,
      'installerExecuted':False,'automaticUpdateFeedsChanged':False,'runtimeAndUpgradeAcceptance':'NOT_RUN'}
    plan_path.write_bytes(encode(result));return result


def publish(api,raw):
    validate_pins();parse_pointer(raw)
    require((len(raw),sha(raw),blob(raw))==tuple(POINTER_PIN),'Pointer differs from reviewed exact bytes')
    def main():
        row=api('GET','/git/ref/heads/main');require(row['ref']=='refs/heads/main' and row['object']['type']=='commit' and hex40(row['object']['sha']),'Main ref differs');return row['object']['sha']
    def entries(tree):
        row=api('GET','/git/trees/'+tree+'?recursive=1');require(row['sha']==tree and row.get('truncated') is False and type(row['tree']) is list,'Complete tree required')
        result={item['path']:(item['mode'],item['type'],item['sha']) for item in row['tree']};require(len(result)==len(row['tree']),'Duplicate tree path');return result
    require(main()==BASE and api('GET','/git/commits/'+BASE)['tree']['sha']==TREE,'Main moved; fresh pointer lease required')
    original=entries(TREE)
    require((POINTER not in original) if PREVIOUS=='absent' else original.get(POINTER)==('100644','blob',PREVIOUS),'Previous manual pointer differs')
    key=api('POST','/git/blobs',{'content':base64.b64encode(raw).decode(),'encoding':'base64'})['sha'];require(key==blob(raw),'Uploaded pointer blob differs')
    expected=original|{POINTER:('100644','blob',key)}
    tree=api('POST','/git/trees',{'base_tree':TREE,'tree':[{'path':POINTER,'mode':'100644','type':'blob','sha':key}]})['sha']
    require(hex40(tree) and entries(tree)==expected,'Pointer tree changed an unrelated path')
    commit=api('POST','/git/commits',{'message':'Add explicit-check signed CtrlOne 1.3.593 download pointer; preserve automatic feeds','tree':tree,'parents':[BASE]})
    head=commit['sha'];require(hex40(head) and commit['tree']['sha']==tree and [p['sha'] for p in commit['parents']]==[BASE],'Pointer commit lineage differs')
    require(main()==BASE,'Main moved; pointer ref update refused')
    try:api('PATCH','/git/refs/heads/main',{'sha':head,'force':False})
    except RuntimeError:require(main()==head,'Pointer ref result unconfirmed; inspect before retry')
    require(main()==head,'Pointer publication not confirmed')
    return {'status':'PUBLISHED_MANUAL_SIGNED593_POINTER_ONLY','repository':REPO,'version':VERSION,'baseCommit':BASE,'baseTree':TREE,
      'commit':head,'tree':tree,'pointer':parse_pointer(raw),'pointerBytes':len(raw),'pointerSha256':sha(raw),'pointerGitBlob':key,
      'previousPointerBlob':PREVIOUS,'automaticUpdateFeedsChanged':False,'unrelatedExistingFilesChanged':False,
      'installerExecuted':False,'runtimeAndUpgradeAcceptance':'NOT_RUN'}


def rollback_plan(receipt,current_head,current_tree):
    validate_pins()
    require(receipt.get('status')=='PUBLISHED_MANUAL_SIGNED593_POINTER_ONLY' and receipt.get('baseCommit')==BASE and receipt.get('baseTree')==TREE and
      (receipt.get('pointerBytes'),receipt.get('pointerSha256'),receipt.get('pointerGitBlob'))==tuple(POINTER_PIN) and
      receipt.get('previousPointerBlob')==PREVIOUS and receipt.get('commit')==current_head and receipt.get('tree')==current_tree and
      hex40(current_head) and hex40(current_tree),'Moved or unrelated pointer publication cannot be rolled back automatically')
    return {'status':'REVIEW_ONLY_NO_MUTATION','parentOfNewRollbackCommit':current_head,'desiredTree':TREE,'onlyChangedPath':POINTER,
      'forceRefUpdate':False,'preserveHistory':True,'executed':False}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):raise ValueError('Public pointer redirect refused')


def verify_public(module,receipt,raw,opener=None):
    validate_pins();pointer=parse_pointer(raw)
    require(receipt.get('status')=='PUBLISHED_MANUAL_SIGNED593_POINTER_ONLY' and
      receipt.get('repository')==REPO and receipt.get('version')==VERSION and receipt.get('baseCommit')==BASE and receipt.get('baseTree')==TREE and
      receipt.get('previousPointerBlob')==PREVIOUS and hex40(receipt.get('commit')) and hex40(receipt.get('tree')) and
      receipt.get('automaticUpdateFeedsChanged') is False and receipt.get('unrelatedExistingFilesChanged') is False and
      receipt.get('installerExecuted') is False and receipt.get('runtimeAndUpgradeAcceptance')=='NOT_RUN' and
      (receipt.get('pointerBytes'),receipt.get('pointerSha256'),receipt.get('pointerGitBlob'))==tuple(POINTER_PIN) and receipt.get('pointer')==pointer,
      'Exact pointer publication receipt required')
    opener=opener or urllib.request.build_opener(NoRedirect());prefix='https://raw.githubusercontent.com/'+REPO+'/'
    for url,cap,wanted in ((prefix+'main/'+POINTER,8192,raw),(prefix+pointer['catalogCommit']+'/CtrlOne-v'+VERSION+'-artifacts.json',65536,None)):
        request=urllib.request.Request(url,headers={'Accept-Encoding':'identity','Cache-Control':'no-cache'})
        with opener.open(request,timeout=30) as response:
            require(response.status==200 and response.geturl()==url and response.headers.get('Content-Encoding','identity')=='identity','Public pointer/catalog origin/status differs')
            body=response.read(cap+1)
        require(len(body)<=cap,'Public pointer/catalog exceeds limit')
        if wanted is not None:require(body==wanted,'Live manual pointer differs')
        else:require(len(body)==pointer['catalogSizeBytes'] and sha(body)==pointer['catalogSha256'],'Immutable catalog digest differs')
    return {'status':'PASS_PUBLIC_MANUAL_SIGNED593_POINTER_ONLY','pointer':pointer,'pointerSha256':sha(raw),'automaticUpdateFeedsReadOrChanged':False,
      'installerExecuted':False,'runtimeAndUpgradeAcceptance':'NOT_RUN'}


def main():
    parser=argparse.ArgumentParser(description=__doc__);commands=parser.add_subparsers(dest='mode',required=True)
    prepare_parser=commands.add_parser('prepare')
    for key in ('frozen-publisher','frozen-publisher-sha256','publication-receipt','publication-receipt-sha256','public-verification','public-verification-sha256',
                'readme','output','base-commit','base-tree','previous-pointer-blob'):prepare_parser.add_argument('--'+key,required=True)
    prepare_parser.add_argument('--root-reviewed-public-bytes',action='store_true')
    commands.add_parser('publish')
    verify_parser=commands.add_parser('verify')
    for key in ('frozen-pointer','frozen-pointer-sha256','transport','publication-receipt','publication-receipt-sha256','output'):
        verify_parser.add_argument('--'+key,required=True)
    args=vars(parser.parse_args());mode=args.pop('mode')
    if mode=='prepare':args['reviewed']=args.pop('root_reviewed_public_bytes');print(json.dumps(prepare(**args)));return
    if mode=='verify':
        frozen=Path(args['frozen_pointer']);pinned(frozen,args['frozen_pointer_sha256'],65536)
        spec=importlib.util.spec_from_file_location('reviewed_frozen_pointer593',frozen);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        publisher,raw=module.reconstruct(Path(args['transport']).absolute())
        receipt=json.loads(pinned(args['publication_receipt'],args['publication_receipt_sha256']).decode('utf-8'),object_pairs_hook=unique)
        output=Path(args['output']).absolute();require(not output.exists() and not output.is_symlink(),'Preserve prior pointer verification')
        result=module.verify_public(publisher,receipt,raw);output.write_bytes(encode(result));print(json.dumps(result));return
    validate_pins()
    require(os.environ.get('GITHUB_REPOSITORY')==REPO and os.environ.get('GITHUB_EVENT_NAME')=='push' and
      os.environ.get('GITHUB_REF')=='refs/heads/'+BRANCH and hex40(os.environ.get('GITHUB_SHA')),'Fixed pointer push branch only')
    module,raw=reconstruct(Path.cwd().resolve());print(json.dumps(publish(module.API(os.environ.get('GITHUB_TOKEN')),raw)))


if __name__=='__main__':main()
