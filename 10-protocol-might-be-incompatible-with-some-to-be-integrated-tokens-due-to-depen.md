---
# Core Classification
protocol: DYAD
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33485
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-dyad
source_link: https://code4rena.com/reports/2024-04-dyad
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[10] Protocol might be incompatible with some to-be integrated tokens due to dependency on `.decimals()` during withdrawal attempts

### Overview

See description below for full details.

### Original Finding Content


https://github.com/code-423n4/2024-04-dyad/blob/4a987e536576139793a1c04690336d06c93fca90/src/core/VaultManagerV2.sol#L137-L158

```solidity
  function withdraw(
    uint    id,
    address vault,
    uint    amount,
    address to
  )
    public
      isDNftOwner(id)
  {
    //@audit
    if (idToBlockOfLastDeposit[id] == block.number) revert DepositedInSameBlock();
    uint dyadMinted = dyad.mintedDyad(address(this), id);
    Vault _vault = Vault(vault);
    uint value = amount * _vault.assetPrice()
                  * 1e18
                  / 10**_vault.oracle().decimals()
                  / 10**_vault.asset().decimals();
    if (getNonKeroseneValue(id) - value < dyadMinted) revert NotEnoughExoCollat();
    _vault.withdraw(id, to, amount);
    if (collatRatio(id) < MIN_COLLATERIZATION_RATIO)  revert CrTooLow();
  }
```

We can see that whenever there is a need to withdraw, protocol queries the `asset.decimals()` for the underlying asset; however, some very popular ERC20 that might be used as assets, do not support the `.decimals()`format and as such this attempt at withdrawal would always revert for these tokens

### Impact

Specific assets would not work with protocol as it directly attempts to call `asset().decimals()`, which would revert since the functionality is non-existent for that token; leading to deposits to be completely locked in the vaults since withdrawals can't be processed and during deposits no query to `.decimals()` are being made.

### Recommended Mitigation Steps

Consider try/catching the logic or outrightly not supporting these tokens.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | DYAD |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-dyad
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-04-dyad

### Keywords for Search

`vulnerability`

