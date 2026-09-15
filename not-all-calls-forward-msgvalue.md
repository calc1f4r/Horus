---
# Core Classification
protocol: Biconomy Nexus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43815
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf
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
finders_count: 7
finders:
  - Blockdev
  - Devtooligan
  - Chinmay Farkya
  - Christoph Michel
  - Víctor Martínez
---

## Vulnerability Title

Not all calls forward msg.value

### Overview


The report states that there is a bug in the codebase of ModuleManager, specifically in line 102 of ModuleManager.sol. This bug has a medium risk severity and affects multiple functions that are payable. When these functions make an inner call, the msg.value is not always forwarded. This includes the Nexus.executeUserOp, Nexus.fallback handler, and BiconomyMetaFactory.deployWithFactory functions. This can result in native tokens getting stuck in the contracts, making them unrecoverable. The recommendation is to fix this bug by ensuring that msg.value is forwarded whenever expected. The report also mentions that the Biconomy team has fixed this issue in their PR 113 and the Spearbit team has also fixed it by forwarding msg.value and calling initNexus with a value of 0. It is recommended that the factories and executeUserOp functions do not require a msg.value.

### Original Finding Content

## Severity: Medium Risk

## Context
`ModuleManager.sol#L102`

## Description
Most functions of the codebase are payable. When these functions perform an inner call, the `msg.value` is not always forwarded:
- `Nexus.executeUserOp` does not forward it in `target.call(data)`.
- `Nexus.fallback` handler.
- `BiconomyMetaFactory.deployWithFactory` does not forward it in `factory.call(factoryData)`.
- Other factories don't forward it in `INexus(account).initializeAccount(initData)`.

Native tokens can be stuck in these contracts; in the case of the factory, they are unrecoverable. The fallback handler calls will not work as expected when receiving `msg.value`.

## Recommendation
Consider forwarding `msg.value` whenever expected. We believe the fallback should forward native tokens to the fallback handler. The factories initializing the smart account should not require a `msg.value`. Neither does the `executeUserOp` as it's called from the entry point with a value of zero.

## Biconomy
Fixed in PR 113.

## Spearbit
Fixed. The `msg.value` is now forwarded; the factories send it to the deployment, and `initNexus` is called with a `msg.value` of 0.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Biconomy Nexus |
| Report Date | N/A |
| Finders | Blockdev, Devtooligan, Chinmay Farkya, Christoph Michel, Víctor Martínez, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Biconomy-Spearbit-Security-Review-October-2024.pdf

### Keywords for Search

`vulnerability`

