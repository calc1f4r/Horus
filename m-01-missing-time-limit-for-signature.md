---
# Core Classification
protocol: Rwa
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48931
audit_firm: Kann
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Kann Audits/2025-01-19-RWA.md
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
  - Kann Audits
---

## Vulnerability Title

[M-01] Missing time limit for signature

### Overview


This bug report discusses an issue with financial contracts that can lead to unfair borrowing conditions or outdated agreements. The problem is that signatures on these contracts can be valid indefinitely, even if market conditions change. This can result in contracts that are no longer fair for the contract owner. To solve this issue, the report suggests adding a time limit to signatures, so that they become invalid after a certain period. The recommended solution involves adding an expiry date to the signature, and checking if it is still valid before executing the contract. This will ensure that the contract can only be executed within the intended window of time.

### Original Finding Content

**Description**

Some actions in financial contracts are time-sensitive, and allowing a signature to be valid indefinitely could break expected business rules. For instance, if the contract terms change or the collateral value fluctuates, an old signature might lead to unfair borrowing conditions or outdated agreements.


Example: A user signs a borrowing agreement for certain collateral amounts and borrowing amounts today. Later, the market conditions change, and collateral values drop or borrowing values gets too high , making the original agreement unfair for the contract owner. By adding a time limit (e.g., valid for 1 hour), the signature would become invalid once the time expires, ensuring that the agreement can only be executed within the intended window

**Recommendations**

```solidity
bytes32 _borrowHash = keccak256(
    abi.encode(
        collaterals,
        borrows,
        collateralAmounts,
        borrowsAmounts,
        msg.sender,
        nonceOf[msg.sender],
        deadline // Add expiry
    )
);

// Check if the signature is expired
if (block.timestamp > deadline) {
    revert SignatureExpired();
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Kann |
| Protocol | Rwa |
| Report Date | N/A |
| Finders | Kann Audits |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Kann Audits/2025-01-19-RWA.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

