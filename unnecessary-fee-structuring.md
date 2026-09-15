---
# Core Classification
protocol: Wido Comet Collateral Swap Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32837
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/wido-comet-collateral-swap-contracts
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

Unnecessary fee structuring

### Overview


The bug report discusses an issue with the collateral swap process in a protocol called Wido. Currently, the flash loan fee is subtracted from the flash loan amount before it is deposited into Comet. This makes it difficult for users to calculate the appropriate amount to withdraw, as they have to account for the fee and other factors like market exchange rate and liquidity. The report suggests removing the fee deduction and providing helper functions to make the calculation easier. The Wido team has acknowledged the issue but it has not been resolved yet. They have mentioned an off-chain SDK that can assist with the calculation. 

### Original Finding Content

During the collateral swap [the flash loan fee is first subtracted from the flash loan amount](https://github.com/widolabs/wido-contracts/blob/d96ef2dd6a7ff3d04c44ebe87994411d1f8c84e7/contracts/compound/libraries/LibCollateralSwap.sol#L56) which is then deposited into Comet. This is to ensure that the protocol has enough to pay the flash loan fee. But the swap process itself also relies on the user to pick a large enough amount to withdraw so as to cover the flash loan amount with a token swap. Since the contract checks for the required amount to be repaid, removing the fee first only adds to the complexity of the calculation with which the user has to decide the withdrawal amount. This could be a difficult task given the process involves unpredictable market exchange rate and slippage caused by available liquidity between the two swapping collaterals.


Consider removing the fee deduction to use the full flash loan for the Comet collateral deposit. Further consider offering helper functions to assist with the calculation of the appropriate final collateral amount.


***Update**: Acknowledged, not resolved. The Wido team stated:*



> *We have an off-chain SDK to assist with the calculation.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Wido Comet Collateral Swap Contracts |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/wido-comet-collateral-swap-contracts
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

