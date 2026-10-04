---
# Core Classification
protocol: SteadeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27615
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf
source_link: none
github_link: https://github.com/Cyfrin/2023-10-SteadeFi

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
finders_count: 7
finders:
  - nervouspika
  - 0xhacksmithh
  - TheSchnilch
  - pks27
  - kz0213871
---

## Vulnerability Title

Incorrect state transition may cause vault in stuck

### Overview


This bug report is about an incorrect state transition that may cause a vault to become stuck. A vault is a form of digital asset storage. The incorrect state transition occurs when a keeper executes a 'compound' action and the GMXCallback returns an 'afterDepositCancellation' action. In this scenario, the protocol will call the 'GMXCompound#processCompoundCancellation' function to change the vault status. However, the vault status is changed to 'GMXTypes.Status.Compound_Failed' instead of 'GMXTypes.Status.Open'. This is different than what is described in the document at the GitHub link provided.

The impact of this bug is that the vault may become stuck in an unexpected state after the 'processCompoundCancellation' action. Tools used to identify the bug include vscode and manual review.

The recommendation to fix this bug is to change the vault status to 'Open' instead of 'Compound_Failed' when calling the 'GMXCompound#processCompoundCancellation' function.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXCompound.sol#L127-L136">https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXCompound.sol#L127-L136</a>


## Summary

Incorrect state transition may cause vault in stuck under `processCompoundCancellation` scenario.

## Vulnerability Details

When keeper execute `compound` action and GMXCallback return `afterDepositCancellation` action, then protocol will call `GMXCompound#processCompoundCancellation` function to change vault status.

However, vault status is changed to `GMXTypes.Status.Compound_Failed` instead of `GMXTypes.Status.Open` by `GMXCompound#processCompoundCancellation` function, which is different with document described below:

https://github.com/Cyfrin/2023-10-SteadeFi/blob/main/docs/sequences/strategy-gmx-compound-sequence-detailed.md

and `All scenarios should be handled to ensure vault eventually returns to an Open status. Consider how a scenario might lead to a stuck vault (other statuses).`

## Impact

Vault may stuck in unexpected state after `processCompoundCancellation` action.

## Tools Used

vscode, Manual Review

## Recommendations

Change the vault status to `Open` instead of `Compound_Failed` when call `GMXCompound#processCompoundCancellation` function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | nervouspika, 0xhacksmithh, TheSchnilch, pks27, kz0213871, 0xAsen, rvierdiiev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

