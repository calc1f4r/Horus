---
# Core Classification
protocol: Unicrow
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21040
audit_firm: AuditOne
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2022-12-14-Unicrow.md
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
  - AuditOne
---

## Vulnerability Title

Reentrancy to UnicrowClaim can claim twice

### Overview


This bug report is about a reentrancy attack in a refund()function, which is used to pay full funds to the buyer by the seller. The singleClaim()function is used to pay funds for the buyer, seller, etc. The malicious buyer and seller can exploit the attack to claim two times per escrow and steal all funds in the contract.

The bug occurs because the functions refund() and singleClaim() have the nonReentrant modifier to prevent a re-entrancy attack, but they are in different contracts and the state into nonReentrant modifier doesn’t synchronize.

The recommendation is to follow the check-effect-interaction pattern and add nonReentrant to functions setClaimed()/sendEscrowShare(). This means that the state of claimed should be changed before sending tokens.

### Original Finding Content

**Description:** 

In function `refund()`,it set `claimed = 1`after withdrawing to buyer. If currency is native token or ERC777 with hook,buyer can take control of the execution flow and call `UnicrowClaim.singleClaim()`function. Since `claimed`is not set and consensus are set to positive value,it will not revert and allow buyer to claim the same escrow again.

The refund()is used to pay full funds to the buyer by the seller. The singleClaim()is used to pay funds for the buyer,seller,etc ... Both refund()and singleClaim have some

implementation as follows.

1. The nonReentrant modifier to prevent a re-entrancy attack
2. The checking of escrow.claimed is 0 to prevent re-claim. However,malicious attackers can claim two times per escrow and all funds in the contract can be stolen.

Example- malicious buyer:Alice,malicious seller:Bob

1. Alice and Bob create an escrow and Alice pay 1ETH for their orders as input.amount. Their escrow doesn’t split for arbitrator and protocol.
2. Bob executes refund()to pay the 1ETH to Alice as a seller
3. Alice received 1ETH before the state of claimed changed yet

4. (4 not 1)Alice executes singleClaim()as soon as Alice receives ETH in the fallback function
5. (5 not 2)It is true that both refund and singleClaim has the nonReentrant modifier

but these functions are in dierent contract. Since both contract import “ReentrancyGuard” separately,the state into nonReentrant modifier doesn’t synchronize.

6. (6 not 3)Finally,Alice and Bob got 2 ETH from 1ETH. If we continue this attack,attackers can get all ETH in the contract. Also,if the token follows ERC777,this token will be stolen like ETH.

You can see more detail of cross contract reentrancy attack

[https://inspexco.medium.com/cross-contract-reentrancy-attack-402d27a02a15 ](https://inspexco.medium.com/cross-contract-reentrancy-attack-402d27a02a15)

**Recommendations:** 

Consider following check-eect-interaction pattern or adding nonReentrant to functions `setClaimed()`/ `sendEscrowShare()`

"Should change the state of claimed before sending tokens.In other words,you should follow the check-eect-interactions pattern [https://fravoll.github.io/solidity-patterns/checks_eects_interactions.html](https://fravoll.github.io/solidity-patterns/checks_effects_interactions.html)

// Update the escrow as claimed in the storage and in the emitted event

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | AuditOne |
| Protocol | Unicrow |
| Report Date | N/A |
| Finders | AuditOne |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2022-12-14-Unicrow.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

