#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import ssl
from datetime import UTC, datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


REPORT_HOSTS = {
    "app.sherlock.xyz",
    "certificate.quantstamp.com",
    "consensys.net",
    "www.consensys.net",
    "halborn.com",
    "www.halborn.com",
    "github.com",
}


HOME_DOMAINS = {
    "mystenlabs.com",
    "www.mystenlabs.com",
    "bluefin.io",
    "bucketprotocol.io",
    "aftermath.finance",
    "www.cetus.zone",
    "cetus.zone",
    "www.volo.fi",
    "volo.fi",
    "www.axelar.network",
    "axelar.network",
    "www.lombard.finance",
    "lombard.finance",
    "turbos.finance",
    "www.turbos.finance",
}


def sanitize(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9._-]+", "-", text.strip())
    return text.strip("-")[:120] or "file"


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---\n"):
        return {}

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}

    meta: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ": " in line:
            key, value = line.split(": ", 1)
            meta[key.strip()] = value.strip()
    return meta


def is_report_like(url: str) -> bool:
    if not url or url == "none":
        return False

    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return False

    host = parsed.netloc.lower()
    path = parsed.path or "/"

    if host in REPORT_HOSTS:
        return path not in {"", "/"}

    if host in HOME_DOMAINS:
        return False

    keywords = ("audit", "audits", "report", "reports", "certificate", "finding", "findings", "issue", "issues")
    return path not in {"", "/"} and any(keyword in path.lower() for keyword in keywords)


def fetch(url: str) -> tuple[bytes, str, str]:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 Copilot downloader"})
    with urlopen(request, timeout=45, context=ssl.create_default_context()) as response:
        content = response.read()
        content_type = response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
        final_url = response.geturl()
    return content, content_type, final_url


def rebuild(base_dir: Path, clean: bool) -> dict:
    artifacts_dir = base_dir / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    if clean:
        for child in artifacts_dir.iterdir():
            if child.is_file():
                child.unlink()

    entries: list[dict] = []
    solodit_ids: dict[str, list[str]] = {}

    for md_path in sorted(base_dir.glob("*.md")):
        meta = parse_frontmatter(md_path)
        solodit_id = meta.get("solodit_id")
        if not solodit_id:
            continue

        solodit_ids.setdefault(solodit_id, []).append(md_path.name)

        refs = []
        for key in ("source_link", "contest_link", "github_link"):
            value = meta.get(key, "none")
            if value != "none":
                refs.append((key, value))

        entries.append({"file": md_path.name, "meta": meta, "refs": refs})

    duplicate_ids = {solodit_id: files for solodit_id, files in solodit_ids.items() if len(files) > 1}

    candidates: dict[str, dict] = {}
    for entry in entries:
        fallback_issue = None

        for kind, url in entry["refs"]:
            if kind == "github_link" and "/issues/" in url:
                fallback_issue = url

            if is_report_like(url):
                item = candidates.setdefault(url, {"sources": [], "kinds": set()})
                item["sources"].append(entry["file"])
                item["kinds"].add(kind)

        if fallback_issue and entry["meta"].get("source_link", "none") == "none":
            item = candidates.setdefault(fallback_issue, {"sources": [], "kinds": set()})
            item["sources"].append(entry["file"])
            item["kinds"].add("github_issue")

    manifest = {
        "generated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "report_count": len(entries),
        "unique_solodit_ids": len(solodit_ids),
        "duplicate_solodit_ids": duplicate_ids,
        "candidate_url_count": len(candidates),
        "downloads": [],
    }

    seen_pdf_urls: set[str] = set()
    for index, (url, info) in enumerate(sorted(candidates.items()), 1):
        parsed = urlparse(url)
        base_name = sanitize(f"{parsed.netloc}-{parsed.path.strip('/').replace('/', '-') or 'root'}")
        base_name = f"{index:02d}-{base_name}-{hashlib.sha1(url.encode()).hexdigest()[:8]}"

        record = {
            "url": url,
            "kinds": sorted(info["kinds"]),
            "referenced_by": sorted(set(info["sources"])),
            "saved_files": [],
        }

        try:
            content, content_type, final_url = fetch(url)
            record["final_url"] = final_url
            record["content_type"] = content_type

            is_pdf = content_type == "application/pdf" or final_url.lower().endswith(".pdf") or url.lower().endswith(".pdf")
            ext = ".pdf" if is_pdf else ".html"

            out_path = artifacts_dir / f"{base_name}{ext}"
            out_path.write_bytes(content)
            record["saved_files"].append(out_path.name)

            if not is_pdf:
                html = content.decode("utf-8", errors="ignore")
                pdf_links = []
                for match in re.findall(r'''href=["']([^"']+?\.pdf(?:[^"']*)?)["']''', html, flags=re.I):
                    absolute_url = urljoin(final_url, match)
                    if absolute_url in seen_pdf_urls:
                        continue
                    seen_pdf_urls.add(absolute_url)
                    pdf_links.append(absolute_url)

                record["linked_pdfs"] = pdf_links
                for pdf_index, pdf_url in enumerate(pdf_links, 1):
                    try:
                        pdf_content, _, _ = fetch(pdf_url)
                        pdf_path = artifacts_dir / f"{base_name}-linked-{pdf_index}.pdf"
                        pdf_path.write_bytes(pdf_content)
                        record["saved_files"].append(pdf_path.name)
                    except Exception as exc:  # noqa: BLE001
                        record.setdefault("pdf_errors", []).append({"url": pdf_url, "error": str(exc)})

            record["status"] = "ok"
        except (HTTPError, URLError, TimeoutError, ssl.SSLError, OSError) as exc:
            record["status"] = "error"
            record["error"] = str(exc)

        manifest["downloads"].append(record)

    (artifacts_dir / "download_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    with (artifacts_dir / "candidate_links.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["url", "kinds", "referenced_by"])
        for url, info in sorted(candidates.items()):
            writer.writerow([url, ";".join(sorted(info["kinds"])), ";".join(sorted(set(info["sources"])))])

    summary_lines = [
        f"reports={len(entries)}",
        f"unique_solodit_ids={len(solodit_ids)}",
        f"duplicate_solodit_ids={len(duplicate_ids)}",
        f"candidate_urls={len(candidates)}",
        f"successful_downloads={sum(1 for item in manifest['downloads'] if item['status'] == 'ok')}",
        f"failed_downloads={sum(1 for item in manifest['downloads'] if item['status'] != 'ok')}",
        f"downloaded_pdf_files={sum(1 for item in manifest['downloads'] for name in item.get('saved_files', []) if name.endswith('.pdf'))}",
    ]
    (artifacts_dir / "summary.txt").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild report artifacts for a fetched reports directory")
    parser.add_argument("report_dir", help="Path to a reports/<topic>_findings directory")
    parser.add_argument("--clean", action="store_true", help="Remove existing files in the artifacts directory before rebuilding")
    args = parser.parse_args()

    report_dir = Path(args.report_dir).resolve()
    manifest = rebuild(report_dir, clean=args.clean)

    print(f"reports={manifest['report_count']}")
    print(f"unique_solodit_ids={manifest['unique_solodit_ids']}")
    print(f"duplicate_solodit_ids={len(manifest['duplicate_solodit_ids'])}")
    print(f"candidate_urls={manifest['candidate_url_count']}")
    print(f"successful_downloads={sum(1 for item in manifest['downloads'] if item['status'] == 'ok')}")
    print(f"failed_downloads={sum(1 for item in manifest['downloads'] if item['status'] != 'ok')}")
    print(f"downloaded_pdf_files={sum(1 for item in manifest['downloads'] for name in item.get('saved_files', []) if name.endswith('.pdf'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())