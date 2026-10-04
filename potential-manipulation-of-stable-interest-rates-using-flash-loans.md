---
# Core Classification
protocol: Aave Protocol V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13609
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/09/aave-protocol-v2/
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Sergii Kravchenko
  - Bernhard Mueller
---

## Vulnerability Title

Potential manipulation of stable interest rates using flash loans

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



This type of manipulation is difficult to prevent completely especially when flash loans are available. In practice however, attacks are mitigated by the following factors:


1. Liquidity providers attempting to increase users' stable rates would have to pay a high flash loan premium. Users could also immediately swap to variable interest meaning that the attack could result in a net loss for the LP. In practice, it is likely that this makes the attack economically unfeasible.
2. Under normal conditions, users would only gain a relatively small advantage by lowering their stable rate due to the design of the stable rate curve. If a user attempted to manipulate their stable rate during a liquidity crisis, Aave could immediately rebalance them and bring the rate back to normal.




Flash loans allow users to borrow large amounts of liquidity from the protocol. It is possible to adjust the stable rate up or down by momentarily removing or adding large amounts of liquidity to reserves.


**LPs increasing the interest rate of borrowers**


The function `rebalanceStableBorrowRate()` increases the stable interest rate of a user if the current liquidity rate is higher than the user’s stable rate. A liquidity provider could trigger an artificial “liquidity crisis” in a reserve and increase the stable interest rates of borrowers by atomically performing the following steps:


1. Take a flash loan to take a large number of tokens from a reserve
2. Re-balance the stable rate of the emptied reserves' borrowers
3. Repay the flash loan (plus premium)
4. Withdraw the collateral and repay the flash loan


Individual borrowers would then have to switch to the variable rate to return to a lower interest rate.


**User borrowing at an artificially lowered interest rate**


Users wanting to borrow funds could attempt to get a lower interest rate by temporarily adding liquidity to a reserve (which could e.g. be flash borrowed from a different protocol). While there’s a check that prevents users from borrowing an asset while also adding a higher amount of the same asset as collateral, this can be bypassed rather easily by depositing the collateral from a different address (via smart contracts). Aave would then have to rebalance the user to restore an appropriate interest rate.


In practice, users would gain only a relatively small advantage here due to the design of the stable rate curve.


**Recommendation**


This type of manipulation is difficult to prevent especially when flash loans are available. The safest option to prevent the first variant would be to restrict access to `rebalanceStableBorrowRate()` to admins. In any case, Aave should monitor the protocol at all times to make sure that interest rates are being rebalanced to sane values.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Aave Protocol V2 |
| Report Date | N/A |
| Finders | Sergii Kravchenko, Bernhard Mueller |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/09/aave-protocol-v2/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

