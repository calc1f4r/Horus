---
# Core Classification
protocol: UnikoinGold Token Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11964
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/unikoingold-token-audit-aafb7de07f3/
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

protocol_categories:
  - dexes
  - bridge
  - cdp
  - cross_chain
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Unnecessary claim step for sale contributors

### Overview


This bug report is about the token distribution process of Unikrn, a platform that allows contributors to participate in a sale by transferring their balance to a set of trusted addresses. The documentation states that the token allocations are set for each contributor, who must then claim the tokens to have them added to their balance in order to prevent 1B tokens from being created. However, this is incorrect because tokens can still be created and allocated to their addresses, resulting in 1B tokens even if some participants can’t move them afterwards. Furthermore, tokens are locked in the TokenDistribution contract and there are no methods to take them out, making them unusable.

To fix this issue, it is suggested to remove the claim mechanic altogether and allocate the tokens to the contributors directly. This will reduce the complexity of the distribution process, simplify the code, and reduce the hassle for end users. The CoinCircle team indicated that this was motivated by the fact that the proxy contract will be deployed before the distribution contract, in order to store the future owners of the token before the final implementation is finalized.

### Original Finding Content

Contributors participate in the sale by transferring their balance to a set of trusted addresses managed by Unikrn, who then distribute the tokens in a later step via the `TokenDistribution` contract. Token allocations are set for each contributor, who must then [claim](https://github.com/unikoingold/UnikoinGold-UKG-Contract/blob/8b38f30039c2d13383c416fd6143f6bd0f091404/contracts/TokenDistribution.sol#L148) the tokens to have them added to their balance.


The [documentation](https://github.com/unikoingold/UnikoinGold-UKG-Contract/blob/8b38f30039c2d13383c416fd6143f6bd0f091404/README.md#participant-claim) indicates that this is done “because if a participant were to lose their key, there would never be 1B tokens created”. This is incorrect, since tokens can still be created and allocated to their addresses. This way, there will be indeed 1B tokens, even if some participants cannot move them afterwards.


Furthermore, if a participant did misplace their keys, tokens are locked in the TokenDistribution contract (as per [L136](https://github.com/unikoingold/UnikoinGold-UKG-Contract/blob/8b38f30039c2d13383c416fd6143f6bd0f091404/contracts/TokenDistribution.sol#L136)) and there are not methods to take them out of the contract, so the tokens are created but are unusable. A participant may misplace their keys after the distribution, so it makes no sense to try to prevent allocation to addresses with lost keys.


Consider removing the claim mechanic altogether, and allocate the tokens to the contributors directly. The whole `ParticipantAdditionProxy` contract seems to be unnecessary. This reduces the complexity of the distribution process, simplifies the code, and reduces the hassle for end users to access their purchased tokens.


**Update:** *The CoinCircle team indicated that this was motivated by the fact that the proxy contract will be deployed before the distribution contract, in order to store the future owners of the token before the final implementation is finalized:*



> 
>  The design decision for the contract was to separate concerns: the proxy contract will be deployed prior to the distribution contract. The proxy contract will be populated by Unikrn, and not be made known to the public until the contract is verified, locked and unchangeable
> 
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | UnikoinGold Token Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/unikoingold-token-audit-aafb7de07f3/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

