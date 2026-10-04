---
# Core Classification
protocol: Buffer Finance
chain: everychain
category: uncategorized
vulnerability_type: erc4626

# Attack Vector Details
attack_type: erc4626
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3626
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/24
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-buffer-judging/issues/81

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.70
financial_impact: high

# Scoring
quality_score: 3.5
rarity_score: 4

# Context Tags
tags:
  - erc4626
  - initial_deposit

protocol_categories:
  - dexes
  - yield
  - services
  - yield_aggregator
  - options_vault

# Audit Details
report_date: unknown
finders_count: 9
finders:
  - 0x52
  - cccz
  - joestakey
  - Ruhum
  - hansfriese
---

## Vulnerability Title

H-3: Early depositors to BufferBinaryPool can manipulate exchange rates to steal funds from later depositors

### Overview


This bug report is about an issue found in the BufferBinaryPool contract which allows early depositors to manipulate exchange rates to steal funds from later depositors. The exchange rate is calculated using the total supply of shares and the totalTokenXBalance, which leaves it vulnerable to manipulation. An adversary can mint a single share, then donate a large amount of tokenX to the vault to grossly manipulate the share price. When later depositors deposit into the vault they will lose value due to precision loss and the adversary will profit. The impact of this vulnerability is that the adversary can effectively steal funds from later users through precision loss. The bug was found manually and the recommendation is to require a small minimum deposit (e.g. 1e6). The issue has been discussed and a solution has been proposed.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-buffer-judging/issues/81 

## Found by 
dipp, gandu, rvierdiiev, Ruhum, hansfriese, cccz, 0x52, ctf\_sec, joestakey

## Summary

To calculate the exchange rate for shares in BufferBinaryPool it divides the total supply of shares by the totalTokenXBalance of the vault. The first deposit can mint a very small number of shares then donate tokenX to the vault to grossly manipulate the share price. When later depositor deposit into the vault they will lose value due to precision loss and the adversary will profit.

## Vulnerability Detail

    function totalTokenXBalance()
        public
        view
        override
        returns (uint256 balance)
    {
        return tokenX.balanceOf(address(this)) - lockedPremium;
    }

Share exchange rate is calculated using the total supply of shares and the totalTokenXBalance, which leaves it vulnerable to exchange rate manipulation. As an example, assume tokenX == USDC. An adversary can mint a single share, then donate 1e8 USDC. Minting the first share established a 1:1 ratio but then donating 1e8 changed the ratio to 1:1e8. Now any deposit lower than 1e8 (100 USDC) will suffer from precision loss and the attackers share will benefit from it.

## Impact

Adversary can effectively steal funds from later users through precision loss

## Code Snippet

https://github.com/sherlock-audit/2022-11-buffer/blob/main/contracts/contracts/core/BufferBinaryPool.sol#L405-L412

## Tool used

Manual Review

## Recommendation

Require a small minimum deposit (i.e. 1e6) 

## Discussion

**bufferfinance**

We'll add the initial liquidity and then burn those LP tokens.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3.5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Buffer Finance |
| Report Date | N/A |
| Finders | 0x52, cccz, joestakey, Ruhum, hansfriese, dipp, gu, rvierdiiev, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-buffer-judging/issues/81
- **Contest**: https://app.sherlock.xyz/audits/contests/24

### Keywords for Search

`ERC4626, Initial Deposit`

