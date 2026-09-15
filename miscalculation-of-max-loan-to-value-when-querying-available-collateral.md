---
# Core Classification
protocol: Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51160
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment
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
  - Halborn
---

## Vulnerability Title

MISCALCULATION OF MAX LOAN TO VALUE WHEN QUERYING AVAILABLE COLLATERAL

### Overview


The bug report describes an issue with the `query_collateral_available` function in the `krp-cdp-contracts/central_control` contract. The problem is that the value of `max_loans_value` is being calculated incorrectly and overwritten in each step of a `for` loop. This results in inaccurate values being returned when querying about available collateral for users. The location of the code causing the issue is in the `krp-cdp-contracts/contracts/central_control/src/contract.rs` file. The BVSS (Bug Vulnerability Severity Scale) of this issue is 7.5, indicating a high severity level. The recommendation states that the issue has been solved by the Kryptonite team in commit `0950837`.

### Original Finding Content

##### Description

In the `query_collateral_available` function in the **krp-cdp-contracts/central\_control** contract, the value of `max_loans_value` is miscalculated, and its value is overwritten in each step of the `for` loop. As a consequence, the value returned when querying about the available collateral for users will be inaccurate.

Currently, the value of `max_loans_value` is:

\begin{math}
max\_loans\_value = collateral.1 \* price\_resp.emv\_price \* collateral\_info.max\_ltv
\end{math}

However, it should be:

\begin{math}
max\_loans\_value += collateral.1 \* price\_resp.emv\_price \* collateral\_info.max\_ltv
\end{math}

Code Location
-------------

#### krp-cdp-contracts/contracts/central\_control/src/contract.rs

```
for collateral in collaterals {
 let collateral_info = read_whitelist_elem(deps.storage, &collateral.0)?;
 let price_resp = query_price(
  deps,
  deps.api.addr_humanize(&config.oracle_contract)?,
  deps.api.addr_humanize(&collateral.0)?.to_string(),
  "".to_string(),
  None,
 )?;
 if collateral.0 == collateral_raw {
  collateral_amount = collateral.1;
  collateral_price = price_resp.emv_price;
  collateral_max_ltv = collateral_info.max_ltv;
 } else {
  max_loans_value = collateral.1 * price_resp.emv_price * collateral_info.max_ltv;
 }
}

```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:H/A:N/D:N/Y:N/R:N/S:U (7.5)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:H/A:N/D:N/Y:N/R:N/S:U)

##### Recommendation

**SOLVED**: The `Kryptonite team` solved this issue in commit [0950837](https://github.com/KryptoniteDAO/krp-cdp-contracts/pull/26/commits/0950837d9f54efd245a51904f4e4e7205c592b61).

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Protocol |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

