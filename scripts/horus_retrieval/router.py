"""Router artifact builders for Horus retrieval generation."""

from __future__ import annotations

from horus_retrieval.protocol_context import router_protocol_mappings


def build_lean_router(manifests):
    """Build the lean router index.json that points to manifests."""
    router = {
        "meta": {
            "description": "Horus Router - lightweight entry point for agents",
            "version": "3.0.0",
            "generated": "2026-02-13",
            "architecture": "Tiered search: router (this file) → manifests (DB/manifests/*.json) → vulnerability files (DB/**/*.md)",
            "usage": "1) Identify category from protocolContext or keywords. 2) Load the relevant manifest. 3) Find specific patterns with line ranges. 4) Read only those lines from the .md file.",
        },
        "searchStrategy": {
            "description": "How agents should search this database for maximum precision",
            "steps": [
                {
                    "step": 1,
                    "action": "Identify category",
                    "detail": "Use protocolContext to match the protocol type being audited, OR use quickKeywords to find the right category",
                },
                {
                    "step": 2,
                    "action": "Load category manifest",
                    "detail": "Read DB/manifests/<category>.json (much smaller than this file). Each manifest has pattern-level entries with exact line ranges.",
                },
                {
                    "step": 3,
                    "action": "Find specific patterns",
                    "detail": "Search manifest patterns by title, severity, codeKeywords, and searchKeywords. Each pattern has lineStart/lineEnd.",
                },
                {
                    "step": 4,
                    "action": "Read targeted content",
                    "detail": "Use read_file with lineStart/lineEnd to read ONLY the relevant section. Do NOT read entire files.",
                },
            ],
        },
        "manifests": {},
        "protocolContext": {},
        "auditChecklist": {},
    }

    for cat_name, manifest in manifests.items():
        router["manifests"][cat_name] = {
            "file": f"DB/manifests/{cat_name}.json",
            "description": manifest["meta"]["description"],
            "fileCount": manifest["meta"]["fileCount"],
            "totalPatterns": manifest["meta"]["totalPatterns"],
        }

    return router


def add_protocol_context(router):
    """Add protocol context mappings with manifest references."""
    router["protocolContext"] = {
        "description": "Map protocol type → relevant manifests + priority patterns. Load the manifest file, then search for patterns matching your codebase.",
        "mappings": router_protocol_mappings(),
    }


def add_audit_checklist(router):
    """Add the audit checklist."""
    router["auditChecklist"] = {
        "description": "Quick checklist items organized by vulnerability type",
        "general": [
            "Check all external calls for reentrancy",
            "Verify slippage protection on all swaps",
            "Check oracle staleness and manipulation vectors",
            "Verify access control on sensitive functions",
            "Check for first depositor/inflation attacks on vaults",
            "Verify rounding direction favors the protocol",
        ],
        "oracle": [
            "Check staleness validation (updatedAt, publishTime)",
            "Verify L2 sequencer uptime checks",
            "Check circuit breaker bounds (minAnswer/maxAnswer)",
            "Verify decimal handling",
            "Check for same-transaction manipulation (Pyth)",
        ],
        "amm": [
            "Check slippage parameters",
            "Verify deadline enforcement",
            "Check for spot price manipulation (slot0)",
            "Verify MINIMUM_LIQUIDITY or equivalent",
            "Check for sandwich attack vectors",
        ],
        "bridge": [
            "Verify message authentication",
            "Check for replay attack protection",
            "Verify gas limit configuration",
            "Check refund address handling",
            "Verify channel blocking recovery",
        ],
        "vault": [
            "Check first depositor attack protection",
            "Verify rounding direction (favor vault)",
            "Check fee handling consistency",
            "Verify ERC4626 compliance",
            "Check for reentrancy in deposit/withdraw",
        ],
    }

