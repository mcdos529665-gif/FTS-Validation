"""Pinned Lean proof checks. Setup is explicit; check never installs or updates.

Windows tools, caches and mirrored Lake workspaces default to E:/Codex.
Run: python -X utf8 tools/lean.py setup | check | version
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tomllib
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'work/v14_rebuild/lean'
ELAN_VERSION = 'v4.2.4'
MATHLIB_REV = '56a005855ea17e0b0958f73ec801ae140b0a1679'
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
IMPORTS = ['Mathlib.Basic.Real.Basic', 'Mathlib.Algebra.Order.Group.Abs', 'Mathlib.Algebra.Ring.CharZero']


def audit_axioms(output, names):
    matches = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", output, re.S)
    axioms = {name: sorted(s.strip() for s in used.split(',') if s.strip()) for name, used in matches}
    for name in re.findall(r"'([^']+)' does not depend on any axioms", output):
        axioms[name] = []
    if set(axioms) != set(names):
        raise RuntimeError('Не удалось полностью разобрать аудит аксиом:\n' + output)
    for name, used in axioms.items():
        if set(used) - ALLOWED_AXIOMS:
            raise RuntimeError(f'{name}: недопустимые аксиомы {set(used) - ALLOWED_AXIOMS}')
    return axioms


def settings(home: Path | None):
    if home is None:
        override = os.environ.get('FTS_LEAN_HOME')
        home = Path(override) if override else Path('E:/Codex/tools/lean') if os.name == 'nt' else Path.home() / '.cache/fts-lean'
    home = home.resolve()
    env = os.environ.copy()
    env['ELAN_HOME'] = str(home / 'elan')
    env['MATHLIB_CACHE_DIR'] = str(home / 'cache/mathlib')
    env['MATHLIB_NO_CACHE_ON_UPDATE'] = '1'
    # Bound memory pressure on the Windows workstation during initial imports.
    env.setdefault('LEAN_NUM_THREADS', '4')
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = str(home / 'tmp')
    env['PATH'] = str(home / 'elan/bin') + os.pathsep + env.get('PATH', '')
    # One shared local workspace for this pinned project; calls are serialized.
    workspace = home / 'workspace/fts-proofs'
    suffix = '.exe' if os.name == 'nt' else ''
    return home, workspace, env, home / 'elan/bin' / ('lake' + suffix)


def run(command, cwd, env, timeout=900, stream=False):
    result = subprocess.run([str(x) for x in command], cwd=cwd, env=env,
                            capture_output=not stream, encoding='utf-8', errors='replace', timeout=timeout)
    output = '\n'.join(x for x in (result.stdout, result.stderr) if x).strip()
    if result.returncode:
        raise RuntimeError(f'Команда завершилась с кодом {result.returncode}: {command[0]}\n{output}')
    return output


def inputs():
    paths = [PROJECT / 'lean-toolchain', PROJECT / 'lakefile.toml', PROJECT / 'proofs.tsv']
    paths += sorted(PROJECT.rglob('*.lean'))
    manifest = PROJECT / 'lake-manifest.json'
    if manifest.exists():
        paths.append(manifest)
    return paths


def synchronize(workspace):
    workspace.mkdir(parents=True, exist_ok=True)
    wanted = {p.relative_to(PROJECT) for p in inputs()}
    # Only delete stale mirrored Lean source files inside this exact workspace.
    for path in workspace.rglob('*.lean'):
        relative = path.relative_to(workspace)
        if '.lake' in relative.parts:
            continue
        if relative not in wanted and path.name != 'Audit.lean':
            path.unlink()
    for source in inputs():
        destination = workspace / source.relative_to(PROJECT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists() or destination.read_bytes() != source.read_bytes():
            shutil.copyfile(source, destination)


def setup(home, workspace, env, lake):
    if os.name != 'nt' and not lake.is_file():
        raise RuntimeError('Установите elan в FTS_LEAN_HOME/elan по https://github.com/leanprover/elan; затем повторите setup.')
    if not lake.is_file():
        bootstrap = home / 'bootstrap'
        bootstrap.mkdir(parents=True, exist_ok=True)
        archive = bootstrap / f'elan-{ELAN_VERSION}.zip'
        url = f'https://github.com/leanprover/elan/releases/download/{ELAN_VERSION}/elan-x86_64-pc-windows-msvc.zip'
        print(f'Установка elan {ELAN_VERSION} в {home}', flush=True)
        with urllib.request.urlopen(url, timeout=60) as response, archive.open('wb') as destination:
            shutil.copyfileobj(response, destination)
        with zipfile.ZipFile(archive) as package:
            # Extract only the known installer, no archive-controlled paths.
            (bootstrap / 'elan-init.exe').write_bytes(package.read('elan-init.exe'))
        run([bootstrap / 'elan-init.exe', '-y', '--no-modify-path', '--default-toolchain', 'none'], bootstrap, env)
    synchronize(workspace)
    toolchain = (PROJECT / 'lean-toolchain').read_text(encoding='utf-8').strip()
    print(f'Установка закреплённого {toolchain}', flush=True)
    elan = lake.with_name('elan.exe' if os.name == 'nt' else 'elan')
    run([elan, 'toolchain', 'install', toolchain], workspace, env, stream=True)
    print('Получение закреплённых зависимостей и готовых модулей Mathlib', flush=True)
    run([lake, 'update'], workspace, env, stream=True)
    run([lake, 'exe', 'cache', 'get', *IMPORTS], workspace, env, stream=True)
    shutil.copyfile(workspace / 'lake-manifest.json', PROJECT / 'lake-manifest.json')
    print('SETUP PASS; теперь tools/lean.py check', flush=True)


def check(workspace, env, lake, report):
    if not lake.is_file():
        raise RuntimeError('Lean не настроен. Выполните python -X utf8 tools/lean.py setup')
    if not (PROJECT / 'lake-manifest.json').is_file():
        raise RuntimeError('Нет закреплённого lake-manifest.json; сначала выполните setup.')
    elan = lake.with_name('elan.exe' if os.name == 'nt' else 'elan')
    toolchain = (PROJECT / 'lean-toolchain').read_text(encoding='utf-8').strip()
    installed = run([elan, 'toolchain', 'list'], lake.parents[2], env)
    if toolchain not in installed:
        raise RuntimeError('Закреплённый toolchain отсутствует; выполните setup. Проверка его не устанавливает.')
    synchronize(workspace)
    manifest = json.loads((workspace / 'lake-manifest.json').read_text(encoding='utf-8'))
    config = tomllib.loads((PROJECT / 'lakefile.toml').read_text(encoding='utf-8'))
    required_mathlib = next(p for p in config['require'] if p['name'] == 'mathlib')
    if required_mathlib['rev'] != MATHLIB_REV:
        raise RuntimeError('Lake configuration differs from the reviewed Mathlib pin')
    mathlib = next(p for p in manifest['packages'] if p['name'] == 'mathlib')
    if mathlib['rev'] != MATHLIB_REV:
        raise RuntimeError('Mathlib revision differs from the reviewed pin')
    for package in manifest['packages']:
        directory = workspace / manifest.get('packagesDir', '.lake/packages') / package['name']
        if package.get('type') != 'git' or not (directory / '.git').exists():
            raise RuntimeError('Закреплённые зависимости отсутствуют; выполните setup.')
        revision = run(['git', 'rev-parse', 'HEAD'], directory, env)
        if revision != package['rev']:
            raise RuntimeError(f"Dependency revision mismatch: {package['name']}")
        if run(['git', 'status', '--porcelain', '--untracked-files=no'], directory, env):
            raise RuntimeError(f"Modified dependency sources: {package['name']}")
    with (PROJECT / 'proofs.tsv').open(encoding='utf-8', newline='') as stream:
        proofs = list(csv.DictReader(stream, delimiter='\t'))
    names = [p['theorem'] for p in proofs]
    if not proofs or len(set(names)) != len(names):
        raise RuntimeError('Пустой реестр доказательств или повтор имени')
    for proof in proofs:
        if not re.fullmatch(r'FTS\.[A-Za-z_][A-Za-z_0-9]*', proof['theorem']):
            raise RuntimeError('Некорректное имя теоремы')
        module = PROJECT / proof['module']
        if not module.resolve().is_relative_to(PROJECT.resolve()) or not module.is_file():
            raise RuntimeError('Нет исходного модуля доказательства')
        source, function = proof['source'].split('#')
        if not re.search(r'^def ' + re.escape(function) + r'\(', (ROOT / source).read_text(encoding='utf-8'), re.M):
            raise RuntimeError('Не найдена исходная C-проверка')
    # Re-elaborate local proof files on each check; lake's cached local objects
    # alone are not treated as evidence for newly edited source.
    run([lake, 'build', 'FTS'], workspace, env)
    for module in sorted({p['module'] for p in proofs}):
        output = run([lake, 'env', 'lean', '-DwarningAsError=true', module], workspace, env)
        if 'sorry' in output.lower():
            raise RuntimeError('Lean reported a proof placeholder')
    audit = workspace / 'Audit.lean'
    audit.write_bytes(('import FTS\n' + '\n'.join(
        'example : (' + proof['lean_type'] + ') := ' + proof['theorem'] + '\n#print axioms ' + proof['theorem']
        for proof in proofs) + '\n').encode('utf-8'))
    output = run([lake, 'env', 'lean', '-DwarningAsError=true', 'Audit.lean'], workspace, env)
    axioms = audit_axioms(output, names)
    version = run([lake, 'env', 'lean', '--version'], workspace, env)
    if 'version ' + toolchain.rsplit(':', 1)[-1].removeprefix('v') not in version:
        raise RuntimeError('Фактическая версия Lean не совпадает с lean-toolchain')
    payload = dict(status='PASS', lean_version=version, mathlib_rev=MATHLIB_REV,
                   source_sha256={p.relative_to(PROJECT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs()},
                   python_verification_sha256=hashlib.sha256((ROOT / 'work/v14_rebuild/verification.py').read_bytes()).hexdigest(),
                   allowed_axioms=sorted(ALLOWED_AXIOMS),
                   proofs=[dict(p, status='PASS', axioms=axioms[p['theorem']]) for p in proofs],
                   scope='Only the listed real mathematical predicates; no semantic or St_FTS promotion.')
    saved_path = PROJECT / 'verification_result.json'
    if not report and saved_path.is_file():
        saved = json.loads(saved_path.read_text(encoding='utf-8'))
        if saved.get('status') != 'PASS' or any(saved.get(key) != payload[key] for key in ('source_sha256', 'python_verification_sha256', 'mathlib_rev')):
            raise RuntimeError('Сохранённый результат устарел: выполните check --report work/v14_rebuild/lean/verification_result.json и пересоберите граф.')
    if report:
        report = report.resolve()
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_bytes((json.dumps(payload, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    checks = '/'.join(p['check_id'] for p in proofs)
    print(f"PASS Lean: {len(proofs)} proofs; {checks}; no sorryAx or custom axioms; {version}")
    return payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['setup', 'check', 'version'])
    parser.add_argument('--home', type=Path, help='tool/cache/workspace root; default E:/Codex/tools/lean on Windows')
    parser.add_argument('--report', type=Path, help='optional JSON result; no report is written by default')
    args = parser.parse_args()
    home, workspace, env, lake = settings(args.home)
    home.mkdir(parents=True, exist_ok=True)
    (home / 'tmp').mkdir(exist_ok=True)
    lock = home / 'fts-proofs.lock'
    descriptor = None
    try:
        descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        os.write(descriptor, str(os.getpid()).encode())
        if args.command == 'setup':
            setup(home, workspace, env, lake)
        elif args.command == 'version':
            synchronize(workspace)
            print(run([lake, 'env', 'lean', '--version'], workspace, env))
        else:
            check(workspace, env, lake, args.report)
    except FileExistsError:
        print(f'NOT_RUN Lean: другое выполнение держит {lock}', file=sys.stderr)
        return 2
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired, StopIteration) as exc:
        if args.command == 'check' and args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_bytes((json.dumps(dict(status='ERROR', error=str(exc)), ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
        print(f'FAIL Lean: {exc}', file=sys.stderr)
        return 1
    finally:
        if descriptor is not None:
            os.close(descriptor)
            lock.unlink(missing_ok=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
