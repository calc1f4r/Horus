---
# Core Classification
protocol: Sublime
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1196
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-sublime-contest
source_link: https://code4rena.com/reports/2021-12-sublime
github_link: https://github.com/code-423n4/2021-12-sublime-findings/issues/90

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

protocol_categories:
  - dexes
  - cdp
  - services
  - leveraged_farming
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - hyh
  - 0x0x0x
---

## Vulnerability Title

[M-02] CreditLine.liquidate doesn't transfer borrowed ETH to a lender

### Overview


This bug report concerns the CreditLine.liquidate function on the Ethereum blockchain. Funds that should be sent to a lender are left with the contract instead. This means that manual accounting and fund transfer for each CreditLine.liquidate usage will be required for after-the-fact mitigation. The recommended mitigation step is to add a transfer to the lender for ETH cases. The code should be changed from what is currently written to the code provided in the report.

### Original Finding Content

_Submitted by hyh, also found by 0x0x0x_

#### Impact

Funds that are acquired from a liquidator and should be sent to a lender are left with the contract instead. The funds aren't lost, but after the fact mitigation will require manual accounting and fund transfer for each CreditLine.liquidate usage.

#### Proof of Concept

ETH sent to CreditLine.liquidate by an external liquidator when `autoLiquidation` is enabled remain with the contract and aren't transferred to the lender:
<https://github.com/code-423n4/2021-12-sublime/blob/main/contracts/CreditLine/CreditLine.sol#L1015>

#### Recommended Mitigation Steps

Add transfer to a lender for ETH case:

Now:
```solidity

if (_borrowAsset == address(0)) {
        uint256 _returnETH = msg.value.sub(_borrowTokens, 'Insufficient ETH to liquidate');
        if (_returnETH != 0) {
                (bool success, ) = msg.sender.call{value: _returnETH}('');
                require(success, 'Transfer fail');
        }
}
```
To be:
```solidity

if (_borrowAsset == address(0)) {
        uint256 _returnETH = msg.value.sub(_borrowTokens, 'Insufficient ETH to liquidate');
        
        (bool success, ) = _lender.call{value: _borrowTokens}('');
        require(success, 'liquidate: Transfer failed');
        
        if (_returnETH != 0) {
                (success, ) = msg.sender.call{value: _returnETH}('');
                require(success, 'liquidate: Return transfer failed');
        }
}
```
**[ritik99 (Sublime) confirmed](https://github.com/code-423n4/2021-12-sublime-findings/issues/90)**




### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sublime |
| Report Date | N/A |
| Finders | hyh, 0x0x0x |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-sublime
- **GitHub**: https://github.com/code-423n4/2021-12-sublime-findings/issues/90
- **Contest**: https://code4rena.com/contests/2021-12-sublime-contest

### Keywords for Search

`vulnerability`

