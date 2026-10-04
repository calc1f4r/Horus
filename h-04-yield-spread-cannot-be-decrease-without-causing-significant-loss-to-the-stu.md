---
# Core Classification
protocol: Stusdcxbloom
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55676
audit_firm: 0x52
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - @IAm0x52
---

## Vulnerability Title

[H-04] Yield spread cannot be decrease without causing significant loss to the stUSDC pool

### Overview


This bug report discusses an issue with the calculation of the value of tbys in the StUsdc contract. The problem lies in the fact that the rate used to calculate the value is dependent on the spread, which can be changed at any time by the owner. This means that any adjustment to the spread would lead to a retroactive change in the valuation of all tbys, causing a sudden change in the value of the stUSDC pool and potentially causing losses for stUSDC holders. The recommended solution is to cache the spread during the creation of the tby, and this has been implemented in a recent pull request.

### Original Finding Content

**Details**

[StUsdc.sol#L313-L324](https://github.com/stakeup-protocol/stakeup-contracts/blob/b4d8a83e9455efb8c7543a0fc62b5aea598c7f49/src/token/StUsdc.sol#L313-L324)

    function _liveTbyValue(IBloomPool pool) internal view returns (uint256 value) {
        uint256 startingId = lastRedeemedTbyId();
        // Because we start at type(uint256).max, we need to increment and overflow to 0.
        unchecked {
            startingId++;
        }
        uint256 lastMintedId = pool.lastMintedId();
        if (lastMintedId == type(uint256).max) return 0;
        for (uint256 i = startingId; i <= lastMintedId; ++i) {
            value += pool.getRate(i).mulWad(_tby.balanceOf(address(this), i)); <- @audit rate pulled from bloomPool.sol
        }
    }

[BloomPool.sol#L476-L492](https://github.com/Blueberryfi/bloom-v2/blob/87a60380331cc914be41ad57691f08b532a4d6fb/src/BloomPool.sol#L476-L492)

    function getRate(uint256 id) public view override returns (uint256) {
        TbyMaturity memory maturity = _idToMaturity[id];
        RwaPrice memory rwaPrice = _tbyIdToRwaPrice[id];


        if (rwaPrice.startPrice == 0) {
            revert Errors.InvalidTby();
        }
        // If the TBY has not started accruing interest, return 1e18.
        if (block.timestamp <= maturity.start) {
            return Math.WAD;
        }


        // If the TBY has matured, and is eligible for redemption, calculate the rate based on the end price.
        uint256 price = rwaPrice.endPrice != 0 ? rwaPrice.endPrice : _rwaPrice();
        uint256 rate = (uint256(price).divWad(uint256(rwaPrice.startPrice)));
        return _takeSpread(rate); <- @audit rate is dependent on spread
    }

When the value of the tbys are calculated, the rate is adjusted by the current spread specified. The issue is that the spread can be changed at any time by the owner. Since spread is a contract wide variable, rather than tby specific, any adjustment would lead to a retroactive change in the valuation of all tbys. The result is that any change to this value would lead to a sudden change in the valuation of the tbys and by extend the value of the stUSDC pool. Decreasing it would cause a large loss to all stUSDC holders.

**Lines of Code**

[PoolStorage.sol#L149-L151](https://github.com/Blueberryfi/bloom-v2/blob/87a60380331cc914be41ad57691f08b532a4d6fb/src/PoolStorage.sol#L149-L151)

**Recommendation**

\_spread should be cached during the creation of the tby.

**Remediation**

Fixed as recommended in bloom-v2 [PR#20](https://github.com/Blueberryfi/bloom-v2/pull/20). \_spread is now cached in the rwaPrice struct for each tby upon creation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | 0x52 |
| Protocol | Stusdcxbloom |
| Report Date | N/A |
| Finders | @IAm0x52 |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

