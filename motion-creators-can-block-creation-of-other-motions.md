---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19458
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf
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

Motion Creators Can Block Creation of Other Motions

### Overview

See description below for full details.

### Original Finding Content

## Description

The EasyTrack contract enforces a global limit to the number of currently active motions. Once reached, no new motions can be created. If a malicious actor is able to create new motions, they can flood the contract with motions to fill up this list and effectively halt the operation of EasyTrack.

The likelihood of any associated attack is fairly low. The current factories correctly restrict authorized creators to a small number of trustedCaller and node operator accounts, with the trustedCaller accounts expected to be multisigs controlled by a small committee. These should all be highly trusted and well-known entities, so it is unlikely that any of them are malicious.

In the event that one of these accounts is compromised by a malicious entity, the severity of this attack is also limited. While the EasyTrack system can be subject to denial-of-service, it can always be overridden by the Aragon voting DAO. The DAO can directly execute scripts on `EVMScriptExecutor` to bypass any blockage and can replace the factory which authorizes the malicious account (via `EVMScriptFactoriesRegistry.removeEVMScriptFactory()`).

As such, the testing team deems the associated severity to be *Low*.

## Recommendations

- Be conscious about these risks when adding new factories and otherwise authorizing new entities to create motions.
- Ensure that any updates continue to prevent unauthenticated attackers from creating motions.
- Consider introducing clear, visible documentation to highlight this for any future maintainers and relevant stakeholders; both in the NatSpec comments for `EVMScriptFactoriesRegistry.addEVMScriptFactory()` and in external documentation like the project README or specification.
- One could also consider enforcing a separate motion limit per factory, but this is likely not worth the increased gas costs.

## Resolution

Relevant documentation has been introduced as part of PR #6. In particular, the README contains documentation describing appropriate guidelines and best practices for those creating a new EVMScript factory, and an appropriate warning was added to the NatSpec for `EVMScriptFactoriesRegistry.addEVMScriptFactory()`.

> Not to mention any other controls the DAO may have to act directly on the relevant contracts like the finance contract.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/lido/lido-easy-track/review.pdf

### Keywords for Search

`vulnerability`

