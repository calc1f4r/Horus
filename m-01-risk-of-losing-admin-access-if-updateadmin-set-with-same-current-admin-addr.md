---
# Core Classification
protocol: Stader Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20174
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-06-stader
source_link: https://code4rena.com/reports/2023-06-stader
github_link: https://github.com/code-423n4/2022-06-stader-findings/issues/390

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
finders_count: 3
finders:
  - ksk2345
  - ChrisTina
  - NoamYakov
---

## Vulnerability Title

[M-01] Risk of losing admin access if `updateAdmin`` set with same current admin address

### Overview


This bug report is about the possibility of loss of protocol admin access to the StaderConfig.sol contract, if the `updateAdmin()` function is set with the same current admin address by mistake. It was possible due to the lack of a check for `oldAdmin != _admin` in the `updateAdmin()` function. This bug could have been exploited to transfer the `DEFAULT_ADMIN_ROLE` role to another address, thus losing admin control of the contract.

The bug was reported with a proof of concept using the Brownie python automation framework. It was then discussed by the judge and wardens on the issue thread to determine the severity of the bug. The severity was decreased from High to Medium. The Stader team confirmed the bug and fixed it in the code. 

The recommended mitigation step is to add a check for `oldAdmin != _admin` in the `updateAdmin()` function to ensure that the same admin address is not used twice. This will ensure that the `DEFAULT_ADMIN_ROLE` role is not transferred to another address, thus preserving the admin control of the contract.

### Original Finding Content


Current admin will lose `DEFAULT_ADMIN_ROLE` role if `updateAdmin` issued with same address.

There is a possibility of loss of protocol admin access to the critical `StaderConfig.sol` contract, if `updateAdmin()` is set with same current admin address by mistake.

### Proof of Concept

Contract : StaderConfig.sol.<br>
Function : function `updateAdmin(address _admin)`.

Using Brownie python automation framework commands in below examples:

*   Step #1 After initialization, admin-A is the admin which has the `DEFAULT_ADMIN_ROLE`.

*   Step #2 update new Admin:<br>
    `StaderConfig.updateAdmin(admin-B, {'from':admin-A})`.<br>
    The value of `StaderConfig.getAdmin()` is admin-B.<br>

*   Step #3 admin-B updates admin to itself again:<br>
    `StaderConfig.updateAdmin(admin-B, {'from':admin-B})`.<br>
    The value of `StaderConfig.getAdmin()` is admin-B, but the `DEFAULT_ADMIN_ROLE` is revoked due to `_revokeRole(DEFAULT_ADMIN_ROLE, oldAdmin)`.<br>
    Now the protocol admin control is lost for StaderConfig contract.

### Recommended Mitigation Steps

Reference: <https://github.com/code-423n4/2023-06-stader/blob/7566b5a35f32ebd55d3578b8bd05c038feb7d9cc/contracts/StaderConfig.sol#L177><br>
In the `updateAdmin()` function, add a check for `oldAdmin != _admin`, like below:

        address oldAdmin = accountsMap[ADMIN];
    +   require(oldAdmin != _admin, "Already set to admin");

### Assessed type
Access Control

**[Picodes (judge) decreased severity to Medium](https://github.com/code-423n4/2022-06-stader-findings/issues/390#issuecomment-1585665576)**

**[manoj9april (Stader) confirmed and commented](https://github.com/code-423n4/2022-06-stader-findings/issues/390#issuecomment-1600790493):**
 > Sure,
> we will fix this.

**[rvierdiyev (warden) commented](https://github.com/code-423n4/2022-06-stader-findings/issues/390#issuecomment-1619667404):**
 > Isn't this same as just transferring roles to the `address 0` or any other address? Why would the protocol need to change roles to same address? Isn't this an informative issue?

**[Co0nan (warden) commented](https://github.com/code-423n4/2022-06-stader-findings/issues/390#issuecomment-1620201044):**
 > I believe this falls under the "Admin Privilege" [category](https://github.com/code-423n4/2023-01-drips-findings/discussions/327#discussioncomment-5099558), as such an issue should be marked as QA based on C4 docs and how similar issues got judged.

**[Picodes (judge) commented](https://github.com/code-423n4/2022-06-stader-findings/issues/390#issuecomment-1620824488):**
 > @rvierdiyev and @Co0nan - I respectfully disagree:
> 
> - This is not an occurrence of "Admin Privilege", which are issues where a privileged role uses their position to grief the protocol. Here, there is clearly a slight bug in the code.
> - We could argue that transferring the role to the same address is very unlikely but it is not an error in itself. The function clearly does not behave as intended in this case.
> - If you combine this with the fact that in `initialize` there is no call to `setAccount(ADMIN, _admin);` see [here]( https://github.com/code-423n4/2022-06-stader-findings/issues/133). It becomes actually likely that the admin calls this function for themselves.

**[Picodes (judge) commented](https://github.com/code-423n4/2022-06-stader-findings/issues/390#issuecomment-1620825512):**
 > @Co0nan - for information, "Admin Privilege" aren't always QA, it depends on the context and is up to the judge. See [here](https://github.com/code-423n4/org/issues/54) and [here](https://github.com/code-423n4/org/issues/59) for the ongoing discussion about this.

**[Co0nan (warden) commented](https://github.com/code-423n4/2022-06-stader-findings/issues/390#issuecomment-1620833254):**
 > >Here there is clearly a slight bug in the code.
> 
> @Picodes - This bug occurs from `Admin` as they pass an address twice. I have to stand with @rvierdiyev. This is likely due to missing `Zero address Check` on `onlyOwner` functions.
> 
> However, it's up to you as the Judge and I respect your final conclusion.

**[sanjay-staderlabs (Stader) commented](https://github.com/code-423n4/2023-06-stader-findings/issues/390#issuecomment-1633520349):**
>This is fixed in the code.
***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Stader Labs |
| Report Date | N/A |
| Finders | ksk2345, ChrisTina, NoamYakov |

### Source Links

- **Source**: https://code4rena.com/reports/2023-06-stader
- **GitHub**: https://github.com/code-423n4/2022-06-stader-findings/issues/390
- **Contest**: https://code4rena.com/reports/2023-06-stader

### Keywords for Search

`vulnerability`

