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
solodit_id: 43818
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

fallback() can be used for direct unauthorised calls to fallback handlers

### Overview


The report discusses a bug in the ModuleManager.sol file that could compromise the security of the Nexus smart account. The issue is with the unrestricted access to the fallback() function, which can be called by anyone and could potentially be used by an attacker to misuse the account's funds. The recommendation is to implement appropriate authorization control in the fallback() function, either by restricting it to only the entrypoint or by allowing a specific set of callers. The report also mentions that the bug has been acknowledged by Biconomy and Spearbit, and a pull request has been opened to fix the issue. 

### Original Finding Content

## Severity: Medium Risk

## Context
ModuleManager.sol#L72

## Description
The `fallback()` function in Nexus smart account is meant for handling calls that need to be routed to a fallback handler module corresponding to the selector in the calldata. 

It checks if a handler has been installed for the selector extracted from the calldata, and if a handler exists in the account, then makes a call to the registered handler with the supplied calldata. 

But the problem is that the `fallback()` function is unrestricted so it can also be called by anyone directly. If an attacker calls the smart account with a `msg.sig` equal to a particular selector, the call will be routed to the installed fallback handler from the account.

This alternate call path does not check if the entrypoint is the caller, and also does not have any signature validation because there is no `userOp` and no validator modules are involved. This can compromise the security of the account in many ways. One example could be a handler having logic to use account's funds in some way, so the account might have given large approvals of funds to the handler. But now the attacker gets to misuse the approvals by using the calldata he wishes.

## Recommendation
All external functions in Nexus.sol are restricted to only entrypoint or self except the fallback itself. While the fallback handlers installed by the user themselves might not be malicious, the unrestricted access to `fallback()` can be used by an attacker.

Implement appropriate authorization control in `fallback()` if required, for example, `onlyEntrypoint()` or a set of allowed callers specific to the handler used. According to EIP-7579, "fallback function must implement authorization control," but note that complying with this will restrict the usefulness of fallback handlers. Alternatively, ensure authorization control is implemented in the fallback handler itself, based on the appended `msg.sender`.

## Biconomy
Acknowledged. Ensure authorization control is implemented in the fallback handler itself, based on the appended `msg.sender`. We believe this is enough.

I have opened PR 590 on the ERC after discussing with the authors. Once merged here, we will ask for merge in the ethereum/repo. We're also hooking the fallback function now.

## Spearbit
Acknowledged.

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

