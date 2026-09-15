---
# Core Classification
protocol: Harmonixfinance Hyperliquid
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57895
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/HarmonixFinance-Hyperliquid-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[M-05] Withdrawal Initiators Suffer Partial Loss When Share Price Increases

### Overview


This bug report describes a vulnerability in the code of a financial contract. The issue occurs when users initiate a withdrawal and the share prices increase before the withdrawal is executed. This results in users receiving fewer assets than they are entitled to. The problem is located in two functions in the contract code and can cause financial losses for users. The recommendation is to decouple the share validation from price fluctuations to prevent this issue from occurring. The team has fixed the bug.

### Original Finding Content

## Severity

Medium Risk

## Description

The vulnerability manifests in the interaction between `initiateWithdrawal()` and `withdraw()`. When share prices increase after initiation but before execution, the proportional calculation in `_withdraw()` divides the originally recorded withdrawal amount by the new, higher share price. This results in users receiving substantially fewer assets than their initial entitlement.

The critical flaw occurs in the shares-to-assets conversion, where `sharesWithdrawAmount = (_shares * userWithdraw.withdrawAmount) / userWithdraw.shares` fails to account for NAV increases. Since userWithdraw.withdrawAmount remains fixed at initiation-time values while share prices appreciate, the equation yields diminished asset payouts despite the fund's increased value.

## Location of Affected Code

File: [vaults/hyperliquid/fundContract.sol](https://github.com/harmonixfi/core-contracts/blob/f02157aba919dcdd4a1133669361224108c5caef/contracts/vaults/hyperliquid/fundContract.sol)

```solidity
function initiateWithdrawal(uint256 _shares) external nonReentrant {
    require(balanceOf(msg.sender) >= _shares, "INVALID_SHARES");
    UserWithdraw.WithdrawData memory userWithdraw = _getUserWithdraw(
        msg.sender
    );
    require(userWithdraw.shares == 0, "INVALID_WD_STATE");
    uint256 withdrawAmount = ShareMath.sharesToAsset(
        _shares,
        _getPricePerShare(),
        decimals()
    );

    uint256 managementFee = _calculateManagementFeeAmount(
        block.timestamp,
        withdrawAmount
    );
    _createUserWithdraw(
        msg.sender,
        userWithdraw,
        _shares,
        withdrawAmount,
        managementFee
    );

    emit WithdrawalInitiated(msg.sender, withdrawAmount, _shares);
}

function withdraw(
    uint256 assets,
    address receiver,
    address owner
) public override returns (uint256) {
    uint256 shares = convertToShares(assets);
    return _withdraw(shares, receiver, owner);
}
```

File: [vaults/hyperliquid/fundContract.sol](https://github.com/harmonixfi/core-contracts/blob/f02157aba919dcdd4a1133669361224108c5caef/contracts/vaults/hyperliquid/fundContract.sol)

```solidity
function _withdraw(
    uint256 _shares,
    address _receiver,
    address _owner
) private returns (uint256) {
    require(msg.sender == _owner, "INVALID_OWNER");

    UserWithdraw.WithdrawData memory userWithdraw = _getUserWithdraw(
        msg.sender
    );
    // @audit confirm this would fail if share price decreases
    require(userWithdraw.shares >= _shares, "INVALID_SHARES");
    .
    .
    uint256 sharesWithdrawAmount = (_shares * userWithdraw.withdrawAmount) /
        userWithdraw.shares;

    // code
}
```

## Impact

Users suffer direct financial losses when share prices rise, as their withdrawals become locked to outdated valuations due to only the partially withdrawn amount, which is set during `initiateWithdrawal()`, would be claimed, and the other remaining amount would be lost to the user.

## Recommendation

The solution requires decoupling the share validation from price fluctuations. Instead of recalculating shares during withdrawal, the contract should store the original share amount from `initiateWithdrawal()` and use it directly in `withdraw()` without recalculation.

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Harmonixfinance Hyperliquid |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/HarmonixFinance-Hyperliquid-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

