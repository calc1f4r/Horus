---
# Core Classification
protocol: Rover Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51550
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/hydrogen-labs/hydrogen-labs-rover-protocol
source_link: https://www.halborn.com/audits/hydrogen-labs/hydrogen-labs-rover-protocol
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

Missing input validation when assigning address to state variable

### Overview

See description below for full details.

### Original Finding Content

##### Description

The assessment of the smart contracts in-scope revealed instances where input validation is missing when assigning an address to a state variable. Failing to validate user-provided addresses can lead to unintended consequences and potential security vulnerabilities.

**- contracts/RoverBtcToken/RovBtcToken.sol [Line: 39]**

```
	        roleManager = _roleManager;
```

  

**- contracts/StakeManager/StakeManager.sol [Line: 53]**

```
	        roleManager = _roleManager;
```

  

**- contracts/StakeManager/StakeManager.sol [Line: 54]**

```
	        rovBTC = _rovBTC;
```

  

When an address is not properly validated, it may be assigned an incorrect or malicious value, such as the zero address (`address(0)`). This can result in broken contract logic, lost funds, or other unintended behavior.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:C (0.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:C)

##### Recommendation

To prevent unintended behavior and potential security vulnerabilities, it is essential to include checks for `address(0)` when assigning values to address state variables. This can be achieved by adding a simple check to ensure that the assigned address is not equal to `address(0)` before proceeding with the assignment.

  

### Remediation Plan

**SOLVED**: The **Hydrogen Labs team** has solved this issue as recommended.

##### Remediation Hash

<https://github.com/Hydrogen-Labs/rover-contracts/commit/b31502c225427259c6786f6c12a73abcd5bbe3ef>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Rover Protocol |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/hydrogen-labs/hydrogen-labs-rover-protocol
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/hydrogen-labs/hydrogen-labs-rover-protocol

### Keywords for Search

`vulnerability`

