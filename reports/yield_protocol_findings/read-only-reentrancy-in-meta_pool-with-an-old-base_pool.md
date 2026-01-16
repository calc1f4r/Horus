---
# Core Classification
protocol: Curve Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27689
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/StableSwapNG/README.md#3-read-only-reentrancy-in-meta_pool-with-an-old-base_pool
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Read-only reentrancy in meta_pool with an old base_pool

### Overview


This bug report is about a possible read-only reentrancy attack in the CurveStableSwapFactoryNG contract. The attack is possible when an old base pool, which is paired with ETH, is added to the meta_pool. When this happens, the virtual price of the base pool LP token can be manipulated, which can lead to funds loss. The bug has been given a critical severity level due to the potential for funds loss. The recommendation is to add checks to the CurveStableSwapFactoryNG contract when base pools are added, so that pools paired with ETH cannot be added.

### Original Finding Content

##### Description
Old base pools cannot be added to CurveStableSwapFactory. Using an old base pool in meta_pool can lead to read-only reentrancy attacks because of the possible manipulation of the virtual price of a base pool LP token. There is a possible read-only reentrancy attack with a call to `get_virtual_price` in a metapool (At the line https://github.com/curvefi/stableswap-ng/blob/8c78731ed43c22e6bcdcb5d39b0a7d02f8cb0386/contracts/main/CurveStableSwapMetaNG.vy#L457). Virtual price can be incorrectly increased, and that rate can be used during a swap from base pool LP to the second coin in metapool. It will work with old base pools that use ETH (new ones have a reentrancy lock on the `get_virtual_price` function).
This issue has been assigned a CRITICAL severity level because working with old base pools that contain ETH will lead to rate manipulation and funds loss (exchanging tokens using manipulated prices).

##### Recommendation
We recommend adding checks to the `CurveStableSwapFactoryNG` contract when base pools are added. It shouldn't be possible to add pools paired with ETH.


***

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Curve Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/StableSwapNG/README.md#3-read-only-reentrancy-in-meta_pool-with-an-old-base_pool
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

