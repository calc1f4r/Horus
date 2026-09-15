---
# Core Classification
protocol: Berachain Pol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52869
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Pol-Spearbit-Security-Review-October-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Pol-Spearbit-Security-Review-October-2024.pdf
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
finders_count: 4
finders:
  - Kaden
  - Optimum
  - 0xDjango
  - Noah Marconi
---

## Vulnerability Title

distributeFor might be reentered leading to the loss of BGT and incentive tokens

### Overview


This bug report is about a high-risk issue in the code of a smart contract called Distributor.sol. The function called "distributeFor" is responsible for giving out tokens to validators. However, there is a problem with the way it is coded. The function first checks for the next block to be processed, then transfers tokens to the validator, and only after that, it increments the block number. This violates a security principle called "Checks-Effects-Interactions" and could potentially allow for a hacker to drain all the tokens from the contract. The report suggests either changing the order of the code or adding a protection against reentrancy. This issue has been fixed in the code by the developers.

### Original Finding Content

Severity: High Risk
Context: Distributor.sol#L113-L114
Description: The code flow of Distributor.distributeFor is in charge of compensating validators with BGT
tokens and additional vault specific tokens. During the flow of the function, it queries the nextActionableBlock ,
then it is transferring (using a potentially untrusted external call) the incentive tokens to the validator and only
then increments the getNextActionableBlock to make sure the next transaction would not double-spend. The
distributeFor is therefore violating the "Checks-Effects-Interactions" pattern since the external interaction is
executed before the effects (incrementing the getNextActionableBlock ). In case one of the incentive tokens
implements an unsafe external call, the call flow can be hijacked to re-enter distributeFor repeatedly and by
this drain the entire BGT and incentive tokens allocated. The reentrant call will have to provide the necessary
parameters that were used originally for the call but this can be fetched by a front runner spotting the call to
distributeFor in the mempool and writing the value to a contract that will be used through the reentrancy flow.
Recommendation: Consider either switching the order of _distributeFor and _incrementBlock so that _in-
crementBlock will be called first, or alternatively, adding a reentrancy guard todistributeFor . ReentrancyGuard-
Transient.sol might help to do it in a more gas efficient way but has partial support in EVM chains. Please refer to
evmdiff.com for more information about opcodes support.
Berachain: Fixed in commit 534a0eba.
Spearbit: Fixed by implementing the auditor's recommendation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Berachain Pol |
| Report Date | N/A |
| Finders | Kaden, Optimum, 0xDjango, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Pol-Spearbit-Security-Review-October-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Pol-Spearbit-Security-Review-October-2024.pdf

### Keywords for Search

`vulnerability`

