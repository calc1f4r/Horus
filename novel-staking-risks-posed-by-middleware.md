---
# Core Classification
protocol: EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36026
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigen-layer-2/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigen-layer-2/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Novel Staking Risks Posed by Middleware

### Overview

See description below for full details.

### Original Finding Content

## Description

Middleware (as named by EigenLayer) poses a unique value proposition within the liquid staking derivative ecosystem. Their premise is that middlewares can leverage existing stake assigned to a single operator, allowing multiple different protocols to leverage the same stake to secure their network, protocol, or application. With novel value propositions comes the reasonably novel risk to staking protocols of ’cross-protocol security implications’. Previously calculated staking risks, and therefore relevant rewards have only accounted for risks to the platform that staking is occurring on. 

With EigenLayer’s middleware contracts, situations may arise that may previously have been unprofitable that are now profitable. Essentially, protocol risk becomes entangled and compounded within subsets of other protocols. For instance, knowing the slashing penalties involved, it may previously have been unprofitable to commit an attestation or proposal violation on Ethereum. However, as we enter a state where multiple protocols and applications (all providing their own rewards) leverage the same stake, an operator can potentially violate all protocols and risk being slashed if the rewards potentially outweigh the slashing penalty risk.

Stakers, Operators, and Middleware alike are all impacted in various ways through compounding risks of operators adding multiple ’unsafe’ or even ’malicious’ middlewares to their whitelist. One middleware could hold a group of other middlewares ransom, by threatening or enacting slashing of its operators if compromising the security of other middlewares can yield more reward than the cost of ruining their own network.

## Recommendations

The testing team acknowledges that EigenLayer does not aim to enforce the use of secure middleware on any Operator. However, the testing team recommends the following actions:

1. Documentation should clearly state the risks of using middleware for operators.
2. Documentation should clearly state the risks of too many middlewares using the same subset of operators.
3. Potentially adding functionality that allows middlewares to dictate which operators match their risk profile. For instance, it could be deemed unsafe for one protocol to use a potentially high-risk set of operators using an extremely large set of middlewares.

## Resolution

The development team has acknowledged this issue and will strive to ensure that the relationships between middlewares, operators, and stakers are clearly defined.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigen-layer-2/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigen-layer-2/review.pdf

### Keywords for Search

`vulnerability`

