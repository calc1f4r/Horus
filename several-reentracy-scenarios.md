---
# Core Classification
protocol: XPress
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56836
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/XPress/OnchainCLOB/README.md#1-several-reentracy-scenarios
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Several reentracy scenarios

### Overview


The report describes a bug in the `LOB` contract that could lead to financial loss. The bug is related to the use of ERC-20 tokens with extensions, which can give an attacker control during a token transfer. This control can be used to exploit the protocol and gain profit through a "reentrancy" attack. This attack involves setting up send/receive hooks and executing additional calls to the protocol to double-spend tokens. The severity of this bug is classified as critical. To prevent this issue, it is recommended to apply the OpenZeppelin `nonReentrant` modifier to all public and external functions and to update the trader's balance before performing transfer operations.

### Original Finding Content

##### Description
The issue is identified within the `LOB` contract.

Some ERC-20 tokens implement extensions, such as the ERC-777 standard, that allow an account to gain execution control during token transfers. As the protocol is planned to be deployed on several networks and support various tokens, it may encounter issues related to these types of tokens.

If an attacker gains control during a token transfer, they can launch a "reentrancy" attack against the protocol by following these steps:
1. Set up send/receive hooks.
2. Perform an action that causes the protocol to send or receive tokens.
3. Execute additional calls to the protocol, exploiting the inconsistent state from step 2 to gain profit.

At a minimum, the following scenarios can be exploited:
- Withdraw tokens, reenter the protocol, and withdraw the same tokens again, effectively double-spending.
- Deposit tokens, reenter the protocol with the `placeOrder` function, and double-spend the tokens.

This issue is classified as **critical** severity because it can lead to significant financial loss through double-spending.

##### Recommendation
We recommend applying the OpenZeppelin `nonReentrant` modifier to all public and external mutable functions to prevent reentrancy attacks. Additionally, consider updating the trader's balance before performing the transfer operations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | XPress |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/XPress/OnchainCLOB/README.md#1-several-reentracy-scenarios
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

