---
# Core Classification
protocol: Status
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19574
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/status/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/status/review.pdf
github_link: none

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
  - Sigma Prime
---

## Vulnerability Title

Users Can Create Unslashable/Non-removeable Subnode Names

### Overview


This bug report concerns a vulnerability in the UsernameRegistrar contract of the Ethereum Name Service (ENS). This vulnerability allows malicious users to register an invalid name (e.g. “SigmaPrime” which includes capitals) as a sub-subnode of the ENSNode. This name is irrevocable and can be obtained for free, regardless of the price variable. This could potentially damage the reputation of the ENSNode.

To demonstrate this vulnerability, a test called test_get_unslashable_subnode was created. To resolve this issue, a new function called eraseNode() was introduced. This function allows a number of iterations of subnodes to be removed if the root subdomain is invalid. Owners of a valid subdomain are free to generate arbitrary levels of subdomains beyond their valid root subdomain.

Additionally, a sub-domain slashing function was proposed. This function would allow users to slash any subdomain by providing a list of labels which recursively hash to an owned namehash. The contract would then reset the owner and slash any funds in the originating sub-domain.

### Original Finding Content

## Description

Users can register any name (including unsavoury ones) as a sub-subnode of the ENSNode. These names are irrevocable and can be obtained for free, regardless of the price variable.

The vulnerability exists because there is no functionality in the `UsernameRegistrar` contract to revoke or deal with subnodes beyond the first level. As such, a malicious user could register a name such as **“SigmaPrime,”** which is invalid because it includes capitals. Once registered, the user may call `setSubnodeOwner()` on the `ensRegistry` contract and create a subnode name of their choosing without restriction (for example, let's use **“OwnedSubnode”**). The user may then call `slashInvalidUsername()` in order to have their deposit returned, whilst maintaining ownership of the sub-subdomain. If, for example, `ENSNode` is set to **stateofus** (assumed to be a subnode of the Ethereum ENS registry), the malicious user would retain ownership of the name **OwnedSubnode.SigmaPrime.stateofus.eth**.

In this process, the user has obtained this domain for free and the name is irrevocable and unslashable. Although this vulnerability may not affect the front-end application dealing with usernames, it allows malicious users to create names derived from `stateofus.eth` which could potentially damage the status’ reputation. See the test: **test_get_unslashable_subnode** that accompanies this report for a demonstration.

## Recommendations

As ENS names are recursive (an arbitrary number of sub-domains can be created), it would be possible to implement a sub-domain slashing function. This function would not be dissimilar to the functionality implemented in slashing reserved names using a Merkle proof. A user could slash any subdomain by providing a list of labels which recursively hash to an owned namehash. The contract could then reset the owner and slash any funds in the originating sub-domain.

## Resolution

A new function `eraseNode()` was introduced which allows a number of iterations of subnodes to be removed if the root subdomain is invalid. Owners of a valid subdomain are free to generate arbitrary levels of subdomains beyond their valid root subdomain.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Status |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/status/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/status/review.pdf

### Keywords for Search

`vulnerability`

