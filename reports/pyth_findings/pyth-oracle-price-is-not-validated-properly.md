---
# Core Classification
protocol: Brt Dci Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52279
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/prodigy/brt-dci-contracts
source_link: https://www.halborn.com/audits/prodigy/brt-dci-contracts
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
  - Halborn
---

## Vulnerability Title

Pyth oracle price is not validated properly

### Overview


The PythAggregator contract has a bug where it does not check if the prices returned from the price feed are valid or trusted. This can cause the contract to accept incorrect prices. The official documentation states that these values should be checked. It is recommended that the contract reverts the transaction if the price is less than or equal to 0, the exponent is less than -18, or the confidence ratio is too low. This bug has been fixed in the latest version of the contract. For more information, refer to the provided links.

### Original Finding Content

##### Description

The `PythAggregator` contract does not perform input validation on the `price`, `conf`, and `expo` values returned from the called price feed, which can lead to the contract accepting invalid or untrusted prices. Those values should be checked as clearly stated in the [official documentation](https://docs.pyth.network/price-feeds/best-practices#confidence-intervals).

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:L/A:L/D:L/Y:N/R:N/S:C (4.7)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:L/A:L/D:L/Y:N/R:N/S:C)

##### Recommendation

It is recommended that the contract revert the transaction [here](https://github.com/prodigyfi/brt-dci-contracts/blob/master/src/AggregatorHelper.sol#L33) if one of the following conditions is triggered:

* `price <= 0`
* `expo < -18`
* `conf > 0 && (price / int64(conf) < MIN_CONF_RATIO` for a given `MIN_CONF_RATIO`

##### Remediation

**SOLVED:** Pyth price now have checks about `price`,`expo` and `conf.`

##### Remediation Hash

<https://github.com/prodigyfi/brt-dci-contracts/commit/ef55a358607299c68249a1705895e524546a8a56>

##### References

<https://solodit.xyz/issues/m-01-pyth-oracle-price-is-not-validated-properly-pashov-audit-group-none-nabla-markdown>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Brt Dci Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/prodigy/brt-dci-contracts
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/prodigy/brt-dci-contracts

### Keywords for Search

`vulnerability`

