---
# Core Classification
protocol: Op Enclave
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58271
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Coinbase-OP-Enclave-Spearbit-Security-Review-December-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Coinbase-OP-Enclave-Spearbit-Security-Review-December-2024.pdf
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
  - Zigtur
  - 0xTylerholmes
  - 0xIcingdeath
  - CarrotSmuggler
---

## Vulnerability Title

Multiple withdrawals in a single L3 transaction are not provable through op-withdrawer

### Overview


This bug report is about a medium-risk issue in the op-withdrawer command. The command is used to prove a withdrawal on the Base L2 using a transaction hash from the L3. However, the function it calls from the Optimism repository does not support multiple withdrawals in the same transaction. This means that the op-withdrawer cannot prove withdrawals when there are multiple in a single L3 transaction. The code snippet provided shows that the function does not support multiple withdrawals and the recommendation is for the op-withdrawer to be able to handle multiple withdrawals in a single transaction. The bug has been fixed by Optimism and Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
`withdrawals.go#L54-L60`

## Description
The op-withdrawer implements the `provideWithdrawal` command that takes as input a `txHash` on the L3 in which there is a withdrawal to prove a withdrawal on the Base L2. This command calls the `withdrawals.ProveWithdrawalParametersForBlock` function from the Optimism repository. It will parse the logs from the given transaction on L3. However, this function from the Optimism repository does not support multiple withdrawals in the same transaction.

This leads the op-withdrawer binary to not be able to prove withdrawals when there are multiple in a single L3 transaction. 

**Note:** The op-stack specifications about withdrawals do not mention that multiple withdrawals in a single transaction are not supported. This behavior should be supported.

## Code Snippet
The `withdrawals.ProveWithdrawalParametersForBlock` function parses the withdrawal logs by calling `ParseMessagePassed`. Comments on this function explain that it does not support multiple withdrawals.

```go
// ParseMessagePassed parses MessagePassed events from
// a transaction receipt. It does not support multiple withdrawals
// per receipt.
func ParseMessagePassed(receipt *types.Receipt) (*bindings.L2ToL1MessagePasserMessagePassed, error) {
    contract, err := bindings.NewL2ToL1MessagePasser(common.Address{}, nil)
    if err != nil {
        return nil, err
    }
    // ...
}
```

## Recommendation
The op-withdrawer should support proving and finalizing all withdrawals that are in a single L3 transaction.

## Base
Fixed in PR 56 and PR 13568 on Optimism.

## Spearbit
Fixed. The withdrawer is now able to handle multiple withdrawals in a single transaction.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Op Enclave |
| Report Date | N/A |
| Finders | Zigtur, 0xTylerholmes, 0xIcingdeath, CarrotSmuggler |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Coinbase-OP-Enclave-Spearbit-Security-Review-December-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Coinbase-OP-Enclave-Spearbit-Security-Review-December-2024.pdf

### Keywords for Search

`vulnerability`

