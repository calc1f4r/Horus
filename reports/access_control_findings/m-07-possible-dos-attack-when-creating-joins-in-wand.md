---
# Core Classification
protocol: Yield
chain: everychain
category: dos
vulnerability_type: denial-of-service

# Attack Vector Details
attack_type: denial-of-service
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 4086
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-05-yield-contest
source_link: https://code4rena.com/reports/2021-05-yield
github_link: https://github.com/code-423n4/2021-05-yield-findings/issues/70

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - denial-of-service
  - dos

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-07] Possible DoS attack when creating Joins in Wand

### Overview


This bug report is about a Denial of Service (DoS) attack that can be performed on the JoinFactory and Wand contracts. It is possible for an attacker to create a fake Join corresponding to a specific token beforehand, which would prevent the Wand from deploying the actual Join. This can be done by using the keccak256 function to determine the address of the Join corresponding to an underlying asset, as the address is unique. Moreover, the function createJoin in the contract JoinFactory is permissionless, so anyone can create the Join corresponding to the asset. The attacker can deploy a large number of Joins with different common underlying assets (e.g., DAI, USDC, ETH) before the Wand deploying them, causing a DoS attack. Additionally, the attacker can also perform DoS attacks on newly added assets by monitoring the mempool to find transactions calling the function addAsset of Wand and front-running them to create the corresponding Join. The recommended mitigation steps are to enable access control in createJoin (e.g., adding the auth modifier) and allow Wand to call it.

### Original Finding Content

## Handle

shw


## Vulnerability details

## Impact

It is possible for an attacker to intendedly create a fake `Join` corresponding to a specific token beforehand to make `Wand` unable to deploy the actual `Join`, causing a DoS attack.

## Proof of Concept

The address of `Join` corresponding to an underlying `asset` is determined as follows and thus unique:

```solidity
Join join = new Join{salt: keccak256(abi.encodePacked(asset))}();
```

Besides, the function `createJoin` in the contract `JoinFactory` is permissionless: Anyone can create the `Join` corresponding to the `asset`. An attacker could then deploy a large number of `Joins` with different common underlying assets (e.g., DAI, USDC, ETH) before the `Wand` deploying them. The attempt of deploying these `Joins` by `Wand` would fail since the attacker had occupied the desired addresses with fake `Joins`, resulting in a DoS attack.

Moreover, the attacker can also perform DoS attacks on newly added assets: He monitors the mempool to find transactions calling the function `addAsset` of `Wand` and front-runs them to create the corresponding `Join` to make the benign transaction fail.

Referenced code:
[JoinFactory.sol#L64-L75](https://github.com/code-423n4/2021-05-yield/blob/main/contracts/JoinFactory.sol#L64-L75)
[Wand.sol#L53](https://github.com/code-423n4/2021-05-yield/blob/main/contracts/Wand.sol#L53)

## Recommended Mitigation Steps

Enable access control in `createJoin` (e.g., adding the `auth` modifier) and allow `Wand` to call it.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Yield |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-05-yield
- **GitHub**: https://github.com/code-423n4/2021-05-yield-findings/issues/70
- **Contest**: https://code4rena.com/contests/2021-05-yield-contest

### Keywords for Search

`Denial-Of-Service, DOS`

