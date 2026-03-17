#!/usr/bin/env python3
"""
Download Move-related (Sui, Aptos, Movement) audit reports from OtterSec's
public Notion page using Playwright for browser automation.
"""

import json
import os
import re
import time
import requests
from pathlib import Path
from playwright.sync_api import sync_playwright

NOTION_URL = "https://ottersec.notion.site/Sampled-Public-Audit-Reports-a296e98838aa4fdb8f3b192663400772"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "reports" / "ottersec_move_audits"

# Keywords identifying Move-ecosystem chains
MOVE_CHAINS = {"sui", "aptos", "movement"}


def is_move_related(chain_text: str) -> bool:
    """Check if the chain field indicates a Move-ecosystem project."""
    lower = chain_text.lower()
    return any(kw in lower for kw in MOVE_CHAINS)


def scrape_notion_table(page):
    """
    Scroll through the Notion database table and collect all rows.
    Returns list of dicts with name, chain, type, pdf_filename, date, etc.
    """
    # Wait for table to load
    page.wait_for_selector(".notion-table-view", timeout=30000)
    time.sleep(3)

    rows = []
    seen = set()

    # Scroll the table to load all rows (Notion uses virtual scrolling)
    scroller = page.query_selector(".notion-scroller.vertical")
    if not scroller:
        scroller = page.query_selector(".notion-table-view")

    for _ in range(150):  # scroll iterations
        row_els = page.query_selector_all(".notion-table-view .notion-collection-item")
        for row_el in row_els:
            cells = row_el.query_selector_all(".notion-table-cell, [style*='width']")
            text = row_el.inner_text().strip()
            if text and text not in seen:
                seen.add(text)
                rows.append({"raw": text, "element": row_el})

        # Scroll down
        page.evaluate("""
            const el = document.querySelector('.notion-scroller.vertical') ||
                       document.querySelector('.notion-table-view');
            if (el) el.scrollTop += 600;
        """)
        time.sleep(0.3)

    return rows


def extract_pdf_links_from_page(page):
    """
    Alternative approach: find all links/file references on the page.
    """
    # Get all anchor elements with .pdf references
    links = page.evaluate("""
        () => {
            const results = [];
            // Check all text content for .pdf filenames
            const allText = document.body.innerText;
            const pdfPattern = /[\\w_-]+\\.pdf/g;
            const matches = allText.match(pdfPattern) || [];
            return [...new Set(matches)];
        }
    """)
    return links


def get_entries_via_scrolling(page):
    """
    Collect all entries by scrolling the Notion page and parsing visible rows.
    Returns list of dicts: {name, chain, pdf_filename}
    """
    print("Scrolling to load all entries...")
    # Don't use networkidle - Notion never stops making requests
    time.sleep(8)

    all_entries = []
    seen_pdfs = set()
    last_count = 0
    stale_rounds = 0

    for i in range(200):
        # Extract current visible entries
        entries = page.evaluate("""
            () => {
                const items = [];
                // Find all collection items (table rows)
                const rows = document.querySelectorAll(
                    '.notion-collection-item, [data-block-id]'
                );
                rows.forEach(row => {
                    const text = row.innerText || '';
                    // Look for PDF filename pattern
                    const pdfMatch = text.match(/([\\w_.-]+\\.pdf)/);
                    if (pdfMatch) {
                        items.push({
                            text: text.trim().substring(0, 500),
                            pdf: pdfMatch[1]
                        });
                    }
                });
                return items;
            }
        """)

        for entry in entries:
            pdf = entry["pdf"]
            if pdf not in seen_pdfs:
                seen_pdfs.add(pdf)
                all_entries.append(entry)

        if len(seen_pdfs) == last_count:
            stale_rounds += 1
            if stale_rounds > 30:
                break
        else:
            stale_rounds = 0
            last_count = len(seen_pdfs)

        # Scroll page
        page.evaluate("window.scrollBy(0, 800)")
        time.sleep(0.4)

        if (i + 1) % 20 == 0:
            print(f"  Scroll {i+1}: found {len(seen_pdfs)} PDFs so far...")

    print(f"Total unique PDF entries found: {len(all_entries)}")
    return all_entries


def click_pdf_and_get_url(page, pdf_filename):
    """
    Click on a PDF link in Notion and capture the download URL from the
    resulting navigation or popup.
    """
    # Try to find and click the PDF link
    try:
        link = page.query_selector(f'text="{pdf_filename}"')
        if link:
            with page.expect_popup() as popup_info:
                link.click()
            popup = popup_info.value
            url = popup.url
            popup.close()
            return url
    except Exception:
        pass
    return None


def try_notion_api_approach():
    """
    Try using the unofficial Notion API to get database entries.
    The database ID from the consolidated table URL.
    """
    db_id = "22c75b20d2514ca2a36b1f70b38093f9"

    # Try splitbee API (unofficial but public)
    try:
        resp = requests.get(
            f"https://notion-api.splitbee.io/v1/table/{db_id}",
            timeout=30
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"Splitbee API failed: {e}")

    # Try Notion's own public API endpoint
    try:
        resp = requests.post(
            f"https://www.notion.so/api/v3/queryCollection",
            json={
                "collection": {"id": db_id},
                "collectionView": {"id": "3632425278e54a788d8b8177a842b51a"},
                "loader": {
                    "type": "table",
                    "limit": 500,
                    "searchQuery": "",
                    "userTimeZone": "UTC",
                    "loadContentCover": False,
                }
            },
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"Notion API v3 failed: {e}")

    return None


def download_pdfs_via_playwright(move_entries):
    """
    For each Move-related entry, navigate to its Notion row,
    click the PDF link, and capture the signed S3 URL for download.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        page.goto(NOTION_URL, wait_until="networkidle")
        time.sleep(5)

        downloaded = []
        for entry in move_entries:
            pdf_name = entry["pdf"]
            out_path = OUTPUT_DIR / pdf_name

            if out_path.exists():
                print(f"  Already exists: {pdf_name}")
                downloaded.append(str(out_path))
                continue

            print(f"  Trying to download: {pdf_name}")

            # Approach: click on the PDF text to trigger download
            try:
                # Find the PDF text element
                el = page.locator(f'text="{pdf_name}"').first
                if el.count() == 0:
                    # Try partial match
                    base = pdf_name.replace(".pdf", "")
                    el = page.locator(f'text="{base}"').first

                if el.count() > 0:
                    # Set up download handler
                    with page.expect_download(timeout=30000) as download_info:
                        el.click()
                    download = download_info.value
                    download.save_as(str(out_path))
                    print(f"  ✓ Downloaded: {pdf_name}")
                    downloaded.append(str(out_path))
                else:
                    print(f"  ✗ Could not find element for: {pdf_name}")
            except Exception as e:
                print(f"  ✗ Failed to download {pdf_name}: {e}")

            time.sleep(1)

        browser.close()

    return downloaded


def main():
    print("=" * 60)
    print("OtterSec Move Audit Reports Downloader")
    print("=" * 60)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Step 1: Try API approach first
    print("\n[1] Trying Notion API approach...")
    api_data = try_notion_api_approach()
    if api_data:
        print(f"  Got API data with {len(api_data) if isinstance(api_data, list) else 'unknown'} entries")
        with open(OUTPUT_DIR / "_api_response.json", "w") as f:
            json.dump(api_data, f, indent=2)

    # Step 2: Use Playwright to scrape table
    print("\n[2] Launching browser to scrape Notion page...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        # Capture all network requests for PDF URLs
        pdf_urls = {}

        def handle_response(response):
            url = response.url
            if ".pdf" in url or "secure.notion-static.com" in url or "prod-files-secure" in url:
                pdf_urls[url.split("?")[0].split("/")[-1]] = url

        page.on("response", handle_response)

        print("  Navigating to Notion page...")
        page.goto(NOTION_URL, wait_until="domcontentloaded", timeout=60000)
        # Give Notion JS time to render the table
        time.sleep(10)

        # Collect all entries via scrolling
        all_entries = get_entries_via_scrolling(page)

        # Filter Move-related entries
        move_entries = []
        for entry in all_entries:
            text = entry["text"].lower()
            if any(kw in text for kw in MOVE_CHAINS):
                move_entries.append(entry)

        print(f"\n[3] Found {len(move_entries)} Move-related entries:")
        for e in move_entries:
            first_line = e["text"].split("\n")[0][:80]
            print(f"  - {e['pdf']}: {first_line}")

        # Save the list
        with open(OUTPUT_DIR / "_move_entries.json", "w") as f:
            json.dump(move_entries, f, indent=2)

        # Step 3: Click each PDF to trigger download
        print(f"\n[4] Downloading {len(move_entries)} PDFs...")
        downloaded = []

        for entry in move_entries:
            pdf_name = entry["pdf"]
            out_path = OUTPUT_DIR / pdf_name

            if out_path.exists():
                print(f"  Already exists: {pdf_name}")
                downloaded.append(str(out_path))
                continue

            print(f"  Downloading: {pdf_name}...")
            try:
                # Find the PDF text on page and click it
                loc = page.get_by_text(pdf_name, exact=False)
                if loc.count() > 0:
                    with page.expect_download(timeout=30000) as dl_info:
                        loc.first.click()
                    dl = dl_info.value
                    dl.save_as(str(out_path))
                    print(f"  ✓ Saved: {pdf_name}")
                    downloaded.append(str(out_path))
                else:
                    print(f"  ✗ PDF text not found: {pdf_name}")
            except Exception as e:
                print(f"  ✗ Error: {pdf_name}: {e}")

            time.sleep(1)

        browser.close()

    print(f"\n[5] Summary:")
    print(f"  Total Move entries: {len(move_entries)}")
    print(f"  Downloaded: {len(downloaded)}")
    print(f"  Output dir: {OUTPUT_DIR}")

    return move_entries, downloaded


if __name__ == "__main__":
    main()
