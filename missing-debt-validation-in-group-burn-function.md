---
# Core Classification
protocol: Radius Technology EVMAuth
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62868
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-10-radiustechnology-evmauth-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-10-radiustechnology-evmauth-securityreview.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4.5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Quan Nguyen Trail of Bits PUBLIC
---

## Vulnerability Title

Missing debt validation in group burn function

### Overview


The `_burnGroupBalances` function in the code has a bug that can cause a denial of service. This means that it can prevent users from accessing their tokens. The function does not check if the burning process was successful when dealing with expired tokens. This can result in incorrect tracking of token balances and group data. An attacker can exploit this by having a mix of valid and expired tokens and attempting to burn them. The recommended solution is to add a check at the end of the function to ensure the burn was completed successfully. In the long term, comprehensive tests should be implemented and the burn logic should be redesigned to properly account for expired tokens.

### Original Finding Content

## Denial of Service: _burnGroupBalances Function

**Diﬃculty:** Medium  
**Type:** Denial of Service  

## Description
The `_burnGroupBalances` function fails to validate that the burn operation completes successfully when expired tokens are present, potentially creating inconsistencies between ERC1155 balance tracking and group array tracking. The function skips over expired token groups during burning but does not verify that the burn was completed successfully.

The `_burnGroupBalances` function iterates through the account’s token groups in FIFO order to burn the requested amount. However, it skips over expired token groups without accounting for them in the burn calculation. When the loop completes, there is no verification that the debt variable has reached zero, meaning that the burn may be incomplete.

```solidity
function _burnGroupBalances(address account, uint256 id, uint256 amount) internal {
    Group[] storage groups = _group[account][id];
    uint256 _now = block.timestamp;
    uint256 debt = amount;
    uint256 i = 0;
    while (i < groups.length && debt > 0) {
        if (groups[i].expiresAt <= _now) {
            i++;
            continue;
        }
        if (groups[i].balance > debt) {
            // Burn partial token group
            groups[i].balance -= debt;
            debt = 0;
        } else {
            // Burn entire token group
            debt -= groups[i].balance;
            groups[i].balance = 0;
        }
        i++;
    }
}
```

*Figure 4.1: Missing debt validation in the `_burnGroupBalances` function*

## Exploit Scenario
Alice has five authentication tokens distributed across two groups:
- **Group A:** Three tokens (expires at t=100, current time t=50)
- **Group B:** Two tokens (expires at t=200, current time t=50)

Time advances to t=150, making Group A expired. The token burner attempts to burn four of Alice’s tokens. The ERC1155 balance tracking correctly updates to show that Alice has one token remaining. However, the group burn processes only two non-expired tokens from Group B, leaving the burn incomplete. The group arrays now contain inconsistent data, where Alice’s group array shows fewer tokens than her ERC1155 balance.

## Recommendations
- **Short term:** Add a check at the end of the `_burnGroupBalances` function to verify that debt equals zero, ensuring the burn was completed successfully.
- **Long term:** Implement comprehensive unit tests that cover burn scenarios with mixed valid and expired tokens, and consider redesigning the burn logic to properly account for expired tokens during the burn process.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4.5/5 |
| Audit Firm | TrailOfBits |
| Protocol | Radius Technology EVMAuth |
| Report Date | N/A |
| Finders | Quan Nguyen Trail of Bits PUBLIC |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2025-10-radiustechnology-evmauth-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2025-10-radiustechnology-evmauth-securityreview.pdf

### Keywords for Search

`vulnerability`

