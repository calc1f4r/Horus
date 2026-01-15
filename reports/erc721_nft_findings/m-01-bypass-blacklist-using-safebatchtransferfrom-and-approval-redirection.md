---
# Core Classification
protocol: Sofamon-August
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41368
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Sofamon-security-review-August.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] Bypass blacklist using `safeBatchTransferFrom` and approval redirection

### Overview


This bug report discusses a medium severity issue in a contract that has a blacklist feature to prevent certain addresses from transferring tokens. The problem is that while the `safeTransferFrom` function checks both the sender and the recipient against the blacklist, the `safeBatchTransferFrom` function only checks the recipient. This allows blacklisted users to bypass the restriction and transfer their funds using `safeBatchTransferFrom`. Additionally, blacklisted users can also redirect their approvals to another address since there is no blacklist check on the `msg.sender` in the approval functions. 

To fix these issues, the report recommends implementing blacklist checks for both the sender and the recipient in the `safeBatchTransferFrom` function. It also suggests adding blacklist checks for the `msg.sender` functions to prevent blacklisted users from redirecting their approvals. The proposed changes involve adding a few lines of code to the existing functions. These changes will ensure that the blacklist feature works as intended and prevents unauthorized transfers of tokens.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The contract includes a blacklist feature intended to prevent certain addresses from transferring tokens. While the `safeTransferFrom` function checks both the sender and the recipient against the blacklist, the `safeBatchTransferFrom` function only checks the recipient. This allows blacklisted users to bypass the restriction and transfer their funds using `safeBatchTransferFrom`. Additionally, blacklisted users can redirect their approvals to another address since there is no blacklist check on the `msg.sender` in the approval functions.

### Vulnerable Code

```solidity
function safeTransferFrom(address from, address to, uint256 id, uint256 amount, bytes calldata data) public override NoBlacklist(to) NoBlacklist(from) {
    super.safeTransferFrom(from, to, id, amount, data);
}

function safeBatchTransferFrom(
    address from,
    address to,
    uint256[] calldata ids,
    uint256[] calldata amounts,
    bytes calldata data
)
    public
    override
    NoBlacklist(to)
{
    super.safeBatchTransferFrom(from, to, ids, amounts, data);
}
```

## Recommendations

To address these issues, ensure that both the sender and the recipient are checked against the blacklist in the `safeBatchTransferFrom` function. Additionally, implement blacklist checks for the `msg.sender` functions to prevent blacklisted users from redirecting their approvals.

```diff
-    function safeTransferFrom(address from, address to, uint256 id, uint256 amount, bytes calldata data) public override NoBlacklist(to) NoBlacklist(from) {
+    function safeTransferFrom(address from, address to, uint256 id, uint256 amount, bytes calldata data) public override NoBlacklist(to) NoBlacklist(from) NoBlacklist(msg.sender) {
        super.safeTransferFrom(from, to, id, amount, data);
    }

    function safeBatchTransferFrom(
        address from,
        address to,
        uint256[] calldata ids,
        uint256[] calldata amounts,
        bytes calldata data
    )
        public
        override
        NoBlacklist(to)
+       NoBlacklist(from)
+       NoBlacklist(msg.sender)
    {
        super.safeBatchTransferFrom(from, to, ids, amounts, data);
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Sofamon-August |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Sofamon-security-review-August.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

