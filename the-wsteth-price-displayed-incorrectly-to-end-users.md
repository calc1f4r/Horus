---
# Core Classification
protocol: Open Dollar - dApp
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59512
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/open-dollar-d-app/f0ff4333-535d-4de6-96e0-8573623c18bf/index.html
source_link: https://certificate.quantstamp.com/full/open-dollar-d-app/f0ff4333-535d-4de6-96e0-8573623c18bf/index.html
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
finders_count: 2
finders:
  - Pavel Shabarkin
  - Mostafa Yassin
---

## Vulnerability Title

The wstETH price Displayed Incorrectly to End Users

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `d0a7a805d1534b5a947be95c092cbf2a28e9afbc`. The client provided the following explanation:

> The source of the error was a function that was incorrectly interpreting different collateral types as OD and thus assuming a 1:1 ratio. The faulty function was replaced with a function named calculateCollateralInUSD that correctly calculates the collateral prices in USD based on their oracle price data populated by the Open Dollar SDK and contract logic.

**Description:** The OpenDollar UI shows incorrect price of the 1 wstETH token, it shows with the rate 1:1 when the actual worth of token is higher. This can confuse and mislead end-users of the application.

**Recommendation:** Apply the correct live rates.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Open Dollar - dApp |
| Report Date | N/A |
| Finders | Pavel Shabarkin, Mostafa Yassin |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/open-dollar-d-app/f0ff4333-535d-4de6-96e0-8573623c18bf/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/open-dollar-d-app/f0ff4333-535d-4de6-96e0-8573623c18bf/index.html

### Keywords for Search

`vulnerability`

