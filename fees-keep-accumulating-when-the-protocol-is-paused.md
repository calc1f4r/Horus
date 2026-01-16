---
# Core Classification
protocol: Filament
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45619
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
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
  - Zokyo
---

## Vulnerability Title

Fees keep accumulating when the protocol is paused.

### Overview


The report discusses a bug in the `updateBalances()` function of the `TradeFacet.sol` smart contract. This function is used to update balances and distribute borrowing fees, but it has no access restrictions and can be called at any time, even when the protocol is paused. The function calculates the elapsed time since it was last executed, but this calculation does not take into account the pause of the protocol. As a result, when the protocol is paused, users are unable to modify their positions but fees continue to accumulate. This leads to a decrease in users' positions while the protocol collects fees. The recommendation is to implement a mechanism to exclude the time when the protocol was paused from the fee calculation. The client has commented that borrowing fees should still be calculated even when the protocol is paused because funds are still being borrowed.

### Original Finding Content

**Severity**: Medium	

**Status**: Acknowledged

**Description**

The function `updateBalances()` within the `TradeFacet.sol` smart contract is used to update balances and distribute borrowing fees. This function is public and has no access restrictions or any other modifier so that it can be called at any point in time even when the rest of the protocol is paused.

The main logic of this function is working around the elapsed time since last execution. For calculating this elapsed time the `lastBalanceUpdateTime` is updated every time this function is executed so that an ‘interval’ is calculated.
```solidity
if (s.lastBalanceUpdateTime[_indexToken] == 0) {
           s.lastBalanceUpdateTime[_indexToken] = block.timestamp;
       }
 uint256 interval = (block.timestamp - s.lastBalanceUpdateTime[_indexToken]);
```

However, this elapsed time does not consider the pause of the protocol.
Consider the following scenario:

The protocol is unpaused, users create positions.
The protocol is paused for X blocks.
Users can not modify their positions but fees are being accumulated by these X blocks.

The interest calculated is used for decreasing long and short collateral which leads to users positions being decreased while the protocol gets fees:
```solidity
s.longCollateral[_indexToken] -= longInterest;
       s.shortCollateral[_indexToken] -= shortInterest;
       uint256 totalInterest = shortInterest + longInterest;

       IERC20(s.USDC).approve(address(s.keeper), totalInterest);
       s.keeper.distributeBorrowingFees(address(this), totalInterest, _indexToken);
```


**Recommendation**:

Implement a mechanism to not consider the blocks while the protocol were paused to be used for generating fees.

**Client comment**: Borrowing fee should still be calculated if protocol is paused because funds are still borrowed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Filament |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

