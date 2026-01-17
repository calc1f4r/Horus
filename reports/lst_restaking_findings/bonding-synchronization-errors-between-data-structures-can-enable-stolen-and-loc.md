---
# Core Classification
protocol: Livepeer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17049
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/livepeer.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/livepeer.pdf
github_link: none

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

protocol_categories:
  - dexes
  - services
  - cross_chain
  - launchpad
  - payments

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - 2018: March 12
  - Changelog March 9
  - Evan Sultanik
  - Chris Evans
  - 2018: March 10
---

## Vulnerability Title

Bonding synchronization errors between data structures can enable stolen and locked tokens

### Overview

See description below for full details.

### Original Finding Content

## Description

Delegated stake is stored in two different data structures. If the data structures ever get out of sync, delegates will be able to claim earnings that are not owed to them, artificially reduce transcoders’ bonded stake, and lock other delegates’ tokens and bonding ability. This is because certain bonding checks validate against one data structure, while others validate against the other.

Delegated stake is stored in two different data structures within the Bonding Manager: `delegators` and `transcoderPool`. The former maps delegators’ bonded stake to their delegates, while the keys of the latter store the sums of the delegated stake for the transcoders. If there is any way to break the synchronization between these data structures—such that the transcoder stake summations in `transcoderPool` are erroneous—then delegators would be able to remove stake from transcoders. When a delegator re-bonds to a new address or unbonds itself completely, if at that time its old delegated stake is for a registered transcoder, then its stake will be subtracted from that transcoder’s key in `transcoderPool` according to the value in `delegators`.

```solidity
if (transcoderStatus(del.delegateAddress) == TranscoderStatus.Registered) {
    // Previously delegated to a transcoder
    // Decrease old transcoder's total stake
    transcoderPool.updateKey(
        del.delegateAddress,
        transcoderPool.getKey(del.delegateAddress).sub(del.bondedAmount),
        address(0), address(0)
    );
}
```

Figure 5: Transcoder stake deletion in BondingManager.sol

The eligibility to claim earnings is based off of a delegator’s `delegateAddress` in the `delegators` data structure, but the actual earnings calculation is based off of the delegated amount in the `transcoderPool` data structure. Moreover, if the erroneously reduced stake is sufficiently high, it can lock other delegators’ stakes to that transcoder, as is demonstrated by the following exploit scenario. Finally, if the original delegator claims earnings before any other delegators bonded to the same transcoder—which will automatically happen when the transcoder either unbonds or re-bonds—then the original delegator will receive earnings intended for the other delegators since the rewards pool did not take into account the original phantom stake. When the other delegators subsequently attempt to claim earnings, a SafeMath assertion will fail when each delegator attempts to subtract their claims from the earnings pool, effectively locking their earnings and preventing the delegator from ever unbonding.

**Note:** The severity of this finding is classified as “Informational” because we were not able to exploit it. Therefore, it does not pose any immediate security risk. However, a future modification to the Bonding Manager contract could easily expose it.

## Exploit Scenario

Alice wants to reduce the stake of Bob’s transcoder. Alice has bonded 1,337 delegated stake to Bob’s transcoder, Bob has bonded 1,000 of his own stake, and Carol has also bonded 2,000 stake to Bob’s transcoder.

Assume that a synchronization error does exist that prevented Alice’s 1,337 stake from appearing in the `transcoderPool` data structure. Therefore, from the perspective of the `transcoderPool`, Bob’s transcoder will only have 3,000 bonded stake, not the correct amount: 4,337.

## Malicious Delegator Can Claim Additional Earnings

As long as Alice claims her earnings for Bob’s transcoder’s claimed work relatively early, she will get an undue increase in her reward. This is because the earnings pool’s claimable stake is based off of the erroneous basis of 3,000 bonded stake. Therefore, Alice will receive \( \frac{1,337}{3,000} \approx 45\% \) of the reward pool instead of \( \frac{1,337}{4,337} \approx 31\% \) that she actually deserves.

## Malicious Delegator Can Artificially Reduce Transcoders’ Bonded Stake

Alice eventually re-bonds her stake to a different address or alternatively un-bonds herself completely. This automatically calls `claimEarnings`, which will once again give Alice an undue share of the rewards. After Alice completes her bonding change, Bob’s transcoder’s address in the `transcoderPool` data structure will have its bonded amount reduced by Alice’s 1,337, resulting in an erroneous bonded stake of 1,663.

## Other Delegators’ Bonded Tokens Can Be Locked

Carol decides to re-bond to a different transcoder. However, she will be unable to because the claimable stake in the earnings pool is less than Carol’s stake of 2,000, causing an assertion error in `autoClaimEarnings`. Even if that were not the case, the safe subtraction in Figure 4 would also fail an assertion because `del.bondedAmount = 2000`, but Bob’s transcoder’s value in the `transcoderPool` is currently 1,663. This effectively locks Carol’s delegated stake, preventing her from unbonding, re-bonding, or claiming her stake.

## Recommendation

- Improve source code comments to provide better context for the interdependency between data structures and their semantics.
- Consider improving the automated integration tests to check for bonding edge cases.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Livepeer |
| Report Date | N/A |
| Finders | 2018: March 12, Changelog March 9, Evan Sultanik, Chris Evans, 2018: March 10, 2018: Initial report delivered Added informational ﬁnding TOB-Livepeer-005 Public release © 2018 Trail of Bits Livepeer Security Assessment | 1 |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/livepeer.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/livepeer.pdf

### Keywords for Search

`vulnerability`

