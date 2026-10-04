---
# Core Classification
protocol: Blueberry
chain: everychain
category: uncategorized
vulnerability_type: withdraw_pattern

# Attack Vector Details
attack_type: withdraw_pattern
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6646
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/41
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/33

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - withdraw_pattern
  - missing-logic
  - coding-bug

protocol_categories:
  - leveraged_farming
  - dexes
  - cdp
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - csanuragjain
  - 0x52
  - y1cunhui
  - Ruhum
  - evan
---

## Vulnerability Title

H-9: BlueBerryBank#withdrawLend will cause underlying token accounting error if soft/hard vault has withdraw fee

### Overview


This bug report is about an issue found in BlueBerryBank#withdrawLend that can cause a token accounting error if a soft/hard vault has a withdraw fee. The issue is that the withdraw fee is not taken into account when the user withdraws their shares, leading to an incorrect calculation of the underlying amount for the user. This can lead to the user having phantom collateral that can be used to take out loans, but is not actually real. 

The issue was found by y1cunhui, rvierdiiev, csanuragjain, Ruhum, evan, and 0x52, and was found through manual review. The code snippet of the affected area is available at https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/BlueBerryBank.sol#L669-L704.

The recommendation is that HardVault/SoftVault#withdraw should also return the fee paid to the vault, so that it can be accounted for. This would ensure that the underlying amount is correctly calculated and that the user does not have phantom collateral.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/33 

## Found by 
y1cunhui, rvierdiiev, csanuragjain, Ruhum, evan, 0x52

## Summary

Soft/hard vaults can have a withdraw fee. This takes a certain percentage from the user when they withdraw. The way that the token accounting works in BlueBerryBank#withdrawLend, it will only remove the amount returned by the hard/soft vault from pos.underlying amount. If there is a withdraw fee, underlying amount will not be decrease properly and the user will be left with phantom collateral that they can still use.

## Vulnerability Detail

        // Cut withdraw fee if it is in withdrawVaultFee Window (2 months)
        if (
            block.timestamp <
            config.withdrawVaultFeeWindowStartTime() +
                config.withdrawVaultFeeWindow()
        ) {
            uint256 fee = (withdrawAmount * config.withdrawVaultFee()) /
                DENOMINATOR;
            uToken.safeTransfer(config.treasury(), fee);
            withdrawAmount -= fee;
        }

Both SoftVault and HardVault implement a withdraw fee. Here we see that withdrawAmount (the return value) is decreased by the fee amount.

        uint256 wAmount;
        if (address(ISoftVault(bank.softVault).uToken()) == token) {
            ISoftVault(bank.softVault).approve(
                bank.softVault,
                type(uint256).max
            );
            wAmount = ISoftVault(bank.softVault).withdraw(shareAmount);
        } else {
            wAmount = IHardVault(bank.hardVault).withdraw(token, shareAmount);
        }

        wAmount = wAmount > pos.underlyingAmount
            ? pos.underlyingAmount
            : wAmount;

        pos.underlyingVaultShare -= shareAmount;
        pos.underlyingAmount -= wAmount;
        bank.totalLend -= wAmount;

The return value is stored as `wAmount` which is then subtracted from `pos.underlyingAmount` the issue is that the withdraw fee has now caused a token accounting error for `pos`. We see that the fee paid to the hard/soft vault is NOT properly removed from `pos.underlyingAmount`. This leaves the user with phantom underlying which doesn't actually exist but that the user can use to take out loans.

Exmaple:
For simplicity let's say that 1 share = 1 underlying and the soft/hard vault has a fee of 5%. Imagine a user deposits 100 underlying to receive 100 shares. Now the user withdraws their 100 shares while the hard/soft vault has a withdraw. This burns 100 shares and softVault/hardVault.withdraw returns 95 (100 - 5). During the token accounting pos.underlyingVaultShares are decreased to 0 but pos.underlyingAmount is still equal to 5 (100 - 95).

      uint256 cv = oracle.getUnderlyingValue(
          pos.underlyingToken,
          pos.underlyingAmount
      );

This accounting error is highly problematic because collateralValue uses pos.underlyingAmount to determine the value of collateral for liquidation purposes. This allows the user to take on more debt than they should.

## Impact

User is left with collateral that isn't real but that can be used to take out a loan

## Code Snippet

https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/BlueBerryBank.sol#L669-L704

## Tool used

Manual Review

## Recommendation

`HardVault/SoftVault#withdraw` should also return the fee paid to the vault, so that it can be accounted for.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry |
| Report Date | N/A |
| Finders | csanuragjain, 0x52, y1cunhui, Ruhum, evan, rvierdiiev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/33
- **Contest**: https://app.sherlock.xyz/audits/contests/41

### Keywords for Search

`Withdraw Pattern, Missing-Logic, Coding-Bug`

