---
# Core Classification
protocol: Yearn v2 Vaults
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16945
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/YearnV2Vaults.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/YearnV2Vaults.pdf
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
  - Gustavo Grieco
  - Mike Martel
---

## Vulnerability Title

Division rounding may a�fect issuance of shares

### Overview


This bug report is about an issue with the Vault.vy system where users might not receive shares in exchange for their deposits if the total asset amount is manipulated by another user through a large "donation". This is because the _issueSharesForAmount function calculates the amount of shares to be issued based on the total supply, total amount of assets, and amount of deposited assets. If a user makes a large donation to the vault, increasing the total supply, other users may not receive shares after making deposits.

The exploit scenario for this issue is as follows: Alice deploys a Yearn vault and makes a minimal initial deposit to obtain one unit of shares, so the totalSupply is one. Eve then wants to block Alice's vault, so she transfers a large number of tokens to the vault address, increasing the totalAssets value without increasing the totalSupply. If more users deposit small amounts, they will not receive any shares in return.

The short-term recommendation for this issue is to document the vault initialization process to ensure that the deployer’s first deposit is large enough to prevent corner cases in which users do not receive shares after making deposits. The long-term recommendation is to review the list of global invariants to make sure there is no way to break them.

### Original Finding Content

## Type: Undefined Behavior
**Target:** Vault.vy

**Difficulty:** Low

## Description
Users might not receive shares in exchange for their deposits if the total asset amount is manipulated by another user through a large "donation."

The `_issueSharesForAmount` function calculates the amount of shares to be issued:

```python
@internal
def _issueSharesForAmount(to: address, amount: uint256) -> uint256:
    # Issues `amount` Vault shares to `to`.
    # Shares must be issued prior to taking on new collateral, or
    # calculation will be wrong. This means that only *trusted* tokens
    # (with no capability for exploitative behavior) can be used.
    shares: uint256 = 0
    # HACK: Saves 2 SLOADs (~4000 gas)
    totalSupply: uint256 = self.totalSupply
    if totalSupply > 0:
        # Mint amount of shares based on what the Vault is managing overall
        # NOTE: if sqrt(token.totalSupply()) > 1e39, this could potentially revert
        precisionFactor: uint256 = self.precisionFactor
        shares = precisionFactor * amount * totalSupply / self._totalAssets() / precisionFactor
    else:
        # No existing shares, so mint 1:1
        shares = amount
    # Mint new shares
    self.totalSupply = totalSupply + shares
    self.balanceOf[to] += shares
    log Transfer(ZERO_ADDRESS, to, shares)
    return shares
```

*Figure 3.1:* A transfer implementation without comments.

Essentially, the number of shares that a user will receive depends on the total supply, the total amount of assets, and the amount of deposited assets. The total asset amount is computed by the following code:

```python
@view
@internal
def _totalAssets() -> uint256:
    # See note on `totalAssets()`.
    return self.token.balanceOf(self) + self.totalDebt
```

*Figure 3.2:* A `revokeStrategy` implementation without comments.

However, if a user makes a large “donation” to the vault, increasing the total supply, other users may not receive shares after making deposits.

## Exploit Scenario
1. Alice deploys a Yearn vault. She makes a minimal initial deposit to obtain one unit of shares, so the `totalSupply` is one.
2. Eve wants to block Alice's vault, so she transfers a large number of tokens to the vault address, increasing the `totalAssets` value without increasing the `totalSupply`.
3. A user calls `deposit` in order to obtain shares. Because his deposit is smaller than Eve’s, he does not receive any shares, even though the transaction succeeds. As a result, the vault has more `totalAssets`, but the same number of shares (one).

If more users deposit small amounts, they will not receive any shares in return. The problem will get worse until a user with enough money makes a large deposit.

## Recommendations
Short term, document the vault initialization process to ensure that the deployer’s first deposit is large enough to prevent corner cases in which users do not receive shares after making deposits.

Long term, review the list of global invariants to make sure there is no way to break them.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Yearn v2 Vaults |
| Report Date | N/A |
| Finders | Gustavo Grieco, Mike Martel |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/YearnV2Vaults.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/YearnV2Vaults.pdf

### Keywords for Search

`vulnerability`

