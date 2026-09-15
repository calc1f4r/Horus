---
# Core Classification
protocol: Treasury Vesting
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52687
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/blockdag/treasury-vesting
source_link: https://www.halborn.com/audits/blockdag/treasury-vesting
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Missing Category Validation

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `executeAddCategory` function in the TreasuryVesting contract allows the creation of arbitrary categories without validating if they match one of the predefined category types (EARLY\_BIRD\_CATEGORY, PRESALE\_CATEGORY, or TEAM\_CATEGORY). While the function includes specific validation logic for known categories, it doesn't prevent the creation of undefined categories:

```
function executeAddCategory(bytes32 operationId) external onlyRole(ADMIN_ROLE) {
    // ... decode parameters ...
    
    // Category-specific validations
    if (category == EARLY_BIRD_CATEGORY) {
        // Early Bird validations
    } 
    else if (category == PRESALE_CATEGORY) {
        // Presale validations
    } 
    else if (category == TEAM_CATEGORY) {
        // Team validations
    }
    // No else clause to prevent undefined categories
```

  

**Impact:**

* Allows creation of non-standard vesting categories
* Could lead to confusion in token distribution
* Inconsistent vesting rules across the protocol

##### BVSS

[AO:A/AC:M/AX:M/R:N/S:U/C:N/A:L/I:L/D:M/Y:N (2.8)](/bvss?q=AO:A/AC:M/AX:M/R:N/S:U/C:N/A:L/I:L/D:M/Y:N)

##### Recommendation

Add explicit category validation at the start of the function:

```
function executeAddCategory(bytes32 operationId) external onlyRole(ADMIN_ROLE) {
    TimelockOperation storage operation = timelockOperations[operationId];
    require(operation.operationId != bytes32(0), "Operation doesn't exist");
    require(!operation.executed, "Already executed");
    require(block.timestamp >= operation.executeTime, "Timelock not expired");

    operation.executed = true;

    // Decode operation parameters
    (
        bytes32 category,
        uint256 start,
        uint256 duration,
        uint256 totalAmount,
        uint256[] memory releaseSteps,
        uint256[] memory timeSteps
    ) = abi.decode(
        operation.encodedParams,
        (bytes32, uint256, uint256, uint256, uint256[], uint256[])
    );

    // Add explicit category validation
    require(
        category == EARLY_BIRD_CATEGORY ||
        category == PRESALE_CATEGORY ||
        category == TEAM_CATEGORY,
        "Invalid category type"
    );

    // Rest of the function...
}
```

##### Remediation

**SOLVED**: The **BlockDAG team** solved this issue as follows:

* Added explicit validation of category types at the start
* Maintains all existing category-specific validations
* Ensures only predefined categories can be created
* Keeps the error message clear and descriptive

##### Remediation Hash

V3

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Treasury Vesting |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/blockdag/treasury-vesting
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/blockdag/treasury-vesting

### Keywords for Search

`vulnerability`

