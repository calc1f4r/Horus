---
# Core Classification
protocol: Genesis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50911
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/coredao/genesis-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/coredao/genesis-smart-contract-security-assessment
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

MISSING ADDRESS CHECK ON THE FEEADDR AND CONSENSUSADDR

### Overview

See description below for full details.

### Original Finding Content

##### Description

Both of the variables are missing address check. Every address should be validated and checked that it is different from zero.

Code Location
-------------

[CandidateHub.sol#L213](https://github.com/coredao-org/core-genesis-contract/blob/audit-halborn/contracts/CandidateHub.sol#L213)

```
  function register(address consensusAddr, address payable feeAddr, uint32 commissionThousandths)
    external payable
    onlyInit
  {
    require(operateMap[msg.sender] == 0, "candidate already exists");
    require(int256(msg.value) >= requiredMargin, "deposit is not enough");
    require(commissionThousandths > 0 && commissionThousandths < 1000, "commissionThousandths should in range (0, 1000)");
    require(consensusMap[consensusAddr] == 0, "consensus already exists");
    require(!isContract(consensusAddr), "contract is not allowed to be consensus address");
    require(!isContract(feeAddr), "contract is not allowed to be fee address");
    // check jail status
    require(jailMap[msg.sender] < roundTag, "it is in jail");

    uint status = SET_CANDIDATE;
    candidateSet.push(Candidate(msg.sender, consensusAddr, feeAddr, commissionThousandths, int256(msg.value), status, roundTag, commissionThousandths));
    uint256 index = candidateSet.length;
    operateMap[msg.sender] = index;
    consensusMap[consensusAddr] = index;

    emit registered(msg.sender, consensusAddr, feeAddr, commissionThousandths, int256(msg.value));
  }

```

##### Score

Impact: 2  
Likelihood: 2

##### Recommendation

**SOLVED**: The `CoreDAO team` solved the issue in commit [b51c87f8](https://github.com/coredao-org/core-genesis-contract/commit/b51c87f842bcfcb817f17ffd277f0063eb4b85b0) by adding validation on addresses.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Genesis |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/coredao/genesis-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/coredao/genesis-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

