#!/usr/bin/env python3
"""
gather_repo.py — collect a structured fact base about an open-source project,
for the oss-deep-analysis skill to reason over.

Accepts any of:
  - a local path to a clone        (full signals: git history, LOC, manifests)
  - a GitHub URL or owner/repo      (API signals: stars, releases, contributors, languages)
  - a GitHub URL pointing at a path

Usage:
  python gather_repo.py <target> [--out repo_facts.json]
  GITHUB_TOKEN=ghp_xxx python gather_repo.py owner/repo   # lifts API rate limits

Design: standard library only. Every probe is wrapped so a missing tool, a
network failure, or an odd repo never aborts the run — the field is set to null
and recorded under "missing", and a summary is printed to stderr at the end.
"""
import argparse, json, os, re, ssl, subprocess, sys, urllib.request, urllib.error
from datetime import datetime, timezone

API = "https://api.github.com"
UA = "oss-deep-analysis/1.0"
README_CHARS = 4000
MISSING = []


def note_missing(what, why=""):
    MISSING.append({"field": what, "reason": why})


def run(cmd, cwd=None, timeout=60):
    """Run a shell command; return stdout or None on any failure."""
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return r.stdout if r.returncode == 0 else None
    except Exception:
        return None


def have(tool):
    return run(["bash", "-lc", f"command -v {tool}"]) not in (None, "")


# ---------------- target parsing ----------------

def parse_target(t):
    """Return dict: {kind: 'local'|'github', path?, owner?, repo?, url?}."""
    if os.path.isdir(t):
        return {"kind": "local", "path": os.path.abspath(t)}
    m = re.search(r"github\.com[:/]+([^/]+)/([^/#?]+?)(?:\.git)?(?:[/#?].*)?$", t)
    if m:
        return {"kind": "github", "owner": m.group(1), "repo": m.group(2),
                "url": f"https://github.com/{m.group(1)}/{m.group(2)}"}
    m = re.match(r"^([\w.-]+)/([\w.-]+)$", t)
    if m:
        return {"kind": "github", "owner": m.group(1), "repo": m.group(2),
                "url": f"https://github.com/{m.group(1)}/{m.group(2)}"}
    return {"kind": "unknown", "raw": t}


# ---------------- github api ----------------

def gh(path, accept="application/vnd.github+json", retries=2):
    url = path if path.startswith("http") else f"{API}{path}"
    headers = {"User-Agent": UA, "Accept": accept}
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        headers["Authorization"] = f"Bearer {tok}"
    ctx = ssl.create_default_context()
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
                if resp.status == 202 and attempt < retries:   # stats still computing
                    import time; time.sleep(2); continue
                raw = resp.read()
                link = resp.headers.get("Link", "")
                return {"data": raw, "link": link, "status": resp.status}
        except urllib.error.HTTPError as e:
            return {"error": f"HTTP {e.code}", "status": e.code}
        except Exception as e:
            if attempt < retries:
                continue
            return {"error": str(e)}
    return {"error": "exhausted retries"}


def gh_json(path, **kw):
    r = gh(path, **kw)
    if "data" in r:
        try:
            return json.loads(r["data"]), r.get("link", "")
        except Exception:
            return None, ""
    return None, ""


def last_page_from_link(link):
    m = re.search(r'[?&]page=(\d+)>;\s*rel="last"', link or "")
    return int(m.group(1)) if m else None


def gather_github(owner, repo):
    out = {"host": "github", "owner": owner, "repo": repo}

    meta, _ = gh_json(f"/repos/{owner}/{repo}")
    if not meta:
        note_missing("github_meta", "repo not found or API unreachable (check name / network / token)")
        return out
    out["meta"] = {
        "description": meta.get("description"),
        "homepage": meta.get("homepage"),
        "stars": meta.get("stargazers_count"),
        "forks": meta.get("forks_count"),
        "watchers": meta.get("subscribers_count"),
        "open_issues": meta.get("open_issues_count"),
        "primary_language": meta.get("language"),
        "topics": meta.get("topics", []),
        "license": (meta.get("license") or {}).get("spdx_id"),
        "archived": meta.get("archived"),
        "created_at": meta.get("created_at"),
        "updated_at": meta.get("updated_at"),
        "pushed_at": meta.get("pushed_at"),
        "default_branch": meta.get("default_branch"),
    }

    langs, _ = gh_json(f"/repos/{owner}/{repo}/languages")
    if langs:
        total = sum(langs.values()) or 1
        out["languages"] = {k: round(v * 100 / total, 1) for k, v in
                            sorted(langs.items(), key=lambda x: -x[1])}
    else:
        note_missing("languages")

    rels, link = gh_json(f"/repos/{owner}/{repo}/releases?per_page=100")
    if isinstance(rels, list):
        dates = [r.get("published_at") for r in rels if r.get("published_at")]
        out["releases"] = {
            "count_recent_page": len(rels),
            "more_pages": bool(last_page_from_link(link)),
            "latest_tag": rels[0].get("tag_name") if rels else None,
            "latest_date": rels[0].get("published_at") if rels else None,
            "recent_dates": dates[:12],
        }
    else:
        note_missing("releases")

    cont, link = gh_json(f"/repos/{owner}/{repo}/contributors?per_page=100&anon=1")
    if isinstance(cont, list) and cont:
        contribs = [(c.get("login") or c.get("name") or "anon", c.get("contributions", 0)) for c in cont]
        tot = sum(c for _, c in contribs) or 1
        out["contributors"] = {
            "count_at_least": len(cont) + (100 * ((last_page_from_link(link) or 1) - 1)),
            "top": [{"who": w, "commits": c, "share_pct": round(c * 100 / tot, 1)} for w, c in contribs[:5]],
            "top1_share_pct": round(contribs[0][1] * 100 / tot, 1) if contribs else None,
        }
    else:
        note_missing("contributors")

    commits, _ = gh_json(f"/repos/{owner}/{repo}/commits?per_page=1")
    if isinstance(commits, list) and commits:
        out["last_commit_date"] = (commits[0].get("commit", {}).get("committer", {}) or {}).get("date")
    else:
        note_missing("last_commit_date")

    activity, _ = gh_json(f"/repos/{owner}/{repo}/stats/commit_activity")
    if isinstance(activity, list) and activity:
        weekly = [w.get("total", 0) for w in activity]      # last 52 weeks
        out["commit_activity"] = {
            "last_52w_total": sum(weekly),
            "last_4w_total": sum(weekly[-4:]),
            "last_13w_total": sum(weekly[-13:]),
        }
    else:
        note_missing("commit_activity", "GitHub stats endpoint was computing or unavailable")

    comm, _ = gh_json(f"/repos/{owner}/{repo}/community/profile")
    if isinstance(comm, dict):
        f = comm.get("files", {}) or {}
        out["community_files"] = {
            "readme": bool(f.get("readme")),
            "contributing": bool(f.get("contributing")),
            "code_of_conduct": bool(f.get("code_of_conduct")),
            "license": bool(f.get("license")),
            "health_pct": comm.get("health_percentage"),
        }

    rd = gh(f"/repos/{owner}/{repo}/readme")
    if "data" in rd:
        try:
            import base64
            j = json.loads(rd["data"])
            text = base64.b64decode(j.get("content", "")).decode("utf-8", "replace")
            out["readme_excerpt"] = text[:README_CHARS]
        except Exception:
            note_missing("readme")
    else:
        note_missing("readme")

    return out


# ---------------- local repo ----------------

def days_ago_count(path, days):
    out = run(["git", "-C", path, "rev-list", "--count", f"--since={days} days ago", "HEAD"])
    return int(out.strip()) if out and out.strip().isdigit() else None


def gather_local(path):
    out = {"path": path}
    is_git = os.path.isdir(os.path.join(path, ".git")) or run(["git", "-C", path, "rev-parse", "--git-dir"])

    # git history
    if is_git:
        g = {}
        tot = run(["git", "-C", path, "rev-list", "--count", "HEAD"])
        g["total_commits"] = int(tot.strip()) if tot and tot.strip().isdigit() else None
        g["commits_90d"] = days_ago_count(path, 90)
        g["commits_365d"] = days_ago_count(path, 365)
        # root-commit date (--max-count is applied before --reverse, so the
        # naive "log --reverse -1" returns the LATEST commit; use root instead)
        first = run(["bash", "-lc", f"git -C {path!r} log --max-parents=0 --format=%cI | tail -1"])
        last = run(["git", "-C", path, "log", "-1", "--format=%cI"])
        g["first_commit"] = first.strip().splitlines()[-1] if first and first.strip() else None
        g["last_commit"] = last.strip() if last else None
        shortlog = run(["bash", "-lc", f"git -C {path!r} shortlog -sne HEAD"])
        if shortlog:
            rows = [r for r in shortlog.strip().splitlines() if r.strip()]
            counts = []
            for r in rows:
                m = re.match(r"\s*(\d+)\s+(.*)", r)
                if m:
                    counts.append((int(m.group(1)), m.group(2)))
            counts.sort(reverse=True)
            tot_c = sum(c for c, _ in counts) or 1
            g["contributor_count"] = len(counts)
            g["top_contributors"] = [{"who": w, "commits": c, "share_pct": round(c * 100 / tot_c, 1)}
                                     for c, w in counts[:5]]
            g["top1_share_pct"] = round(counts[0][0] * 100 / tot_c, 1) if counts else None
        out["git"] = g
    else:
        note_missing("git_history", "not a git repo (no .git)")

    # lines of code
    out["loc"] = gather_loc(path)

    # files / structure signals
    def exists(*names):
        return [n for n in names if os.path.exists(os.path.join(path, n))]
    out["files"] = {
        "license": exists("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "COPYING.txt"),
        "readme": exists("README.md", "README.rst", "README.txt", "README"),
        "changelog": exists("CHANGELOG.md", "CHANGELOG", "CHANGES.md", "HISTORY.md"),
        "contributing": exists("CONTRIBUTING.md", "CONTRIBUTING"),
        "code_of_conduct": exists("CODE_OF_CONDUCT.md"),
        "tests_dir": exists("tests", "test", "spec", "__tests__"),
        "ci": exists(".github/workflows", ".gitlab-ci.yml", ".circleci", "azure-pipelines.yml",
                     ".travis.yml", "Jenkinsfile"),
        "docs_dir": exists("docs", "doc", "documentation", "website"),
        "dockerfile": exists("Dockerfile", "docker-compose.yml", "compose.yaml"),
        "editorconfig": exists(".editorconfig"),
    }

    # manifests / dependency metadata
    out["manifests"] = gather_manifests(path)

    # readme excerpt
    for r in out["files"]["readme"]:
        try:
            with open(os.path.join(path, r), encoding="utf-8", errors="replace") as fh:
                out["readme_excerpt"] = fh.read()[:README_CHARS]
            break
        except Exception:
            note_missing("readme")
    return out


def gather_loc(path):
    if have("tokei"):
        j = run(["tokei", "--output", "json", path])
        if j:
            try:
                data = json.loads(j)
                langs = {k: v.get("code") for k, v in data.items()
                         if k != "Total" and isinstance(v, dict)}
                total = data.get("Total", {}).get("code")
                top = dict(sorted(langs.items(), key=lambda x: -(x[1] or 0))[:10])
                return {"tool": "tokei", "total_code_lines": total, "by_language": top}
            except Exception:
                pass
    if have("cloc"):
        j = run(["cloc", "--json", "--quiet", path])
        if j:
            try:
                data = json.loads(j)
                total = data.get("SUM", {}).get("code")
                langs = {k: v.get("code") for k, v in data.items()
                         if k not in ("header", "SUM") and isinstance(v, dict)}
                top = dict(sorted(langs.items(), key=lambda x: -(x[1] or 0))[:10])
                return {"tool": "cloc", "total_code_lines": total, "by_language": top}
            except Exception:
                pass
    # fallback: count tracked source lines by extension
    note_missing("loc_tool", "tokei/cloc not installed; used a rough line count")
    EXT = {".py": "Python", ".js": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript",
           ".jsx": "JavaScript", ".go": "Go", ".rs": "Rust", ".java": "Java", ".rb": "Ruby",
           ".c": "C", ".h": "C", ".cpp": "C++", ".cc": "C++", ".cs": "C#", ".php": "PHP",
           ".kt": "Kotlin", ".swift": "Swift", ".scala": "Scala", ".sh": "Shell"}
    files = run(["git", "-C", path, "ls-files"])
    file_list = files.splitlines() if files else None
    counts, total = {}, 0
    try:
        if file_list is None:
            file_list = []
            for root, dirs, fs in os.walk(path):
                dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "venv", ".venv", "dist", "build")]
                for f in fs:
                    file_list.append(os.path.relpath(os.path.join(root, f), path))
        for rel in file_list:
            ext = os.path.splitext(rel)[1].lower()
            if ext in EXT:
                try:
                    with open(os.path.join(path, rel), encoding="utf-8", errors="ignore") as fh:
                        n = sum(1 for _ in fh)
                    counts[EXT[ext]] = counts.get(EXT[ext], 0) + n
                    total += n
                except Exception:
                    continue
        return {"tool": "fallback-linecount", "total_code_lines": total,
                "by_language": dict(sorted(counts.items(), key=lambda x: -x[1])[:10])}
    except Exception:
        return None


def gather_manifests(path):
    m = {}

    def read(name):
        p = os.path.join(path, name)
        if os.path.exists(p):
            try:
                with open(p, encoding="utf-8", errors="replace") as fh:
                    return fh.read()
            except Exception:
                return None
        return None

    pkg = read("package.json")
    if pkg:
        try:
            j = json.loads(pkg)
            m["npm"] = {"name": j.get("name"), "version": j.get("version"),
                        "license": j.get("license"),
                        "deps": len(j.get("dependencies", {}) or {}),
                        "devDeps": len(j.get("devDependencies", {}) or {})}
        except Exception:
            note_missing("package.json_parse")

    pyproject = read("pyproject.toml")
    if pyproject:
        m["python_pyproject"] = {
            "name": (re.search(r'(?m)^\s*name\s*=\s*["\']([^"\']+)', pyproject) or [None, None])[1],
            "version": (re.search(r'(?m)^\s*version\s*=\s*["\']([^"\']+)', pyproject) or [None, None])[1],
            "license_hint": (re.search(r'(?mi)license.*?["\']([^"\']+)', pyproject) or [None, None])[1],
        }
    elif read("setup.py") or read("requirements.txt"):
        req = read("requirements.txt")
        m["python_legacy"] = {"requirements_count":
                              len([l for l in req.splitlines() if l.strip() and not l.startswith("#")]) if req else None,
                              "has_setup_py": bool(read("setup.py"))}

    cargo = read("Cargo.toml")
    if cargo:
        m["rust"] = {"name": (re.search(r'(?m)^\s*name\s*=\s*["\']([^"\']+)', cargo) or [None, None])[1],
                     "version": (re.search(r'(?m)^\s*version\s*=\s*["\']([^"\']+)', cargo) or [None, None])[1]}

    gomod = read("go.mod")
    if gomod:
        m["go"] = {"module": (re.search(r'(?m)^module\s+(\S+)', gomod) or [None, None])[1],
                   "go_version": (re.search(r'(?m)^go\s+(\S+)', gomod) or [None, None])[1]}

    for fn, key in [("composer.json", "php"), ("Gemfile", "ruby"), ("pom.xml", "java_maven"),
                    ("build.gradle", "java_gradle"), ("pubspec.yaml", "dart")]:
        if read(fn):
            m.setdefault("other_ecosystems", []).append(key)
    return m


# ---------------- main ----------------

def main():
    ap = argparse.ArgumentParser(description="Gather facts about an open-source project.")
    ap.add_argument("target", help="local path, GitHub URL, or owner/repo")
    ap.add_argument("--out", default="repo_facts.json", help="output JSON path")
    args = ap.parse_args()

    tgt = parse_target(args.target)
    result = {
        "gathered_at": datetime.now(timezone.utc).isoformat(),
        "target": tgt,
    }

    if tgt["kind"] == "local":
        result["local"] = gather_local(tgt["path"])
        # opportunistically enrich with GitHub if the clone has a github remote
        remote = run(["git", "-C", tgt["path"], "config", "--get", "remote.origin.url"])
        if remote:
            gh_tgt = parse_target(remote.strip())
            if gh_tgt["kind"] == "github":
                result["github"] = gather_github(gh_tgt["owner"], gh_tgt["repo"])
    elif tgt["kind"] == "github":
        result["github"] = gather_github(tgt["owner"], tgt["repo"])
    else:
        note_missing("target", "could not parse as local path, GitHub URL, or owner/repo")

    result["missing"] = MISSING

    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)

    # human summary on stderr
    print(f"✓ wrote {args.out}", file=sys.stderr)
    if "github" in result and result["github"].get("meta"):
        mm = result["github"]["meta"]
        print(f"  github: {tgt.get('owner')}/{tgt.get('repo')} · ★{mm.get('stars')} · "
              f"{mm.get('primary_language')} · {mm.get('license')} · pushed {mm.get('pushed_at')}",
              file=sys.stderr)
    if "local" in result and result["local"].get("git"):
        g = result["local"]["git"]
        print(f"  local: {g.get('total_commits')} commits · "
              f"{g.get('commits_90d')} in 90d · {g.get('contributor_count')} contributors · "
              f"top1 {g.get('top1_share_pct')}%", file=sys.stderr)
    if MISSING:
        print(f"  could not gather: {', '.join(sorted(set(x['field'] for x in MISSING)))}", file=sys.stderr)


if __name__ == "__main__":
    main()
