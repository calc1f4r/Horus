---
# Core Classification
protocol: Dumont
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38024
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Dumont-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-01] Missing sanity checks on `_lockedAmount`

### Overview

See description below for full details.

### Original Finding Content

In the initialize() function of the TaxBasedLocker contract, the contract is initialized with a specified amount of tokens to lock. According to NatSpec requirements, it is mandated that "The specified amount of tokens must be greater than zero." However, the current implementation lacks validation to ensure `_lockedAmount` is indeed greater than zero, as illustrated below:

```solidity
    function initialize(uint256 _lockedAmount) external onlyOwner {
        if (lockedAmount > 0) {
            revert AlreadyInitialized();
        }
        lockedAmount = _lockedAmount;
        uint256 balance = token.balanceOf(address(this));
        if (balance < lockedAmount) {
            token.safeTransferFrom(owner(), address(this), lockedAmount - balance);
        }
        startTime = block.timestamp;
        emit Initialized();
    }
```

Add a check to confirm that the specified amount of tokens is greater than zero to align with NatSpec requirements.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Dumont |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Dumont-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

