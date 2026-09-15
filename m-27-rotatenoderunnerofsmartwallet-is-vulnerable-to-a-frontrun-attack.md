---
# Core Classification
protocol: Stakehouse Protocol
chain: everychain
category: economic
vulnerability_type: front-running

# Attack Vector Details
attack_type: front-running
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5935
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest
source_link: https://code4rena.com/reports/2022-11-stakehouse
github_link: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/386

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - front-running

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
  - Franfran
---

## Vulnerability Title

[M-27] rotateNodeRunnerOfSmartWallet is vulnerable to a frontrun attack

### Overview


This bug report is about a vulnerability in the `rotateNodeRunnerOfSmartWallet` function of the Liquid Staking Manager contract. This function can be called by anyone who is a node runner in the LSD network, leaving it vulnerable to a frontrun attack in the case of this node runner being malicious. If a malicious node runner is identified, the DAO would call this same `rotateNodeRunnerOfSmartWallet` with the `_wasPreviousNodeRunnerMalicious` flag turned on. However, the malicious node runner could frontrun the DAO transaction and submit it before the DAO in order to avoid getting banned and rotate their EOA representation of the node. This would cause the DAO transaction to revert when it checks if the current (old) node representative is still a wallet.

The vulnerability was identified through manual inspection. The recommended mitigation steps include restricting the function to DAO only with the `onlyDAO` modifier.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-11-stakehouse/blob/main/contracts/liquid-staking/LiquidStakingManager.sol#L356
https://github.com/code-423n4/2022-11-stakehouse/blob/main/contracts/liquid-staking/LiquidStakingManager.sol#L369


## Vulnerability details

## Impact
As the `rotateNodeRunnerOfSmartWallet` function can be called by anyone who is a node runner in the LSD network, this function is vulnerable to a frontrun attack in the case of this node runner being malicious.

## Proof of Concept
If that is the current node runner is malicious, the DAO would purposely call this same `rotateNodeRunnerOfSmartWallet` with the `_wasPreviousNodeRunnerMalicious` flag turned on.
An actual node runner that has been malicious could monitor the mempool and frontrun the DAO transaction that wanted to slash it and submit the transaction before the DAO to avoid getting banned and rotate their EOA representation of the node.

```solidity
if (msg.sender == dao && _wasPreviousNodeRunnerMalicious) {
    bannedNodeRunners[_current] = true;
    emit NodeRunnerBanned(_current);
}
```

When the DAO transaction would go through, it would revert when it's checking if the current (old) node representative is still a wallet, but it's not because the mapping value has been deleted before.

```solidity
address wallet = smartWalletOfNodeRunner[_current];
require(wallet != address(0), "Wallet does not exist");
```

## Tools Used
Manual inspection

## Recommended Mitigation Steps
Restrict this function to DAO only with the `onlyDAO` modifier.

```solidity
// - function rotateNodeRunnerOfSmartWallet(address _current, address _new, bool _wasPreviousNodeRunnerMalicious) external {
+ function rotateNodeRunnerOfSmartWallet(address _current, address _new, bool _wasPreviousNodeRunnerMalicious) onlyDAO external {
    require(_new != address(0) && _current != _new, "New is zero or current");

    address wallet = smartWalletOfNodeRunner[_current];
    require(wallet != address(0), "Wallet does not exist");
    require(_current == msg.sender || dao == msg.sender, "Not current owner or DAO");

    address newRunnerCurrentWallet = smartWalletOfNodeRunner[_new];
    require(newRunnerCurrentWallet == address(0), "New runner has a wallet");

    smartWalletOfNodeRunner[_new] = wallet;
    nodeRunnerOfSmartWallet[wallet] = _new;

    delete smartWalletOfNodeRunner[_current];

    // - if (msg.sender == dao && _wasPreviousNodeRunnerMalicious) {
    if (_wasPreviousNodeRunnerMalicious) {
        bannedNodeRunners[_current] = true;
        emit NodeRunnerBanned(_current);
    }

    emit NodeRunnerOfSmartWalletRotated(wallet, _current, _new);
}

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Stakehouse Protocol |
| Report Date | N/A |
| Finders | Franfran |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-stakehouse
- **GitHub**: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/386
- **Contest**: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest

### Keywords for Search

`Front-Running`

