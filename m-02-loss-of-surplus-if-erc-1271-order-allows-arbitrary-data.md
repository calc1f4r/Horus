---
# Core Classification
protocol: Cove_2024-12-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57956
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Cove-security-review_2024-12-30.md
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

[M-02] Loss of surplus if ERC-1271 order allows arbitrary data

### Overview


The bug report discusses a problem with the CoWSwapClone::isValidSignature() function in the cove-contracts-core repository. This function does not properly check the app data field, which can be manipulated by an attacker to transfer surplus funds to their own address. This issue affects all ERC-1271 orders and can result in a loss of funds for the user. The report suggests making the app data immutable or rejecting orders with mismatched app data. This is considered a high severity issue with a low likelihood of occurrence. More information can be found in the provided links.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

[CoWSwapClone::isValidSignature()](https://github.com/Storm-Labs-Inc/cove-contracts-core/blob/6b607d137f898c0f421b4ba4e748f41b09b41518/src/swap_adapters/CoWSwapClone.sol#L86) do not check app data field.

This applies to all ERC-1271 orders where the app data field can be changed by an adversary in a way that keeps the signature valid for that order (for example, because isValidSignature ignores the appData field in the order).

An adversary can manipulate vulnerable ERC-1271 orders, thereby transferring part of the expected surplus from the user order to an address that the adversary controls.

More details can be seen [here](https://docs.cow.fi/cow-protocol/reference/contracts/core#loss-of-surplus-if-erc-1271-order-allows-arbitrary-app-data).

## Recommendations

making the app data immutable at deployment time (or equal to bytes(0)), and
have isValidSignature reject an order if the app data doesn't match.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Cove_2024-12-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Cove-security-review_2024-12-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

