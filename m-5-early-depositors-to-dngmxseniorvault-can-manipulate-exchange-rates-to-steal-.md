---
# Core Classification
protocol: Rage Trade
chain: everychain
category: arithmetic
vulnerability_type: rounding

# Attack Vector Details
attack_type: rounding
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3517
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/16
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-rage-trade-judging/issues/37

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - rounding
  - first_depositor_issue

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 10
finders:
  - clems4ever
  - 0x52
  - cccz
  - joestakey
  - tives
---

## Vulnerability Title

M-5: Early depositors to DnGmxSeniorVault can manipulate exchange rates to steal funds from later depositors

### Overview


A bug has been identified in the code for DnGmxSeniorVault that could allow an early depositor to manipulate exchange rates to steal funds from later depositors. This is because the exchange rate for shares is calculated using the total supply of shares and the totalAsset. If the first deposit is a very small number of shares then an adversary can donate aUSDC to the vault to grossly manipulate the share price, resulting in later depositors losing value due to precision loss while the adversary profits. The same issue is present in DnGmxJuniorVault. In order to protect against this, a guarded launch process should be implemented that safeguards the first deposit and prevents it from being manipulated. This will ensure that later depositors are not adversely affected.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-rage-trade-judging/issues/37 

## Found by 
rvierdiiev, tives, peanuts, joestakey, cccz, ctf\_sec, \_\_141345\_\_, 0x52, GimelSec, clems4ever

## Summary

To calculate the exchange rate for shares in DnGmxSeniorVault it divides the total supply of shares by the totalAssets of the vault. The first deposit can mint a very small number of shares then donate aUSDC to the vault to grossly manipulate the share price. When later depositor deposit into the vault they will lose value due to precision loss and the adversary will profit.

## Vulnerability Detail

    function convertToShares(uint256 assets) public view virtual returns (uint256) {
        uint256 supply = totalSupply(); // Saves an extra SLOAD if totalSupply is non-zero.

        return supply == 0 ? assets : assets.mulDivDown(supply, totalAssets());
    }

Share exchange rate is calculated using the total supply of shares and the totalAsset. This can lead to exchange rate manipulation. As an example, an adversary can mint a single share, then donate 1e8 aUSDC. Minting the first share established a 1:1 ratio but then donating 1e8 changed the ratio to 1:1e8. Now any deposit lower than 1e8 (100 aUSDC) will suffer from precision loss and the attackers share will benefit from it.

This same vector is present in DnGmxJuniorVault.

## Impact

Adversary can effectively steal funds from later users

## Code Snippet

https://github.com/sherlock-audit/2022-10-rage-trade/blob/main/dn-gmx-vaults/contracts/vaults/DnGmxSeniorVault.sol#L211-L221

## Tool used

Manual Review

## Recommendation

Initialize should include a small deposit, such as 1e6 aUSDC that mints the share to a dead address to permanently lock the exchange rate:

        aUsdc.approve(address(pool), type(uint256).max);
        IERC20(asset).approve(address(pool), type(uint256).max);

    +   deposit(1e6, DEAD_ADDRESS);

## Discussion

**0xDosa**

We will ensure a guarded launch process that safeguards the first deposit to avoid being manipulated.

**Evert0x**

We are still considering it a valid issue as the guarded launch process is out of scope.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Sherlock |
| Protocol | Rage Trade |
| Report Date | N/A |
| Finders | clems4ever, 0x52, cccz, joestakey, tives, \_\_141345\_\_, peanuts, rvierdiiev, GimelSec, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-rage-trade-judging/issues/37
- **Contest**: https://app.sherlock.xyz/audits/contests/16

### Keywords for Search

`Rounding, First Depositor Issue`

