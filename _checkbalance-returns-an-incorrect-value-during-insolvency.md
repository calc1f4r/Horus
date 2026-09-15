---
# Core Classification
protocol: OETH Withdrawal Queue Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36592
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/oeth-withdrawal-queue-audit
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

_checkBalance Returns an Incorrect Value During Insolvency

### Overview


The `_checkBalance` function in the OETHVaultCore.sol contract is not returning the correct balance in certain scenarios. Specifically, if the WETH in the withdrawal queue exceeds the total amount of workable assets, the function should return a balance of 0 but instead returns the amount of WETH in the vault and strategies. This can happen during a mass slashing event when multiple users are trying to withdraw their OETH. The suggested solution is to update the function to return 0 in this case and to potentially call the `_totalValue` function instead. This bug has been resolved in a recent pull request.

### Original Finding Content

The [`_checkBalance`](https://github.com/OriginProtocol/origin-dollar/blob/eca6ffa74d9d0c5fb467551a30912cb722fab9c2/contracts/contracts/vault/OETHVaultCore.sol#L392-L407) function returns the balance of an asset held in the vault and all the strategies. If the requested asset is WETH, the amount of WETH reserved for the withdrawal queue is subtracted from this balance to reflect the correct amount of workable assets. In this specific case, the function returns the same result as [the `_totalValue` function](https://github.com/OriginProtocol/origin-dollar/blob/eca6ffa74d9d0c5fb467551a30912cb722fab9c2/contracts/contracts/vault/OETHVaultCore.sol#L455-L472).


In the event that the vault becomes insolvent (e.g., during a mass slashing event) and multiple users are requesting to withdraw their OETH, the WETH in the withdrawal queue may exceed the total amount of workable assets. In this case, the function should return a balance of 0\. However, it will actually [return](https://github.com/OriginProtocol/origin-dollar/blob/eca6ffa74d9d0c5fb467551a30912cb722fab9c2/contracts/contracts/vault/OETHVaultCore.sol#L398) the amount of WETH in the vault and strategies without subtracting the WETH reserved for the withdrawal queue.


Consider returning 0 in case the amount of WETH reserved for the withdrawal queue exceeds the total amount of workable assets. In addition, since the `_checkBalance` function should return the same value as the `_totalValue` function if the asset is WETH, consider calling `_totalValue` in `_checkBalance` or vice versa.


***Update:** Resolved in [pull request \#2166](https://github.com/OriginProtocol/origin-dollar/pull/2166/) at commit [2a6901a](https://github.com/OriginProtocol/origin-dollar/pull/2166/commits/2a6901a87f3016c85b720291c39c5a5fdfb7d715).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | OETH Withdrawal Queue Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/oeth-withdrawal-queue-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

