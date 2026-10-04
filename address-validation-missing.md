---
# Core Classification
protocol: MonoX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50183
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/monox/monox-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/monox/monox-smart-contract-security-assessment
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
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

ADDRESS VALIDATION MISSING

### Overview

See description below for full details.

### Original Finding Content

##### Description

Address validation is missing in multiple functions in contracts `Monoswap.sol` and `MonoXPool.sol`. This may result with users irreversibly locking their tokens when incorrect address is provided.

Code Location
-------------

#### Monoswap.sol

```
function mint (address account, uint256 id, uint256 amount) internal {
    monoXPool.mint(account, id, amount);
}

function burn (address account, uint256 id, uint256 amount) internal {
    monoXPool.burn(account, id, amount);
}

```

#### MonoXPool.sol

```
constructor (address _WETH) {
      WETH = _WETH;
}

```

#### MonoXPool.sol

```
function mint (address account, uint256 id, uint256 amount) public onlyOwner {
    totalSupply[id]=totalSupply[id].add(amount);
    _mint(account, id, amount, "");
}

function burn (address account, uint256 id, uint256 amount) public onlyOwner {
    totalSupply[id]=totalSupply[id].sub(amount);
    _burn(account, id, amount);
}

```

##### Score

Impact: 2  
Likelihood: 2

##### Recommendation

**PARTIALLY SOLVED**: Vulnerable function calls in `Monoswap.sol` have been removed but address validation is missing in `MonoXPool.sol`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | MonoX |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/monox/monox-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/monox/monox-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

