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
solodit_id: 27594
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
finders_count: 5
finders:
  - marqymarq10
  - pontifex
  - hash
  - rvierdiiev
  - 0xanmol
---

## Vulnerability Title

The protocol will mint unnecessary fees if the vault is paused and reopened later.

### Overview


This bug report is about an issue with the protocol used in the SteadeFi vault. If the vault is paused and then reopened later, the protocol will mint unnecessary fees to the treasury. This can result in a loss of user shares for the duration when the vault was not active. 

The severity of the impact depends on the fee the protocol charges per second, the totalSupply of vault tokens, and the duration of the vault being paused. The bug was found by manual review and the recommended solution is to have a function to override the lastFeeCollected variable with the current block timestamp when the vault is reopened.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXReader.sol#L38">https://github.com/Cyfrin/2023-10-SteadeFi/blob/0f909e2f0917cb9ad02986f631d622376510abec/contracts/strategy/gmx/GMXReader.sol#L38</a>


## Summary
Unnecessary fees will be minted to the treasury if the vault is paused and reopened later. 
## Vulnerability Details
Based on the test results, the protocol mints 5(this can be more) wei(gvToken) for each `gvToken` every second since the last fee collection. For example, if the `totalSupply` of `gvToken` is 1000000e18 and the time difference between the current block and the last fee collection is 10 seconds, the amount of lp tokens minted as a fee will be ***50000000*** wei in terms of `gvToken`. This is acceptable when the protocol is functioning properly.

```js
function pendingFee(GMXTypes.Store storage self) public view returns (uint256) {
        uint256 totalSupply_ = IERC20(address(self.vault)).totalSupply();
        uint256 _secondsFromLastCollection = block.timestamp - self.lastFeeCollected;
        return (totalSupply_ * self.feePerSecond * _secondsFromLastCollection) / SAFE_MULTIPLIER;
    }
```
However, if the protocol needs to be paused due to a hack or other issues, and then the vault is reopened, let's say after 1 month of being paused, the time difference from `block.timestamp - _secondsFromLastCollection` will be = ***2630000s***

If the first user tries to deposit after the vault reopens, the fees charged will be 1000000e18 * 5 * 2630000 / 1e18 = ***1315000000000***

This is an unnecessary fee generated for the treasury because the vault was paused for a long time, but the fee is still generated without taking that into account. This can result in the treasury consuming a portion of the user shares.
## Impact
This will lead to a loss of user shares for the duration when the vault was not active. The severity of the impact depends on the fee the protocol charges per second, the totalSupply of vault tokens, and the duration of the vault being paused.

## Tools Used
manual review

## Recommendations
If the vault is being reopened, there should be a function to override the _store.lastFeeCollected = block.timestamp; with block.timestamp again.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | SteadeFi |
| Report Date | N/A |
| Finders | marqymarq10, pontifex, hash, rvierdiiev, 0xanmol |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-10-SteadeFi
- **Contest**: https://www.codehawks.com/contests/clo38mm260001la08daw5cbuf

### Keywords for Search

`vulnerability`

