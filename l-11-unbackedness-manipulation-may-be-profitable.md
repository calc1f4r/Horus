---
# Core Classification
protocol: Bold Report
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53965
audit_firm: Recon Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-23-bold-report.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Alex The Entreprenerd
---

## Vulnerability Title

[L-11] Unbackedness manipulation may be profitable

### Overview

See description below for full details.

### Original Finding Content

**Impact**

The code to determine the ratio at which to redeem collaterals is as follows:
https://github.com/liquity/bold/blob/3ad11270a22190e77c1e8ef7742d2ebec133a317/contracts/src/CollateralRegistry.sol#L122-L132

```solidity
        for (uint256 index = 0; index < totals.numCollaterals; index++) {
            ITroveManager troveManager = getTroveManager(index);
            (uint256 unbackedPortion, uint256 price, bool redeemable) =
                troveManager.getUnbackedPortionPriceAndRedeemability();
            prices[index] = price;
            if (redeemable) {
                totals.unbacked += unbackedPortion;
                unbackedPortions[index] = unbackedPortion;
            }
        }

```

Given certain conditions, we can have the following:

The cost of minting BOLD is X
The redemption fee is Y
The cost of swapping between the two LSTs is N
The realised deviation threshold of an Oracle A and B is D > c + (X + Y + N)
This can create a scenario where redemtpions are not just a profitable arb (higher likelyhood than this)
But a scenario in which manipulating the unbackedness of a collateral makes the redemption even more profitable

**Napkin math**

Anytime the Oracle Drift inaccuracy is higher than the sum of:
- Swap Fees
- Redemption Fee
- 7 days of interest of Debt that will be redeemed that is necessary to manipulate the unbackedness of branches

Then manipulating the unbackedness will be profitable

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Recon Audits |
| Protocol | Bold Report |
| Report Date | N/A |
| Finders | Alex The Entreprenerd |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-23-bold-report.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

