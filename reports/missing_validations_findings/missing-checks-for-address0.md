---
# Core Classification
protocol: Intent Assets
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52075
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/dappos/intent-assets
source_link: https://www.halborn.com/audits/dappos/intent-assets
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

Missing checks for address(0)

### Overview

See description below for full details.

### Original Finding Content

##### Description

In some of the smart contracts in-scope, values are assigned to address state variables without checking whether the assigned address is the zero address (`address(0)`). This oversight can lead to unintended behavior and potential security vulnerabilities in the contract.

This behavior was identified in multiple (**22**) instances. The following is a non-exhaustive list:

`- contracts/checker/WearChecker.sol`

```
	        intentToken = _intentToken;
```

  

`- contracts/core/pools/cachePool/CachePool.sol`

```
	        intentToken = _intentToken;
```

  

`- contracts/core/pools/cachePool/CachePool.sol`

```
	        wearChecker = _wearChecker;
```

  

`- contracts/core/pools/cachePool/CachePool.sol`

```
	        intentTokenMinting = _intentTokenMinting;
```

  

`- contracts/core/pools/cachePool/CachePool.sol`

```
	        plugins[_executionPlugin] = isEnabled;
```

`- contracts/core/pools/mainPool/MainPool.sol`

```
	        intentToken = _intentToken;
```

`- contracts/core/pools/mainPool/MainPoolConfiguration.sol`

```
	        intentToken = _intentToken;
```

##### Score

Impact:   
Likelihood:

##### Recommendation

To prevent unintended behavior and potential security vulnerabilities, it is essential to include checks for `address(0)` when assigning values to address state variables. This can be achieved by adding a simple check to ensure that the assigned address is not equal to `address(0)` before proceeding with the assignment.

##### Remediation

**ACKNOWLEDGED:** The **dappOS team** acknowledged this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Intent Assets |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/dappos/intent-assets
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/dappos/intent-assets

### Keywords for Search

`vulnerability`

