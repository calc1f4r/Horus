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
solodit_id: 50896
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

MISSING VALIDATOR EXISTENCE CHECK

### Overview

See description below for full details.

### Original Finding Content

##### Description

**SlashIndicator.slash** function updates the slash count for the misbehaving validator. If this validator meets the felony threshold, **SlashIndicator.slash** calls the felony method in **ValidatorSet** to forfeit rewards of the validator in the round and distribute them to other honest validators. And the validator is kicked out of the validator set immediately. However, at the beginning of slash function, validator existence is not checked.

Code Location
-------------

[SlashIndicator.sol#L66](https://github.com/coredao-org/core-genesis-contract/blob/audit-halborn/contracts/SlashIndicator.sol#L66)

```
  function slash(address validator) external onlyCoinbase onlyInit oncePerBlock onlyZeroGasPrice{
    Indicator memory indicator = indicators[validator];
    if (indicator.exist) {
      indicator.count++;
    } else {
      indicator.exist = true;
      indicator.count = 1;
      validators.push(validator);
    }
    indicator.height = block.number;
    if (indicator.count % felonyThreshold == 0) {
      indicator.count = 0;
      IValidatorSet(VALIDATOR_CONTRACT_ADDR).felony(validator, felonyRound, felonyDeposit);
    } else if (indicator.count % misdemeanorThreshold == 0) {
      IValidatorSet(VALIDATOR_CONTRACT_ADDR).misdemeanor(validator);
    }
    indicators[validator] = indicator;
    emit validatorSlashed(validator);
  }

```

##### Score

Impact: 3  
Likelihood: 2

##### Recommendation

**SOLVED**: The `CoreDAO team` solved the issue in commit [9145da64](https://github.com/coredao-org/core-genesis-contract/commit/9145da64739b424c53f4f02d57dd5b4c1abd3ee7) by adding the validator existence check.

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

