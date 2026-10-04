---
# Core Classification
protocol: Scroll Phase 1 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32933
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/scroll-phase-1-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Users Can Lose Refund by Default

### Overview


The `L1ScrollMessenger` has a function called `sendMessage` that allows users to initiate a transaction from one blockchain to another. However, there are two versions of this function, one with a refund address parameter and one without. The problem is that the function without the parameter uses a default refund address, which can cause users with smart contract wallets to lose funds. This is because the default refund address is set to a specific account, even if the user intends to receive the refund themselves. This issue affects all of the gateways that use this function, meaning a high percentage of users with smart contract wallets may lose funds when using this feature. The suggested solution is to default the refund address to the user's own address and update the gateway contracts accordingly. This issue has been resolved in a recent update to the code.

### Original Finding Content

In the `L1ScrollMessenger`, the `sendMessage` functions allow a user to initiate a transaction on L2 from L1. There are two `sendMessage` implementations, with and without a refund address parameter. For the function without the parameter, the refund address of the internal `_sendMessage` call is [defined as `tx.origin`](https://github.com/scroll-tech/scroll/blob/3bc8a3f5c6ac816ddffadca41024331dcf4d3064/contracts/src/L1/L1ScrollMessenger.sol#L106).


This poses a risk of loss of funds for smart contract wallets. More concretely, with account abstraction gradually emerging, this default refund recipient would end up being the [`UserOperations` bundler](https://eips.ethereum.org/EIPS/eip-4337#definitions). Hence, while a user might think to receive the refund themselves, they end up losing their excessive funds.


Further, all of the gateways make use of this particular `sendMessage` function with the default `tx.origin` refund address. Hence, a high percentage of users with smart contract wallets may lose some ETH during bridging.


Consider defaulting the refund address in the `L1ScrollMessenger` contract to `msg.sender`. In the gateway contracts, consider using the `sendMessage` function with the definable refund recipient that is then set to `msg.sender`.


***Update:** Resolved in [pull request #605](https://github.com/scroll-tech/scroll/pull/605) at commit [76d4230](https://github.com/scroll-tech/scroll/pull/605/commits/76d4230571da5909499ace4c7bc90ad31a721325).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Scroll Phase 1 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/scroll-phase-1-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

