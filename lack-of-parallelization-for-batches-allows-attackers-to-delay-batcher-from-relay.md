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
solodit_id: 58269
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

Lack of parallelization for batches allows attackers to delay batcher from relaying data

### Overview


This report discusses a medium risk vulnerability in a code that processes withdrawals. The issue occurs when multiple withdrawals are submitted one after another, causing delays in sending batches to the data availability provider. This can potentially be exploited by an attacker to create a denial of service attack. The report suggests fixing this by either parallelizing the batcher or documenting proper assumptions for expected behavior. The vulnerability has been fixed in a recent PR.

### Original Finding Content

## Medium Risk Vulnerability Report

**Severity:** Medium Risk  
**Context:** `channel_out.go#L30-L35`, `driver.go#L341-L343`  

## Description
If withdrawals are submitted one after another, this will delay batches from being sent to the data availability provider, as each withdrawal that is submitted is processed sequentially. This means any transactions submitted to the batcher in between the withdrawal executions are dropped. 

One of the changes from the existing op-enclave is that when a withdrawal comes in, the batch is immediately closed and sent for batching. In scenarios where there are many withdrawals or if an attacker wishes to block proper execution of this flow, it poses a relatively low-cost denial of service attack vector.

## Exploit Scenario
Transactions are being batched for batch 1. A series of 0.1 ETH withdrawals are submitted by a user. The first will result in block 1 closing and being batched. Each new transaction will result in a new batch being created, which means there is no chance to add transactions to a block between batches 1-10, and incoming transactions will be delayed.

## Recommendation
Consider either:
- Parallelizing the batcher to ensure that transactions are not missed during this time period.
- Documenting proper assumptions for what the expected behavior is.

## Base
This will be remediated with PR 41, which ensures that the `ErrWithdrawalDetected` is only used if the block is within the last 10 seconds. If multiple withdrawals happen in series, it will ensure the block is fresh before it submits the batch.

**Spearbit:** Fixed.

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

