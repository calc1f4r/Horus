---
# Core Classification
protocol: Cryptex
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40221
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/c146b746-c0ce-4310-933c-d2e5e3ec934a
source_link: https://cdn.cantina.xyz/reports/cantina_cryptex_sep2024.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cccz
  - Patrick Drotleff
---

## Vulnerability Title

Create Token Integration Checklist 

### Overview

See description below for full details.

### Original Finding Content

## TCAPv2 Governance and Token Integration Checklist

## Context
(No context files were provided by the reviewer)

## Description
Like other contracts of Cryptex before, TCAPv2 is planned to be under the control of Community Governance (DAO). This includes the creation of additional Vaults, of which there will likely be an increasing amount in order to attract liquidity.

To allow the community to verify the Vaults being added, an important aspect is checking whether the token supposed to serve as collateral is properly compatible with the protocol. For this purpose, it is recommendable to provide those who will vote on such proposals a **Token Integration Checklist**.

## Recommendations
We provide the following recommendations regarding the creation of such a checklist based on our review and understanding of the protocol:

- **Token Standards:** This protocol only deals with underlying tokens of ERC-20 compatible standards. Other fungible token standards such as ERC-1155 are not supported.

- **Double-Entry-Point Tokens:** These are tokens that share the same tracking of balances but have two separate contract addresses from which these balances can be controlled. Typically, protocols that have sweeping functions (for rescuing funds) are vulnerable to these since they bypass checks preventing sweeping of underlying funds. Pocket contracts do not appear to be vulnerable to this, and using such tokens as underlying should not cause any issues.

- **Token Error Handling:** ERC-20 Tokens historically handle errors in two possible ways: they either revert on errors or they simply return a false boolean as a result. With the fixes applied, this protocol correctly handles both cases thanks to the usage of Solady’s `SafeTransferLib`'s `safeTransferFrom()`.

- **ERC-20 Optional Decimals:** Within the ERC-20 standard, the existence of a `decimals()` function is optional. This protocol, however, requires it to be present (`BaseOracleUSD.assetDecimals`) and constant over its lifetime. Assuming the function is implemented by the token, it should return its value as `uint8` type; if not, the value must be below 255.

- **Tokens with Callbacks:** There exist various standard extensions such as ERC-223, ERC-677, ERC-777, etc., as well as custom ERC-20 compatible token implementations that call the sender, receiver, or both during a token transfer. Furthermore, such implementations may choose to call before or after the token balances were updated. This is especially dangerous since it may allow re-entering the protocol and exploit incomplete state updates.

  – To avoid any issues with such tokens, it is recommended to follow the **CEI-pattern**. There is currently only one place apparent where this pattern is not being followed: within `Vault.sol`, the withdrawal of tokens should come after the burning of TCAP debt.

  ```diff
  - pocket.withdraw(user, liquidationReward, msg.sender);
  TCAPV2.burn(msg.sender, burnAmount);
  + pocket.withdraw(user, liquidationReward, msg.sender);
  ```

- **Deflationary/Inflationary or Rebasing Tokens:** There are tokens (such as Aave’s aToken) which increase or decrease in balance over time (various algorithmic stable coins). This may cause accounting issues within smart contracts holding them. Pockets should be resistant to such issues since they take account of shares, not the actual underlying balances. Whether an underlying token decreases or increases in balance, it would effectively decrease or increase the locked underlying value behind each share.

- **Tokens with Transfer Fees:** Some tokens may charge a fee for transfers. This fee could be applied on the value being sent, decreasing the amount reaching the receiver, or it could be applied on the sender's remaining balance. Pocket contracts are currently not equipped to handle either of these cases appropriately and won't be without significant changes to how deposits and withdrawals are handled.

- **Tokens with Strict Allowance Handling:** There exist tokens that error when attempting to change an existing token allowance from one non-zero value to another non-zero value. At the moment, this is only relevant for the `AaveV3Pocket` contract which should be able to handle this whether the logic stays as is (approving the exact amount to be deposited) or is changed according to other recommendations within this audit (unlimited approval once in the constructor).

- **Non-Standard Decimals:** Tokens typically have 18 decimals, but some deviate from this, usually towards lower numbers. During this audit, we pointed out a few places where the handling of such non-standard decimals was lacking. Assuming those were all places and they have been fixed appropriately, this protocol should be able to handle such assets.

- **Extreme Scale Deviations:** There may be tokens which have both:
  1. Very low decimal values and...
  2. Are very valuable.

  This means that the balances when dealing with these tokens could be so small that rounding errors lead to significant differences in monetary value. It should be checked whether tokens fall into such a category, and if potentially so, it should be mathematically verified whether rounding errors are within acceptable ranges.

- **Oracle Integration:** For an asset to be used as collateral within this protocol, it must have an active Chainlink Price Feed. Furthermore, the `AggregatedChainlinkOracle` contract adjusts the price responses to 18 decimals based on the reported `decimals()` of the feed. As a sanity check, it should be verified that:
  1. This decimals value indeed is below 18 as expected by the contract and...
  2. The reported decimals value truthfully matches the actual prices currently reported by the feed.

Consider consulting the [Crytic Checklist](https://trailofbits.com/) for further inspiration.

## Acknowledgments
- Cryptex: Acknowledged.
- Cantina Managed: Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Cryptex |
| Report Date | N/A |
| Finders | cccz, Patrick Drotleff |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_cryptex_sep2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/c146b746-c0ce-4310-933c-d2e5e3ec934a

### Keywords for Search

`vulnerability`

