---
# Core Classification
protocol: Fyde May
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36405
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Fyde-security-review-May.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - yield

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-02] Functions cannot be called

### Overview


This bug report discusses an issue with the `YieldToken` implementation within the `YieldTokenFactory` constructor. The `YieldManager` contract inherits from the `YieldTokenFactory` contract and will be the owner of the `YieldToken` implementation. However, the `YieldToken` contract contains two functions that can only be called by the `owner` (i.e., the `YieldManager`), but there is no mechanism provided to do so. The recommendation is to transfer ownership of the `YieldToken` implementation to the `YieldManager.owner()`.

### Original Finding Content

**Severity**

**Impact:** Medium

**Likelihood:** High

**Description**

The `YieldToken` implementation is created within the `YieldTokenFactory` constructor:

```solidity
  constructor(address _fyde, address _relayer) {
    TOKEN_IMPLEMENTATION = address(new YieldToken(address(this), _fyde, _relayer));
  }
```

The `YieldManager` contract inherits from the `YieldTokenFactory` contract:

```solidity
  constructor() YieldTokenFactory(_fyde, _relayer) Ownable(msg.sender) ERC1967Proxy(_stratgies, "") {}
```

Therefore, the `YieldManager` will be the owner of the `YieldToken` implementation since it will be the `msg.sender` and thus the `owner` of the implementation:

```solidity
  constructor(address _yieldManager, address _fyde, address _relayer) Ownable(msg.sender) {
    yieldManager = _yieldManager;
    fyde = _fyde;
    relayer = _relayer;
    baseYieldToken = IYieldToken(address(this));
  }
```

The issue is that the `YieldToken` contract contains two functions that can only be called by the `owner` (i.e., the `YieldManager`):

```solidity
  function setYieldManager(address _yieldManager) public onlyOwner {
    yieldManager = _yieldManager;
  }

  function setRelayer(address _relayer) public onlyOwner {
    relayer = _relayer;
  }
```

However, the `YieldManager` cannot call these functions as there is no mechanism provided to do so.

**Recommendations**

Consider transferring ownership of the `YieldToken` implementation to the `YieldManager.owner()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Fyde May |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Fyde-security-review-May.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

