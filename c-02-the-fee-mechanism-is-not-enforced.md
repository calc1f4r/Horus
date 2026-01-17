---
# Core Classification
protocol: Pino
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27250
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-09-01-Pino.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov
---

## Vulnerability Title

[C-02] The fee mechanism is not enforced

### Overview


This bug report is about a fee mechanism in the codebase which is allowing users to bypass fees. The impact of this is high as the protocol can lose potential yield in the form of fees, and the likelihood is also high as users can craft such transactions in a permissionless way. The problem is that the value of the fee is controlled by the user through the `_proxyFeeInWei` argument, meaning he can always send 0 value to it so he doesn't pay any fees. The recommendation is to rearchitecture the fees approach so that a fee can be enforced on users, for example by using a sensible admin set value for it.

### Original Finding Content

**Severity**

**Impact:**
High, as the protocol can lose potential yield in the form of fees

**Likelihood:**
High, as users can craft such transactions in a permissionless way

**Description**

The codebase is using a fee mechanism where the users pay a fee for using some functionality. An example where this is done is the `Compound::depositETHV2` method, as we can see here:

```solidity
    function depositETHV2(address _recipient, uint256 _proxyFeeInWei) external payable nonETHReuse {
        address _cEther = address(cEther);

        ICEther(_cEther).mint{value: msg.value - _proxyFeeInWei}();
    ....
    ....
```

The problem with this approach is that the value of the fee is controlled by the user through the `_proxyFeeInWei` argument, meaning he can always send 0 value to it so he doesn't pay any fees.

**Recommendations**

Rearchitecture the fees approach so that a fee can be enforced on users, for example by using a sensible admin set value for it.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Pino |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-09-01-Pino.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

