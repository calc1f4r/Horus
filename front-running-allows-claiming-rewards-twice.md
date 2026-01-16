---
# Core Classification
protocol: /Reach - Diff 2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59763
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/reach-diff-2/41dcd3b3-eee0-4759-96b4-6c6e19fa3ae2/index.html
source_link: https://certificate.quantstamp.com/full/reach-diff-2/41dcd3b3-eee0-4759-96b4-6c6e19fa3ae2/index.html
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
finders_count: 3
finders:
  - Julio Aguilar
  - Jeffrey Kam
  - Guillermo Escobero
---

## Vulnerability Title

Front Running Allows Claiming Rewards Twice

### Overview


The team has identified a bug where a user can claim their rewards twice by delaying the claiming process until a new distribution is created. They recommend establishing a clear dependency between claiming and distribution creation, such as adding a deadline for claiming rewards and updating it with each new distribution. Another solution is to add a lock to the contract to freeze the redemption state and update the Merkle root before allowing users to claim their rewards.

### Original Finding Content

**Update**
This issue is introduced upon clarification during the fix review phase. The team addressed the issue in `eaf15c` and `7a5149`. The team mitigated this attack vector by adding a `claimingPaused` boolean such that `createDistribution()` can only be called if claiming is paused.

**File(s) affected:**`ReachAffiliateDistribution.sol`, `ReachMainDistribution.sol`

**Description:** The off-chain system generating the Merkle trees and distributions is out of the scope of this audit, but as stated by the Reach team, non-claimed rewards will be included in the next distribution.

An exploitable behavior has been identified where a user can intentionally delay claiming rewards until observing a new `createDistribution()` transaction by the system owner in the mempool. Subsequently, the user can claim their un-claimed rewards before the execution of `createDistribution()` and then claim them again after the distribution creation process.

**Recommendation:** Establish a clear dependency between the claiming process and the execution of `createDistribution()`, ensuring that rewards are considered and processed within a well-defined sequence. For example, consider adding a deadline when creating a new distribution. After this deadline, users are restricted from claiming rewards for that distribution period. The deadline should be updated with each new distribution creation to provide a reasonable timeframe for users to claim and to allow the owner to take the necessary snapshot. Another way to resolve this is to add a lock to the contract to freeze the redemption state, then update the Merkle root based on this frozen state (like a snapshot), and, only then, unlock the contract to resume user redemptions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | /Reach - Diff 2 |
| Report Date | N/A |
| Finders | Julio Aguilar, Jeffrey Kam, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/reach-diff-2/41dcd3b3-eee0-4759-96b4-6c6e19fa3ae2/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/reach-diff-2/41dcd3b3-eee0-4759-96b4-6c6e19fa3ae2/index.html

### Keywords for Search

`vulnerability`

