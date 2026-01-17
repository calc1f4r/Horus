---
# Core Classification
protocol: Mass
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29683
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-nestedfinance-smartcontracts-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-nestedfinance-smartcontracts-securityreview.pdf
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
finders_count: 5
finders:
  - Gustavo Grieco
  - Josselin Feist
  - Tarun Bansal
  - Kurt Willis
  - Richie Humphrey
---

## Vulnerability Title

DCA tasks can be stopped by anyone

### Overview


The report discusses a bug in the NestedDca.sol code, which is used for automated trading. The bug allows anyone to stop an active DCA (dollar-cost averaging) task by providing a task ID, without any validation checks. This means that someone can stop another user's automated task without their permission, potentially causing financial loss. The report recommends implementing short-term and long-term solutions, such as adding validation checks and creating unit tests, to prevent this bug from being exploited in the future.

### Original Finding Content

## Vulnerability Report

## Difficulty: Low

## Type: Data Validation

### Description
Stopping an active DCA task relies on a user-provided parameter, the task ID. However, there is no validation performed on this value, so any automated DCA task can be stopped by anyone. 

The `stopDca` function takes as input a DCA ID and a Gelato-ops task ID.

```solidity
function stopDca(bytes32 dcaId, bytes32 _taskId) public override onlyDcaOwner(dcaId) {
    Dca storage dca = dcas[dcaId];
    if (!dca.isGelatoWatching) revert DcaAlreadyStopped(dcaId);
    IOps(ops).cancelTask(_taskId);
    dca.isGelatoWatching = false;
    emit DcaStopped(dcaId, _taskId);
}
```

*Figure 25.1: The `stopDca` function in NestedDca.sol*

Ownership of the DCA is verified through the `onlyDcaOwner(dcaId)` modifier. However, there are no checks performed on the `_taskId` parameter to verify that the given task ID belongs to the provided DCA ID (i.e., `require(_taskId == dcas[dcaId].taskId)`), or that the given DCA has ever successfully started a task in the first place. This means that anyone is able to supply a task ID of a running DCA to shut down another user's automated task.

### Exploit Scenario
Alice sets up a task to dollar-cost-average her 100 million TokenA back to USDC over the next month. Eve stops Alice’s DCA task. After one month, TokenA's value suddenly declines to nearly zero. Without her knowledge, Alice’s token has lost all of its value, since the DCA task was not performed after being stopped by Eve without Alice’s approval.

### Recommendations
- **Short term:** Add a check that verifies that the task ID matches the task ID from the provided DCA, or have the code simply directly access the task ID stored for the given DCA.
- **Long term:** Document the expected validation that should occur when a DCA task is stopped. Create a diagram highlighting the life cycle of a DCA and the underlying invariants. Create unit tests for each state transition, and consider using Echidna to test multiple-transaction invariants.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Mass |
| Report Date | N/A |
| Finders | Gustavo Grieco, Josselin Feist, Tarun Bansal, Kurt Willis, Richie Humphrey |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-nestedfinance-smartcontracts-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-02-nestedfinance-smartcontracts-securityreview.pdf

### Keywords for Search

`vulnerability`

