---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: weth

# Attack Vector Details
attack_type: weth
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7311
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
rarity_score: 5

# Context Tags
tags:
  - weth
  - erc4626
  - approve

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

Multiple ERC4626Router and ERC4626RouterBase functions will always revert

### Overview


This bug report is about the ERC4626Router.sol and ERC4626RouterBase.sol functions not working as intended. The intention of the functions is to allow deposit and redemption of funds without needing an approval, but this is not working as expected.

The depositToVault function works as intended, with WETH being transferred from the user to the router, then the router approving the vault for the correct amount of WETH, and finally vault.deposit() being called to transfer the WETH from the router into the vault.

However, the redeemMax function does not work as expected. The router approves the vault to spend its WETH, then vault.redeem() is called, which tries to transfer vault tokens from the router to the vault, and then mints the withdraw proxy tokens to the receiver. This does not work because the vault tokens need to be approved for transfer.

The same issue exists in the redeem() and withdraw() functions in ERC4626RouterBase.sol.

The recommendation is that the redeemMax function should follow the same flow as depositToVault, and that the ERC4626RouterBase functions should change the approval to be vault tokens rather than WETH.

### Original Finding Content

## Severity: Medium Risk

## Context
- `ERC4626Router.sol#L49-58`
- `ERC4626RouterBase.sol#L47`
- `ERC4626RouterBase.sol#L60`

## Description
The intention of the `ERC4626Router.sol` functions is that they are approval-less ways to deposit and redeem:

> For the below, no approval needed, assumes vault is already max approved.

As long as the user has approved the `TRANSFER_PROXY` for WETH, this works for the `depositToVault` function:
- WETH is transferred from the user to the router with `pullTokens`.
- The router approves the vault for the correct amount of WETH.
- `vault.deposit()` is called, which uses `safeTransferFrom` to transfer WETH from the router into the vault.

However, for the `redeemMax` function, it doesn't work:
- Approves the vault to spend the router's WETH.
- `vault.redeem()` is called, which tries to transfer vault tokens from the router to the vault, and then mints withdraw proxy tokens to the receiver.

This error occurs assuming that the vault tokens would be burned, in which case the logic would work. But since they are transferred into the vault until the end of the epoch, we require approvals.

The same issue also exists in these two functions in `ERC4626RouterBase.sol`:
- `redeem()`: this is where the incorrect approval lives, so the same issue occurs when it is called directly.
- `withdraw()`: the same faulty approval exists in this function.

## Recommendation
`redeemMax` should follow the same flow as `deposit` to make this work:
- `redeemMax` should `pullTokens` to pull the vault tokens from the user.
- The router should approve the vault to spend its own tokens, not WETH.
- Then we can call `vault.redeem()` and it will work as intended.

Both the `ERC4626RouterBase` functions should change the approval to be vault tokens rather than WETH:
```diff
- ERC20(vault.asset()).safeApprove(address(vault), amount);
+ vault.safeApprove(address(vault), amount);
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Zach Obront, Sawmon and Natalie, Blockdev, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf

### Keywords for Search

`WETH, ERC4626, Approve`

