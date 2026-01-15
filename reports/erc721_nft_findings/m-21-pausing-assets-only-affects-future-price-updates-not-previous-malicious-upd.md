---
# Core Classification
protocol: ParaSpace
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16004
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-paraspace-contest
source_link: https://code4rena.com/reports/2022-11-paraspace
github_link: https://github.com/code-423n4/2022-11-paraspace-findings/issues/490

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
  - dexes
  - cdp
  - services
  - cross_chain
  - indexes

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Trust
  - pashov
---

## Vulnerability Title

[M-21] Pausing assets only affects future price updates, not previous malicious updates

### Overview


This bug report is about a vulnerability in the NFTFloorOracle contract, which is used to retrieve ERC721 prices for ParaSpace. The contract is pausable by admin on a per asset level using setPause(asset, flag). The setPrice function will not be callable when an asset is paused, however the getPrice() function is unaffected by the pause flag. This is a dangerous behavior, because it means that there will be a 6 hour period when the current price is treated as valid, even though the asset is intended to be on lockdown. The impact of this vulnerability is that pauses only affect future price updates, not previous malicious updates. The tools used to find this vulnerability were manual audit. The recommended mitigation step is to add whenNotPaused to the getPrice() function as well.

### Original Finding Content


<https://github.com/code-423n4/2022-11-paraspace/blob/c6820a279c64a299a783955749fdc977de8f0449/paraspace-core/contracts/misc/NFTFloorOracle.sol#L236>

NFTFloorOracle retrieves ERC721 prices for ParaSpace. It is pausable by admin on a per asset level using setPause(asset, flag).
setPrice will not be callable when asset is paused:

    function setPrice(address _asset, uint256 _twap)
        public
        onlyRole(UPDATER_ROLE)
        onlyWhenAssetExisted(_asset)
        whenNotPaused(_asset)

However, getPrice() is unaffected by the pause flag. This is really dangerous behavior, because there will be 6 hours when the current price treated as valid, although the asset is clearly intended to be on lockdown.

Basically, pauses are only forward facing, and whatever happened is valid. But, if we want to pause an asset, something fishy has already occured, or will occur by the time setPause() is called. So, "whatever happened happened" mentality is overly dangerous.

### Impact

Pausing assets only affects future price updates, not previous malicious updates.

### Recommended Mitigation Steps

Add whenNotPaused to getPrice() function as well.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | ParaSpace |
| Report Date | N/A |
| Finders | Trust, pashov |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-paraspace
- **GitHub**: https://github.com/code-423n4/2022-11-paraspace-findings/issues/490
- **Contest**: https://code4rena.com/contests/2022-11-paraspace-contest

### Keywords for Search

`vulnerability`

