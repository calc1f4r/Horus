#!/usr/bin/env python3
"""
Stage 1: DeFiHackLabs Metadata Extraction
==========================================
Parses all yearly README files and PoC headers to extract structured exploit metadata.
Handles 4+ header format variants across 2017-2025.

Output: scripts/output/defihacklabs_raw_index.json
"""

import os
import re
import json
import glob
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent
DEFIHACKLABS_DIR = BASE_DIR / "DeFiHackLabs"
README_FILES = sorted(DEFIHACKLABS_DIR.glob("past/*/README.md"))
POC_DIR = DEFIHACKLABS_DIR / "src" / "test"
OUTPUT_FILE = BASE_DIR / "scripts" / "output" / "defihacklabs_raw_index.json"

# ─── README Parsing ───────────────────────────────────────────────────────────

# Matches heading formats:
#   ### 20251201 yETH - Unsafe Math
#   ### 20230328 - Thena - Yield Protocol Flaw
#   ### 20240924-MARA---price-manipulation
HEADING_RE = re.compile(
    r"^###\s+"
    r"(\d{8})"                       # date YYYYMMDD
    r"[\s\-]+"                       # separator (spaces/dashes)
    r"(.+?)"                         # protocol name (non-greedy)
    r"\s*[-–—]+\s*"                  # dash separator
    r"(.+?)\s*$",                    # vulnerability label (rest of line)
    re.IGNORECASE
)

# Fallback: handles edge cases like "20240924-MARA---price-manipulation"
HEADING_DASH_RE = re.compile(
    r"^###\s+"
    r"(\d{8})"
    r"-+"
    r"([A-Za-z0-9_]+)"
    r"-{2,}"
    r"(.+?)\s*$",
    re.IGNORECASE
)

LOST_RE = re.compile(
    r"(?:Lost|Rescued|Profit)\s*:\s*(.+?)$",
    re.IGNORECASE | re.MULTILINE
)

FORGE_CMD_RE = re.compile(
    r"forge\s+test\s+--contracts\s+(\S+\.sol)",
    re.IGNORECASE
)

URL_RE = re.compile(r"https?://\S+")


def parse_readme(readme_path: Path) -> list[dict]:
    """Parse a yearly README.md file into exploit entries."""
    text = readme_path.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")
    year = readme_path.parent.name  # e.g., "2025"

    entries = []
    current_entry = None

    for i, line in enumerate(lines):
        # Try heading patterns
        m = HEADING_RE.match(line)
        if not m:
            m = HEADING_DASH_RE.match(line)

        if m:
            # Save previous entry
            if current_entry:
                entries.append(current_entry)

            date_str = m.group(1)
            protocol = m.group(2).strip().strip("-").strip()
            vuln_label = m.group(3).strip().strip("-").strip()

            # Clean up protocol name: remove leading "- " artifacts
            protocol = re.sub(r"^[\s\-]+", "", protocol)
            vuln_label = re.sub(r"^[\s\-]+", "", vuln_label)

            # Remove markdown bold markers
            vuln_label = vuln_label.replace("**", "").strip()
            protocol = protocol.replace("**", "").strip()

            current_entry = {
                "date": date_str,
                "year": year,
                "protocol": protocol,
                "raw_vuln_label": vuln_label,
                "loss_amount": None,
                "poc_file_path": None,
                "reference_links": [],
                "readme_file": str(readme_path.relative_to(BASE_DIR)),
                "readme_line": i + 1,
            }
            continue

        if current_entry:
            # Extract loss amount
            lost_m = LOST_RE.search(line)
            if lost_m and current_entry["loss_amount"] is None:
                current_entry["loss_amount"] = lost_m.group(1).strip()

            # Extract PoC file path from forge command
            forge_m = FORGE_CMD_RE.search(line)
            if forge_m and current_entry["poc_file_path"] is None:
                raw_path = forge_m.group(1)
                # Normalize path: ./src/test/... or src/test/...
                raw_path = raw_path.lstrip("./")
                current_entry["poc_file_path"] = raw_path

            # Extract reference links
            urls = URL_RE.findall(line)
            for url in urls:
                # Skip forge test command URLs or contract URLs that are relative
                if url not in current_entry["reference_links"]:
                    current_entry["reference_links"].append(url)

    # Don't forget the last entry
    if current_entry:
        entries.append(current_entry)

    return entries


# ─── PoC Header Parsing ──────────────────────────────────────────────────────

CHAIN_RE = re.compile(
    r"""(?:createSelectFork|vm\.createSelectFork)\s*\(\s*["']([^"']+)["']""",
    re.IGNORECASE
)

# @KeyInfo style
KEY_INFO_TOTAL_LOST_RE = re.compile(r"@KeyInfo\s*-?\s*Total\s+Lost\s*:\s*(.+)", re.IGNORECASE)
ATTACKER_RE = re.compile(r"(?:Attacker|attacker)\s*:\s*(https?\S+)", re.IGNORECASE)
ATTACK_CONTRACT_RE = re.compile(r"Attack\s*Contract\s*:\s*(https?\S+)", re.IGNORECASE)
VULN_CONTRACT_RE = re.compile(r"Vulnerable\s*Contract\s*:\s*(https?\S+)", re.IGNORECASE)
ATTACK_TX_RE = re.compile(r"(?:Attack\s*Tx|TX|tx)\s*:\s*(https?\S+)", re.IGNORECASE)

# Comment-based metadata (2024-2025 era)
REASON_RE = re.compile(r"//\s*reason\s*:\s*(.+)", re.IGNORECASE)
GUY_RE = re.compile(r"//\s*(?:guy|GUY|Twitter\s*Guy)\s*:\s*(https?\S+)", re.IGNORECASE)
TX_COMMENT_RE = re.compile(r"//\s*(?:tx|TX|Attack\s*Tx)\s*:\s*(https?\S+)", re.IGNORECASE)
TOTAL_LOSS_COMMENT_RE = re.compile(r"//\s*(?:total\s*loss|Profit|profit)\s*:\s*(.+)", re.IGNORECASE)

# Post-mortem
POSTMORTEM_RE = re.compile(r"Post-mortem\s*:\s*(https?\S+)", re.IGNORECASE)

CHAIN_ALIASES = {
    "mainnet": "ethereum",
    "eth": "ethereum",
    "bsc": "bsc",
    "bnb": "bsc",
    "polygon": "polygon",
    "matic": "polygon",
    "arbitrum": "arbitrum",
    "arb": "arbitrum",
    "optimism": "optimism",
    "op": "optimism",
    "avalanche": "avalanche",
    "avax": "avalanche",
    "fantom": "fantom",
    "ftm": "fantom",
    "base": "base",
    "gnosis": "gnosis",
    "xdai": "gnosis",
    "celo": "celo",
    "cronos": "cronos",
    "moonbeam": "moonbeam",
    "moonriver": "moonriver",
    "harmony": "harmony",
    "aurora": "aurora",
    "metis": "metis",
    "blast": "blast",
    "linea": "linea",
    "scroll": "scroll",
    "zksync": "zksync",
    "mantle": "mantle",
    "mode": "mode",
    "sonic": "sonic",
}


def parse_poc_header(poc_path: Path) -> dict:
    """Parse the first ~80 lines of a PoC .sol file for metadata."""
    result = {
        "chain": None,
        "attacker_address": None,
        "attack_contract": None,
        "vulnerable_contract": None,
        "attack_tx": None,
        "post_mortem_links": [],
        "poc_loss_amount": None,
    }

    try:
        with open(poc_path, "r", encoding="utf-8", errors="replace") as f:
            header_lines = []
            for idx, line in enumerate(f):
                header_lines.append(line)
                if idx >= 120:  # Read first 120 lines
                    break
        header_text = "".join(header_lines)
    except (FileNotFoundError, PermissionError):
        return result

    # Chain detection
    chain_m = CHAIN_RE.search(header_text)
    if chain_m:
        raw_chain = chain_m.group(1).lower().strip()
        result["chain"] = CHAIN_ALIASES.get(raw_chain, raw_chain)

    # @KeyInfo style
    m = KEY_INFO_TOTAL_LOST_RE.search(header_text)
    if m:
        result["poc_loss_amount"] = m.group(1).strip()

    # Comment-based loss
    if not result["poc_loss_amount"]:
        m = TOTAL_LOSS_COMMENT_RE.search(header_text)
        if m:
            result["poc_loss_amount"] = m.group(1).strip()

    # Addresses
    m = ATTACKER_RE.search(header_text)
    if m:
        result["attacker_address"] = m.group(1).strip()

    m = ATTACK_CONTRACT_RE.search(header_text)
    if m:
        result["attack_contract"] = m.group(1).strip()

    m = VULN_CONTRACT_RE.search(header_text)
    if m:
        result["vulnerable_contract"] = m.group(1).strip()

    # TX hash
    m = ATTACK_TX_RE.search(header_text)
    if m:
        result["attack_tx"] = m.group(1).strip()
    if not result["attack_tx"]:
        m = TX_COMMENT_RE.search(header_text)
        if m:
            result["attack_tx"] = m.group(1).strip()

    # Post-mortem links
    for pm_m in re.finditer(POSTMORTEM_RE, header_text):
        url = pm_m.group(1).strip()
        if url and url not in result["post_mortem_links"]:
            result["post_mortem_links"].append(url)

    # GUY / reference links from header
    for guy_m in re.finditer(GUY_RE, header_text):
        url = guy_m.group(1).strip()
        if url and url not in result["post_mortem_links"]:
            result["post_mortem_links"].append(url)

    return result


def resolve_poc_path(entry: dict) -> Optional[Path]:
    """Try to find the actual PoC .sol file on disk."""
    if entry.get("poc_file_path"):
        # Try direct path
        direct = DEFIHACKLABS_DIR / entry["poc_file_path"]
        if direct.exists():
            return direct
        # Try with ./ prefix stripped
        alt = DEFIHACKLABS_DIR / entry["poc_file_path"].lstrip("./")
        if alt.exists():
            return alt

    # Fallback: search by protocol name in expected year-month folder
    date_str = entry.get("date", "")
    if len(date_str) == 8:
        year_month = f"{date_str[:4]}-{date_str[4:6]}"
        folder = POC_DIR / year_month
        if folder.exists():
            protocol = entry.get("protocol", "")
            # Try to find a matching file
            for sol_file in folder.glob("*_exp.sol"):
                if protocol.lower().replace(" ", "").replace("-", "") in sol_file.stem.lower().replace("_", ""):
                    return sol_file
    return None


def parse_loss_to_usd(loss_str: Optional[str]) -> float:
    """Best-effort parse of loss string to USD value for sorting."""
    if not loss_str:
        return 0.0

    loss_str = loss_str.strip().lower()

    # Remove common prefixes/suffixes
    loss_str = loss_str.replace("~", "").replace(">", "").replace("<", "").strip()
    loss_str = loss_str.replace("$", "").replace("usd", "").replace("usdt", "").replace("usdc", "").strip()

    # Handle "XM" (millions) and "XK" (thousands)
    m_match = re.search(r"([\d,\.]+)\s*m(?:illion)?", loss_str, re.IGNORECASE)
    if m_match:
        try:
            return float(m_match.group(1).replace(",", "")) * 1_000_000
        except ValueError:
            pass

    k_match = re.search(r"([\d,\.]+)\s*k", loss_str, re.IGNORECASE)
    if k_match:
        try:
            return float(k_match.group(1).replace(",", "")) * 1_000
        except ValueError:
            pass

    # Try plain number
    num_match = re.search(r"([\d,\.]+)", loss_str)
    if num_match:
        try:
            val = float(num_match.group(1).replace(",", ""))
            # Heuristic: if there's "million" or "M" context, scale
            if val < 1000 and ("million" in loss_str or "m " in loss_str):
                return val * 1_000_000
            return val
        except ValueError:
            pass

    return 0.0


# ─── Main Pipeline ────────────────────────────────────────────────────────────

def main():
    all_entries = []

    print(f"[*] Parsing {len(README_FILES)} README files...")
    for readme in README_FILES:
        entries = parse_readme(readme)
        print(f"    {readme.parent.name}/README.md: {len(entries)} entries")
        all_entries.extend(entries)

    print(f"\n[*] Total README entries extracted: {len(all_entries)}")

    # Parse PoC headers
    poc_found = 0
    poc_missing = 0

    print(f"\n[*] Parsing PoC file headers...")
    for entry in all_entries:
        poc_path = resolve_poc_path(entry)
        if poc_path:
            poc_found += 1
            poc_data = parse_poc_header(poc_path)
            entry["poc_resolved_path"] = str(poc_path.relative_to(DEFIHACKLABS_DIR))
            entry.update(poc_data)
        else:
            poc_missing += 1
            entry["poc_resolved_path"] = None
            entry["chain"] = None
            entry["attacker_address"] = None
            entry["attack_contract"] = None
            entry["vulnerable_contract"] = None
            entry["attack_tx"] = None
            entry["post_mortem_links"] = entry.get("reference_links", [])
            entry["poc_loss_amount"] = None

    print(f"    PoC resolved: {poc_found}/{len(all_entries)}")
    print(f"    PoC missing:  {poc_missing}/{len(all_entries)}")

    # Add parsed loss USD for sorting
    for entry in all_entries:
        loss_str = entry.get("poc_loss_amount") or entry.get("loss_amount", "")
        entry["loss_usd_estimate"] = parse_loss_to_usd(loss_str)

    # Sort by loss amount descending
    all_entries.sort(key=lambda e: e["loss_usd_estimate"], reverse=True)

    # Assign unique IDs
    for i, entry in enumerate(all_entries):
        entry["id"] = i + 1

    # Write output
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_entries, f, indent=2, ensure_ascii=False)

    print(f"\n[✓] Wrote {len(all_entries)} entries to {OUTPUT_FILE}")

    # Summary statistics
    chains = {}
    labels = {}
    years = {}
    for entry in all_entries:
        chain = entry.get("chain") or "unknown"
        chains[chain] = chains.get(chain, 0) + 1

        label = entry.get("raw_vuln_label", "unknown")
        labels[label] = labels.get(label, 0) + 1

        year = entry.get("year", "unknown")
        years[year] = years.get(year, 0) + 1

    print(f"\n[*] Chain distribution:")
    for chain, count in sorted(chains.items(), key=lambda x: -x[1])[:15]:
        print(f"    {chain}: {count}")

    print(f"\n[*] Year distribution:")
    for year, count in sorted(years.items()):
        print(f"    {year}: {count}")

    print(f"\n[*] Top 20 vulnerability labels:")
    for label, count in sorted(labels.items(), key=lambda x: -x[1])[:20]:
        print(f"    [{count:3d}] {label}")

    # Count null fields
    null_counts = {}
    for field in ["protocol", "date", "loss_amount", "poc_file_path", "chain"]:
        null_counts[field] = sum(1 for e in all_entries if not e.get(field))
    print(f"\n[*] Null field counts:")
    for field, count in null_counts.items():
        pct = count / len(all_entries) * 100
        print(f"    {field}: {count} ({pct:.1f}%)")


if __name__ == "__main__":
    main()
