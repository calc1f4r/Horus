---
# Core Classification
protocol: LoopFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33359
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-05-loop
source_link: https://code4rena.com/reports/2024-05-loop
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
finders_count: 0
finders:
---

## Vulnerability Title

[05] Missing input validation for `_percentage` in `PrelaunchPoints::_claim`

### Overview

See description below for full details.

### Original Finding Content


`PrelaunchPoints::_claim` does not perform input validation on `_percentage`. Transaction flow will continue and only fails much later in the execution. 

### Impact

Users calling `PrelaunchPoints::claim` or `PrelaunchPoints::claimAndStake` and accidentally inputting `0` for `_percentage` will waste more gas, as the transaction will fail much later in the execution.

### Recommended Mitigation Steps

Perform input validation on `_percentage` as follows:

```diff

    function _claim(address _token, address _receiver, uint8 _percentage, Exchange _exchange, bytes calldata _data)
        internal
        returns (uint256 claimedAmount)
    {
        uint256 userStake = balances[msg.sender][_token];
        if (userStake == 0) {
            revert NothingToClaim();
        }

+       require(_percentage > 0 && _percentage <= 100, "Invalid percentage value");

        ...


    }
```



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | LoopFi |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-05-loop
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-05-loop

### Keywords for Search

`vulnerability`

