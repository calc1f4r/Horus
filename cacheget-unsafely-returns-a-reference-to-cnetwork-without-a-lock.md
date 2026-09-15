---
# Core Classification
protocol: Omni Halo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41500
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Omni-Halo-Spearbit-Security-Review-August-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Omni-Halo-Spearbit-Security-Review-August-2024.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Dtheo
  - Shotes
  - Justin Traglia
---

## Vulnerability Title

cache::Get() unsafely returns a reference to c.network without a lock

### Overview


A bug has been found in the code for a network cache. This bug is considered to be of medium risk and can potentially cause memory corruption. The problem occurs in the cache.go file at line 34, specifically in the Get() function. This function returns a pointer to the network object and releases its lock when the function ends. However, this can lead to race conditions and memory corruption when the function is called periodically by the getLatestPortals() function. The recommended solution is to either return a copy of the network object or create thread safe getter routines for the cache object. This bug has been fixed in version 60904774 and has been verified by Spearbit. 

### Original Finding Content

## Cache Vulnerability Report

**Severity:** Medium Risk  
**Context:** `cache.go#L34`  
**Description:**  
(c *cache) `Get()` returns a pointer to `c.network` and releases its lock upon the function return. This function is called periodically by `(k Keeper) getLatestPortals()`, which will dereference the pointer when it calls `network.GetPortals()`. This makes the node vulnerable to race conditions and thus memory corruption.  

**Recommendation:**  
Return a copy of the network object or create thread-safe getter routines for the cache object.  

**Omni:** Fixed in 60904774 as recommended.  
**Spearbit:** Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Omni Halo |
| Report Date | N/A |
| Finders | Dtheo, Shotes, Justin Traglia |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Omni-Halo-Spearbit-Security-Review-August-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Omni-Halo-Spearbit-Security-Review-August-2024.pdf

### Keywords for Search

`vulnerability`

