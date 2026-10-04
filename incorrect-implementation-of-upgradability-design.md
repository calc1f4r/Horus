---
# Core Classification
protocol: SynFutures Governance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61374
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/syn-futures-governance/499d4d21-2f10-4b73-9b64-d4ab0684f837/index.html
source_link: https://certificate.quantstamp.com/full/syn-futures-governance/499d4d21-2f10-4b73-9b64-d4ab0684f837/index.html
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
  - Shih-Hung Wang
  - Nikita Belenkov
  - Ruben Koch
  - Hytham Farah
---

## Vulnerability Title

Incorrect Implementation of Upgradability Design

### Overview


This report is about a bug in the code for a project called SynFuturesStakingVault. The bug affects the ability to upgrade the code in the future. The report suggests that the libraries used in the code are not the correct version and that the constructor function should be empty except for a specific call. It also mentions that an immutable variable is being used in a way that is not recommended. The report recommends fixing these issues to ensure that the code can be upgraded properly in the future.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `9377a450ce5d5c01e91233ae306fe14c44c7728a`.

**File(s) affected:**`SynFuturesStakingVault.sol`

**Description:** The upgradability mechanism is currently not implemented correctly:

*   The used libraries of `Ownable` and `ReentrancyGuard` are not the upgradeable version ([link](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#use-upgradeable-libraries)). This results in the constructor-set variables of the libraries to be unset when called through the proxy and also in potential storage collision in contract upgrades due to their sequential storage variables. The `SynFuturesStakingVault.initialize()` function should also call the `x_init()` function of the upgradeable libraries.
*   The constructor in an upgradeable contract should be empty except for a call to `_disableInitializers()` ([link](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#initializing_the_implementation_contract)), which currently makes the `initialize()` function in the implementation contract callable by anyone. 
*   An immutable variable, `token`, is set in the constructor, which is a discouraged pattern in implementation contracts ([link](https://docs.openzeppelin.com/upgrades-plugins/1.x/faq#why-cant-i-use-immutable-variables)). As immutable values are are stored in the bytecode, its value would be shared between all the proxies associated with the implementation contract, which might cause confusion. We recommend removing the `immutable` keyword and assigning the value in the `initialize()` function.

**Recommendation:** To have a functioning proxy setup that can go through contract upgrades, we recommend fixing the listed aspects.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | SynFutures Governance |
| Report Date | N/A |
| Finders | Shih-Hung Wang, Nikita Belenkov, Ruben Koch, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/syn-futures-governance/499d4d21-2f10-4b73-9b64-d4ab0684f837/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/syn-futures-governance/499d4d21-2f10-4b73-9b64-d4ab0684f837/index.html

### Keywords for Search

`vulnerability`

