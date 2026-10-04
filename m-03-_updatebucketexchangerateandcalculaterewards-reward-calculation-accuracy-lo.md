---
# Core Classification
protocol: Ajna Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20082
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-ajna
source_link: https://code4rena.com/reports/2023-05-ajna
github_link: https://github.com/code-423n4/2023-05-ajna-findings/issues/394

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
  - kutugu
---

## Vulnerability Title

[M-03] `_updateBucketExchangeRateAndCalculateRewards` reward calculation accuracy loss

### Overview


A bug has been discovered in Ajna's rewards manager contract that causes precision loss when dividing and then multiplying. The amount of loss depends on the denominator, which can be at most one less than the denominator. To reduce the loss, the Maths.wdiv rounded adopted in _updateBucketExchangeRateAndCalculateRewards, however, it still leads to a theoretical loss of half the interestEarned_ when calculating the interestFactor. This means that the more interest is earned, the more users lose. 

To test the bug, Foundry was used to modify the code and test the reward calculation. For a Fuzzing input with indexes: 3 and mintAmount: 73528480588506366763626, when dividing first and then multiplying, the emit CalculateReward was 334143554965844407584, while when multiplying first and then dividing, the emit CalculateReward was 334143554965846586903. 

The recommended mitigation step is to multiply first and then divide, as modified above. This was confirmed by MikeHathaway (Ajna).

### Original Finding Content


Divide first and then multiply, which has precision loss. The loss depends on the denominator, which is at most `denominator - 1`.\
Although `Maths.wdiv rounded` adopted in \_updateBucketExchangeRateAndCalculateRewards, reduce the loss, but theoretically `interestFactor` loss is about `interestEarned_ / 2`.\
This means that the more interest are earned, the more users lose.

### Proof of Concept

Modify for testing

```diff
diff --git a/ajna-core/src/RewardsManager.sol b/ajna-core/src/RewardsManager.sol
index 314b476..421940f 100644
--- a/ajna-core/src/RewardsManager.sol
+++ b/ajna-core/src/RewardsManager.sol
@@ -801,8 +801,12 @@ contract RewardsManager is IRewardsManager, ReentrancyGuard {
                 rewards_ += Maths.wmul(UPDATE_CLAIM_REWARD, Maths.wmul(burnFactor, interestFactor));
             }
         }
+
+        emit CalculateReward(rewards_);
     }
 
+    event CalculateReward(uint256);
+
     /** @notice Utility method to transfer `Ajna` rewards to the sender
      *  @dev   This method is used to transfer rewards to the `msg.sender` after a successful claim or update.
      *  @dev   It is used to ensure that rewards claimers will be able to claim some portion of the remaining tokens if a claim would exceed the remaining contract balance.
```

Modify reward calculation

```diff
diff --git a/ajna-core/src/RewardsManager.sol b/ajna-core/src/RewardsManager.sol
index 421940f..4cdfefa 100644
--- a/ajna-core/src/RewardsManager.sol
+++ b/ajna-core/src/RewardsManager.sol
@@ -792,13 +792,15 @@ contract RewardsManager is IRewardsManager, ReentrancyGuard {
                 (, , , uint256 bucketDeposit, ) = IPool(pool_).bucketInfo(bucketIndex_);
 
                 uint256 burnFactor     = Maths.wmul(totalBurned_, bucketDeposit);
-                uint256 interestFactor = interestEarned_ == 0 ? 0 : Maths.wdiv(
-                    Maths.WAD - Maths.wdiv(prevBucketExchangeRate, curBucketExchangeRate),
-                    interestEarned_
-                );
 
                 // calculate rewards earned for updating bucket exchange rate 
-                rewards_ += Maths.wmul(UPDATE_CLAIM_REWARD, Maths.wmul(burnFactor, interestFactor));
+                rewards_ += interestEarned_ == 0 ? 0 : Maths.wmul(UPDATE_CLAIM_REWARD, Maths.wdiv(
+                    Maths.wmul(
+                        Maths.WAD - Maths.wdiv(prevBucketExchangeRate, curBucketExchangeRate),
+                        burnFactor
+                    ),
+                    interestEarned_
+                ));
             }
         }
```

```shell
forge test --match-test testClaimRewardsFuzzy -vvvv

For a Fuzzing input:
indexes: 3
mintAmount: 73528480588506366763626

Divide first and multiply
emit CalculateReward(: 334143554965844407584)

Multiply first and divide
emit CalculateReward(: 334143554965846586903)
```

### Tools Used

Foundry

### Recommended Mitigation Steps

As modified above, multiply first and then divide.

**[MikeHathaway (Ajna) confirmed](https://github.com/code-423n4/2023-05-ajna-findings/issues/394#issuecomment-1555151437)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Ajna Protocol |
| Report Date | N/A |
| Finders | kutugu |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-ajna
- **GitHub**: https://github.com/code-423n4/2023-05-ajna-findings/issues/394
- **Contest**: https://code4rena.com/reports/2023-05-ajna

### Keywords for Search

`vulnerability`

