---
# Core Classification
protocol: Huma Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52212
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/huma/huma-protocol
source_link: https://www.halborn.com/audits/huma/huma-protocol
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

INCONSISTENCIES IN DOCUMENTATION

### Overview

See description below for full details.

### Original Finding Content

##### Description

Some inconsistencies have been found in Huma Protocol Spec for Solana document:

* In the `Introduction` section: "*Institutional investor participation. The most critical thing for institutional investors is principal safety. This makes tranche support essential so that* ***intentional investors can choose to participate in senior tranches only***." However, investor can choose to participate in a senior tranche only, but if the pool has the senior tranche (in addition to the juniot tranche, since there is no pool with only a senior tranche)
* In the `Pool-level User Roles` , section (3.1.2 ) *"Pool Owners:* ***Pool owners are a list of addresses that are approved by the Protocol Owner*** *to create and manage pools.".* However, a pool can be created by anyone.
* In the `Credit Approval` , section (5.1.2) : " *For example, assuming the approved credit is 1000, the borrower has borrowed 500, and the borrower pays back 400.* ***If it is not revolving, the remaining credit is only 500*."** However, this is Inaccurate/confusing revolving description. The non-revolving credit borrowers can drawdown only once and not multiple times which is not explicitly stated in the docs.
* In the `Credit Approval` , section (5.1.2) : "***The credit limit cannot exceed 4 billion of the coin (stablecoin) supported by the pool.***" This requirement is not relevant and should be removed.
* In the `Redemption Request and Cancellation`, section (4.2.1)"only requests that meet lockup period requirements will be accepted. Redemption requests can be canceled **before the epoch starts to process the requests** at no cost." This can be not accurate and can be confusing, as a non processed redemption request that has been rolled up to the next epoch can also be cancelled at no cost.

Other inconsistencies have been found in [lib.rs](http://lib.rs) file in the program:

In `add_pool_operator` the comments mention the huma owner can call this instruction. However, only the pool owner can add operators.

[***lib.rs***](http://deposit.rs)

```
 /// # Access Control
    /// Only the pool owner and the Huma owner can call this instruction.
    pub fn add_pool_operator(ctx: Context<AddPoolOperator>, operator: Pubkey) -> Result<()> {
        pool::add_pool_operator(ctx, operator)
    }
```

In `remove_pool_operator` the comments mention the huma owner can call this instruction. However, only the pool owner can add operators.

```
 /// # Access Control
    /// Only the pool owner and the Huma owner can call this instruction.
    pub fn remove_pool_operator(ctx: Context<RemovePoolOperator>, operator: Pubkey) -> Result<()> {
        pool::remove_pool_operator(ctx, operator)
```

In `start_committed_credit` the comments the mention the pool owner and sentinel can call this instruction. However, it is the Evaluation Agent and the sentinel who can call this instruction.

```
/// # Access Control
    /// Only the pool owner and the Sentinel Service account can call this instruction.
    pub fn start_committed_credit(ctx: Context<StartCommittedCredit>) -> Result<()> {
        credit::start_committed_credit(ctx)
    }
```

##### Score

Impact:   
Likelihood:

##### Recommendation

It is recommended to update the documentation to remove all the inconsistencies.

##### Remediation

**PARTIALLY SOLVED:** The **Huma team** partially solved this issue. They updated the [lib.rs](http://lib.rs) file with the appropriate modifications correcting the mentioned inconsistent comments.

##### Remediation Hash

<https://github.com/00labs/huma-solana-programs/pull/98>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Huma Protocol |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/huma/huma-protocol
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/huma/huma-protocol

### Keywords for Search

`vulnerability`

