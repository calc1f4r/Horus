---
# Core Classification
protocol: LoopFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49027
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-loopfi
source_link: https://code4rena.com/reports/2024-07-loopfi
github_link: https://github.com/code-423n4/2024-07-loopfi-findings/issues/170

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - lian886
  - novamanbg
---

## Vulnerability Title

[H-05] There is a calculation error in `AuraVault::redeem()`

### Overview


This bug report discusses an issue where users are losing funds due to a mistake in the code for the AuraVault contract. The code confuses the shares of the AuraVault contract with the shares of the rewardPool contract, causing users to receive less assets than they should when they withdraw. This is a problem because the ratio of share to asset is not always 1:1 in the AuraVault contract, but it is in the rewardPool contract. The report recommends a mitigation step to fix the issue by modifying the code in the redeem function. The type of bug is an error and the team has acknowledged it and will remove the AuraVault contract.

### Original Finding Content


The amount of funds that users can withdraw decreases, leading to a loss of funds for users.

### Proof of Concept

```javascript
  function redeem(
        uint256 shares,
        address receiver,
        address owner
    ) public virtual override(IERC4626, ERC4626) returns (uint256) {
        require(shares <= maxRedeem(owner), "ERC4626: redeem more than max");

        // Redeem assets from Aura reward pool and send to "receiver"
@>>        uint256 assets = IPool(rewardPool).redeem(shares, address(this), address(this));

        _withdraw(_msgSender(), receiver, owner, assets, shares);

        return assets;
    }
```

We can see that `AuraVault::redeem()` confuses AuraVault’s shares with `rewardPool`’s shares. AuraVault’s shares need to be converted into AuraVault’s underlying tokens (assets) before they can be withdrawn. This is particularly problematic because, as we know from the `rewardPool` contract address, `rewardPool::redeem()` functions the same way as `rewardPool::withdraw()`.

<https://vscode.blockscan.com/ethereum/0x00A7BA8Ae7bca0B10A32Ea1f8e2a1Da980c6CAd2>

```javascript
 function redeem(
        uint256 shares,
        address receiver,
        address owner
    ) external virtual override returns (uint256) {
        return withdraw(shares, receiver, owner);
    }
```

Moreover, in the `rewardPool`, the ratio of share to asset is always 1:1.

**Scenario Example:**

Let’s assume that in `AuraVault`, the ratio of share to asset is always 1:2. In this case, if a user withdraws 1 share, they will ultimately receive only 1 asset; whereas, they should have received 2 assets.

### Recommended Mitigation Steps

```diff
  function redeem(
        uint256 shares,
        address receiver,
        address owner
    ) public virtual override(IERC4626, ERC4626) returns (uint256) {
        require(shares <= maxRedeem(owner), "ERC4626: redeem more than max");
+        uint256 assets = previewRedeem(shares);

        // Redeem assets from Aura reward pool and send to "receiver"
-       uint256 assets = IPool(rewardPool).redeem(shares, address(this), address(this));
+        assets = IPool(rewardPool).redeem(assets, address(this), address(this));

        _withdraw(_msgSender(), receiver, owner, assets, shares);

        return assets;
    }
```

### Assessed type

Error

**[amarcu (LoopFi) acknowledged and commented](https://github.com/code-423n4/2024-07-loopfi-findings/issues/170#issuecomment-2363355582):**
> Acknowledged but we will remove and not use the `AuraVault`.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | LoopFi |
| Report Date | N/A |
| Finders | lian886, novamanbg |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-loopfi
- **GitHub**: https://github.com/code-423n4/2024-07-loopfi-findings/issues/170
- **Contest**: https://code4rena.com/reports/2024-07-loopfi

### Keywords for Search

`vulnerability`

