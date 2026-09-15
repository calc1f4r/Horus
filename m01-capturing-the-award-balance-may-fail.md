---
# Core Classification
protocol: PoolTogether v3 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11254
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/pooltogether-v3-audit/
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

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - payments
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M01] Capturing the award balance may fail

### Overview


The `captureAwardBalance` function of the `PrizePool` contract is used to calculate any available interest as award balance. The way of calculating this balance may differ on each yield source, and there is a possibility that the calculated `totalInterest` may be greater than the `_currentAwardBalance` accumulated. This could lead to an underflow when calculating the unnacounted prize balance in extreme cases, and therefore stall the function for future calls. To avoid this, it is important to check that the `totalInterest` value is greater than the `_currentAwardBalance` value. This issue has been fixed in pull request #205, and the `captureAwardBalance` function now checks for this to prevent any subtraction underflow.

### Original Finding Content

The [`captureAwardBalance` function](https://github.com/pooltogether/pooltogether-pool-contracts/blob/5a9381340a7cef139c77e44c5ad5c2a5d6e12e36/contracts/prize-pool/PrizePool.sol#L461) of the `PrizePool` contract relies on the [underlying asset balance](https://github.com/pooltogether/pooltogether-pool-contracts/blob/5a9381340a7cef139c77e44c5ad5c2a5d6e12e36/contracts/prize-pool/PrizePool.sol#L463) to calculate any available interest as award balance. Given that the way of calculating this balance may differ on each yield source, there is a possiblity that the [calculated `totalInterest`](https://github.com/pooltogether/pooltogether-pool-contracts/blob/5a9381340a7cef139c77e44c5ad5c2a5d6e12e36/contracts/prize-pool/PrizePool.sol#L464) may be greater than the `_currentAwardBalance` accumulated. For instance, the [`balanceOfUnderlying`](https://github.com/compound-finance/compound-protocol/blob/23eac9425accafb82551777c93896ee7678a85a3/contracts/CToken.sol#L190) function in the Compound’s `CToken` contract [truncates the returned result](https://github.com/compound-finance/compound-protocol/blob/23eac9425accafb82551777c93896ee7678a85a3/contracts/CToken.sol#L192), which could lead into [an underflow when calculating the unnacounted prize balance](https://github.com/pooltogether/pooltogether-pool-contracts/blob/5a9381340a7cef139c77e44c5ad5c2a5d6e12e36/contracts/prize-pool/PrizePool.sol#L465) in extreme cases, and therefore stall the function for future calls.


Even though this might not occur in the system as it is, this may change in future versions of the protocol when introducing new yield sources.


Consider checking that the [`totalInterest`](https://github.com/pooltogether/pooltogether-pool-contracts/blob/5a9381340a7cef139c77e44c5ad5c2a5d6e12e36/contracts/prize-pool/PrizePool.sol#L464) value calculated using the underlying asset’s balance is greater than the accumulated `_currentAwardBalance`.


***Update:** Fixed in [pull request #205](https://github.com/pooltogether/pooltogether-pool-contracts/pull/205). The `captureAwardBalance` function now checks that the `totalInterest` value is greater than the `_currentAwardBalance` value to avoid the subtraction underflow.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | PoolTogether v3 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/pooltogether-v3-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

