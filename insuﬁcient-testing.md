---
# Core Classification
protocol: Advanced Blockchain
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17653
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchain.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchain.pdf
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
finders_count: 2
finders:
  - Natalie Chin
  - Michael Colburn
---

## Vulnerability Title

Insu�ﬁcient testing

### Overview

See description below for full details.

### Original Finding Content

## Type: Undefined Behavior
## Target: 
- polkastrategies/truffle-config.js
- ForceDAO/contracts/truffle-config.js

## Difficulty: Low

## Description
The repositories under review lack appropriate testing, which increases the likelihood of errors in the development process and makes the code more difficult to review.

The polkastrategies repository manages the bookkeeping of users’ principals and the rewards they earn on deposits made into other applications. This portion of the code must be implemented correctly, as a bug would allow an attacker to steal funds from the contract by withdrawing excess funds or undeserved rewards. However, despite the importance of the withdrawal, deposit, and reward flows, the tests of those flows fail:

- 0 passing (1s)
- 9 failing

```
9)  Contract: SushiSLP
    should test yUSD-WETH SLP
    should test positive scenario:
    Error: Invalid address passed to SushiETHSLP.at(): undefined
        at Function.at
        (~/.nvm/versions/node/v12.18.3/lib/node_modules/truffle/build/webpack:/packages/contract/lib/contract/constructorMethods.js:67:1)
        at execute (test/strategies/sushiSLP.ts:53:40)
        at Context.<anonymous> (test/strategies/sushiSLP.ts:128:19)
        at processImmediate (internal/timers.js:456:21)
```

*Figure 5.1: The terminal output when polkastrategies tests are run.*

The EQLC codebase builds off of an MKR-like stablecoin, requiring users to lock in funds as collateral to mint EQLC. Running this command during the audit resulted in compilation errors.

The ForceDAO repository contains tests for the setter functions and time lock. However, the contracts lack tests for the core deposit-withdrawal flow.

The Cyclical repository contains some tests; however, the deployment scripts fail and throw errors.

## Exploit Scenario
The development team modifies the implementation of one of the contracts, introducing a security issue that remains when the contracts are deployed.

## Recommendations
- **Short term:** Ensure that the unit tests cover all public functions at least once, as well as all known corner cases.
- **Long term:** Integrate coverage analysis tools into the development process and regularly review the coverage.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Advanced Blockchain |
| Report Date | N/A |
| Finders | Natalie Chin, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchain.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/AdvancedBlockchain.pdf

### Keywords for Search

`vulnerability`

