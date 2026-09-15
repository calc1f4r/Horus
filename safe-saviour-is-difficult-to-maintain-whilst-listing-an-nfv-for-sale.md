---
# Core Classification
protocol: Open Dollar - Smart Contract Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59519
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/open-dollar-smart-contract-audit/202828fa-eb09-4d33-beab-c1ebee11ebd1/index.html
source_link: https://certificate.quantstamp.com/full/open-dollar-smart-contract-audit/202828fa-eb09-4d33-beab-c1ebee11ebd1/index.html
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
  - Nikita Belenkov
  - Ibrahim Abouzied
  - Mostafa Yassin
---

## Vulnerability Title

Safe Saviour Is Difficult to Maintain Whilst Listing an NFV for Sale

### Overview


The report states that there is a bug in the Safe Saviour system, specifically in the `contracts/LiquidationEngine.sol` file. This bug allows a user to assign a savior to their NFV (non-fungible vault) and maintain that savior even after the NFV is transferred to a new owner. This can be problematic for users who are trying to sell their NFV, as the savior will also be transferred to the new owner unless the original owner removes it beforehand. This can only be done by front-running the NFV transfer, which is not an ideal solution. The recommendation is to either remove saviors on NFV transfers or only remove them if the transfer was not initiated by the token owner. 

### Original Finding Content

**Update**
Safe Saviour is now cleared on transfer. Fixed in commit `0be444a6b2c48c7fca60a5e156f6092b57b6025f`.

**File(s) affected:**`contracts/LiquidationEngine.sol`

**Description:** A user can assign an `ISAFESaviour` to their NFV. If a liquidation attempt is ever made, the `LiquidationEngine` will first make a call to `ISAFESaviour.saveSAFE()` to give the savior an opportunity to restore the safe to a healthy collateralization ratio before it is liquidated.

The current implementation maintains the assigned savior after an `NFV` transfer. Whilst the savior implementations may vary, the `LiquidationEngine.protectSAFE()` call assigns a savior to a particular safe rather than the safe owner. A user may want to maintain their savior to protect their NFV until a sale is guaranteed, but there is no clear way to facilitate the removal of a savior before an NFV transfer. Though this behavior is documented, we would like to note that this behavior is restrictive for listed NFV's.

**Exploit Scenario:**

1.   Alice's NFV is close to being liquidated, so she assigns a savior.
2.   Alice lists the NFV in a marketplace.
3.   Alice knows that the NFV savior is not cleared on transfer but is unsure when/if her safe will be purchased, so she decides to maintain the savior in the meantime.
4.   Bob buys the safe. The only way Alice can prevent Bob from inheriting her savior is by front-running the NFV transfer and removing the savior.

**Recommendation:** Remove saviors on NFV transfer. Alternatively, remove saviors specifically on NFV transfers that were not initiated by the token owner (and instead triggered by a marketplace).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Open Dollar - Smart Contract Audit |
| Report Date | N/A |
| Finders | Nikita Belenkov, Ibrahim Abouzied, Mostafa Yassin |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/open-dollar-smart-contract-audit/202828fa-eb09-4d33-beab-c1ebee11ebd1/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/open-dollar-smart-contract-audit/202828fa-eb09-4d33-beab-c1ebee11ebd1/index.html

### Keywords for Search

`vulnerability`

