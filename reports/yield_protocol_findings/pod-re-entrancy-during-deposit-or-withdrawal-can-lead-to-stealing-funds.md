---
# Core Classification
protocol: PoolTogether - Pods
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13467
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/03/pooltogether-pods/
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
  - yield
  - services
  - rwa
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

Pod: Re-entrancy during deposit or withdrawal can lead to stealing funds

### Overview


This bug report concerns a vulnerability in the Pod.sol contract, specifically the code on lines 274-281. This code allows an attacker to make a deposit and then transfer tokens, but if the token allows re-entrancy, the attacker can deposit a second time before the first token transfer is completed. This could result in the attacker minting more tokens than intended, allowing them to drain the pod.

The recommendation is to add a re-entrancy guard to the external functions to prevent this vulnerability. This guard would check for any re-entrant calls and block them, thus preventing the attacker from exploiting the bug.

### Original Finding Content

#### Description


During the deposit, the token transfer is made after the Pod shares are minted:


**code/pods-v3-contracts/contracts/Pod.sol:L274-L281**



```
uint256 shares = \_deposit(to, tokenAmount);

// Transfer Token Transfer Message Sender
IERC20Upgradeable(token).transferFrom(
    msg.sender,
    address(this),
    tokenAmount
);

```
That means that if the `token` allows re-entrancy, the attacker can deposit one more time inside the token transfer. If that happens, the second call will mint more tokens than it is supposed to, because the first token transfer will still not be finished.
By doing so with big amounts, it’s possible to drain the pod.


#### Recommendation


Add re-entrancy guard to the external functions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | PoolTogether - Pods |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/03/pooltogether-pods/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

