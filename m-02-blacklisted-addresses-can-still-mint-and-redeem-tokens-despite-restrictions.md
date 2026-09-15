---
# Core Classification
protocol: Terplayer Berabtc
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55102
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Terplayer-BeraBTC-Security-Review.md
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

[M-02] Blacklisted Addresses Can Still Mint and Redeem Tokens Despite Restrictions

### Overview


This bug report is about a medium-risk vulnerability found in the contract code for a token called BeraBitcoin. The issue is that the contract does not have proper checks in place to prevent blacklisted users from receiving or burning tokens. This means that even if someone is flagged as a malicious actor and blacklisted, they can still receive newly minted tokens or redeem their existing tokens, potentially allowing them to continue exploiting the system. The affected code can be found in three functions: `custodianMint()`, `excessStakeMint()`, and `redeem()`. The recommendation is to add a blacklist check within these functions to prevent this vulnerability. The team has responded that the issue has been fixed.

### Original Finding Content

## Severity

Medium Risk

## Description

The contract fails to implement blacklist checks in critical token operations including `custodianMint()`, `excessStakeMint()`, and `redeem()` functions. While the contract maintains a blacklist mapping and implements checks for standard transfers via the `notBlacklisted()` modifier, these critical administrative functions lack similar protections.

The `custodianMint()` and `excessStakeMint()` functions allow privileged roles to mint tokens to any address without verifying if the recipient is blacklisted. Similarly, the redeem function permits any caller to burn tokens without checking if their address is blacklisted.

## Location of Affected Code

File: [src/BeraBitcoin.sol#L178](https://github.com/batoshidao/bera-bitcoin/blob/19d509911de64a062dfaeef33f14e26f08b23c10/src/BeraBitcoin.sol#L178)

```solidity
function custodianMint(
   address to,
   uint256 value
) public onlyRole(CUSTODIAN_ROLE) nonReentrant {
   if (mintFeeRate > 0) {
      value -= (value * mintFeeRate) / BASE_RATE;
   }
   _mint(to, value);
   emit CustodianMinted(to, value);
}
```

File: [src/BeraBitcoin.sol#L192](https://github.com/batoshidao/bera-bitcoin/blob/19d509911de64a062dfaeef33f14e26f08b23c10/src/BeraBitcoin.sol#L192)

```solidity
/// @notice Mints beraBTC by the excess stake role.
/// @param account The address to mint the beraBTC to.
/// @param value The amount of beraBTC to mint.
function excessStakeMint(
   address account,
   uint256 value
) public onlyRole(EXCESS_STAKE_ROLE) nonReentrant {
   _mint(account, value);
   emit ExcessStakeMinted(account, value);
}
```

File: [src/BeraBitcoin.sol#L203](https://github.com/batoshidao/bera-bitcoin/blob/19d509911de64a062dfaeef33f14e26f08b23c10/src/BeraBitcoin.sol#L203)

```solidity
function redeem(
   uint256 value,
   string memory recipient
) public nonReentrant {
   uint256 burned = value;
   _burn(msg.sender, burned);
   if (redeemFeeRate > 0) {
      value -= (burned * redeemFeeRate) / BASE_RATE;
   }
   emit Redeemed(msg.sender, burned, value, recipient);
}
```

## Impact

This vulnerability severely compromises the effectiveness of the blacklisting mechanism. Malicious actors who have been blacklisted can still receive newly minted tokens through the custodian or excess stake minting functions, allowing them to maintain token holdings despite sanctions. Additionally, blacklisted users can continue redeeming tokens, potentially enabling them to extract value from the system even after being flagged.

## Recommendation

Add blacklist check inside `custodianMint()`, `excessStakeMint()`, and `redeem()` functions to check the user is receiving/burning tokens is blacklisted or not.

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Terplayer Berabtc |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Terplayer-BeraBTC-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

