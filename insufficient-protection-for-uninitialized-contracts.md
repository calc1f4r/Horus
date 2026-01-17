---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19480
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Insufficient Protection for Uninitialized Contracts

### Overview

See description below for full details.

### Original Finding Content

## Description

Several state changing functions defined in `Lido.sol` and `StETH.sol` are not protected by the `isInitialized` modifier. Prior to v0.2.0-rc.0 this was not a problem, as they all performed external function calls that would revert when uninitialized. As of v0.2.0-rc.0, however, these functions no longer make external calls and can succeed without error.

Most relevant is `Lido._submit()`, which is the implementation for the external `Lido.submit()` and fallback functions. This affects more than non-standard deployments (where it may be possible to interact with an uninitialized Aragon proxy). Indeed, it should be possible to submit funds without error to a base Lido contract that was correctly petrified during deployment. The petrified status is intended to disable any state changing functionality in the base logic contract (which should be used only as the source of logic per the DelegateProxy pattern). However, the Petrifiable implementation only disables functions that have an `isInitialized` modifier (including those with an `auth` or `authP` modifier).

Because `Lido.transferToVault()` only allows the recovery of unbuffered ETH, any ETH successfully submitted to the petrified base contract would be lost entirely.

The security risk is deemed low, as this does not appear to be exploitable by a malicious attacker to affect other users. The primary impact appears to be that a user can accidentally lock their own funds by submitting to a base Lido contract. At most, a malicious entity may trick a user into submitting ETH to the base contract, from which it could not be recovered.

## Recommendations

Consider adding `isInitialized` modifiers to any state changing functions that are not already protected by `auth()` or `authP()`. In particular, the following functions:
- `Lido._submit()` (or the fallback and `Lido.submit()`)
- `StETH._transfer()`
- `stETH._approve()`

To protect the StETH functions, this would need to inherit from `AragonApp` (or `Initializable` at the least). For Lido to compile after StETH inherits from `AragonApp`, the order of inheritance would need to be changed from:

```solidity
contract Lido is ILido, IsContract, StETH, AragonApp
```

to:

```solidity
contract Lido is ILido, IsContract, AragonApp, StETH
```

Also consider adding the modifier for any externally accessible function that is not `view` or `pure` to protect against unintentional exposure in future updates. For example, although `Lido._depositBufferedEther()` should revert when not initialized due to an external call to `NodeOperatorRegistry.assignNextSigningKeys()`, a later update may unintentionally allow this to succeed, sending buffered ETH to the zero address.

Because these functions already use the `whenNotStopped` modifier, an alternative remediation could be to change the `Pausable` definition such that the uninitialized value counts as “Paused” (i.e., `isStopped() == true` by default). `Lido.initialize()` would then include a call to `_resume()`.

## Resolution

This issue was remediated in PR #253, which set `Pausable` contracts to paused by default (`isStopped() == true`). Lido then resumes during initialization and existing authentication protections prevent the DAO from resuming the petrified base contract.

With the existing inheritance order, compilation would fail with an “Linearization of inheritance graph impossible” error. See [Solidity Documentation](https://docs.soliditylang.org/en/v0.7.4/contracts.html#multiple-inheritance-and-linearization) for explanation. Though this documents a newer Solidity version, it is still applicable.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf

### Keywords for Search

`vulnerability`

