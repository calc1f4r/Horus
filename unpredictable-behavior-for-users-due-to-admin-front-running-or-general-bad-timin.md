---
# Core Classification
protocol: 1inch Liquidity Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13573
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/12/1inch-liquidity-protocol/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - indexes

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

Unpredictable behavior for users due to admin front running or general bad timing

### Overview


This bug report describes a security vulnerability in a system that allows privileged roles to make malicious changes just ahead of incoming transactions, or purely accidental negative effects to occur due to the unfortunate timing of changes. The report provides three examples of how this vulnerability can be exploited: by locking a user's staked token, by front-running a transaction to prevent stake sync, and by front-running an unstake to prevent it from propagating. The report recommends giving users advance notice of changes with a two-step process, including a mandatory time window between them, so that users can withdraw if they do not accept the change. Additionally, users should be guaranteed to be able to redeem their staked tokens, and no entity in the system should be able to lock them indefinitely.

### Original Finding Content

#### Description


In a number of cases, administrators of contracts can update or upgrade things in the system without warning. This has the potential to violate a security goal of the system.


Specifically, privileged roles could use front running to make malicious changes just ahead of incoming transactions, or purely accidental negative effects could occur due to the unfortunate timing of changes.


In general users of the system should have assurances about the behavior of the action they’re about to take.


#### Examples


##### MooniswapFactoryGovernance - Admin opportunity to lock `swapFor` with a referral when setting an invalid `referralFeeReceiver`


* `setReferralFeeReceiver` and `setGovernanceFeeReceiver` takes effect immediately.


**code/contracts/governance/MooniswapFactoryGovernance.sol:L92-L95**



```
function setReferralFeeReceiver(address newReferralFeeReceiver) external onlyOwner {
    referralFeeReceiver = newReferralFeeReceiver;
    emit ReferralFeeReceiverUpdate(newReferralFeeReceiver);
}

```
* `setReferralFeeReceiver` can be used to set an invalid receiver address (or one that reverts on every call) effectively rendering `Mooniswap.swapFor` unusable if a referral was specified in the swap.


**code/contracts/Mooniswap.sol:L281-L286**



```
if (referral != address(0)) {
    referralShare = invIncrease.mul(referralShare).div(\_FEE\_DENOMINATOR);
    if (referralShare > 0) {
        if (referralFeeReceiver != address(0)) {
            \_mint(referralFeeReceiver, referralShare);
            IReferralFeeReceiver(referralFeeReceiver).updateReward(referral, referralShare);

```
##### Locking staked token


At any point in time and without prior notice to users an admin may accidentally or intentionally add a broken governance sub-module to the system that blocks all users from unstaking their `1INCH` token. An admin can recover from this by removing the broken sub-module, however, with malicious intent tokens may be locked forever.


Since `1INCH` token gives voting power in the system, tokens are considered to hold value for other users and may be traded on exchanges. This raises concerns if tokens can be locked in a contract by one actor.


* An admin adds an invalid address or a malicious sub-module to the governance contract that always `reverts` on calls to `notifyStakeChanged`.


**code/contracts/inch/GovernanceMothership.sol:L63-L66**



```
function addModule(address module) external onlyOwner {
    require(\_modules.add(module), "Module already registered");
    emit AddModule(module);
}

```
**code/contracts/inch/GovernanceMothership.sol:L73-L78**



```
function \_notifyFor(address account, uint256 balance) private {
    uint256 modulesLength = \_modules.length();
    for (uint256 i = 0; i < modulesLength; ++i) {
        IGovernanceModule(\_modules.at(i)).notifyStakeChanged(account, balance);
    }
}

```
##### Admin front-running to prevent user stake sync


An admin may front-run users while staking in an attempt to prevent submodules from being notified of the stake update. This is unlikely to happen as it incurs costs for the attacker (front-back-running) to normal users but may be an interesting attack scenario to exclude a whale’s stake from voting.


For example, an admin may front-run `stake()` or `notoify*()` by briefly removing all governance submodules from the mothership and re-adding them after the users call succeeded. The stake-update will not be propagated to the sub-modules. A user may only detect this when they are voting (if they had no stake before) or when they actually check their stake. Such an attack might likely stay unnoticed unless someone listens for `addmodule` `removemodule` events on the contract.


* An admin front-runs a transaction by removing all modules and re-adding them afterwards to prevent the stake from propagating to the submodules.


**code/contracts/inch/GovernanceMothership.sol:L68-L71**



```
function removeModule(address module) external onlyOwner {
    require(\_modules.remove(module), "Module was not registered");
    emit RemoveModule(module);
}

```
##### Admin front-running to prevent unstake from propagating


An admin may choose to front-run their own `unstake()`, temporarily removing all governance sub-modules, preventing `unstake()` from syncing the action to sub-modules while still getting their previously staked tokens out. The governance sub-modules can be re-added right after unstaking. Due to double-accounting of the stake (in governance and in every sub-module) their stake will still be exercisable in the sub-module even though it was removed from the mothership. Users can only prevent this by manually calling a state-sync on the affected account(s).


#### Recommendation


The underlying issue is that users of the system can’t be sure what the behavior of a function call will be, and this is because the behavior can change at any time.


We recommend giving the user advance notice of changes with a time lock. For example, make all system-parameter and upgrades require two steps with a mandatory time window between them. The first step merely broadcasts to users that a particular change is coming, and the second step commits that change after a suitable waiting period. This allows users that do not accept the change to withdraw immediately.


Furthermore, users should be guaranteed to be able to redeem their staked tokens. An entity - even though trusted - in the system should not be able to lock tokens indefinitely.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | 1inch Liquidity Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/12/1inch-liquidity-protocol/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

