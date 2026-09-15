---
# Core Classification
protocol: Reserve
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16028
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-reserve-contest
source_link: https://code4rena.com/reports/2023-01-reserve
github_link: https://github.com/code-423n4/2023-01-reserve-findings/issues/211

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

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - launchpad
  - privacy

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - fs0c
---

## Vulnerability Title

[M-18] If name is changed then the domain separator would be wrong

### Overview


This bug report is about a vulnerability in the StRSR.sol code which is part of the Reserve Protocol. The vulnerability occurs when the name used in the init function call is changed by governance using the setName function. The problem is that the domain separator is still calculated using the old name, which should not be the case. The impact of this is that permit transactions and vote delegation would be reverted if the domain separator is wrong. The recommended solution is to update the domain separator while changing the name in the setName function.

### Original Finding Content


<https://github.com/reserve-protocol/protocol/blob/df7ecadc2bae74244ace5e8b39e94bc992903158/contracts/p1/StRSR.sol#L803><br>
<https://github.com/reserve-protocol/protocol/blob/df7ecadc2bae74244ace5e8b39e94bc992903158/contracts/p1/StRSR.sol#L791>

In `StRSR.sol` the `_domainSeparatorV4` is calculated using the EIP-721 standard, which uses the `name` and `version` that are passed in the init at the function call `__EIP712_init(name, "1");`

Now, governance can change this `name` anytime using the following function:

```solidity
function setName(string calldata name_) external governance {
        name = name_;
    }
```

After that call the domain separator would still be calculated using the old name, which shouldn’t be the case.

### Impact

The permit transactions and vote delegation would be reverted if the domain separator is wrong.

### Recommendation

While changing the name in setName function, update the domain separator.

**[tbrent (Reserve) confirmed](https://github.com/code-423n4/2023-01-reserve-findings/issues/211)**

**[tbrent (Reserve) mitigated](https://github.com/code-423n4/2023-02-reserve-mitigation-contest#mitigations-to-be-reviewed):**
 > This PR removes the ability to change StRSR token's name and symbol: [reserve-protocol/protocol#614](https://github.com/reserve-protocol/protocol/pull/614)

**Status:** Mitigation confirmed. Full details in reports from [HollaDieWaldfee](https://github.com/code-423n4/2023-02-reserve-mitigation-contest-findings/issues/7), [0xA5DF](https://github.com/code-423n4/2023-02-reserve-mitigation-contest-findings/issues/62), and [AkshaySrivastav](https://github.com/code-423n4/2023-02-reserve-mitigation-contest-findings/issues/42).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Reserve |
| Report Date | N/A |
| Finders | fs0c |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-reserve
- **GitHub**: https://github.com/code-423n4/2023-01-reserve-findings/issues/211
- **Contest**: https://code4rena.com/contests/2023-01-reserve-contest

### Keywords for Search

`vulnerability`

