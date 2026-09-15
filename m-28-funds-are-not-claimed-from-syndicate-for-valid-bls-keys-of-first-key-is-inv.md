---
# Core Classification
protocol: Stakehouse Protocol
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5936
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest
source_link: https://code4rena.com/reports/2022-11-stakehouse
github_link: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/408

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - validation
  - business_logic

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
  - Trust
---

## Vulnerability Title

[M-28] Funds are not claimed from syndicate for valid BLS keys of first key is invalid (no longer part of syndicate).

### Overview


A bug was identified in the claimRewards code in the StakingFundsVault.sol file. The code has an if statement that requires the first BLS public key to be part of the syndicate in order for the _claimFundsFromSyndicateForDistribution function to be called. If the first BLS public key is not part of the syndicate, users will not receive rewards for claims of valid public keys. This bug leads to reduced rewards for users.

The bug was identified through manual audit. The recommended mitigation step is to drop the i==0 requirement and use a hasClaimed boolean instead. This will ensure that users receive rewards for claims of valid public keys, regardless of whether the first BLS public key is part of the syndicate or not.

### Original Finding Content


<https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/StakingFundsVault.sol#L218>

claimRewards in StakingFundsVault.sol has this code:

    if (i == 0 && !Syndicate(payable(liquidStakingNetworkManager.syndicate())).isNoLongerPartOfSyndicate(_blsPubKeys[i])) {
        // Withdraw any ETH accrued on free floating SLOT from syndicate to this contract
        // If a partial list of BLS keys that have free floating staked are supplied, then partial funds accrued will be fetched
        _claimFundsFromSyndicateForDistribution(
            liquidStakingNetworkManager.syndicate(),
            _blsPubKeys
        );
        // Distribute ETH per LP
        updateAccumulatedETHPerLP();
    }

The issue is that if the first BLS public key is not part of the syndicate, then \_claimFundsFromSyndicateForDistribution will not be called, even on BLS keys that are eligible for syndicate rewards. This leads to reduced rewards for user.

This is different from a second bug which discusses the possibility of using a stale acculmulatedETHPerLP.

### Impact

Users will not receive rewards for claims of valid public keys if first passed key is not part of syndicate.

### Recommended Mitigation Steps

Drop the `i==0` requirement, which was intended to make sure the claim isn't called multiple times. Use a hasClaimed boolean instead.

**[vince0656 (Stakehouse) confirmed](https://github.com/code-423n4/2022-11-stakehouse-findings/issues/408#event-8238936350)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Stakehouse Protocol |
| Report Date | N/A |
| Finders | Trust |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-stakehouse
- **GitHub**: https://github.com/code-423n4/2022-11-stakehouse-findings/issues/408
- **Contest**: https://code4rena.com/contests/2022-11-lsd-network-stakehouse-contest

### Keywords for Search

`Validation, Business Logic`

