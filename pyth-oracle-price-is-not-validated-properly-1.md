---
# Core Classification
protocol: v2.1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51983
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/rfx-exchange/v21
source_link: https://www.halborn.com/audits/rfx-exchange/v21
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
  - Halborn
---

## Vulnerability Title

Pyth oracle price is not validated properly

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `PythDataStreamProvider` contract does not perform input validation on the `price`, `conf`, and `expo` values returned from the called price feed, which can lead to the contract accepting invalid or untrusted prices. Those values should be checked as clearly stated in the [official documentation](https://docs.pyth.network/price-feeds/best-practices#confidence-intervals).

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:L/A:L/D:L/Y:N/R:N/S:C (4.7)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:L/A:L/D:L/Y:N/R:N/S:C)

##### Recommendation

The contract should revert the transaction [here](https://github.com/relative-finance/rfx-contracts/blob/0466b4a880d7d5b87ff75b639358fbe53db3b313/contracts/oracle/PythDataStreamProvider.sol#L127) if one of the following conditions is triggered:

* `price <= 0`
* `expo < -18`
* `conf > 0 && (price / int64(conf) < MIN_CONF_RATIO` for a given `MIN_CONF_RATIO`

### Remediation Plan

**SOLVED:** The **Relative Finance team** solved this issue by checking the recommended conditions, and reverting the transaction if the values were not the expected ones.

##### Remediation Hash

<https://github.com/relative-finance/rfx-contracts/commit/53b871efdaa63437c8397aa7bae4f3cdb6364ae5>

##### References

<https://solodit.xyz/issues/m-01-pyth-oracle-price-is-not-validated-properly-pashov-audit-group-none-nabla-markdown>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | v2.1 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/rfx-exchange/v21
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/rfx-exchange/v21

### Keywords for Search

`vulnerability`

