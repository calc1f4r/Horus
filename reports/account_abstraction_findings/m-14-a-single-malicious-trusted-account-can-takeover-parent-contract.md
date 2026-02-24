---
# Core Classification
protocol: Sandclock
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1292
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-sandclock-contest
source_link: https://code4rena.com/reports/2022-01-sandclock
github_link: https://github.com/code-423n4/2022-01-sandclock-findings/issues/132

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
  - dexes
  - cdp
  - yield
  - yield_aggregator
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - leastwood
  - hickuphh3
---

## Vulnerability Title

[M-14] A Single Malicious Trusted Account Can Takeover Parent Contract

### Overview


This bug report is about a vulnerability in the `requiresTrust()` modifier in the strategy, vault and factory contracts. This modifier is used to prevent unauthorised accounts from calling restricted functions. Accounts can be added and removed from the `isTrusted` mapping by calling `setIsTrusted()`. However, if any single account has its private keys compromised or decides to become malicious, they can remove all other trusted accounts from the mapping. As a result, they are effectively able to take over the trusted group that controls all restricted functions in the parent contract. 

To mitigate this vulnerability, it is recommended to utilise Rari Capital's updated `Auth.sol` contract which gives the `owner` account authority over its underlying trusted accounts. This prevents any single account from taking over the trusted group. The `owner` account should point to a multisig managed by the Sandclock team or by a community DAO. The vulnerability was identified through manual code review.

### Original Finding Content

_Submitted by leastwood, also found by hickuphh3_

The `requiresTrust()` modifier is used on the strategy, vault and factory contracts to prevent unauthorised accounts from calling restricted functions. Once an account is considered trusted, they are allowed to add and remove accounts by calling `setIsTrusted()` as they see fit.

However, if any single account has its private keys compromised or decides to become malicious on their own, they can remove all other trusted accounts from the `isTrusted` mapping. As a result, they are effectively able to take over the trusted group that controls all restricted functions in the parent contract.

#### Proof of Concept
```solidity
abstract contract Trust {
    event UserTrustUpdated(address indexed user, bool trusted);

    mapping(address => bool) public isTrusted;

    constructor(address initialUser) {
        isTrusted[initialUser] = true;

        emit UserTrustUpdated(initialUser, true);
    }

    function setIsTrusted(address user, bool trusted) public virtual requiresTrust {
        isTrusted[user] = trusted;

        emit UserTrustUpdated(user, trusted);
    }

    modifier requiresTrust() {
        require(isTrusted[msg.sender], "UNTRUSTED");

        _;
    }
}
```

#### Recommended Mitigation Steps

Consider utilising Rari Capital's updated `Auth.sol` contract found [here](https://github.com/Rari-Capital/solmate/blob/main/src/auth/Auth.sol). This updated contract gives the `owner` account authority over its underlying trusted accounts, preventing any single account from taking over the trusted group. The `owner` account should point to a multisig managed by the Sandclock team or by a community DAO.

**[naps62 (Sandclock) confirmed](https://github.com/code-423n4/2022-01-sandclock-findings/issues/132)**

**[dmvt (judge) changed severity and commented](https://github.com/code-423n4/2022-01-sandclock-findings/issues/132#issuecomment-1024609919):**
 > If this were to happen, funds would definitely be lost. Accordingly, this is a medium risk issue.
> 
> `
> 2 — Med: Assets not at direct risk, but the function of the protocol or its availability could be impacted, or leak value with a hypothetical attack path with stated assumptions, but external requirements.
> `





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sandclock |
| Report Date | N/A |
| Finders | leastwood, hickuphh3 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-sandclock
- **GitHub**: https://github.com/code-423n4/2022-01-sandclock-findings/issues/132
- **Contest**: https://code4rena.com/contests/2022-01-sandclock-contest

### Keywords for Search

`vulnerability`

