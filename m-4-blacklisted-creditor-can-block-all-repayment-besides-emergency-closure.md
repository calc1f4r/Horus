---
# Core Classification
protocol: Real Wagmi #2
chain: everychain
category: uncategorized
vulnerability_type: blacklisted

# Attack Vector Details
attack_type: blacklisted
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27401
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/118
source_link: none
github_link: https://github.com/sherlock-audit/2023-10-real-wagmi-judging/issues/83

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.95
financial_impact: medium

# Scoring
quality_score: 4.75
rarity_score: 3.333333333333333

# Context Tags
tags:
  - blacklisted
  - usdc
  - usdt

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - tsvetanovv
  - Bauer
  - 0x52
  - ArmedGoose
---

## Vulnerability Title

M-4: Blacklisted creditor can block all repayment besides emergency closure

### Overview


This bug report is about a vulnerability found in the LiquidityManager.sol contract of the Wagmi Leverage platform. The code in question is executed when attempting to repay a loan, where the creditor is directly transferred their tokens from the vault. If the creditor is blacklisted for the hold token, then the transfer will revert, preventing the user from ever repaying their loan and forcing them to default. This issue was found by 0x52, ArmedGoose, Bauer, and tsvetanovv. 

The recommendation to fix this issue is to create an escrow to hold funds in the event that the creditor cannot receive their funds. A try-catch block should be implemented around the transfer to the creditor, so if it fails then the funds are sent instead to an escrow account. This allows the creditor to claim their tokens later and for the transaction to complete. 

The issue has since been fixed, according to a comment from fann95, with a commit to the github repository.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-10-real-wagmi-judging/issues/83 

## Found by 
0x52, ArmedGoose, Bauer, tsvetanovv

After liquidity is restored to the LP, accumulated fees are sent directly from the vault to the creditor. Some tokens, such as USDC and USDT, have blacklists the prevent users from sending or receiving tokens. If the creditor is blacklisted for the hold token then the fee transfer will always revert. This forces the borrower to defualt. LPs can recover their funds but only after the user has defaulted and they request emergency closure.

## Vulnerability Detail

https://github.com/sherlock-audit/2023-10-real-wagmi/blob/main/wagmi-leverage/contracts/abstract/LiquidityManager.sol#L306-L315

            address creditor = underlyingPositionManager.ownerOf(loan.tokenId);
            // Increase liquidity and transfer liquidity owner reward
            _increaseLiquidity(cache.saleToken, cache.holdToken, loan, amount0, amount1);
            uint256 liquidityOwnerReward = FullMath.mulDiv(
                params.totalfeesOwed,
                cache.holdTokenDebt,
                params.totalBorrowedAmount
            ) / Constants.COLLATERAL_BALANCE_PRECISION;

            Vault(VAULT_ADDRESS).transferToken(cache.holdToken, creditor, liquidityOwnerReward);

The following code is executed for each loan when attempting to repay. Here we see that each creditor is directly transferred their tokens from the vault. If the creditor is blacklisted for holdToken, then the transfer will revert. This will cause all repayments to revert, preventing the user from ever repaying their loan and forcing them to default. 

## Impact

Borrowers with blacklisted creditors are forced to default

## Code Snippet

[LiquidityManager.sol#L223-L321](https://github.com/sherlock-audit/2023-10-real-wagmi/blob/main/wagmi-leverage/contracts/abstract/LiquidityManager.sol#L223-L321)

## Tool used

Manual Review

## Recommendation

Create an escrow to hold funds in the event that the creditor cannot receive their funds. Implement a try-catch block around the transfer to the creditor. If it fails then send the funds instead to an escrow account, allowing the creditor to claim their tokens later and for the transaction to complete.



## Discussion

**fann95**

Fixed: https://github.com/RealWagmi/wagmi-leverage/commit/3c17a39e8a69a8912e6f87e84a19f55889353328

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4.75/5 |
| Rarity Score | 3.333333333333333/5 |
| Audit Firm | Sherlock |
| Protocol | Real Wagmi #2 |
| Report Date | N/A |
| Finders | tsvetanovv, Bauer, 0x52, ArmedGoose |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-10-real-wagmi-judging/issues/83
- **Contest**: https://app.sherlock.xyz/audits/contests/118

### Keywords for Search

`Blacklisted, USDC, USDT`

