---
# Core Classification
protocol: THORSwap Aggregators
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50474
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/thorswap/thorswap-aggregators-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/thorswap/thorswap-aggregators-smart-contract-security-assessment
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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

MISSING RE-ENTRANCY PROTECTION

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `vTHOR` contract missed the nonReentrant guard in the `deposit`, `mint`, `withdraw` and `redeem` public functions. Even if the functions follow the check-effects-interactions pattern, we recommend using a mutex to be protected against cross-function reentrancy attacks. By using this lock, an attacker can no longer exploit the function with a recursive call.

Note that the `vTHOR` contract included a mutex implementation called `ReentrancyGuard`, which provides a modifier to any function called `nonReentrant` that guards with a mutex against reentrancy attacks. However, the modifier is not used within the contract.

Code Location
-------------

#### vTHOR.sol

```
function deposit(uint256 assets, address receiver) public returns (uint256 shares) {
    // Check for rounding error since we round down in previewDeposit.
    require((shares = previewDeposit(assets)) != 0, "ZERO_SHARES");
    // Need to transfer before minting or ERC777s could reenter.
    address(_asset).safeTransferFrom(msg.sender, address(this), assets);
    _mint(receiver, shares);
    emit Deposit(msg.sender, receiver, assets, shares);
}

function mint(uint256 shares, address receiver) public returns (uint256 assets) {
    assets = previewMint(shares); // No need to check for rounding error, previewMint rounds up.
    // Need to transfer before minting or ERC777s could reenter.
    address(_asset).safeTransferFrom(msg.sender, address(this), assets);
    _mint(receiver, shares);
    emit Deposit(msg.sender, receiver, assets, shares);
}

function withdraw(
    uint256 assets,
    address receiver,
    address owner
) public returns (uint256 shares) {
    shares = previewWithdraw(assets); // No need to check for rounding error, previewWithdraw rounds up.
    if (msg.sender != owner) {
        uint256 allowed = allowance[owner][msg.sender]; // Saves gas for limited approvals.
        if (allowed != type(uint256).max) allowance[owner][msg.sender] = allowed - shares;
    }
    _burn(owner, shares);
    emit Withdraw(msg.sender, receiver, owner, assets, shares);
    address(_asset).safeTransfer(receiver, assets);
}

function redeem(
    uint256 shares,
    address receiver,
    address owner
) public returns (uint256 assets) {
    if (msg.sender != owner) {
        uint256 allowed = allowance[owner][msg.sender]; // Saves gas for limited approvals.
        if (allowed != type(uint256).max) allowance[owner][msg.sender] = allowed - shares;
    }
    // Check for rounding error since we round down in previewRedeem.
    require((assets = previewRedeem(shares)) != 0, "ZERO_ASSETS");
    _burn(owner, shares);
    emit Withdraw(msg.sender, receiver, owner, assets, shares);
    address(_asset).safeTransfer(receiver, assets);
}

```

##### Score

Impact: 3  
Likelihood: 1

##### Recommendation

**SOLVED**: The `THORSwap team` added the `nonReentrant` modifier to the `deposit`, `mint`, `withdraw` and `redeem` functions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | THORSwap Aggregators |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/thorswap/thorswap-aggregators-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/thorswap/thorswap-aggregators-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

