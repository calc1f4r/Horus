---
# Core Classification
protocol: Aragon DAO Gov Plugin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62261
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Aragon-Spearbit-Security-Review-July-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Aragon-Spearbit-Security-Review-July-2025.pdf
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
finders_count: 3
finders:
  - Om Parikh
  - Emanuelle Ricci
  - Patrick Drotleff
---

## Vulnerability Title

Using idle balance in computing isGranted doesn't account for freezed & blacklisted tokens

### Overview


The bug report is about a medium risk bug in the MinVotingPowerCondition.sol file. The issue is in the `isGranted` function, which allows addresses with frozen or blacklisted tokens to still create proposals. This is not the intended behavior, as the function should not allow proposals from addresses with non-transferable tokens. The recommendation is to fix this by actually locking the tokens in the LockManager instead of just checking the balance. The bug has been fixed in PR 28 and verified by Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
MinVotingPowerCondition.sol#L45

## Description
In `MinVotingPowerCondition.isGranted`.

```solidity
function isGranted(address _where, address _who, bytes32 _permissionId, bytes calldata _data)
public
view
override
returns (bool)
{
    (_where, _data, _permissionId);
    uint256 _currentBalance = token.balanceOf(_who) + lockManager.getLockedBalance(_who);
    uint256 _minProposerVotingPower = plugin.minProposerVotingPower();
    return _currentBalance >= _minProposerVotingPower;
}
```

If an address holds tokens but can't spend them due to being frozen or blacklisted, then they are granted access (i.e., in this case, they can create a proposal). However, the intended behavior should be to not allow calling create proposal as tokens are not transferable.

### Examples:
- Token is USDT/USDC, address holds funds but is blacklisted; then they can still create a proposal.
- Token is morpho-vault-v2 share, but holder is blacklisted by gates.

## Recommendation
Do not use `token.balanceOf(_who)`; rather, actually lock the tokens in `LockManager` by making a transfer.

## Aragon
Fixed in PR 28.

## Spearbit
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Aragon DAO Gov Plugin |
| Report Date | N/A |
| Finders | Om Parikh, Emanuelle Ricci, Patrick Drotleff |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Aragon-Spearbit-Security-Review-July-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Aragon-Spearbit-Security-Review-July-2025.pdf

### Keywords for Search

`vulnerability`

