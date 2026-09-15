---
# Core Classification
protocol: Yield
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 4078
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-05-yield-contest
source_link: https://code4rena.com/reports/2021-05-yield
github_link: https://github.com/code-423n4/2021-05-yield-findings/issues/5

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-02] auth collision possible

### Overview


This bug report is about a vulnerability in the auth mechanism of AccessControl.sol, a smart contract. The vulnerability is that the auth mechanism uses function selectors (msg.sig) as a (unique) role definition. It also allows the code to be extended through the _moduleCall function. If an attacker is able to add a new module with an innocent-looking function, with a signature of 0x00000000, they can gain root authorization. This is because the ROOT constant is also 0x00000000. This is possible because it is easy to generate function names for any signature value, as it is only 4 bytes. The recommended mitigation steps are to not allow third parties to define or suggest new modules, and to double check the function signatures of new functions of a new module for collisions.

### Original Finding Content


The auth mechanism of `AccessControl.sol` uses function selectors `(msg.sig)` as a `(unique)` role definition. Also the `_moduleCall` allows the code to be extended.

Suppose an attacker wants to add the innocent-looking function "`left_branch_block(uint32)` "in a new module. Suppose this module is added via `_moduleCall`, and the attacker gets authorization for the innocent function.

This function happens to have a signature of 0x00000000, which is equal to the root authorization. In this way, the attacker could get authorization for the entire project.

Note: it's pretty straightforward to generate function names for any signature value; you can just brute force it because it's only 4 bytes.

Recommend not allowing third parties to define or suggest new modules and double-checking the function signatures of new functions of a new module for collisions.

**[albertocuestacanada (Yield) confirmed](https://github.com/code-423n4/2021-05-yield-findings/issues/5#issuecomment-852035261):**
 > The execution of any `auth` function will only happen after a governance process or by a contract that has gone through a thorough review and governance process.
>
> We are aware that new modules can have complete control of the Ladle, and for that reason, the addition of new modules would be subject to the highest level of scrutiny. Checking for signature collisions is a good item to add to that process.
>
> In addition to that, I would implement two changes in `AccessControl.sol` so that giving ROOT access is explicit.

```solidity
    function grantRole(bytes4 role, address account) external virtual admin(role) {
        require(role != ROOT, "Not ROOT role");
        _grantRole(role, account);
    }
>
    function grantRoot(address account) external virtual admin(ROOT) {
        _grantRole(ROOT, account);
    }
```
> However, given that this could be exploited only through a malicious governance exploit, I would reduce the risk to "Low."

**[albertocuestacanada (Yield) acknowledged](https://github.com/code-423n4/2021-05-yield-findings/issues/5#issuecomment-864995915):**
 > After further thinking, instead of preventing auth collisions in the smart contracts, we will add CI checks for this specific issue instead.



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Yield |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-05-yield
- **GitHub**: https://github.com/code-423n4/2021-05-yield-findings/issues/5
- **Contest**: https://code4rena.com/contests/2021-05-yield-contest

### Keywords for Search

`vulnerability`

