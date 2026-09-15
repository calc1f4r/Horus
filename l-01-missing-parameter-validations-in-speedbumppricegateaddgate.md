---
# Core Classification
protocol: FactoryDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42557
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-05-factorydao
source_link: https://code4rena.com/reports/2022-05-factorydao
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - rwa
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-01] Missing parameter validations in `SpeedBumpPriceGate#addGate`

### Overview

See description below for full details.

### Original Finding Content


Callers of `addGate` can create price gates with a zero price floor (allowing users to claim free tokens), and zero `priceIncreaseDenominator` (causing price calculation to revert with a divide by zero error).

[`SpeedBumpPriceGate#addGate`](https://github.com/code-423n4/2022-05-factorydao/blob/e22a562c01c533b8765229387894cc0cb9bed116/contracts/SpeedBumpPriceGate.sol#L36-L45)

```solidity

    function addGate(uint priceFloor, uint priceDecay, uint priceIncrease, uint priceIncreaseDenominator, address beneficiary) external {
        // prefix operator increments then evaluates
        Gate storage gate = gates[++numGates];
        gate.priceFloor = priceFloor;
        gate.decayFactor = priceDecay;
        gate.priceIncreaseFactor = priceIncrease;
        gate.priceIncreaseDenominator = priceIncreaseDenominator;
        gate.beneficiary = beneficiary;
    }
```

Suggestion: Validate that `priceFloor` and `priceIncreaseDenominator` are nonzero.

```solidity

    function addGate(uint priceFloor, uint priceDecay, uint priceIncrease, uint priceIncreaseDenominator, address beneficiary) external {
        require(priceFloor != 0, "Price floor must be nonzero");
        require(priceIncreaseDenominator != 0, "Denominator must be nonzero");
        // prefix operator increments then evaluates
        Gate storage gate = gates[++numGates];
        gate.priceFloor = priceFloor;
        gate.decayFactor = priceDecay;
        gate.priceIncreaseFactor = priceIncrease;
        gate.priceIncreaseDenominator = priceIncreaseDenominator;
        gate.beneficiary = beneficiary;
    }
```



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | FactoryDAO |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-factorydao
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-05-factorydao

### Keywords for Search

`vulnerability`

