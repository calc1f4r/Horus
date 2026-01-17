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
solodit_id: 52872
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Pol-Spearbit-Security-Review-October-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Pol-Spearbit-Security-Review-October-2024.pdf
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

Activation of queued cutting board can be manipulated leading to redirection of BGT

### Overview


This bug report discusses an issue with the Berachef.sol#158 code, where a validator operator can queue a new cutting board at any time and activate it after a certain delay. However, this system can be manipulated by a malicious validator by publicly queueing a cutting board to attract BGT stakes from interested stakeholders. This can result in the rewards being cut to different reward vaults than originally intended. The recommendation is to not allow validators to queue a new cutting board if there is already one ready for activation. This bug has been fixed in the Berachain and Spearbit code.

### Original Finding Content

Severity: Medium Risk
Context: Berachef.sol#158
Description: A validator operator can queue a new cutting board at any time. Once thecuttingBoardBlockDelay
has passed, the queued cutting board is ready for activation. The activation of a cutting board occurs viadistrib-
utor.distributeFor() which calls beraChef.activateReadyQueuedCuttingBoard(pubkey, blockNumber); .
The validator is incentivized to emit the BGT reward to reward vaults that will provide the best financial incentives
while also incentivizing BGT holders to stake their BGT to the validator to boost emissions.
However, a malicious validator can game this system by publicly queueing a cutting board to incentivize certain
reward vaults. This will attract the BGT stakes of interested stakeholders. When the validator is chosen to validate
a block, the validator can queue a new cutting board which will invalidate the previously queued cutting board that
would be activated and used for emissions when calling distributor.distributeFor() .
Example:
• Validator currently has weights set to three reward vaults A, B, and C.
• Validator queues to instead cut rewards to D, E, and F . ThestartBlock is set at 1000.
• Protocols benefitting from D, E, and F shift support to Validator based on proposed cutting board.
• Blocks pass, now on block 1100.
• Validator gets selected for block.
• Someone calls distributeFor().
• Validator frontruns and calls queueNewCuttingBoard(). It doesn't matter which weights they select. Simply,
it will set the queuedCuttingBoard[valPubKey.startBlock] in the future.
• isQueuedCuttingBoardReady() will return false and short-circuit activateReadyQueuedCuttingBoard() .
• The rewards will still be cut to A, B, and C.
Recommendation: Do not allow validators to queue a new cutting board if the currently queued cutting board is
ready for activation.
Berachain: Fixed in commit 62c6d466.
Spearbit: Fixed by removing the ability to queue another cutting board if an operator already has a queued cutting
board.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

