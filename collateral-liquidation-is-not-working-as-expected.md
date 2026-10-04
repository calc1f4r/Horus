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
solodit_id: 51157
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

COLLATERAL LIQUIDATION IS NOT WORKING AS EXPECTED

### Overview


The `liquidate_collateral` function in the **krp-cdp-contracts/central\_control** contract is not working properly. It is querying its own balance instead of the balance of the **krp-cdp-contracts/stable\_pool** contract. This can cause unexpected problems, such as trying to repay with the wrong amount of stable coins or the collateral liquidation failing and the operation being reverted. The issue has been resolved by the Kryptonite team in commit [2b1e9bb](https://github.com/KryptoniteDAO/krp-cdp-contracts/pull/24/commits/2b1e9bb578845e4720bb6931792198bf5b453b20).

### Original Finding Content

##### Description

The `liquidate_collateral` function in the **krp-cdp-contracts/central\_control** contract is querying its own balance instead of the balance of **krp-cdp-contracts/stable\_pool** contract. As a consequence, some unexpected situations can happen:

* Trying to repay with an erroneous amount of stable coins.
* Collateral liquidation fails, and the operation is reverted.

Code Location
-------------

#### krp-cdp-contracts/contracts/central\_control/src/contract.rs

```
let pre_balance: Uint256 = query_balance(
 deps.as_ref(),
 env.contract.address.clone(),
 config.stable_denom.to_string(),
)?;

```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:M/A:M/D:M/Y:N/R:N/S:U (7.5)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:M/A:M/D:M/Y:N/R:N/S:U)

##### Recommendation

**SOLVED**: The `Kryptonite team` solved this issue in commit [2b1e9bb](https://github.com/KryptoniteDAO/krp-cdp-contracts/pull/24/commits/2b1e9bb578845e4720bb6931792198bf5b453b20).

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

