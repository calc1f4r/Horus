---
# Core Classification
protocol: Syntetika
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62202
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
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
  - Dacian
  - Jorge
---

## Vulnerability Title

Missing check if `receiver` is whitelisted in `StakingVault::mint, deposit`

### Overview

See description below for full details.

### Original Finding Content

**Description:** `StakingVault::mint, deposit` only validates that `msg.sender` is whitelisted but fails to check if the receiver parameter is whitelisted. Since non-whitelisted addresses cannot withdraw, redeem, or transfer shares, any shares minted to non-whitelisted receivers become permanently locked and unusable.
```solidity
 function mint(
        uint256 shares,
        address receiver //@audit receiver could be not whitelisted?
    ) public override onlyWhitelisted(msg.sender) returns (uint256 assets) {
        ...
    }
```

**Impact:** Permanent loss of user funds or temporary if owner give whitelisted permissions.

**Proof of Concept:** Run the next proof of concept in `StakingVault.sol`:
```solidity
function test_mint_non_whitelist_receiver() public {
        uint256 amount = 100 ether;

        vm.startPrank(user1);
        asset.approve(address(vault), amount);

        //create a non whitelisted receiver
        address bob = makeAddr("receiver");

        // 1. Alice (whitelisted) mints shares to Bob (non-whitelisted)
        vault.mint(1000 * 1e8, bob); // Success - only checks Alice is whitelisted

        vm.stopPrank();

        // 2. Bob tries to withdraw - REVERTS
        vm.prank(bob);
        vault.withdraw(1000 * 1e8, bob, bob); // Reverts: not whitelisted
        // Result: 1000 shares worth of HilBTC permanently locked
    }

```

**Recommended Mitigation:** Add a whitelist check for the receiver in the mint() function:

```diff
function mint(
    uint256 shares,
    address receiver
+ ) public override onlyWhitelisted(msg.sender) onlyWhitelisted(receiver) returns (uint256 assets) {
-   ) public override onlyWhitelisted(msg.sender) returns (uint256 assets) {
 ...
}
// Similar fix to `deposit`
```

**Syntetika:**
Fixed in commit [86384fe](https://github.com/SyntetikaLabs/monorepo/commit/86384fe1504780338649d25f720fb78b25132875) by removing the whitelist functionality entirely from `StakingVault` to resolve finding L-4.

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Syntetika |
| Report Date | N/A |
| Finders | Dacian, Jorge |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

