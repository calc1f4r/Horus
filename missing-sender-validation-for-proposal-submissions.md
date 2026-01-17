---
# Core Classification
protocol: Layer N
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54111
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/c2a14eb1-a159-4fd8-8494-a4ead69ec097
source_link: https://cdn.cantina.xyz/reports/cantina_layern_l2rollup_jul2024.pdf
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
  - zigtur
  - Rikard Hjort
  - defsec
---

## Vulnerability Title

Missing Sender Validation for Proposal Submissions 

### Overview


The current code for the `submit_proposal` function in the RollupManager does not verify the identity of the sender. This means that anyone can submit a proposal, even if they are not authorized to do so. The recommendation is to implement a whitelist of authorized proposer addresses. This issue has been acknowledged and it has been noted that validation is already being done at the contract level, which decreases the severity of the bug.

### Original Finding Content

## Proposal Submission Review

## Context
(No context files were provided by the reviewer)

## Description
The current implementation of the `submit_proposal` function in the RollupManager does not verify the identity of the sender submitting the proposal. The relevant code snippet is:

```rust
async fn submit_proposal(&self, proposal: Proposal) -> Result<Option<OnchainUpdates>> {
    // ... (existing implementation)
    self.settlement
        .propose_state_update_claim(state_update_facts.clone())
        .await?;
    // ... (rest of the implementation)
}
```

## Recommendation
Implement a whitelist of authorized proposer addresses.

## Layer N
Acknowledged. Validation is done at the contract level.

## Cantina Managed
Acknowledged. Validation being done at the contract level decreases severity to informational.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Layer N |
| Report Date | N/A |
| Finders | zigtur, Rikard Hjort, defsec |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_layern_l2rollup_jul2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/c2a14eb1-a159-4fd8-8494-a4ead69ec097

### Keywords for Search

`vulnerability`

