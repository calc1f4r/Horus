---
# Core Classification
protocol: Across V3 Incremental Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32549
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/across-v3-incremental-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Permit2OrderLib Is Not Fully Compliant With EIP-712

### Overview


This bug report is about a problem in the `Permit2OrderLib` contract, where the argument `witnessTypeString` in the `permit2WitnessTransferFrom` function does not fully follow the EIP-712 specification. Specifically, there are some entries that have a different type in the struct's declaration than what is included in the typestring, and some entries are included in the witness but not in the typestring. The report suggests fixing these inconsistencies to comply with the EIP-712 specification. The bug has been resolved in a recent pull request.

### Original Finding Content

In the [`Permit2OrderLib`](https://github.com/UMAprotocol/across-contracts-v2-private/blob/8595081d0edf6aa265fc5e0d04437e9aa07efbcd/contracts/permit2-order/Permit2OrderLib.sol) contract, the [`witnessTypeString`](https://github.com/UMAprotocol/across-contracts-v2-private/blob/8595081d0edf6aa265fc5e0d04437e9aa07efbcd/contracts/permit2-order/Permit2OrderLib.sol#L123) argument when calling the external [`permit2WitnessTransferFrom`](https://github.com/Uniswap/permit2/blob/main/src/SignatureTransfer.sol#L32) function does not fully follow the EIP-712 specification.


Specifically:


* [Some of the entries](https://github.com/UMAprotocol/across-contracts-v2-private/blob/8595081d0edf6aa265fc5e0d04437e9aa07efbcd/contracts/permit2-order/Permit2OrderLib.sol#L25-L44) have a different type in the [struct's](https://github.com/UMAprotocol/across-contracts-v2-private/blob/8595081d0edf6aa265fc5e0d04437e9aa07efbcd/contracts/permit2-order/Permit2Order.sol#L46) declaration than what is included in the [typestring](https://github.com/UMAprotocol/across-contracts-v2-private/blob/8595081d0edf6aa265fc5e0d04437e9aa07efbcd/contracts/permit2-order/Permit2OrderLib.sol#L25). Namely, these entries are: `fillPeriod`, `validationContract`, and `validationData`.
* Some entries are included in the [witness](https://github.com/UMAprotocol/across-contracts-v2-private/blob/8595081d0edf6aa265fc5e0d04437e9aa07efbcd/contracts/permit2-order/Permit2OrderLib.sol#L122) but are not included in the [typestring](https://github.com/UMAprotocol/across-contracts-v2-private/blob/8595081d0edf6aa265fc5e0d04437e9aa07efbcd/contracts/permit2-order/Permit2OrderLib.sol#L25). Namely, [`order.challengerCollateral.token`](https://github.com/UMAprotocol/across-contracts-v2-private/blob/8595081d0edf6aa265fc5e0d04437e9aa07efbcd/contracts/permit2-order/Permit2OrderLib.sol#L86) and [`order.challengerCollateral.amount`](https://github.com/UMAprotocol/across-contracts-v2-private/blob/8595081d0edf6aa265fc5e0d04437e9aa07efbcd/contracts/permit2-order/Permit2OrderLib.sol#L87).


Consider fixing all the inconsistencies described above in order to fully comply with the EIP-712 specification.


***Update:** Resolved in [pull request #15](https://github.com/UMAprotocol/across-contracts-v2-private/pull/15) at commit [446aae6](https://github.com/UMAprotocol/across-contracts-v2-private/commit/446aae6736602096061af98bd9ec090b654aeee5).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Across V3 Incremental Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/across-v3-incremental-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

