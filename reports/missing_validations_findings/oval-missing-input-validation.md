---
# Core Classification
protocol: Across V3 and Oval Incremental Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34963
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/across-v3-and-oval-incremental-audit
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
  - OpenZeppelin
---

## Vulnerability Title

[Oval] Missing Input Validation

### Overview

See description below for full details.

### Original Finding Content

The deployer of the [`CoinbaseOracle`](https://github.com/UMAprotocol/oval-contracts/blob/297ab25a914171aedaeb01dabf4a829a304cce08/src/oracles/CoinbaseOracle.sol) contract [sets the immutable `reporter` variable](https://github.com/UMAprotocol/oval-contracts/blob/297ab25a914171aedaeb01dabf4a829a304cce08/src/oracles/CoinbaseOracle.sol#L32) during the contract's construction. The `reporter` is the sole entity authorized to submit new prices to the oracle via the [`pushPrice`](https://github.com/UMAprotocol/oval-contracts/blob/297ab25a914171aedaeb01dabf4a829a304cce08/src/oracles/CoinbaseOracle.sol#L81) function. The access control mechanism in `pushPrice` involves [recovering the signer](https://github.com/UMAprotocol/oval-contracts/blob/297ab25a914171aedaeb01dabf4a829a304cce08/src/oracles/CoinbaseOracle.sol#L95) of the provided message and verifying that it matches the reporter's address. However, the [`ecrecover`](https://github.com/UMAprotocol/oval-contracts/blob/297ab25a914171aedaeb01dabf4a829a304cce08/src/oracles/CoinbaseOracle.sol#L114) precompile does not fail on invalid signatures. Instead, it returns the zero address. If the `reporter` address is erroneously configured to the zero address, it becomes trivial for any entity to push arbitrary prices to the oracle contract.


Consider implementing a validation check to ensure that the reporter address is not set to the zero address to prevent erroneous contract deployments.


***Update:** Resolved in [pull request \#18](https://github.com/UMAprotocol/oval-contracts/pull/18) at commit [b057756](https://github.com/UMAprotocol/oval-contracts/commit/b057756cc75b13cbe0e4355bc2084f3807f4fcbc).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Across V3 and Oval Incremental Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/across-v3-and-oval-incremental-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

