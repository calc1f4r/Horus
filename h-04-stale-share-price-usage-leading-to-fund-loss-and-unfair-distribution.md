---
# Core Classification
protocol: Nexus_2024-11-29
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44984
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Nexus-security-review_2024-11-29.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[H-04] Stale share price usage leading to fund loss and unfair distribution

### Overview


This bug report discusses a problem with the share conversion in the `DepositETH` and `DepositUSD` contracts. These contracts are used for deposits and withdrawals and rely on the current share price, which can change over time due to yield from `Lido` and `sDAI`. However, the contracts do not properly update the share price when users perform deposits, withdrawals, or quote LayerZero fees. This can lead to a loss of funds and unfair share distribution for users. The report recommends updating the functions involved in share calculations to ensure the share price is always recalculated and updated.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

The share conversion is a critical operation in the `DepositETH` and `DepositUSD` contracts, where deposits and withdrawals are based on the current share price. The share price can fluctuate over time due to the yield received from `Lido` and `sDAI`, respectively.

However, the `DepositETH` and `DepositUSD` contracts do not properly update the share price when users perform deposits, withdrawals, or quote LayerZero fees. This failure to update the share price can result in the use of stale share prices, leading to a loss of funds and unfair share distribution for users.

```solidity
function _depositETH(string memory _receiver, uint256 _value, uint32 _destID, uint256 _lzFee) internal {
    if(msg.value==_value+_lzFee){
@>      uint256 nETHShares= (sharePrice*_value)/BASE_POINT;
        bytes memory data = abi.encode(ASSET_ID,1, _receiver,nETHShares);
        ethDeposited+=_value;
        nETHMinted+=nETHShares;
        IMessaging(messageApp).sendMessage{value:_lzFee}(data, _destID,_lzFee);
    }else{
        revert IncorrectValue();
    }
}
```

```solidity
function messageReceivedL2(uint256 _id, address _receiver, uint256 _value) external override onlyMessageApp {
    if(_id==3){
@>      uint256 _valueUSDCWithdraw = _value*BASE_POINT/sharePrice;
        _withdrawFunds(_receiver, _valueUSDCWithdraw);
    }
    else {
        revert IncorrectTypeID(_id,msg.sender);
    }
}
```

For example, during a withdrawal, if rewards accrue (thus changing the share price) between the time of the withdrawal request and its execution, the user will calculate the withdrawal amount using an outdated share price, which does not account for the new rewards. This can result in users withdrawing fewer funds than they are entitled to.

## Recommendations

Consider updating the functions that involve share calculations, such as deposits, withdrawals, and LayerZero fee quotes, to ensure that the share price is recalculated and updated during each crucial action.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Nexus_2024-11-29 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Nexus-security-review_2024-11-29.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

