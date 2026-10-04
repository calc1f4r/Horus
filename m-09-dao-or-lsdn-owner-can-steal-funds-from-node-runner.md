---
# Core Classification
protocol: Stakehouse Protocol
chain: everychain
category: uncategorized
vulnerability_type: admin

# Attack Vector Details
attack_type: admin
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5917
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest
source_link: https://code4rena.com/reports/2022-11-stakehouse
github_link: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/109

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - admin

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - koxuan
---

## Vulnerability Title

[M-09] DAO or lsdn owner can steal funds from node runner

### Overview


This bug report is about a vulnerability in the LiquidStakingManager.sol smart contract code. The vulnerability allows the DAO or LSD network owner to swap out the node runner of the smart contract to their own External Owned Account (EOA), which in turn allows them to withdraw ETH or claim rewards from the node runner. A malicious DAO or LSD network owner can take advantage of this vulnerability by swapping out the node runner just after they have deposited 4 Ether in the smart wallet. The recommended mitigation steps are to send back any outstanding ETH and rewards that belong to the node runner if swapping is needed. The bug report was tested using Forge.

### Original Finding Content


<https://github.com/code-423n4/2022-11-stakehouse/blob/main/contracts/liquid-staking/LiquidStakingManager.sol#L356-L377>

DAO or LSD network owner can swap node runner of the smart contract to their own eoa, allowing them to withdrawETH or claim rewards from node runner.

### Proof of Concept

There are no checks done when swapping the node runner whether there are funds in the smart contract that belongs to the node runner. Therefore, a malicious dao or lsd network owner can simply swap them out just right after the node runner has deposited 4 ether in the smart wallet.

Place poc in LiquidStakingManager.sol

```solidity
    function testDaoCanTakeNodeRunner4ETH() public {
        address nodeRunner = accountOne; vm.deal(nodeRunner, 4 ether);
        address feesAndMevUser = accountTwo; vm.deal(feesAndMevUser, 4 ether);
        address savETHUser = accountThree; vm.deal(savETHUser, 24 ether);
        address attacker = accountFour;


        registerSingleBLSPubKey(nodeRunner, blsPubKeyOne, accountFour);

        vm.startPrank(admin);
        manager.rotateNodeRunnerOfSmartWallet(nodeRunner, attacker, true);

        vm.stopPrank();

        vm.startPrank(attacker);
        emit log_uint(attacker.balance);
        manager.withdrawETHForKnot(attacker,blsPubKeyOne);
        emit log_uint(attacker.balance);
        vm.stopPrank();
    }

```

### Tools Used

forge

### Recommended Mitigation Steps

Send back outstanding ETH and rewards that belongs to node runner if swapping is needed.

**[vince0656 (Stakehouse) confirmed](https://github.com/code-423n4/2022-11-stakehouse-findings/issues/109#issuecomment-1329514501)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Stakehouse Protocol |
| Report Date | N/A |
| Finders | koxuan |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-stakehouse
- **GitHub**: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/109
- **Contest**: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest

### Keywords for Search

`Admin`

