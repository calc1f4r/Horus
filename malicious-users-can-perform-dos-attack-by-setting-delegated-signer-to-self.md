---
# Core Classification
protocol: Ethena Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60279
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/ethena-labs/307f3777-9f03-4b08-8b92-b6c243388ebc/index.html
source_link: https://certificate.quantstamp.com/full/ethena-labs/307f3777-9f03-4b08-8b92-b6c243388ebc/index.html
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

protocol_categories:
  - staking_pool
  - decentralized_stablecoin

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Michael Boyle
  - Jeffrey Kam
  - Jonathan Mevs
---

## Vulnerability Title

Malicious Users Can Perform Dos Attack by Setting Delegated Signer to Self

### Overview


The client has marked a bug in the `EthenaMinting.sol` file as fixed. The issue was related to a nested mapping structure for delegated signers and a new function to undelegate. When a smart contract called `setDelegatedSigner()`, it could delegate an EOA to be the signer for the contract. However, a malicious actor could exploit this by blocking `mint()` or `redeem()` calls for the contract by front-running it with a call to `delegateSigner()`. The recommendation is to reverse the order of the mapping or create a nested mapping to prevent this exploit.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `e4282dcf1471841f71dd5cb6efe303b104481f92`. The client provided the following explanation:

> Nested mapping structure for delegatedSigner, plus added function to undelegate

**File(s) affected:**`EthenaMinting.sol`

**Description:** When `order.benefector` is a smart contract, it can delegate an EOA to be the signer for the contract, by calling `setDelegatedSigner()`. When `mint()` and `redeem()` are called, they first check that the order is valid by calling `validateOrder()`, which in turn checks that the signer of the order is either `msg.sender` or a delegated signer for `msg.sender` (i.e. `delegatedSigner[signer] == order.benefactor`). Suppose contract A delegates Alice to be the signer by calling `delegateSigner(Alice)`, this would result in `delegatedSigner[Alice] = A`. However, since `setDelegatedSigner()` can be called by anyone, this allows a malicious actor, Bob, to block any `mint()` or `redeem()` calls for contract A (signed by Alice) by front-running it with a call `delegateSigner(Alice)`, which would set `delegatedSigner[Alice] = Bob`, causing `verifyOrder()` to fail.

**Recommendation:** Consider reversing the order of the mapping so that the order benefactor sets the signer. If this goes against the design philosophy, consider creating a nested mapping from the delegated signer to the order benefactor to a boolean. This would prevent a DoS as a single user could have multiple valid delegated signers.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Ethena Labs |
| Report Date | N/A |
| Finders | Michael Boyle, Jeffrey Kam, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/ethena-labs/307f3777-9f03-4b08-8b92-b6c243388ebc/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/ethena-labs/307f3777-9f03-4b08-8b92-b6c243388ebc/index.html

### Keywords for Search

`vulnerability`

