---
# Core Classification
protocol: FactoryDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2243
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-factorydao-contest
source_link: https://code4rena.com/reports/2022-05-factorydao
github_link: https://github.com/code-423n4/2022-05-factorydao-findings/issues/130

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 2

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - rwa
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - IllIllI
  - kenzo
---

## Vulnerability Title

[H-03] MerkleVesting withdrawal does not verify that tokens were transferred successfully

### Overview


The codebase of the protocol is missing a check that verifies that an ERC20 transfer has succeeded in the MerkleVesting's `withdraw` function. This could lead to users losing their allocation and funds if the ERC20 transfer fails for any reason. The function is sending the funds to the user without checking the return value, so if the transfer fails, the contract won't know and the function will finish "successfully". To mitigate this vulnerability, it is recommended to add a check that verifies that the transfer has succeeded, as done throughout the rest of the protocol.

### Original Finding Content

_Submitted by kenzo, also found by IllIllI_

Across the codebase, the protocol is usually checking that ERC20 transfers have succeeded by checking their return value.
This check is missing in MerkleVesting's `withdraw` function.

### Impact

If for some reason the ERC20 transfer is temporarily failing, the user would totally lose his allocation and funds.
All the state variables would already have been updated at this stage, so he can't call `withdraw` again.
There is no way to withdraw these locked tokens.

### Proof of Concept

At the last point of `withdraw`, the function [is sending](https://github.com/code-423n4/2022-05-factorydao/blob/main/contracts/MerkleVesting.sol#L173) the funds to the user, and does not check the return value - whether it has succeeded:

            IERC20(tree.tokenAddress).transfer(destination, currentWithdrawal);

Note that this is (nicely and rightfully) done after all the state variables have been updated.
As the return value of the external call is not checked, if it has failed, the contract wouldn't know about it, and the function will finish "successfully".

### Recommended Mitigation Steps

As done throughout the rest of the protocol, add a check that verifies that the transfer has succeeded.


**[illuzen (FactoryDAO) acknowledged, disagreed with severity and commented](https://github.com/code-423n4/2022-05-factorydao-findings/issues/130#issuecomment-1122570209):**
 > Debatable, since requiring successful transfer means we can't do non-standard tokens like USDT. Also, tokens could be malicious and simply lie about the success.

**[Justin Goro (judge) commented](https://github.com/code-423n4/2022-05-factorydao-findings/issues/130#issuecomment-1155855225):**
 > Regarding the non standard tokens that don't return bools, the common approach to performing a low level call with 
> ```
> (bool success, _)  = address(token).call(//etc
> ```
> allows for transfers to be validated for USDT.
> 
> Severity will stand because this function represents user funds.
> 



***

 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 2/5 |
| Audit Firm | Code4rena |
| Protocol | FactoryDAO |
| Report Date | N/A |
| Finders | IllIllI, kenzo |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-factorydao
- **GitHub**: https://github.com/code-423n4/2022-05-factorydao-findings/issues/130
- **Contest**: https://code4rena.com/contests/2022-05-factorydao-contest

### Keywords for Search

`vulnerability`

