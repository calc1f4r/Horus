---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: first_depositor_issue

# Attack Vector Details
attack_type: first_depositor_issue
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7321
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
github_link: none

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
  - first_depositor_issue

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Zach Obront
  - Sawmon and Natalie
  - Blockdev
  - Noah Marconi
---

## Vulnerability Title

First vault deposit can cause excessive rounding

### Overview


This bug report is about an issue with the ERC4626-Cloned.sol#L130 code. The modification requires the initial mint to cost 10 full WETH, but the deposit is still unchanged and the initial deposit may be 1 wei worth of WETH, in return for 1 wad worth of vault shares. This issue may still surface by calling mint in a way that sets the price per share high. 

The recommendation is to revert the hardcoding of 10e18 in previewMint and previewWithdraw, so that the first minting is 1:1 asset to share price. To prevent share price manipulation, a condition should be added in each of mint and deposit reverting if assets (when depositing) or shares (when minting) are not above the minimum asset amount when totalSupply() == 0. This comes at the cost of a duplicate storage read. For WETH vaults, the minimum asset amount for initial deposit can be a small amount, such as 100 gwei so long as shares are issued 1:1 for the first mint/deposit.

### Original Finding Content

## ERC4626 Clone Analysis

## Severity
**Medium Risk**

## Context
`ERC4626-Cloned.sol#L130`

## Description
Aside from storage layout/getters, the context above notes the other major departure from Solmate's ERC4626 implementation. The modification requires the initial mint to cost 10 full WETH.

### Code Snippet
```solidity
function mint(
    uint256 shares,
    address receiver
) public virtual returns (uint256 assets) {
    // assets is 10e18, or 10 WETH, whenever totalSupply() == 0
    assets = previewMint(shares); // No need to check for rounding error, previewMint rounds up.
    // Need to transfer before minting or ERC777s could reenter.
    // minter transfers 10 WETH to the vault
    ERC20(asset()).safeTransferFrom(msg.sender, address(this), assets);
    // shares received are based on user input
    _mint(receiver, shares);
    emit Deposit(msg.sender, receiver, assets, shares);
    afterDeposit(assets, shares);
}
```

Astaria highlighted that the code diff from Solmate is in relation to this finding from the previous Sherlock audit. However, the deposit is still unchanged, and the initial deposit may be 1 wei worth of WETH, in return for 1 wad worth of vault shares.

Furthermore, the previously cited issue may still surface by calling `mint` in a way that sets the price per share high (e.g., 10 shares for 10 WETH produces a price per of 1:1e18). Albeit, it comes at a higher cost to the minter to set the initial price that high.

## Recommendation
- Revert the hardcoding of `10e18` in `previewMint` and `previewWithdraw`; this will require the first minting to be at a 1:1 asset to share price.
- Prevent share price manipulation by adding a condition in each of `mint` and `deposit` that reverts if `assets` (when depositing) or `shares` (when minting) are not above the minimum asset amount when `totalSupply() == 0`. This comes at the cost of a duplicate storage read.

For WETH vaults, the minimum asset amount for the initial deposit can be a small amount, such as 100 gwei, so long as shares are issued 1:1 for the first mint/deposit.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Zach Obront, Sawmon and Natalie, Blockdev, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf

### Keywords for Search

`First Depositor Issue`

