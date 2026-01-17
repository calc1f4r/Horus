---
# Core Classification
protocol: Morpho Vaults v2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62918
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Vaults-v2-Spearbit-Security-Review-May-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Vaults-v2-Spearbit-Security-Review-May-2025.pdf
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
finders_count: 4
finders:
  - Saw-mon and Natalie
  - Om Parikh
  - Jonatas Martins
  - Emmanuele Ricci
---

## Vulnerability Title

interestPerSecond limits minimum rate that can be set and causes significant deviation for low

### Overview


Bug Report Summary:

The contract "ManualVic" has a problem with precision limitations in its interest calculation function. This makes it impractical for real-world use, especially for low interest rates and tokens with varying decimal precision. The issue is caused by the function returning raw interest amounts without any decimal scaling, leading to precision constraints when used by the vault contract. This can result in impossibly high annual interest rates and deviations from the target APR. The issue also affects other on-chain integrations using the contract. The recommendation is to experiment with lower precision and store the numerator and denominator separately. The issue has been acknowledged by the developers. 

### Original Finding Content

## Precision Tokens

**Severity:** Medium Risk  

**Context:** (No context files were provided by the reviewer)  

**Description:**  
The ManualVic contract's interestPerSecond implementation suffers from precision limitations that make it impractical for real-world usage, particularly for low interest rates and tokens with varying decimal precision. The contract returns raw interest amounts without any decimal scaling in the `interestPerSecond()` function. When consumed by the vault contract using the calculation `uint256 interest = interestPerSecond * elapsed`, this creates precision constraints.

**For GUSD (2 decimals):**
- The minimum non-zero `interestPerSecond = 1` creates: 
  - Annual interest: `1 * 31,536,000 = 31,536,000` units = 315,360 GUSD. 
- Minimum achievable APR is impossibly high regardless of AUM.

**For USDC (6 decimals), 100k AUM with 4% target APR, the minimum non-zero `interestPerSecond = 1` creates:**
- Target interest per year: `4,000 = 4000e6`.
- Required `interestPerSecond`: `4000e6 / 31536000 = 126.84`.
- Settable value: `126` (truncated).
- Actual APR: `(126 * 31,536,000) / 4,000,000,000 = 3.9853%`.
- Deviation: ~15 bps.

There might be cases where the notional interest rate might need to be very low (think 0.2 - 0.5%) ranges where the majority of the rewards are provided via alternate tokens. Given VIC needs to be general and be functional for a wide range of use cases, this not just limits ManualVic but any implementation since vault v2 considers interestPerSecond returned raw so it can't be switched with a new VIC implementation in the future to fix this particular issue. Also, other on-chain integrations (except vault v2) using VIC as a reference might suffer from the same issue.

**Recommendation:**
- Since precision ultimately needs to be adjusted back while saving totalAssets, try experimenting with lower precision such as BPS (10,000) instead of WAD so that rounding is minimal.
- Store numerator and denominator separately.

**Morpho:** Acknowledged. NatSpec comments have been added in PR 390.  
**Spearbit:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Morpho Vaults v2 |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, Om Parikh, Jonatas Martins, Emmanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Vaults-v2-Spearbit-Security-Review-May-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Vaults-v2-Spearbit-Security-Review-May-2025.pdf

### Keywords for Search

`vulnerability`

