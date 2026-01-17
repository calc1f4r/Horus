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
solodit_id: 33481
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

[06] `dNFT` owners can liquidate themselves

### Overview

See description below for full details.

### Original Finding Content


https://github.com/code-423n4/2024-04-dyad/blob/4a987e536576139793a1c04690336d06c93fca90/src/core/VaultManagerV2.sol#L214-L240

```solidity
  function liquidate(
    uint id,
    uint to
  )
    external
      isValidDNft(id)
      isValidDNft(to)
    {
      uint cr = collatRatio(id);
      if (cr >= MIN_COLLATERIZATION_RATIO) revert CrTooHigh();
      dyad.burn(id, msg.sender, dyad.mintedDyad(address(this), id));

      uint cappedCr               = cr < 1e18 ? 1e18 : cr;
      uint liquidationEquityShare = (cappedCr - 1e18).mulWadDown(LIQUIDATION_REWARD);
      uint liquidationAssetShare  = (liquidationEquityShare + 1e18).divWadDown(cappedCr);

      uint numberOfVaults = vaults[id].length();
      for (uint i = 0; i < numberOfVaults; i++) {
          Vault vault      = Vault(vaults[id].at(i));
          uint  collateral = vault.id2asset(id).mulWadUp(liquidationAssetShare);
          vault.move(id, to, collateral);
      }
      emit Liquidate(id, msg.sender, to);
  }
```

This function is used to liquidate a dNFT that's currently underwater, i.e. whose collateral ratio is less than `MIN_COLLATERIZATION_RATIO` which is `150%`; however, this attempt does not check to ensure that the `to` address is not the current owner of the `dNFT` that's to be liquidated. This then allows any user whose position goes underwater to instead of bringing back their positions afloat just liquidate themselves.

### Impact

Some `dNFT` owners can attempt gaming the system by liquidating themselves instead of getting their positions back afloat when it's profitable to do so.

### Recommended Mitigation Steps

Consider checking that the position to be liquidated is not owned by the liquidator who's liquidating it.



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

