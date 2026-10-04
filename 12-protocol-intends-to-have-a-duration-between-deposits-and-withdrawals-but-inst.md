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
solodit_id: 33487
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

[12] Protocol intends to have a duration between deposits and withdrawals but instead hardcodes this to `0`

### Overview

See description below for full details.

### Original Finding Content


https://github.com/code-423n4/2024-04-dyad/blob/4a987e536576139793a1c04690336d06c93fca90/src/core/VaultManagerV2.sol#L138-L163

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

Evidently, as hinted by the `@audit` tag, we can see that protocol intends to apply a duration logic. After discussions with the sponsor, this check is placed so as not to allow the kerosene price to be manipulated; however, this check is not really sufficient as it doesn't have any waiting duration. This means that a user can just deposit and withdraw in the next block allowing them to still game the system with a 12 second wait time.

### Impact

Check can easily be sidestepped in 12 seconds (block mining duration).

### Recommended Mitigation Steps

Consider having a waiting period whenever attempting to withdraw, i.e., apply this pseudo fix [here](https://github.com/code-423n4/2024-04-dyad/blob/4a987e536576139793a1c04690336d06c93fca90/src/core/VaultManagerV2.sol#L138-L163).

```diff

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
-    if (idToBlockOfLastDeposit[id] == block.number) revert DepositedInSameBlock();
+    if (idToBlockTimestampOfLastDeposit[id] + WAITING_DURATION < block.timestamp) revert DepositedForTooShortDuration();
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

*Note: For full discussion, see [here](https://github.com/code-423n4/2024-04-dyad-findings/issues/725).*

***



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

