---
# Core Classification
protocol: Octodefi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61602
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md
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

protocol_categories:
  - oracle

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Giovanni Di Siena
  - Farouk
---

## Vulnerability Title

Volume-based fee can be bypassed with a wrapper contract

### Overview


The bug report describes a problem with the `_executeAction()` function in the `_action` contract. This function is supposed to charge a percentage fee when it can map the `(target, selector)` pair to a tracked token using the `FeeController.getTokenForAction()` function. However, if the mapping is not present, it falls back to charging the minimum fee in USD. This allows attackers to wrap high-value calls inside a helper contract that is not known by the `FeeController`, resulting in them only paying the minimum fee instead of the expected percentage fee. This can lead to a loss of revenue for executors. The recommended solution is to document the issue and discuss possible design changes to address it. The bug has been fixed in the OctoDeFi project and verified by Cyfrin.

### Original Finding Content

**Description:** `_executeAction()` levies a percentage fee only when `FeeController.getTokenForAction()` can map the `(target, selector)` pair to a tracked token. If the mapping is absent it falls back to `minFeeInUSD`.
An attacker can therefore wrap any high-value call inside a helper contract that the `FeeController` does not know about.
*Example – Aave deposit:*
```text
User → StrategyBuilder → AAVEHandler.supplyFor(100 000 USDC) → Aave Pool.supply()
```
`AAVEHandler` receives the user’s 100 000 USDC, approves the Aave pool, and supplies on the user’s behalf, returning aUSDC. Because `(AAVEHandler, supplyFor)` is not registered, `getTokenForAction()` returns `(address(0), false)`, so the strategy pays only the minimum fee instead of ~1 000 USDC (1 %). The same trick works for withdrawals, swaps, or any volume-based selector.

```solidity
function _executeAction(address _wallet, Action memory _action) internal returns (uint256 feeInUSD) {
    (address tokenToTrack, bool exist) =
        feeController.getTokenForAction(_action.target, _action.selector, _action.parameter);
    // If the volume token exist track the volume before and after the execution, else get the min fee

    uint256 preExecBalance = exist ? IERC20(tokenToTrack).balanceOf(_wallet) : 0;

    _execute(_wallet, _action);

    IFeeController.FeeType feeType = feeController.functionFeeConfig(_action.selector).feeType;

    if (exist) {
        uint256 postExecBalance = IERC20(tokenToTrack).balanceOf(_wallet);
        uint256 volume = feeType == IFeeController.FeeType.Deposit
            ? preExecBalance - postExecBalance
            : postExecBalance - preExecBalance;

        feeInUSD = feeController.calculateFee(tokenToTrack, _action.selector, volume);
    } else {
        feeInUSD = feeController.minFeeInUSD(feeType);
    }

    emit ActionExecuted(_wallet, _action);
}
```
**Impact:** Large transactions can be executed while paying the protocol’s minimum flat fee, severely reducing or eliminating expected revenue for executors.

**Recommended Mitigation:** Because this stems from design choices rather than a simple coding bug, solving it on-chain is non-trivial. It is to document the behavior and discuss any design adjustment that can remediate its risk.

**OctoDeFi:** Fixed in PR [\#25](https://github.com/octodefi/strategy-builder-plugin/pull/25).

**Cyfrin:** Verified. The `ActionRegistry` contract has been added to validate action contracts allowed to be integrated into `StrategyBuilderPlugin`.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Octodefi |
| Report Date | N/A |
| Finders | Giovanni Di Siena, Farouk |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

