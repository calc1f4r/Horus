#!/usr/bin/env python3
"""
Solodit Vulnerability Fetcher Tool
==================================
Fetches security findings from Cyfrin Solodit API and saves them as markdown files
following the Horus template format.

Usage:
    python solodit_fetcher.py --keywords "pyth oracle" --output ./oracle
    python solodit_fetcher.py --tags Oracle --impact HIGH MEDIUM --max-results 50
    python solodit_fetcher.py --keywords "reentrancy" --quality 3 --output ./reentrancy
"""

import os
import re
import json
import time
import argparse
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://solodit.cyfrin.io/api/v1/solodit"
FINDINGS_ENDPOINT = f"{BASE_URL}/findings"

# Rate limit: 20 requests per 60 seconds
RATE_LIMIT_DELAY = 3.5  # seconds between requests to stay safe


def sanitize_filename(title: str) -> str:
    """Convert title to a safe filename."""
    # Remove special characters and limit length
    safe = re.sub(r'[^\w\s-]', '', title.lower())
    safe = re.sub(r'[-\s]+', '-', safe).strip('-')
    return safe[:80] if len(safe) > 80 else safe


def extract_tags(finding: dict) -> list:
    """Extract tags from finding."""
    tags = []
    if finding.get("issues_issuetagscore"):
        for tag_score in finding["issues_issuetagscore"]:
            if tag_score.get("tags_tag", {}).get("title"):
                tags.append(tag_score["tags_tag"]["title"])
    return tags


def extract_finders(finding: dict) -> list:
    """Extract finder handles from finding."""
    finders = []
    if finding.get("issues_issue_finders"):
        for finder in finding["issues_issue_finders"]:
            if finder.get("wardens_warden", {}).get("handle"):
                finders.append(finder["wardens_warden"]["handle"])
    return finders


def extract_protocol_categories(finding: dict) -> list:
    """Extract protocol categories from finding."""
    categories = []
    protocol = finding.get("protocols_protocol")
    if protocol and protocol.get("protocols_protocolcategoryscore"):
        for cat_score in protocol["protocols_protocolcategoryscore"]:
            if cat_score.get("protocols_protocolcategory", {}).get("title"):
                categories.append(cat_score["protocols_protocolcategory"]["title"])
    return categories


def finding_to_markdown(finding: dict) -> str:
    """Convert a Solodit finding to markdown format following the template."""
    
    tags = extract_tags(finding)
    finders = extract_finders(finding)
    protocol_categories = extract_protocol_categories(finding)
    
    # Determine category from tags
    category = "uncategorized"
    category_mappings = {
        "oracle": ["Oracle", "Price Manipulation", "Chainlink", "Pyth"],
        "reentrancy": ["Reentrancy", "Cross-Function Reentrancy", "Read-Only Reentrancy"],
        "access_control": ["Access Control", "Authorization", "Privilege Escalation"],
        "arithmetic": ["Integer Overflow", "Integer Underflow", "Precision Loss", "Rounding"],
        "logic": ["Logic Error", "Business Logic", "Validation"],
        "economic": ["Flash Loan", "Front-running", "MEV", "Sandwich Attack"],
        "dos": ["DOS", "Denial of Service", "Griefing"],
    }
    
    for cat, keywords in category_mappings.items():
        if any(kw.lower() in [t.lower() for t in tags] for kw in keywords):
            category = cat
            break
    
    # Build frontmatter
    frontmatter = f"""---
# Core Classification
protocol: {finding.get("protocol_name") or "unknown"}
chain: everychain
category: {category}
vulnerability_type: {tags[0].lower().replace(" ", "_") if tags else "unknown"}

# Attack Vector Details
attack_type: {tags[0].lower().replace(" ", "_") if tags else "unknown"}
affected_component: {"oracle" if "oracle" in category else "smart_contract"}

# Source Information
source: solodit
solodit_id: {finding.get("id", "unknown")}
audit_firm: {finding.get("firm_name") or "unknown"}
contest_link: {finding.get("contest_link") or "none"}
source_link: {finding.get("source_link") or "none"}
github_link: {finding.get("github_link") or "none"}

# Impact Classification
severity: {finding.get("impact", "MEDIUM").lower()}
impact: security_vulnerability
exploitability: {finding.get("quality_score", 3) / 5:.2f}
financial_impact: {"high" if finding.get("impact") == "HIGH" else "medium" if finding.get("impact") == "MEDIUM" else "low"}

# Scoring
quality_score: {finding.get("quality_score", 0)}
rarity_score: {finding.get("general_score", 0)}

# Context Tags
tags:
"""
    
    for tag in tags[:10]:  # Limit to 10 tags
        frontmatter += f"  - {tag.lower().replace(' ', '_')}\n"
    
    if protocol_categories:
        frontmatter += "\nprotocol_categories:\n"
        for cat in protocol_categories[:5]:
            frontmatter += f"  - {cat.lower().replace(' ', '_')}\n"
    
    frontmatter += f"""
# Audit Details
report_date: {finding.get("report_date") or "unknown"}
finders_count: {finding.get("finders_count", 0)}
finders:
"""
    
    for finder in finders[:5]:  # Limit to 5 finders
        frontmatter += f"  - {finder}\n"
    
    frontmatter += "---\n"
    
    # Build content
    content = finding.get("content", "No content available.")
    title = finding.get("title", "Unknown Vulnerability")
    summary = finding.get("summary") or ""
    
    markdown = f"""{frontmatter}
## Vulnerability Title

{title}

### Overview

{summary if summary else "See description below for full details."}

### Original Finding Content

{content}

### Metadata

| Field | Value |
|-------|-------|
| Impact | {finding.get("impact", "N/A")} |
| Quality Score | {finding.get("quality_score", "N/A")}/5 |
| Rarity Score | {finding.get("general_score", "N/A")}/5 |
| Audit Firm | {finding.get("firm_name") or "N/A"} |
| Protocol | {finding.get("protocol_name") or "N/A"} |
| Report Date | {finding.get("report_date") or "N/A"} |
| Finders | {", ".join(finders) if finders else "N/A"} |

### Source Links

- **Source**: {finding.get("source_link") or "N/A"}
- **GitHub**: {finding.get("github_link") or "N/A"}
- **Contest**: {finding.get("contest_link") or "N/A"}

### Keywords for Search

`{", ".join(tags[:15]) if tags else "vulnerability"}`

"""
    
    return markdown


class SoloditFetcher:
    """Fetches and saves Solodit findings."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or API_KEY
        if not self.api_key:
            raise ValueError("API key is required. Set API_KEY in .env or pass directly.")
        
        self.headers = {
            "Content-Type": "application/json",
            "X-Cyfrin-API-Key": self.api_key
        }
        self.rate_limit_remaining = 20
        self.rate_limit_reset = 0
    
    def _handle_rate_limit(self, response: requests.Response):
        """Update rate limit info from response headers."""
        self.rate_limit_remaining = int(response.headers.get("X-RateLimit-Remaining", 20))
        self.rate_limit_reset = int(response.headers.get("X-RateLimit-Reset", 0))
        
        if self.rate_limit_remaining < 3:
            wait_time = max(self.rate_limit_reset - time.time(), 5)
            print(f"⏳ Rate limit low ({self.rate_limit_remaining} remaining). Waiting {wait_time:.0f}s...")
            time.sleep(wait_time)
    
    def search_findings(
        self,
        keywords: str = None,
        impact: list = None,
        tags: list = None,
        firms: list = None,
        protocol: str = None,
        protocol_category: list = None,
        languages: list = None,
        quality_score: int = 1,
        rarity_score: int = 1,
        reported: str = "alltime",
        sort_field: str = "Quality",
        sort_direction: str = "Desc",
        page: int = 1,
        page_size: int = 50
    ) -> dict:
        """Search Solodit findings with filters."""
        
        filters = {
            "qualityScore": quality_score,
            "rarityScore": rarity_score,
            "sortField": sort_field,
            "sortDirection": sort_direction,
            "reported": {"value": reported}
        }
        
        if keywords:
            filters["keywords"] = keywords
        
        if impact:
            filters["impact"] = impact
        
        if tags:
            filters["tags"] = [{"value": t} for t in tags]
        
        if firms:
            filters["firms"] = [{"value": f} for f in firms]
        
        if protocol:
            filters["protocol"] = protocol
        
        if protocol_category:
            filters["protocolCategory"] = [{"value": c} for c in protocol_category]
        
        if languages:
            filters["languages"] = [{"value": l} for l in languages]
        
        payload = {
            "page": page,
            "pageSize": page_size,
            "filters": filters
        }
        
        response = requests.post(
            FINDINGS_ENDPOINT,
            headers=self.headers,
            json=payload
        )
        
        if response.status_code == 429:
            print("⚠️  Rate limit exceeded. Waiting 60 seconds...")
            time.sleep(60)
            return self.search_findings(**{k: v for k, v in locals().items() if k != 'self'})
        
        response.raise_for_status()
        self._handle_rate_limit(response)
        
        return response.json()
    
    def fetch_all_findings(
        self,
        max_results: int = 100,
        **search_kwargs
    ) -> list:
        """Fetch all findings matching criteria up to max_results."""
        
        all_findings = []
        page = 1
        page_size = min(100, max_results)
        
        while len(all_findings) < max_results:
            print(f"📥 Fetching page {page}...")
            
            try:
                data = self.search_findings(
                    page=page,
                    page_size=page_size,
                    **search_kwargs
                )
            except requests.exceptions.HTTPError as e:
                print(f"❌ Error fetching page {page}: {e}")
                break
            
            findings = data.get("findings", [])
            metadata = data.get("metadata", {})
            
            if not findings:
                break
            
            all_findings.extend(findings)
            
            print(f"   Got {len(findings)} findings. Total: {len(all_findings)}/{metadata.get('totalResults', '?')}")
            
            if page >= metadata.get("totalPages", 1):
                break
            
            if len(all_findings) >= max_results:
                break
            
            page += 1
            time.sleep(RATE_LIMIT_DELAY)
        
        return all_findings[:max_results]
    
    def save_findings(
        self,
        findings: list,
        output_dir: str = "./findings",
        format: str = "markdown"
    ) -> list:
        """Save findings to files."""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        saved_files = []
        
        for i, finding in enumerate(findings, 1):
            title = finding.get("title", f"finding-{finding.get('id', i)}")
            filename = f"{sanitize_filename(title)}.md"
            filepath = output_path / filename
            
            # Skip if the finding already exists
            if filepath.exists():
                print(f"⚠️  Skipping duplicate: {filepath.name}")
                continue
            
            if format == "markdown":
                content = finding_to_markdown(finding)
            elif format == "json":
                filepath = filepath.with_suffix(".json")
                content = json.dumps(finding, indent=2, default=str)
            else:
                content = finding_to_markdown(finding)
            
            filepath.write_text(content, encoding="utf-8")
            saved_files.append(str(filepath))
            print(f"✅ Saved: {filepath.name}")
        
        return saved_files


def main():
    parser = argparse.ArgumentParser(
        description="Fetch security findings from Solodit API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --keywords "pyth oracle" --output ./oracle
  %(prog)s --tags Oracle --impact HIGH MEDIUM --max-results 50
  %(prog)s --keywords "reentrancy" --quality 3 --output ./reentrancy
  %(prog)s --firms Cyfrin Sherlock --impact HIGH --output ./high-severity
  %(prog)s --protocol-category DeFi --tags "Flash Loan" --output ./flash-loans
        """
    )
    
    # Search filters
    parser.add_argument(
        "--keywords", "-k",
        type=str,
        help="Search keywords (searches title and content)"
    )
    parser.add_argument(
        "--impact", "-i",
        nargs="+",
        choices=["HIGH", "MEDIUM", "LOW", "GAS"],
        default=["HIGH", "MEDIUM"],
        help="Impact levels to filter (default: HIGH MEDIUM)"
    )
    parser.add_argument(
        "--tags", "-t",
        nargs="+",
        help="Tags to filter by (e.g., Oracle, Reentrancy, 'Access Control')"
    )
    parser.add_argument(
        "--firms", "-f",
        nargs="+",
        help="Audit firms to filter by (e.g., Cyfrin, Sherlock, Code4rena)"
    )
    parser.add_argument(
        "--protocol", "-p",
        type=str,
        help="Protocol name to filter by"
    )
    parser.add_argument(
        "--protocol-category",
        nargs="+",
        help="Protocol categories (e.g., DeFi, NFT, Lending)"
    )
    parser.add_argument(
        "--languages", "-l",
        nargs="+",
        help="Programming languages (e.g., Solidity, Rust, Cairo)"
    )
    
    # Quality filters
    parser.add_argument(
        "--quality", "-q",
        type=int,
        default=1,
        choices=[1, 2, 3, 4, 5],
        help="Minimum quality score (1-5, default: 1)"
    )
    parser.add_argument(
        "--rarity",
        type=int,
        default=1,
        choices=[1, 2, 3, 4, 5],
        help="Minimum rarity score (1-5, default: 1)"
    )
    
    # Time filters
    parser.add_argument(
        "--reported",
        choices=["30", "60", "90", "alltime"],
        default="alltime",
        help="Time period for reported findings (default: alltime)"
    )
    
    # Sorting
    parser.add_argument(
        "--sort-by",
        choices=["Recency", "Quality", "Rarity"],
        default="Quality",
        help="Sort field (default: Quality)"
    )
    parser.add_argument(
        "--sort-dir",
        choices=["Desc", "Asc"],
        default="Desc",
        help="Sort direction (default: Desc)"
    )
    
    # Output options
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="./findings",
        help="Output directory for saved findings (default: ./findings)"
    )
    parser.add_argument(
        "--max-results", "-m",
        type=int,
        default=50,
        help="Maximum number of results to fetch (default: 50)"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)"
    )
    
    # Other
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be fetched without saving"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="API key (overrides .env)"
    )
    
    args = parser.parse_args()
    
    try:
        fetcher = SoloditFetcher(api_key=args.api_key)
        
        print(f"🔍 Searching Solodit...")
        print(f"   Keywords: {args.keywords or 'any'}")
        print(f"   Impact: {args.impact}")
        print(f"   Tags: {args.tags or 'any'}")
        print(f"   Quality >= {args.quality}")
        print(f"   Max results: {args.max_results}")
        print()
        
        findings = fetcher.fetch_all_findings(
            max_results=args.max_results,
            keywords=args.keywords,
            impact=args.impact,
            tags=args.tags,
            firms=args.firms,
            protocol=args.protocol,
            protocol_category=args.protocol_category,
            languages=args.languages,
            quality_score=args.quality,
            rarity_score=args.rarity,
            reported=args.reported,
            sort_field=args.sort_by,
            sort_direction=args.sort_dir
        )
        
        print(f"\n📊 Found {len(findings)} findings")
        
        if args.dry_run:
            print("\n🔍 Dry run - findings would be saved:")
            for f in findings[:10]:
                print(f"   [{f.get('impact')}] {f.get('title')[:60]}...")
            if len(findings) > 10:
                print(f"   ... and {len(findings) - 10} more")
            return
        
        if findings:
            print(f"\n💾 Saving to {args.output}...")
            saved = fetcher.save_findings(
                findings,
                output_dir=args.output,
                format=args.format
            )
            print(f"\n✅ Saved {len(saved)} files to {args.output}")
        else:
            print("❌ No findings matched the criteria")
    
    except ValueError as e:
        print(f"❌ Error: {e}")
        return 1
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main() or 0)
