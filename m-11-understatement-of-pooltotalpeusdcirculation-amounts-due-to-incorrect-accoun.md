---
# Core Classification
protocol: Lybra Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21156
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-06-lybra
source_link: https://code4rena.com/reports/2023-06-lybra
github_link: https://github.com/code-423n4/2023-06-lybra-findings/issues/532

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
finders_count: 28
finders:
  - gs8nrv
  - peanuts
  - bytes032
  - Iurii3
  - OMEN
---

## Vulnerability Title

[M-11] Understatement of `poolTotalPeUSDCirculation` amounts due to incorrect accounting after function `_repay` is called

### Overview


A bug has been found in the accounting of `poolTotalPeUSDCirculation` in the function `_repay` of `LybraPeUSDVaultBase.sol`. This bug results in an understatement of `poolTotalPeUSDCirculation` amounts, causing inaccurate bookkeeping and affecting any other functions dependent on the use of `poolTotalPeUSDCirculation`.

The bug was found through manual review. The recommended mitigation step is to correct the accounting as follows: 

```solidity
   -     poolTotalPeUSDCirculation -= amount;
   +     poolTotalPeUSDCirculation -= (amount - totalFee);
```

The bug has been confirmed by LybraFinance.

### Original Finding Content


Incorrect accounting of `poolTotalPeUSDCirculation`, results in an understatement of `poolTotalPeUSDCirculation` amounts. This causes inaccurate bookkeeping and in turn affects any other functions dependent on the use of `poolTotalPeUSDCirculation`.

### Proof of Concept

We look at function `_repay` of `LybraPeUSDVaultBase.sol` as [follows](https://github.com/code-423n4/2023-06-lybra/blob/7b73ef2fbb542b569e182d9abf79be643ca883ee/contracts/lybra/pools/base/LybraPeUSDVaultBase.sol#L192-L210):

```solidity
 function _repay(address _provider, address _onBehalfOf, uint256 _amount) internal virtual {
     try configurator.refreshMintReward(_onBehalfOf) {} catch {}
     _updateFee(_onBehalfOf);
     uint256 totalFee = feeStored[_onBehalfOf];
     uint256 amount = borrowed[_onBehalfOf] + totalFee >= _amount ? _amount : borrowed[_onBehalfOf] + totalFee;
     if(amount >= totalFee) {
         feeStored[_onBehalfOf] = 0;
         PeUSD.transferFrom(_provider, address(configurator), totalFee);
         PeUSD.burn(_provider, amount - totalFee);
     } else {
         feeStored[_onBehalfOf] = totalFee - amount;
         PeUSD.transferFrom(_provider, address(configurator), amount);
     }
     try configurator.distributeRewards() {} catch {}
     borrowed[_onBehalfOf] -= amount;
     poolTotalPeUSDCirculation -= amount;


     emit Burn(_provider, _onBehalfOf, amount, block.timestamp);
 }
```

In particular, note the accounting of `poolTotalPeUSDCirculation` after repayment as [follows](https://github.com/code-423n4/2023-06-lybra/blob/7b73ef2fbb542b569e182d9abf79be643ca883ee/contracts/lybra/pools/base/LybraPeUSDVaultBase.sol#L207):

```solidity
        poolTotalPeUSDCirculation -= amount;
```

Consider a scenario per below for user Alice, where:

- Amount borrowed = 200
- TotalFee = 2

| Repay Scenario (PeUSD)        |         |
| ----------------------------- | ------: |
| _amount input                 |     100 |
| totalFee                      |       2 |
| amount (repay)                |     100 |
| Fees left                     |       0 |
| PeUSD transfer to config addr |       2 |
| PeUSD burnt                   |      98 |
| borrowed[Alice]               |     100 |
| poolTotalPeUSDCirculation (X) | X - 100 |


Based on the accounting flow of the function, the fees incurred are transferred to `address(configurator)`.
The amount burned is `amount - totalFee`. However, we see that `poolTotalPeUSDCirculation` reduces the entire `amount` where it should be `amount - totalFee` reduced.

This results in an understatement of `poolTotalPeUSDCirculation` amounts.

### Tools Used

Manual review

### Recommended Mitigation Steps

Correct the accounting as follows:

```solidity
   -     poolTotalPeUSDCirculation -= amount;
   +     poolTotalPeUSDCirculation -= (amount - totalFee);
```

### Assessed type

Error

**[LybraFinance confirmed](https://github.com/code-423n4/2023-06-lybra-findings/issues/532#issuecomment-1639805030)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Lybra Finance |
| Report Date | N/A |
| Finders | gs8nrv, peanuts, bytes032, Iurii3, OMEN, CrypticShepherd, SpicyMeatball, mahdikarimi, Vagner, Kenshin, Co0nan, cccz, 0xRobocop, Toshii, kenta, pep7siup, DedOhWale, Musaka, RedOneN, max10afternoon, lanrebayode77, hl\_ |

### Source Links

- **Source**: https://code4rena.com/reports/2023-06-lybra
- **GitHub**: https://github.com/code-423n4/2023-06-lybra-findings/issues/532
- **Contest**: https://code4rena.com/reports/2023-06-lybra

### Keywords for Search

`vulnerability`

