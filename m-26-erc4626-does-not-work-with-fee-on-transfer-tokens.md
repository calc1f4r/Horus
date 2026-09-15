---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: fee_on_transfer

# Attack Vector Details
attack_type: fee_on_transfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3701
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/3

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
  - fee_on_transfer

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Bnke0x0
  - w42d3n
  - pashov
---

## Vulnerability Title

M-26: ERC4626 does not work with fee-on-transfer tokens

### Overview


This bug report is about an issue with the ERC4626 code, which does not work with fee-on-transfer tokens. The issue is that the `assets` variable is the pre-fee amount, including the fee, whereas the totalAssets do not include the fee anymore. This can be abused to mint more shares than desired. The code snippet provided shows the deposit function which is affected by this issue. It is recommended that the `assets` should be the amount excluding the fee, i.e., the amount the contract actually received. However, this could create another issue with ERC777 tokens. An alternative solution could be to overwrite the `previewDeposit` function to predict the post-fee amount and do the shares computation on that. The discussion section of the bug report states that the team will not be supporting fee-on-transfer tokens at the time.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/3 

## Found by 
pashov, w42d3n, Bnke0x0

## Summary

## Vulnerability Detail

## Impact
The ERC4626-Cloned.deposit/mint functions do not work well with fee-on-transfer tokens as the `assets` variable is the pre-fee amount, including the fee, whereas the totalAssets do not include the fee anymore.

## Code Snippet
This can be abused to mint more shares than desired.

https://github.com/sherlock-audit/2022-10-astaria/blob/main/lib/astaria-gpl/src/ERC4626-Cloned.sol#L305-L322

             '  function deposit(uint256 assets, address receiver)
                 public
                 virtual
                 override(IVault)
                 returns (uint256 shares)
               {
                 // Check for rounding error since we round down in previewDeposit.
                 require((shares = previewDeposit(assets)) != 0, "ZERO_SHARES");

                 // Need to transfer before minting or ERC777s could reenter.
                 ERC20(underlying()).safeTransferFrom(msg.sender, address(this), assets);

                 _mint(receiver, shares);

                 emit Deposit(msg.sender, receiver, assets, shares);

                 afterDeposit(assets, shares);
               }'

https://github.com/sherlock-audit/2022-10-astaria/blob/main/lib/astaria-gpl/src/ERC4626-Cloned.sol#L315

     `ERC20(underlying()).safeTransferFrom(msg.sender, address(this), assets);`

A `deposit(1000)` should result in the same shares as two deposits of `deposit(500)` but it does not because `assets` is the pre-fee amount.
Assume a fee-on-transfer of `20%`. Assume current `totalAmount = 1000`, `totalShares = 1000` for simplicity.

`deposit(1000) = 1000 / totalAmount * totalShares = 1000 shares`.
`deposit(500) = 500 / totalAmount * totalShares = 500 shares`. Now the `totalShares` increased by 500 but the `totalAssets` only increased by `(100% - 20%) * 500 = 400`. Therefore, the second `deposit(500) = 500 / (totalAmount + 400) * (newTotalShares) = 500 / (1400) * 1500 = 535.714285714 shares`.

In total, the two deposits lead to `35` more shares than a single deposit of the sum of the deposits.

## Tool used

Manual Review

## Recommendation
`assets` should be the amount excluding the fee, i.e., the amount the contract actually received.
This can be done by subtracting the pre-contract balance from the post-contract balance.
However, this would create another issue with ERC777 tokens.

Maybe `previewDeposit` should be overwritten by vaults supporting fee-on-transfer tokens to predict the post-fee amount. And do the shares computation on that, but then the `afterDeposit` is still called with the original `assets`and implementers need to be aware of this.

## Discussion

**androolloyd**

we will not be supporting fee on transfer tokens at the time

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Bnke0x0, w42d3n, pashov |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/3
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`Fee On Transfer`

