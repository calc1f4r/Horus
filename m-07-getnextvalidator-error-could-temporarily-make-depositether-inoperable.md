---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25444
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-09-frax
source_link: https://code4rena.com/reports/2022-09-frax
github_link: https://github.com/code-423n4/2022-09-frax-findings/issues/219

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
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-07] `getNextValidator()` error could temporarily make `depositEther()` inoperable

### Overview



The bug report is about a potential Denial of Service (DoS) attack on the `depositEther()` function in the Frax project. The issue is that if the `pubKey` is already in use, the whole loop will revert, and the deposit operation cannot move on. This could cause the `depositEther()` function to be inaccessible until the governance calls the registry to pop the wrong validator.

The proof of concept provided shows the code of the `depositEther()` function, the `totalAssets()` function, and the `popValidators()` function. The recommended mitigation steps are to use `try/catch` to skip the wrong validator, making the deposit function more robust to unexpected situations.

The 0xean judge commented that the issue should be awarded as a medium severity since it can disable deposits and the registry should check against the mapping. FortisFortuna (Frax) commented that they plan to keep an eye on the number of free validators and have a decent sized buffer of them.

### Original Finding Content


When `depositEther()`, if 1 `validators` is used before, the whole deposit function will revert, causing DoS. `depositEther()` function will be inoperable until the gov manually removes the mistaken validator.

### Proof of Concept

In `depositEther()`, if the `pubKey` is already used, the whole loop will revert, and the deposit operation cannot move on.

```solidity
// src/frxETHMinter.sol
    function depositEther() external nonReentrant {
        // ...

        for (uint256 i = 0; i < numDeposits; ++i) {
            // Get validator information
            (
                bytes memory pubKey,
                bytes memory withdrawalCredential,
                bytes memory signature,
                bytes32 depositDataRoot
            ) = getNextValidator(); // Will revert if there are not enough free validators

            // Make sure the validator hasn't been deposited into already, to prevent stranding an extra 32 eth
            // until withdrawals are allowed
            require(!activeValidators[pubKey], "Validator already has 32 ETH");
        // ...        
    }
```

And in the next rewards cycle, `lastRewardAmount` will be linearly added to `storedTotalAssets`, their sum is the return value of `totalAssets()`:

```solidity
    function totalAssets() public view override returns (uint256) {
        // ...

        if (block.timestamp >= rewardsCycleEnd_) {
            // no rewards or rewards fully unlocked
            // entire reward amount is available
            return storedTotalAssets_ + lastRewardAmount_;
        }

        // rewards not fully unlocked
        // add unlocked rewards to stored total
        uint256 unlockedRewards = (lastRewardAmount_ * (block.timestamp - lastSync_)) / (rewardsCycleEnd_ - lastSync_);
        return storedTotalAssets_ + unlockedRewards;
    }
```

Temporarily the `depositEther()` function will be inaccessible. Until the governance calls the registry to pop the wrong validator.

```solidity
// src/OperatorRegistry.sol
    function popValidators(uint256 times) public onlyByOwnGov {
        // Loop through and remove validator entries at the end
        for (uint256 i = 0; i < times; ++i) {
            validators.pop();
        }

        emit ValidatorsPopped(times);
    }
```

### Recommended Mitigation Steps

Use `try/catch` to skip the wrong validator, then the deposit function will be more robust to unexpected situations.

**[FortisFortuna (Frax) commented](https://github.com/code-423n4/2022-09-frax-findings/issues/219#issuecomment-1257301152):**
 > We plan to keep an eye on the number of free validators and have a decent sized buffer of them.

**[0xean (judge) commented](https://github.com/code-423n4/2022-09-frax-findings/issues/219#issuecomment-1278241225):**
 > Awarding as Medium, given that this can disable deposits, the registry should check against the mapping. 



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-09-frax
- **GitHub**: https://github.com/code-423n4/2022-09-frax-findings/issues/219
- **Contest**: https://code4rena.com/reports/2022-09-frax

### Keywords for Search

`vulnerability`

