---
# Core Classification
protocol: Chainport
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58456
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-03-Chainport.md
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
  - zokyo
---

## Vulnerability Title

Missing Transaction Reverts for Zero Address Checks.

### Overview

See description below for full details.

### Original Finding Content

**Description**

ChainportSideBridge: _setTokenProxyAdmin, _setTokenLogic.
The functions_setTokenProxyAdmin() and_setTokenLogic() contain checks to prevent setting their respective addresses to the zero address. However, these checks are currently silent that is, if a zero address is provided as an argument, the function will simply not update the state, but the transaction will not revert and will appear successful. This behavior might lead to a misunderstanding, where calling functions believe that they have successfully set a new address when, in fact, no update has occurred due to providing an invalid zero address. Ensuring that transactions revert with an informative error message when critical checks fail is a fundamental security best practice in smart contract development. If the function's intended behavior is to disallow a zero address, it should be enforced with a revert statement that clearly indicates why the transaction failed. This ensures transparency and helps prevent potential errors during contract interactions.

**Recommendation**

Update the functions to explicitly revert if the input argument is the zero address.

**Re-audit comment**

Verified.

Post audit.
The team verified that this behavior is intentional as the initialization flow is made to cross the roles of maintainer and congress authorities, and there is an initialization function so that initially, the maintainer can do it but may lack an address, so it is possible to set only one address and leave the other one zero.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Chainport |
| Report Date | N/A |
| Finders | zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-03-Chainport.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

