---
# Core Classification
protocol: SteadeFi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27609
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf
source_link: none
github_link: https://github.com/Cyfrin/2023-10-SteadeFi

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
finders_count: 10
finders:
  - Maroutis
  - 0xhacksmithh
  - innertia
  - Drynooo
  - dipp
---

## Vulnerability Title

Missing minimum token amounts in the emergency contract functions allows MEV bots to take advantage of the protocols emergency situation

### Overview


This bug report is about missing minimum token amounts in the emergency contract functions of a protocol. This bug allows MEV bots to take advantage of the protocol's emergency situation and make huge profits with it. When an emergency situation arises and the protocol pauses or resumes the operation of the vault, all funds of the vault are removed from GMX or added back to GMX without any protection against slippage. This is because the minimum tokens amount to get back when removing liquidity is not provided to the RemoveLiquidityParams, thus allowing up to 100% slippage. This could lead to a big loss of funds as all funds of the strategy vault are unprotected against MEV bots.

The manual review was used as a tool to identify the bug. The recommendation is to implement a custom minMarketTokens parameter, but do not implement the usual slippage calculation, as this could potentially lead to new critical vulnerabilities.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXEmergency.sol#L83-L90">https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXEmergency.sol#L83-L90</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXEmergency.sol#L54-L61">https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXEmergency.sol#L54-L61</a>


## Summary

When an emergency situation arises and the protocol pauses or resumes the operation of the vault. All funds of the vault are removed from GMX or added back to GMX without any protection against slippage. This allows MEV bots to take advantage of the protocol's emergency situation and make huge profits with it.

## Vulnerability Details

When an emergency situation arises the protocol owners can call the emergencyPause function to remove all the liquidity from GMX:

```jsx
function emergencyPause(
  GMXTypes.Store storage self
) external {
  self.refundee = payable(msg.sender);

  GMXTypes.RemoveLiquidityParams memory _rlp;

  // Remove all of the vault's LP tokens
  _rlp.lpAmt = self.lpToken.balanceOf(address(this));
  _rlp.executionFee = msg.value;

  GMXManager.removeLiquidity(
    self,
    _rlp
  );

  self.status = GMXTypes.Status.Paused;

  emit EmergencyPause();
}
```

But the minimum tokens amount to get back when removing liquidity is not provided to the RemoveLiquidityParams:

```jsx
struct RemoveLiquidityParams {
  // Amount of lpToken to remove liquidity
  uint256 lpAmt;
  // Array of market token in array to swap tokenA to other token in market
  address[] tokenASwapPath;
  // Array of market token in array to swap tokenB to other token in market
  address[] tokenBSwapPath;
  // Minimum amount of tokenA to receive in token decimals
  uint256 minTokenAAmt;
  // Minimum amount of tokenB to receive in token decimals
  uint256 minTokenBAmt;
  // Execution fee sent to GMX for removing liquidity
  uint256 executionFee;
}
```

As it is not set, the default value 0 (uint256) is used. Therefore, up to 100% slippage is allowed.

The same parameters are also missing when normal operation resumes:

```jsx
function emergencyResume(
  GMXTypes.Store storage self
) external {
  GMXChecks.beforeEmergencyResumeChecks(self);

  self.status = GMXTypes.Status.Resume;

  self.refundee = payable(msg.sender);

  GMXTypes.AddLiquidityParams memory _alp;

  _alp.tokenAAmt = self.tokenA.balanceOf(address(this));
  _alp.tokenBAmt = self.tokenB.balanceOf(address(this));
  _alp.executionFee = msg.value;

  GMXManager.addLiquidity(
    self,
    _alp
  );
}
```

Therefore, MEV bots could take advantage of the protocol's emergency situation and as these trades include all funds of the vault it could lead to a big loss.

Ignoring slippage when pausing could be a design choice of the protocol to avoid the possibility of a revert and pause the system as quickly as possible. However, this argument does not apply during the resume.

## Impact

Big loss of funds as all funds of the strategy vault are unprotected against MEV bots.

## Tools Used

Manual Review

## Recommendations

Implement a custom minMarketTokens parameter, but do not implement the usual slippage calculation, as this could potentially lead to new critical vulnerabilities. If for example the reason for this emergency situation is a no longer supported chainlink feed, which will lead to reverts and therefore also to DoS of the emergency close / withdraw flow.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | Maroutis, 0xhacksmithh, innertia, Drynooo, dipp, 0xCiphky, rvierdiiev, Cosine |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

