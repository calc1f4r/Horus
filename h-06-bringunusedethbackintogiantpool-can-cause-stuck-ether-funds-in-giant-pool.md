---
# Core Classification
protocol: Stakehouse Protocol
chain: everychain
category: uncategorized
vulnerability_type: don't_update_state

# Attack Vector Details
attack_type: don't_update_state
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5893
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest
source_link: https://code4rena.com/reports/2022-11-stakehouse
github_link: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/115

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - don't_update_state

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - koxuan
  - hihen
---

## Vulnerability Title

[H-06] BringUnusedETHBackIntoGiantPool can cause stuck ether funds in Giant Pool

### Overview


This bug report is about the vulnerability in the contracts GiantMevAndFeesPool and GiantSavETHVaultPool, which are part of the code-423n4/2022-11-stakehouse project. The vulnerability allows funds to be withdrawn from the vault if staking has not commenced and the idleETH variable is not updated. This means that the withdrawn funds will be stuck forever.

To prove the concept, a poc was added to the GiantPools.t.sol file. The poc involves withdrawing and depositing ETH for staking which fails and reverts due to the underflow in idleETH. The same problem exists in GiantSavETHVaultPool, but a poc cannot be done for it as another bug exists which prevents it from receiving funds.

The Foundry tool was used to find the vulnerability. To mitigate the problem, the idleETH variable should be updated in withdrawUnusedETHToGiantPool.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-11-stakehouse/blob/main/contracts/liquid-staking/GiantMevAndFeesPool.sol#L126-L138
https://github.com/code-423n4/2022-11-stakehouse/blob/main/contracts/liquid-staking/GiantSavETHVaultPool.sol#L137-L158


## Vulnerability details

## Impact
withdrawUnusedETHToGiantPool will withdraw any eth from the vault if staking has not commenced(knot status is INITIALS_REGISTERED), the eth will be drawn successful to the giant pool. However, idleETH variable is not updated. idleETH  is the available ETH for withdrawing and depositing eth for staking. Since there is no other places that updates idleETH other than depositing eth for staking and withdrawing eth, the eth withdrawn from the vault will be stuck forever. 

## Proof of Concept
place poc in GiantPools.t.sol with `import { MockStakingFundsVault } from "../../contracts/testing/liquid-staking/MockStakingFundsVault.sol";`


```solidity
    function testStuckFundsInGiantMEV() public {

        stakingFundsVault = MockStakingFundsVault(payable(manager.stakingFundsVault()));
        address nodeRunner = accountOne; vm.deal(nodeRunner, 4 ether);
        //address feesAndMevUser = accountTwo; vm.deal(feesAndMevUser, 4 ether);
        //address savETHUser = accountThree; vm.deal(savETHUser, 24 ether);
        address victim = accountFour; vm.deal(victim, 1 ether);


        registerSingleBLSPubKey(nodeRunner, blsPubKeyOne, accountFour);

        emit log_address(address(giantFeesAndMevPool));
        vm.startPrank(victim);

        emit log_uint(victim.balance);
        giantFeesAndMevPool.depositETH{value: 1 ether}(1 ether);
        bytes[][] memory blsKeysForVaults = new bytes[][](1);
        blsKeysForVaults[0] = getBytesArrayFromBytes(blsPubKeyOne);

        uint256[][] memory stakeAmountsForVaults = new uint256[][](1);
        stakeAmountsForVaults[0] = getUint256ArrayFromValues(1 ether);
        giantFeesAndMevPool.batchDepositETHForStaking(getAddressArrayFromValues(address(stakingFundsVault)),getUint256ArrayFromValues(1 ether) , blsKeysForVaults, stakeAmountsForVaults);

        emit log_uint(victim.balance);


        vm.warp(block.timestamp + 60 minutes);
        LPToken lp = (stakingFundsVault.lpTokenForKnot(blsKeysForVaults[0][0]));
        LPToken [][] memory lpToken = new LPToken[][](1);
        LPToken[] memory temp  = new LPToken[](1);
        temp[0] = lp;
        lpToken[0] = temp;

        emit log_uint(address(giantFeesAndMevPool).balance);
        giantFeesAndMevPool.bringUnusedETHBackIntoGiantPool(getAddressArrayFromValues(address(stakingFundsVault)),lpToken, stakeAmountsForVaults);

        emit log_uint(address(giantFeesAndMevPool).balance);
        vm.expectRevert();
        giantFeesAndMevPool.batchDepositETHForStaking(getAddressArrayFromValues(address(stakingFundsVault)),getUint256ArrayFromValues(1 ether) , blsKeysForVaults, stakeAmountsForVaults);

        vm.expectRevert();
        giantSavETHPool.withdrawETH(1 ether);

        vm.stopPrank();
    }


``` 
both withdrawing eth for user and depositing eth to stake fails and reverts as shown in the poc due to underflow in idleETH

Note that the same problem also exists in GiantSavETHVaultPool, however a poc cannot be done for it as another bug exist in GiantSavETHVaultPool which prevents it from receiving funds as it lacks a receive() or fallback() implementation.

## Tools Used

Foundry

## Recommended Mitigation Steps
update `idleETH`  in withdrawUnusedETHToGiantPool

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Stakehouse Protocol |
| Report Date | N/A |
| Finders | koxuan, hihen |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-stakehouse
- **GitHub**: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/115
- **Contest**: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest

### Keywords for Search

`Don't update state`

