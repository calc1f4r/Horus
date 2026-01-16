---
# Core Classification
protocol: Cosmos LSM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46742
audit_firm: OtterSec
contest_link: https://cosmos.network/
source_link: https://cosmos.network/
github_link: https://github.com/cosmos/cosmos-sdk

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
  - James Wang
  - Robert Chen
  - Tuyết Dương
---

## Vulnerability Title

Freezing of Validator Bond Delegations

### Overview


This bug report identifies a vulnerability in the staking module that allows a malicious user to manipulate the balance of a validator's bond shares. This can potentially freeze the bond delegations of other users. The issue can be exploited by transferring tokens to a delegator with a bond delegation and then redeeming and undelegating them, which reduces the validator's bond shares and prevents other users from undelegating their funds. The bug has been fixed in PR#22519, which verifies the destination delegation and updates the bond shares accordingly.

### Original Finding Content

## Vulnerability Details

The vulnerability arises from the interaction between tokenized shares, validator bond shares, and the delegation mechanisms in the staking module. Specifically, it exploits a flaw that allows a malicious user to repeatedly manipulate the `ValidatorBondShares` balance of a validator, potentially freezing other delegators’ validator bond delegations. 

While `TokenizeShares` does not permit `validatorbond`, tokens can still be transferred to a delegator with a `validatorbond` delegation. Additionally, `RedeemTokensForShares` currently allows `validatorbond` delegations but does not update `ValidatorBondShares`.

This issue may be abused by any delegator to reduce a validator’s `ValidatorBondShares`. A delegator may delegate a small amount, mark it as `ValidatorBond`, obtain a large number of LSM tokens, redeem and undelegate them, and thereby significantly decrease the validator’s `ValidatorBondShares`. This will prevent other delegators with `ValidatorBond` delegations to that validator from undelegating their funds, as `SafelyDecreaseValidatorBond` would fail due to insufficient `ValidatorBondShares`. This requires minimal capital compared to the amount of funds disrupted.

## Remediation

`RedeemTokensForShares` should verify if the destination delegation is a `validator bond`, either preventing redemption entirely or ensuring `ValidatorBondShares` are updated accordingly.

## Patch

Fixed in PR#22519.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Cosmos LSM |
| Report Date | N/A |
| Finders | James Wang, Robert Chen, Tuyết Dương |

### Source Links

- **Source**: https://cosmos.network/
- **GitHub**: https://github.com/cosmos/cosmos-sdk
- **Contest**: https://cosmos.network/

### Keywords for Search

`vulnerability`

