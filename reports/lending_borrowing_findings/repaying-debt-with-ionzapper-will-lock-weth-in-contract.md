---
# Core Classification
protocol: Ion Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32700
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/ion-protocol-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Repaying Debt With IonZapper Will Lock WETH in Contract

### Overview


The `zapRepay` function in the `IonZapper` contract is not working as intended. It is supposed to allow users to repay debt in their vault in the `IonPool` contract by transferring ETH into the `IonZapper` contract. However, the function is not using the WETH held in the `IonZapper` contract and instead is transferring WETH from the user's account into the `IonPool` contract. This results in the user spending twice as much funds as expected and the ETH sent to the `IonZapper` contract becoming unrecoverable. To fix this issue, the `payer` argument for the `repay` function should be set to the `IonZapper` contract address within the `zapRepay` function. This will ensure that the WETH held by the `IonZapper` contract is used to repay the debt in the `IonPool` contract. This bug has been resolved in a recent pull request.

### Original Finding Content

The [`zapRepay` function](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/periphery/IonZapper.sol#L54) in the `IonZapper` contract is intended to allow a user to repay debt in their vault in the `IonPool` contract by transferring ETH into the `IonZapper` contract. The `zapRepay` function [wraps the ETH sent](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/periphery/IonZapper.sol#L63) into WETH and then is supposed to [use this to repay debt on behalf of the `msg.sender`](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/periphery/IonZapper.sol#L64).


The [`payer` argument](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/IonPool.sol#L584) to the `repay` function in the `IonPool` contract specifies what address the WETH is transferred from for repaying debt. This is set to the [original caller's address](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/periphery/IonZapper.sol#L64C42-L64C52) within the `zapRepay` function. As a result, if `msg.sender` has approved the `IonPool` contract to spend WETH on their behalf, and they hold a sufficient WETH balance, the `IonPool` will transfer WETH from the user's account into the pool contract and not use the WETH that is held in the `IonZapper` contract. Thus, the user will spend twice as much funds as expected while the ETH, now held as WETH, sent to the `IonZapper` contract will be unrecoverable.


Consider setting the `payer` argument for the `repay` function to the `IonZapper` contract address within the `zapRepay` function. This will ensure that the WETH held by the `IonZapper` contract is transferred into the `IonPool` contract.


***Update:** Resolved in [pull request #21](https://github.com/Ion-Protocol/ion-protocol/pull/21).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Ion Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/ion-protocol-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

