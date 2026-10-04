---
# Core Classification
protocol: USG - Tangent
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63048
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1073
source_link: none
github_link: https://github.com/sherlock-audit/2025-08-usg-tangent-judging/issues/50

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
finders_count: 13
finders:
  - newspacexyz
  - v1c7
  - greekfreakxyz
  - X0sauce
  - Orhukl
---

## Vulnerability Title

M-2: Incorrect assumption that one (1) Pendle SY token equals one (1) Yield Token in oracle pricing

### Overview


The bug report is about an incorrect assumption in the `OraclePendlePT` contract that leads to systemic mispricing. The pricing formula used in the contract assumes that 1 Pendle Standard Yield (SY) token is always equal in value to 1 unit of the underlying Yield Token. However, in real Pendle markets, the SY token can deviate significantly from this 1:1 peg, causing the oracle to overstate the value of the PT token. This can result in liquidation reverts and financial loss for users, affecting the protocol's solvency. The root cause of this bug is a hardcoded pricing formula that does not consider the actual market price of the SY token. It is recommended to fix this issue to prevent any potential financial loss or insolvency for the protocol.

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-08-usg-tangent-judging/issues/50 

## Found by 
0xSolus, BADROBINX, Bluedragon, Mishkat6451, Orhukl, Suryaa\_\_, X0sauce, algiz, deadmanwalking, greekfreakxyz, magickenn, newspacexyz, v1c7

### Summary

The `OraclePendlePT` contract incorrectly assumes that 1 Pendle Standard Yield (SY) token is always equal in value to 1 unit of the underlying Yield Token. This assumption is embedded in the following pricing formula:
```solidity
return (oracle.getPtToSyRate(address(_params.pendleMarket), uint32(_params.duration)) * underlyingPrice) / 1e18;
```
However, in real Pendle markets, the SY token can deviate significantly from a 1:1 peg with the Yield Token, depending on market conditions, liquidity, and accrued yield. By treating SY as if it is always equal to the Yield Token, the oracle overstates the value of the PT token, introducing systemic mispricing.
Pendle's SY.redeem function showing that slippage might occur during the exchange, and thus 1 SY == 1 Yield Token does not always hold.
https://github.com/pendle-finance/pendle-core-v2-public/blob/46d13ce4168e8c5ad9e5641dd6380fea69e48490/contracts/interfaces/IStandardizedYield.sol#L87

### Root Cause

https://github.com/sherlock-audit/2025-08-usg-tangent/blob/main/tangent-contracts/src/USG/Oracles/Pendle/OraclePendlePT.sol#L45
A hardcoded pricing formula that assumes SY = underlying asset, without checking or incorporating the actual market price of the SY token.

### Internal Pre-conditions

.

### External Pre-conditions

.

### Attack Path

.

### Impact

Inflated oracle price will cause liquidation revert and protocol broken. Users can borrow more than expected and never liquidated affecting the protocol's solvency and increasing the risk of bad debt.
Thus this will lead to financial loss or insolvency to the protocol.

### PoC

_No response_

### Mitigation

_No response_



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | USG - Tangent |
| Report Date | N/A |
| Finders | newspacexyz, v1c7, greekfreakxyz, X0sauce, Orhukl, magickenn, 0xSolus, BADROBINX, Bluedragon, Suryaa\_\_, deadmanwalking, Mishkat6451, algiz |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-08-usg-tangent-judging/issues/50
- **Contest**: https://app.sherlock.xyz/audits/contests/1073

### Keywords for Search

`vulnerability`

