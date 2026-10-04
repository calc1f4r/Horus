---
# Core Classification
protocol: Blueberry
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6660
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/41
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/82

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - leveraged_farming
  - dexes
  - cdp
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - rvierdiiev
---

## Vulnerability Title

M-13: BasicSpell.doCutRewardsFee uses depositFee instead of withdraw fee

### Overview


This bug report is about the BasicSpell.doCutRewardsFee function in the 2023-02-blueberry-judging project on Github. The bug was found by rvierdiiev using manual review. The bug is that this function takes the bank.config().depositFee() instead of the bank.config().withdrawFee() when getting fee from ICHI rewards collected by farming. This means that the wrong fee amount is taken, resulting in an impact to the project. The code snippet and recommendation for this bug is given in the report. The recommendation is to take the withdraw fee from rewards.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/82 

## Found by 
rvierdiiev

## Summary
BasicSpell.doCutRewardsFee uses depositFee instead of withdraw fee
## Vulnerability Detail
https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/spell/BasicSpell.sol#L65-L79
```solidity
    function doCutRewardsFee(address token) internal {
        if (bank.config().treasury() == address(0)) revert NO_TREASURY_SET();


        uint256 balance = IERC20Upgradeable(token).balanceOf(address(this));
        if (balance > 0) {
            uint256 fee = (balance * bank.config().depositFee()) / DENOMINATOR;
            IERC20Upgradeable(token).safeTransfer(
                bank.config().treasury(),
                fee
            );


            balance -= fee;
            IERC20Upgradeable(token).safeTransfer(bank.EXECUTOR(), balance);
        }
    }
```
This function is called in order to get fee from ICHI rewards, collected by farming.
But currently it takes `bank.config().depositFee()` instead of `bank.config().withdrawFee()`.
## Impact
Wrong fee amount is taken.
## Code Snippet
https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/spell/BasicSpell.sol#L65-L79
## Tool used

Manual Review

## Recommendation
Take withdraw fee from rewards.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry |
| Report Date | N/A |
| Finders | rvierdiiev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/82
- **Contest**: https://app.sherlock.xyz/audits/contests/41

### Keywords for Search

`vulnerability`

