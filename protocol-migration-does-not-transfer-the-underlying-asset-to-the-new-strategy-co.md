---
# Core Classification
protocol: Balmy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46437
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/d365c977-e13a-41e2-84e3-67083ecbc362
source_link: https://cdn.cantina.xyz/reports/antina_balmy_november2024.pdf
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
finders_count: 2
finders:
  - Blockdev
  - ladboy233
---

## Vulnerability Title

Protocol migration does not transfer the underlying asset to the new strategy contract when the rescue is completed 

### Overview


This bug report discusses an issue with the ExternalGuardian contract, specifically with the _guardian_underlying_withdraw function. When a rescue is initiated, this function is supposed to withdraw underlying funds back to the strategy contract. However, when a strategy is migrated, only the aToken or cToken is transferred instead of both the token and the underlying asset. This can result in a loss of funds if a rescue is executed during the 3-day timelock period. The recommendation is to transfer both the token and underlying asset to the new strategy contract. The bug has been fixed in PR 109.

### Original Finding Content

## Context: ExternalGuardian.sol#L83-L87

## Description

When rescue starts, the `_guardian_underlying_withdraw` (see ExternalGuardian.sol#L84) withdraws underlying funds back to the strategy contract.

```solidity
(tokens, rescued) = _guardian_underlying_maxWithdraw();
IEarnStrategy.WithdrawalType[] memory types = _guardian_underlying_withdraw(0, tokens, rescued, address(this));
if (!_areAllImmediate(types)) {
    revert OnlyImmediateWithdrawalsSupported();
}
```

For example, if the strategy is AAVE V3, xxD:
- User deposits underlying asset in exchange for aToken.
- When withdrawing, aToken in the contract is burnt and underlying asset is transferred back.

Yet when the strategy is migrated, only the aToken is transferred (see AaveV3Connector.sol#L319):

```solidity
function _connector_migrateToNewStrategy(
    IEarnStrategy newStrategy,
    bytes calldata
) internal override returns (bytes memory) {
    IERC20 vault_ = aToken();
    uint256 balance = vault_.balanceOf(address(this));
    vault_.safeTransfer(address(newStrategy), balance);
    return abi.encode(balance);
}
```

The compound V2 strategy follows the same pattern, where only cToken is transferred out.

## Sequence of Actions

1. The strategy owner proposes a strategy migration.
2. The migration is subject to a 3-day time-lock (see EarnStrategyRegistry.sol#L110).
3. During these 3 days, a rescue transaction is executed, and all aToken is burnt to withdraw underlying token.
4. Migration is executed; yet no underlying asset is transferred to the new strategy.

## Recommendation

While executing the rescue in the 3-day time-lock is an edge case, the protocol can consider:
- Transfer both aToken and underlying token to the new strategy contract in AAVE V3 connector.
- Transfer both cToken and underlying token to the new strategy contract in Compound V2 connector.
- Transfer both vault share and vault underlying asset to the new strategy contract in ERC4626 connector.

## Balmy

We've decided to simply disable migrations on strategies that:
- Have an ongoing rescue (one that still needs confirmation).
- Have a confirmed rescue.

The fix is in PR 109.

## Cantina Managed

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Balmy |
| Report Date | N/A |
| Finders | Blockdev, ladboy233 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/antina_balmy_november2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/d365c977-e13a-41e2-84e3-67083ecbc362

### Keywords for Search

`vulnerability`

