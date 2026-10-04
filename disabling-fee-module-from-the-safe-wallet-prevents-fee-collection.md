---
# Core Classification
protocol: Brava Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53567
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/brava/report.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/brava/report.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Disabling Fee Module From The Safe Wallet Prevents Fee Collection

### Overview


The bug report discusses a vulnerability in the Safe wallet's fee collection mechanism. This allows malicious wallet owners to disable the fee-taking module and prevent bots from collecting fees. The recommended solution is to prevent users from disabling the fee module, but this may require significant changes to the design. The issue has been resolved by adding a guard to the Safe wallets to restrict unauthorized calls.

### Original Finding Content

## Description

Safe wallet owners can disable the fee-taking module from their wallets by utilizing the built-in module management functionality. Consequently, bots will be unable to collect fees from these wallets.

The fee collection mechanism relies on whitelisted bots invoking the `FeeTakeSafeModule.takeFees()` function to extract fees from Safe wallets. This function initiates a zero-amount deposit which is executed in the context of the Safe wallet using the function `execTransactionFromModule()`:

```solidity
bool success = ISafe(_safeAddr).execTransactionFromModule(
    SEQUENCE_EXECUTOR_ADDR,
    msg.value,
    sequenceData,
    Enum.Operation.DelegateCall
);
```

Malicious Safe wallet owners can bypass this mechanism by simply disabling the fee-taking module from their wallet using the `disableModule()` function. This action effectively prevents bots from executing the `takeFees()` function and collecting the intended fees.

## Recommendations

Safe wallet users should not be able to disable the fee module from their wallet to prevent regular fee collection. Addressing this vulnerability would likely require significant modifications to the design of the Safe fee module. Note, the users who disable the fee module would still end up paying fees to Brava, but only when they interact with the protocol through new deposits or withdrawals.

## Resolution

Brava Labs have added a guard to the Safe wallets that end users deploy. This restricts calls made from the Safe wallet to only be sent to the `SequenceExecutor` contract which, in turn, checks that only approved actions are performed from the Safe wallet.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Brava Labs |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/brava/report.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/brava/report.pdf

### Keywords for Search

`vulnerability`

