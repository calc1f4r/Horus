---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25829
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-astaria
source_link: https://code4rena.com/reports/2023-01-astaria
github_link: https://github.com/code-423n4/2023-01-astaria-findings/issues/369

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
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - obront
---

## Vulnerability Title

[M-13] Processing an epoch must be done in a timely manner, but can be halted by non liquidated expired liens

### Overview


A bug was found in the Astaria platform, which could cause delays in the epoch processing and cause arithmetic errors in formulas regarding epochs and timestamps. This is due to the processEpoch() endpoint not being called regularly, especially close to the epoch boundaries. This can happen if there are open liens and they remain open when a lien expires and isn't promptly liquidated. To mitigate this issue, Astaria should implement a monitoring solution to ensure that liquidate() is always called promptly for expired liens, and that processEpoch() is always called promptly when the epoch ends. The Astaria team has acknowledged this issue and has stated that they are monitoring vaults to process epochs.

### Original Finding Content


As pointed out in the [Spearbit audit](https://github.com/spearbit-audits/review-astaria/issues/121):

> If the processEpoch() endpoint does not get called regularly (especially close to the epoch boundaries), the updated currentEpoch would lag behind the actual expected value and this will introduce arithmetic errors in formulas regarding epochs and timestamps.

This can cause a problem because `processEpoch()` cannot be called when there are open liens, and liens may remain open in the event that a lien expires and isn't promptly liquidated.

### Proof of Concept

`processEpoch()` contains the following check to ensure that all liens are closed before the epoch is processed:

    if (s.epochData[s.currentEpoch].liensOpenForEpoch > 0) {
      revert InvalidState(InvalidStates.LIENS_OPEN_FOR_EPOCH_NOT_ZERO);
    }

The accounting considers a lien open (via `s.epochData[s.currentEpoch].liensOpenForEpoch`) unless this value is decremented, which happens in three cases: when (a) the full payment is made, (b) the lien is bought out, or (c) the lien is liquidated.

In the event that a lien expires and nobody calls `liquidate()` (for example, if the NFT seems worthless and no other user wants to pay the gas to execute the function for the fee), this would cause `processEpoch()` to fail, and could create delays in the epoch processing and cause the accounting issues pointed out in the previous audit.

### Recommended Mitigation Steps

Astaria should implement a monitoring solution to ensure that `liquidate()` is always called promptly for expired liens, and that `processEpoch()` is always called promptly when the epoch ends.

**[SantiagoGregory (Astaria) acknowledged and commented](https://github.com/code-423n4/2023-01-astaria-findings/issues/369#issuecomment-1412914783):**
 > Yes, us and strategists know to be monitoring vaults to process epochs.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | obront |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-astaria
- **GitHub**: https://github.com/code-423n4/2023-01-astaria-findings/issues/369
- **Contest**: https://code4rena.com/reports/2023-01-astaria

### Keywords for Search

`vulnerability`

