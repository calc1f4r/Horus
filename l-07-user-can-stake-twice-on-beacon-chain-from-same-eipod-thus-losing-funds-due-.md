---
# Core Classification
protocol: EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20066
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-04-eigenlayer
source_link: https://code4rena.com/reports/2023-04-eigenlayer
github_link: https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/54

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-07] User can stake twice on beacon chain from same eipod, thus losing funds due to same withdrawal credentials

### Overview

See description below for full details.

### Original Finding Content


### Proof of Concept
There are no restriction to how many times user can stake on beacon with `EigenPodManager` on `EigenPod`, thus all of them will have the same `_podWithdrawalCredentials()` and I think first deposit will be lost.
```sodlidity
    function stake(bytes calldata pubkey, bytes calldata signature, bytes32 depositDataRoot) external payable onlyEigenPodManager {
        // stake on ethpos
        require(msg.value == 32 ether, "EigenPod.stake: must initially stake for any validator with 32 ether");
        ethPOS.deposit{value : 32 ether}(pubkey, _podWithdrawalCredentials(), signature, depositDataRoot);
        emit EigenPodStaked(pubkey);
    }
```
[src/contracts/pods/EigenPod.sol#L159](https://github.com/code-423n4/2023-04-eigenlayer/blob/398cc428541b91948f717482ec973583c9e76232/src/contracts/pods/EigenPod.sol#L159)

There are some ways users can make a mistake by calling it twice or they would like to create another one.
I've looked into rocketpool contracts; they are not allowing users to stake twice with the same pubkeys, so I think its important to implement the same security issue.
```solidity
    function preStake(bytes calldata _validatorPubkey, bytes calldata _validatorSignature, bytes32 _depositDataRoot) internal {
...
        require(rocketMinipoolManager.getMinipoolByPubkey(_validatorPubkey) == address(0x0), "Validator pubkey is in use");
        // Set minipool pubkey
        rocketMinipoolManager.setMinipoolPubkey(_validatorPubkey);
        // Get withdrawal credentials
        bytes memory withdrawalCredentials = rocketMinipoolManager.getMinipoolWithdrawalCredentials(address(this));
        // Send staking deposit to casper
        casperDeposit.deposit{value : prelaunchAmount}(_validatorPubkey, withdrawalCredentials, _validatorSignature, _depositDataRoot);
        // Emit event
        emit MinipoolPrestaked(_validatorPubkey, _validatorSignature, _depositDataRoot, prelaunchAmount, withdrawalCredentials, block.timestamp);
    }
```
[contracts/contract/minipool/RocketMinipoolDelegate.sol#L235](https://github.com/rocket-pool/rocketpool/blob/967e4d3c32721a84694921751920af313d1467af/contracts/contract/minipool/RocketMinipoolDelegate.sol#L235)

Same safe thing done in frax finance: 
```
    function depositEther(uint256 max_deposits) external nonReentrant {
...
            // Deposit the ether in the ETH 2.0 deposit contract
            depositContract.deposit{value: DEPOSIT_SIZE}(
                pubKey,
                withdrawalCredential,
                signature,
                depositDataRoot
            );

            // Set the validator as used so it won't get an extra 32 ETH
            activeValidators[pubKey] = true;
    ...
}
```
[src/frxETHMinter.sol#L156](https://github.com/FraxFinance/frxETH-public/blob/7f7731dbc93154131aba6e741b6116da05b25662/src/frxETHMinter.sol#L156)

### Tools Used
POC

```diff
    function testWithdrawFromPod() public {
        cheats.startPrank(podOwner);
        eigenPodManager.stake{value: stakeAmount}(pubkey, signature, depositDataRoot);
+        eigenPodManager.stake{value: stakeAmount}(pubkey, signature, depositDataRoot);
        cheats.stopPrank();

        IEigenPod pod = eigenPodManager.getPod(podOwner);
        uint256 balance = address(pod).balance;
        cheats.deal(address(pod), stakeAmount);

        cheats.startPrank(podOwner);
        cheats.expectEmit(true, false, false, false);
        emit DelayedWithdrawalCreated(podOwner, podOwner, balance, delayedWithdrawalRouter.userWithdrawalsLength(podOwner));
        pod.withdrawBeforeRestaking();
        cheats.stopPrank();
        require(address(pod).balance == 0, "Pod balance should be 0");
    }

```
### Recommended Mitigation Steps
You can look at rocketpool contracts and borrow their logic:
```diff
    function stake(bytes calldata pubkey, bytes calldata signature, bytes32 depositDataRoot) external payable onlyEigenPodManager {
+        require(EigenPodManager.getEigenPodByPubkey(_validatorPubkey) == address(0x0), "Validator pubkey is in use");
+        EigenPodManager.setEigenPodByPubkey(_validatorPubkey);

        require(msg.value == 32 ether, "EigenPod.stake: must initially stake for any validator with 32 ether");
        ethPOS.deposit{value : 32 ether}(pubkey, _podWithdrawalCredentials(), signature, depositDataRoot);
        emit EigenPodStaked(pubkey);
    }

```

**[ChaoticWalrus (EigenLayer) disagreed with severity and commented](https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/54#issuecomment-1549011639):**
>We believe this is purely informational. People can already stake multiple times through the `ETH2Deposit` contract.

**[Alex the Entreprenerd (judge) decreased severity to QA and commented](https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/54#issuecomment-1572315807):**
>Downgrading to QA for now. @volodya - please do send me proof that a new withdrawal would be bricked (I believe it would be releasable via the normal flow).

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/54#issuecomment-1582367586):**
>Have had a informal confirmation that excess ETH is refunded as rewards.
>
>In lack of additional info, am maintaining the judgment.

***


### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-04-eigenlayer
- **GitHub**: https://github.com/code-423n4/2023-04-eigenlayer-findings/issues/54
- **Contest**: https://code4rena.com/reports/2023-04-eigenlayer

### Keywords for Search

`vulnerability`

