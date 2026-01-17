---
# Core Classification
protocol: OpenLeverage
chain: everychain
category: uncategorized
vulnerability_type: call_vs_transfer

# Attack Vector Details
attack_type: call_vs_transfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1353
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-openleverage-contest
source_link: https://code4rena.com/reports/2022-01-openleverage
github_link: https://github.com/code-423n4/2022-01-openleverage-findings/issues/75

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 1

# Context Tags
tags:
  - call_vs_transfer

protocol_categories:
  - dexes
  - yield
  - derivatives
  - indexes
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - hyh
---

## Vulnerability Title

[H-01] OpenLevV1Lib’s and LPool’s doTransferOut functions call native payable.transfer, which can be unusable for smart contract calls

### Overview


This bug report is about an issue with OpenLev and LPool operations when using a wrapped native token. The issue is that when a user withdraws, the whole process is handled with a `payable.transfer()` call, which has a hard-coded gas budget and can fail if the user is a smart contract. This means that any programmatic usage of OpenLevV1 and LPool is at risk, and user funds can be frozen in the principal funds freeze scenario. The proof of concept provided in the report outlines the affected functions, and the recommended mitigation steps are to replace the `transfer()` with either a low-level `call.value(amount)` with the corresponding result check or with the OpenZeppelin `Address.sendValue`.

### Original Finding Content

## Handle

hyh


## Vulnerability details

## Impact

When OpenLev operations use a wrapped native token, the whole user withdraw is being handled with a `payable.transfer()` call.

This is unsafe as `transfer` has hard coded gas budget and can fail when the user is a smart contract. This way any programmatical usage of OpenLevV1 and LPool is at risk.

Whenever the user either fails to implement the payable fallback function or cumulative gas cost of the function sequence invoked on a native token transfer exceeds 2300 gas consumption limit the native tokens sent end up undelivered and the corresponding user funds return functionality will fail each time.

As OpenLevV1 `closeTrade` is affected this includes user's principal funds freeze scenario, so marking the issue as a high severity one.

## Proof of Concept

OpenLevV1Lib and LPool have `doTransferOut` function that calls native token payable.transfer:

OpenLevV1Lib.doTransferOut

https://github.com/code-423n4/2022-01-openleverage/blob/main/openleverage-contracts/contracts/OpenLevV1Lib.sol#L253


LPool.doTransferOut

https://github.com/code-423n4/2022-01-openleverage/blob/main/openleverage-contracts/contracts/liquidity/LPool.sol#L297


LPool.doTransferOut is used in LPool redeem and borrow, while OpenLevV1Lib.doTransferOut is used in OpenLevV1 trade manipulation logic:

closeTrade

https://github.com/code-423n4/2022-01-openleverage/blob/main/openleverage-contracts/contracts/OpenLevV1.sol#L204

https://github.com/code-423n4/2022-01-openleverage/blob/main/openleverage-contracts/contracts/OpenLevV1.sol#L215


liquidate

https://github.com/code-423n4/2022-01-openleverage/blob/main/openleverage-contracts/contracts/OpenLevV1.sol#L263

https://github.com/code-423n4/2022-01-openleverage/blob/main/openleverage-contracts/contracts/OpenLevV1.sol#L295

https://github.com/code-423n4/2022-01-openleverage/blob/main/openleverage-contracts/contracts/OpenLevV1.sol#L304


## References

The issues with `transfer()` are outlined here:

https://consensys.net/diligence/blog/2019/09/stop-using-soliditys-transfer-now/


## Recommended Mitigation Steps

OpenLevV1's `closeTrade` and `liquidate` as well as LPool's `redeem`, `redeemUnderlying`, `borrowBehalf`, `repayBorrowBehalf`, `repayBorrowEndByOpenLev` are all `nonReentrant`, so reentrancy isn't an issue and `transfer()` can be just replaced.

Using low-level `call.value(amount)` with the corresponding result check or using the OpenZeppelin `Address.sendValue` is advised:

https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/Address.sol#L60

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 1/5 |
| Audit Firm | Code4rena |
| Protocol | OpenLeverage |
| Report Date | N/A |
| Finders | hyh |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-openleverage
- **GitHub**: https://github.com/code-423n4/2022-01-openleverage-findings/issues/75
- **Contest**: https://code4rena.com/contests/2022-01-openleverage-contest

### Keywords for Search

`call vs transfer`

