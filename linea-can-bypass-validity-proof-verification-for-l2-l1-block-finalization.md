---
# Core Classification
protocol: Linea
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33302
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
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
  - Dacian
---

## Vulnerability Title

Linea can bypass validity proof verification for L2->L1 block finalization

### Overview

See description below for full details.

### Original Finding Content

**Description:** One major advantage of using zk rollups over Optimistic rollups is that zk rollups use math & cryptography to verify L2->L1 block finalization via a validity proof which must be submitted and verified.

In the current codebase the Linea team has two options to bypass validity proof verification during block finalization:

1) Explicitly by calling `LineaRollup::finalizeBlocksWithoutProof` which takes no proof parameter as input and doesn't call the `_verifyProof` function.

2) More subtly by calling `LineaRollup::setVerifierAddress` to associate a `_proofType` with a `_newVerifierAddress` that implements the `IPlonkVerifier::Verify` interface, but which simply returns `true` and doesn't perform any actual verification. Then call `LineaRollup::finalizeBlocksWithProof` passing `_proofType` associated with `_newVerifierAddress` which will always return true.

**Impact:** Using either option makes Linea roughly equivalent to an Optimistic roll-up but without Watchers and the ability to challenge. That said if either option is used, `LineaRollup::_finalizeBlocks` always executes which enforces many "sanity checks" that significantly limit how these options can be abused.

The "without proof" functionality can also be used to add false L2 merkle roots which could then be used to call `L1MessageService::claimMessageWithProof` to drain ETH from the L1.

**Recommended Mitigation:** Linea is still at the alpha stage so these functions are likely needed as a last resort. Ideally once Linea is more mature such functionality would be removed.

**Linea:**
Acknowledged; the ability to finalize blocks without proof is primarily part of our "training wheels" controlled via the Security Council, analyzed by Security partners and reserved for particular cases like we had when we upgraded our state manager to another hashing algorithm (the last time it was used).

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Linea |
| Report Date | N/A |
| Finders | Dacian |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

