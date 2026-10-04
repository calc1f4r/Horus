---
# Core Classification
protocol: The LAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13873
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/01/the-lao/
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
  - cdp
  - services
  - insurance
  - payments

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Sergii Kravchenko
  - Shayan Eskandari
  -  Daniel Luca
---

## Vulnerability Title

Emergency processing can be blocked ✓ Fixed in Pull Pattern

### Overview


A bug has been reported in the code/contracts/Moloch.sol, lines 407-411, which affects the emergency processing mechanism. This mechanism exists to prevent token transfers from being blocked, for example if a sender or a receiver is in the USDC blacklist. Currently, the emergency processing no longer exists in the Pull Pattern update, meaning there is a chance that token transfers could still be blocked. This would prevent proposals from being processed and the LAO from being able to function. To fix this, it is recommended to implement Pull Pattern for all token withdrawals. An alternative solution would be to keep the deposit tokens in the LAO, but this would make sponsoring the proposal more risky for the sponsor.

### Original Finding Content

#### Resolution



Emergency Processing no longer exists in the Pull Pattern update.


#### Description


The main reason for the emergency processing mechanism is that there is a chance that some token transfers might be blocked. For example, a sender or a receiver is in the USDC blacklist. Emergency processing saves from this problem by not transferring tribute token back to the user (if there is some) and rejecting the proposal.


**code/contracts/Moloch.sol:L407-L411**



```
if (!emergencyProcessing) {
    require(
        proposal.tributeToken.transfer(proposal.proposer, proposal.tributeOffered),
        "failing vote token transfer failed"
    );

```
The problem is that there is still a deposit transfer back to the sponsor and it could be potentially blocked too. If that happens, proposal can’t be processed and the LAO is blocked.


#### Recommendation


Implementing pull pattern for all token withdrawals would solve the problem. The alternative solution would be to also keep the deposit tokens in the LAO, but that makes sponsoring the proposal more risky for the sponsor.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | The LAO |
| Report Date | N/A |
| Finders | Sergii Kravchenko, Shayan Eskandari,  Daniel Luca |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/01/the-lao/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

