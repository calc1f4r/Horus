---
# Core Classification
protocol: Berachain Beaconkit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49772
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Beacon-kit-Spearbit-Security-Review-November-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Beacon-kit-Spearbit-Security-Review-November-2024.pdf
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
  - Guido Vranken
  - Shotes
  - Hack3r0m
  - 0xDeadbeef
---

## Vulnerability Title

validatorUpdates ignores the effects of ProcessBlock leading to wrong voting power for validators

### Overview


A bug has been reported in the state_processor.go file, specifically in lines 187-195. The bug affects the order of state processing in the Transition function. This can result in incorrect handling of validator updates and balance changes. It also breaks important rules and specifications, leading to inaccurate voting power and temporary changes in stake. The recommendation is to fix this by sending validator updates to cometbft after the ProcessBlock step. This bug has been acknowledged and verified by the developers. 

### Original Finding Content

## Temporary Issue

**Severity:** Medium Risk  
**Context:** state_processor.go#L187-L195  

**Description:**  
Here is the current order of state processing in the Transition function:  

- **Transition**
  - `ProcessSlots` (validatorUpdates and IncreaseBalance/DecreaseBalance happen correctly).
    - *processSlot* (for each slot until target).
      - If epoch boundary: processEpoch.
  - `ProcessBlock` (IncreaseBalance/DecreaseBalance happen correctly, validatorUpdates are ignored and not sent to cometbft till next epoch).
    - *processBlockHeader*.
    - *processExecutionPayload*.
    - *processWithdrawals* (can decrease balance).
    - *processRandaoReveal*.
    - *processOperations* (can increase balance).

This breaks the various invariants and specs, major ones being voting power does not reflect the underlying stake and can be temporarily undermined or inflated.

**Recommendation:**  
ValidatorUpdates should be sent to cometbft after ProcessBlock.

**Berachain:** Acknowledged. This has been deprecated by a fix in PR 2226.  
**Spearbit:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Berachain Beaconkit |
| Report Date | N/A |
| Finders | Guido Vranken, Shotes, Hack3r0m, 0xDeadbeef |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Beacon-kit-Spearbit-Security-Review-November-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Beacon-kit-Spearbit-Security-Review-November-2024.pdf

### Keywords for Search

`vulnerability`

