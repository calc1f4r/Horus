---
# Core Classification
protocol: Vesync
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44807
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-23-VeSync.md
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
  - Zokyo
---

## Vulnerability Title

Missing checks for address(0) in setter methods

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**: Acknowledged

**Description**

In contract Voting.sol, the following methods are missing zero-address checks.

function initialize(address[] memory _tokens, address _minter) external;
This method does not check if _minter is a zero-address or not.

function setGovernor(address _governor); 
For setGoverner(), there is no check for zero-address for _governer parameter and the method checks that only the governor should be able to set a new governor. So, suppose accidentally governor is set as address(0). In that case, it will be impossible to set the governor again; all the methods callable only by the governor can not be called anymore.

function setEmergencyCouncil(address _council);
The above case of the setGovernor method applies to the setEmergencyCouncil method as well.

In contract VotingEscrow.sol, the following methods are missing zero-address checks:

function setTeam(address _team) external;
For setTeam(), there is no check for zero-address for _teamparameter and the method checks that only the team should be able to set a new team. So, suppose accidentally team is set as address(0). In that case, it will be impossible to set the team again; all the methods callable only by the team can not be called anymore.


function setArtProxy(address _proxy) external;
This method does not check if _proxy is zero-address or not.


In contract Voting.sol, the following methods are missing zero-address checks:

function setTeam(address _team) external;
There is no check for zero-address for _team parameter. 



**Recommendation**:

Add checks to revert in case zero-address parameters are passed in the above-mentioned scenarios.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vesync |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-23-VeSync.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

