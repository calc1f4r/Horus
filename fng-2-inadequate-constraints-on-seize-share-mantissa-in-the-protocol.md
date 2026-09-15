---
# Core Classification
protocol: Fungify
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62383
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-11-06-Fungify.md
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
finders_count: 1
finders:
  - Hexens
---

## Vulnerability Title

[FNG-2] Inadequate constraints on Seize Share Mantissa in the protocol

### Overview


This bug report is about a problem in the CToken.sol file of the protocol. The `protocolSeizeShareMantissa` parameter, which is used for comparing with Compound, can be changed by the admin without any restrictions. This could cause potential risks and imbalances in the protocol's functioning. There are two main concerns with this: overcapitalization and imbalance in collateral seizure. To fix this issue, an upper limit or a reasonable range should be set for the `protocolSeizeShareMantissa` parameter. This bug has been fixed.

### Original Finding Content

**Severity:** Medium

**Path:** CToken.sol#L878-L894

**Description:** In the current implementation of the protocol, the `protocolSeizeShareMantissa` parameter in comparison with Compound is not constant (`CTokenInterface.sol` line 113) and can be adjusted by the admin. This lack of constraints could potentially introduce risks and imbalances in the protocol's operation.

Allowing the admin to modify this parameter without appropriate restrictions might lead to the following concerns:

1. Risk of Overcapitalization: If an admin decides to set the `protocolSeizeShareMantissa` too high, it could lead to overcapitalization of the reserves, potentially causing inefficiencies in the allocation of assets and negatively impacting users' earnings.

2. Imbalance in Collateral Seizure: An excessively high `protocolSeizeShareMantissa` may incentivize users to seek liquidations, potentially leading to a sudden surge in collateral seized by the protocol. This could create an imbalance in the ecosystem and undermine stability.
```
    function _setProtocolSeizeShare(uint newProtocolSeizeShareMantissa) virtual override external returns (uint) {
        // Check caller is admin
        if (msg.sender != admin) {
            revert SetReserveFactorAdminCheck();
        }

        // Save current value for use in log
        uint oldProtocolSeizeShareMantissa = protocolSeizeShareMantissa;

        // Set liquidation incentive to new incentive
        protocolSeizeShareMantissa = newProtocolSeizeShareMantissa;

        // Emit event with old incentive, new incentive
        emit NewProtocolSeizeShare(oldProtocolSeizeShareMantissa, newProtocolSeizeShareMantissa);

        return NO_ERROR;
    }
```

**Remediation:**  Define an upper bound or a reasonable range for the `protocolSeizeShareMantissa` parameter to prevent it from being set too high or too low.

**Status:** Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Fungify |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-11-06-Fungify.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

