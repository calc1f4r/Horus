---
# Core Classification
protocol: Yeet Cup
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44204
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Yeet-Cup-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[M-03] Dysfunctional Instantiation of the `Yeetback.sol` Contract

### Overview


The Yeetback contract is experiencing issues with its core methods not working as expected. This is due to incorrect addresses being provided for the `entropy` and `entropyProvider` contracts during construction. The recommendation is to provide the correct addresses according to the Pyth Network contract documentation. The team has acknowledged and fixed the issue.

### Original Finding Content

## Severity

Medium Risk

## Description

The `Yeetback` contract is expected to be constructed with an `entropy` contract, which implements the [IEntropy](https://github.com/pyth-network/pyth-crosschain/blob/main/target_chains/ethereum/entropy_sdk/solidity/IEntropy.sol) interface, and an `entropyProvider` contract as follows:

```solidity
constructor(
    address _entropy,
    address _entropyProvider
) Ownable(msg.sender) {
    entropy = IEntropy(_entropy);
    entropyProvider = _entropyProvider;
}
```

However, the `Yeet` contract itself (`address(this)`) is provided on construction which does not implement any of the `IEntropy` methods required by the `Yeetback` contract, nor does it serve with any `entropyProvider` functionality.

As a consequence, core methods, i.e. `restart`, `addYeetback` & `getEntropyFee`, of the `Yeet` and `Yeetback` contracts will always fail to work as expected.

## Location of Affected Code

File: [src/Yeet.sol#L142](https://github.com/0xKingKoala/contracts/blob/f43ad283290293e18e5d9ab0c9d56e29bffa3eb3/src/Yeet.sol#L142)

```solidity
constructor(
    YeetToken _token,
    Reward _reward,
    DiscreteStakingRewards _staking,
    YeetGameSettings _gameSettings,
    address _publicGoodsAddress,
    address _lpStakingAddress,
    address _teamAddress
) Pauseable(msg.sender) {
    // code

    yeetback = new Yeetback(
        address(this),
        address(this)
    );

    // code
```

## Recommendation

Provide the correct `entropy` and `entropyProvider` contract addresses according to the [Pyth Network contract documentation](https://docs.pyth.network/entropy/contract-addresses).

## Team Response

Fixed as suggested

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Yeet Cup |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Yeet-Cup-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

