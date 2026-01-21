---
# Core Classification
protocol: Coinbase Solady
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45414
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Solady-Coinbase-Spearbit-Security-Review-December-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Solady-Coinbase-Spearbit-Security-Review-December-2024.pdf
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
finders_count: 4
finders:
  - Kaden
  - Riley Holterhus
  - Optimum
  - Philogy
---

## Vulnerability Title

Unsafe EOA validation can be bypassed

### Overview


This bug report discusses a medium risk issue in the LifeBuoy contract, which is used to recover funds sent to the wrong chain or contract. The issue is related to a validation that checks if the caller is an externally owned account (EOA), which can be bypassed during deployment. This allows an attacker to withdraw funds that were intended to be safely recoverable. The impact of this bug is that an attacker can steal or disrupt the recovery of funds sent to the wrong chain. The likelihood of this exploit depends on a user's mistake and the attacker's ability to monitor and deploy contracts on different chains. The recommendation is to follow the suggestions provided in a previous finding about wrong chain fund recovery. The developers have acknowledged the bug.

### Original Finding Content

## Severity: Medium Risk

## Context
(No context files were provided by the reviewer)

## Relevant Context
Lifebuoy.sol#L300

## Summary
An unsafe validation that the caller is an EOA is used, resulting in an attacker being able to withdraw funds which are intended to be safely recoverable.

## Finding Description
LifeBuoy.sol is a contract that can be used to mitigate common mistakes, as indicated in the documentation:

- Careless user sends tokens to the wrong chain or wrong contract.
- Careless dev deploys a contract without a withdraw function in an attempt to rescue careless user’s tokens, due to deployment nonce mismatch caused by script misfire/misconfiguration.
- Careless dev forgets to add a withdraw function to an NFT sale contract.

In this finding, we will be focusing on: "Careless user sends tokens to the wrong chain or wrong contract". As documented, rescue authorization functions depend on either:

- Caller is the deployer AND caller is an EOA AND the contract is not a proxy AND `rescueLocked() & _LIFEBUOY_DEPLOYER_ACCESS_LOCK == 0`.
- Caller is `owner()` AND `rescueLocked() & _LIFEBUOY_OWNER_ACCESS_LOCK == 0`.

The dependency of focus here is, "caller is an EOA". In `_checkRescuer`, we validate that the caller is an EOA with the following logic:

```solidity
if iszero(or(extcodesize(caller()), ...)) { break }
```

The behavior of this line is that if the caller has a code size of zero at the time of execution, we will break out of the loop and avoid an impending revert. The problem with this expectation is that, as noted in the Ethereum Yellow Paper:

> During initialization code execution, EXTCODESIZE on the address should return zero.

This means that as long as a contract is making a call from its constructor, during deployment, the `extcodesize` will be zero, allowing this validation to be bypassed.

The presence of this "caller is an EOA" dependency is used to prevent an attacker from being able to deploy to the same address on a different chain via `create2`, allowing them to then recover funds accidentally sent to the wrong chain. As such, since this validation can be bypassed, it's unexpectedly possible for an attacker to recover funds sent to the same address on the wrong chain.

## Impact Explanation
It's possible for an attacker to withdraw funds sent to the same address on a different chain which are intended to be safely recoverable.

## Likelihood Explanation
This exploit depends upon a user sending funds to the wrong network, but an attacker can have a script running to monitor whether other chains at the same addresses receive funds and immediately deploy and withdraw the funds.

## Recommendation
In general, there is no clear safe way to validate that a caller is an EOA. However, regardless of whether the EOA is validated or not, there are remaining risks to this contract, as noted in the LifeBuoy wrong chain fund recovery can be stolen or griefed, and the recommendation provided with that finding should be followed.

## Solady
Acknowledged.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Coinbase Solady |
| Report Date | N/A |
| Finders | Kaden, Riley Holterhus, Optimum, Philogy |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Solady-Coinbase-Spearbit-Security-Review-December-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Solady-Coinbase-Spearbit-Security-Review-December-2024.pdf

### Keywords for Search

`vulnerability`

