---
# Core Classification
protocol: Mugen
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20424
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-01-01-Mugen.md
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
  - Pashov
---

## Vulnerability Title

[M-01] Use `quoteLayerZeroFee` instead of sending all native asset balance as gas fee for `swap` call

### Overview


This bug report is about an issue in the `StargateArbitrum::stargateSwap` contract. Currently, when doing a call to the `swap` method of `stargateRouter`, the whole contract's native asset balance is sent to it, instead of using the `quoteLayerZeroFee` method to calculate the fee correctly. The likelihood of this bug is high, as the wrong value will be sent always, however the impact is low, as the `swap` function has a gas refund mechanism. It is recommended to follow the documentation to calculate the fee correctly, instead of always sending the whole contract's balance as a fee.

### Original Finding Content

**Likelihood:**
High, because the wrong value will be sent always

**Impact:**
Low, because the `swap` function has a gas refund mechanism

**Description**

Currently in `StargateArbitrum::stargateSwap` when doing a call to the `swap` method of `stargateRouter`, all of the contract's native asset balance is sent to it so it can be used to pay the gas fee. The [Stargate docs](https://stargateprotocol.gitbook.io/stargate/developers/cross-chain-swap-fee) show that there is a proper way to calculate the fee and it is by utilizing the `quoteLayerZeroFee` method of `stargateRouter`.

**Recommendations**

Follow the documentation to calculate the fee correctly instead of always sending the whole contract's balance as a fee, even though there is a refund mechanism.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Mugen |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-01-01-Mugen.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

