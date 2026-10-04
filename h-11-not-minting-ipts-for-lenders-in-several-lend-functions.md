---
# Core Classification
protocol: Illuminate
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25279
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-illuminate
source_link: https://code4rena.com/reports/2022-06-illuminate
github_link: https://github.com/code-423n4/2022-06-illuminate-findings/issues/391

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-11] Not minting iPTs for lenders in several lend functions

### Overview


A bug was reported in the code-423n4/2022-06-illuminate repository. It was reported by Metatron and also found by other users. The bug causes loss of funds to the lender when using any of the "lend" functions mentioned. The bug is that funds are transferred from the lender but no iPTs (illuminate PTs) are sent back to the lender. This makes lending via these external PTs unusable. 

The bug was confirmed by sourabhmarathe from the Illuminate team. The recommended mitigation step is to mint the appropriate amount of iPTs to the lender, like in the rest of the lend functions.

### Original Finding Content

_Submitted by Metatron, also found by 0x52, auditor0517, cccz, datapunk, hansfriese, hyh, kenzo, kirk-baird, shenwilly, unforgiven, and WatchPug_

<https://github.com/code-423n4/2022-06-illuminate/blob/912be2a90ded4a557f121fe565d12ec48d0c4684/lender/Lender.sol#L247-L305>

<https://github.com/code-423n4/2022-06-illuminate/blob/912be2a90ded4a557f121fe565d12ec48d0c4684/lender/Lender.sol#L317-L367>

<https://github.com/code-423n4/2022-06-illuminate/blob/912be2a90ded4a557f121fe565d12ec48d0c4684/lender/Lender.sol#L192-L235>

### Impact

Using any of the `lend` function mentioned, will result in loss of funds to the lender - as the funds are transferred from them but no iPTs are sent back to them!

Basically making lending via these external PTs unusable.

### Proof of Concept

There is no minting of iPTs to the lender (or at all) in the 2 `lend` functions below:<br>
<https://github.com/code-423n4/2022-06-illuminate/blob/912be2a90ded4a557f121fe565d12ec48d0c4684/lender/Lender.sol#L247-L305>

<https://github.com/code-423n4/2022-06-illuminate/blob/912be2a90ded4a557f121fe565d12ec48d0c4684/lender/Lender.sol#L317-L367>

Corresponding to lending of (respectively):<br>
swivel<br>
element<br>

Furthermore, in:<br>
<https://github.com/code-423n4/2022-06-illuminate/blob/912be2a90ded4a557f121fe565d12ec48d0c4684/lender/Lender.sol#L227-L234><br>
Comment says "Purchase illuminate PTs directly to msg.sender", but this is not happening. sending yield PTs at best.

### Recommended Mitigation Steps

Mint the appropriate amount of iPTs to the lender - like in the rest of the lend functions.

**[sourabhmarathe (Illuminate) confirmed](https://github.com/code-423n4/2022-06-illuminate-findings/issues/391)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Illuminate |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-illuminate
- **GitHub**: https://github.com/code-423n4/2022-06-illuminate-findings/issues/391
- **Contest**: https://code4rena.com/reports/2022-06-illuminate

### Keywords for Search

`vulnerability`

