---
# Core Classification
protocol: Mantle Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63671
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Mantle%20Network/mETH%20x%20Aave%20Integration/README.md#5-missing-freshness-check-on-oracle-data-in-stakingtotalcontrolled-enables-stale-rate-arbitrage
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Missing freshness check on oracle data in `Staking.totalControlled()` enables stale-rate arbitrage

### Overview


The bug report discusses an issue with the `Staking.totalControlled()` function in the contracts of a project called Mantle. This function uses data from another function called `oracle.latestRecord()` to calculate the exchange rate between mETH and ETH. However, there is a problem with this as the `oracle.latestRecord()` function does not check for the freshness of the data it uses, which means that it could use outdated information. This can be exploited by attackers to gain excess ETH or mETH, causing harm to other users. The recommendation is to add a validation check for the freshness of the data used in the `oracle.latestRecord()` function when minting or burning mETH. The client has acknowledged the issue but has decided not to fix it due to the risk involved in changing a high-value contract.

### Original Finding Content

##### Description
`Staking.totalControlled()` derives the mETH/ETH exchange rate inputs from `oracle.latestRecord()` without validating the record timestamp.

If the oracle lags significant state changes (e.g., validator rewards or slashing), the resulting rate becomes stale. An attacker can exploit this by timing mint/burn operations against outdated totals: redeeming mETH for excess ETH when a slashing is not yet reflected (overstated `totalControlled()`), or depositing ETH to mint excess mETH when recent rewards are not yet reflected (understated `totalControlled()`), extracting value from other users.

https://github.com/mantle-lsp/contracts/blob/6210e907b0f790ee9e11fe8ccb4d4baf12de6609/src/Staking.sol#L596-L611

##### Recommendation
We recommend enforcing freshness validation for oracle records when minting or burning mETH.

> **Client's Commentary:**
> **Client**: Most sanity checks are in the Oracle contract, ensuring consistency.
> **MixBytes**: The `Oracle.latestRecord()` function has no sanity checks—it simply returns `_records[_records.length - 1]`. This is correct, as the function is not supposed to perform any checks. The validations should be implemented on the caller side, specifically in the `Staking.totalControlled()` function.
> **Client**: the issue is known; won’t fix;
> **MixBytes**: we accept the decision since changing a high-TVL contract is risky and the oracle’s failure risk is low.

---


### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Mantle Network |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Mantle%20Network/mETH%20x%20Aave%20Integration/README.md#5-missing-freshness-check-on-oracle-data-in-stakingtotalcontrolled-enables-stale-rate-arbitrage
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

