---
# Core Classification
protocol: Sparkn
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27425
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/cllcnja1h0001lc08z7w0orxx
source_link: none
github_link: https://github.com/Cyfrin/2023-08-sparkn

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
finders_count: 65
finders:
  - RugpullDetector
  - bronzepickaxe
  - 0xRizwan
  - sm4rty
  - 0x4ka5h
---

## Vulnerability Title

If a winner is blacklisted on any of the tokens they can't receive their funds

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-08-sparkn/blob/0f139b2dc53905700dd29a01451b330f829653e9/src/Distributor.sol#L144-L150">https://github.com/Cyfrin/2023-08-sparkn/blob/0f139b2dc53905700dd29a01451b330f829653e9/src/Distributor.sol#L144-L150</a>




## Summary

Normally this would be a big issue since transfers are done in a loop to all winners _i.e all winners wouldn't be able to get their tokens_, but winners are chosen off chain and from [the Q&A section of SparkN onboarding video](https://www.youtube.com/watch?v=_VqXB1t9Evo) we can see that after picking a set of winners they can later on be changed, that's the set of winners.
This means that, reasonably, after an attempt to send the tokens to winners has been made and it reverts due to one or a few of the users being in the blacklist/blocklist of USDC/USDT, the set of winners can just be re-chosen without the blacklisted users, now whereas that helps other users from having their funds locked in the contract, this unfairly means that the blacklisted users would lose their earned tokens, since their share must be re-shared to other winners to cause [this](https://github.com/Cyfrin/2023-08-sparkn/blob/0f139b2dc53905700dd29a01451b330f829653e9/src/Distributor.sol#L134-L137) not to revert

```solidity
        if (totalPercentage != (10000 - COMMISSION_FEE)) {
            revert Distributor__MismatchedPercentages();
        }
```

## Vulnerability Detail

See summary

Additionally note that, the contest readMe's section has indicated that that general stablecoins would be used... _specifically hinting USDC, DAI, USDT & JPYC_,

Now important is to also keep in mind that https://github.com/d-xo/weird-erc20#tokens-with-blocklists shows that:

> Some tokens (e.g. USDC, USDT) have a contract level admin controlled address blocklist. If an address is blocked, then transfers to and from that address are forbidden.


## Impact

Two impacts, depending on how SparkN decides to sort this out, either:

- All winners funds ends up stuck in contract if sparkN doesn't want to change the percentages of each winner by setting that of blacklisted users to zero and sharing their percentages back in the pool

- Some users would have their funds unfairly given to other users

## Tool used

Manual Audit

## Recommendation

Consider introducing a functionality that allows winners to specify what address they'd like to be paid, that way even a blocklisted account can specify a different address he/she owns, this case also doesn't really sort this as an attacker could just send any blacklisted address to re-grief the whole thing, so a pull over push method could be done to transfer rewards to winners

### Additional Note

With this attack window in mind, if a pull method is going to be used then the `_commisionTransfer()` function needs to be refactored to only send the commision.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Sparkn |
| Report Date | N/A |
| Finders | RugpullDetector, bronzepickaxe, 0xRizwan, sm4rty, 0x4ka5h, SanketKogekar, kamui, tsvetanovv, arnie, trachev, B353N, alymurtazamemon, Infect3d, 0xdraiakoo, 0xsandy, Chinmay, Tripathi, Polaristow, carrotsmuggler, InAllHonesty, 0xyPhilic, Maroutis, ke1caM, golanger85, aslanbek, Alhakista, kaliberpoziomka, kodyvim, ohi0b, VanGrim, 0xMosh, 0xlucky, deadrosesxyz, 0xhals, Cosine, radeveth, Bauer, Deivitto, crippie, Kose, Stoicov, smbv1923, Madalad, 0x3b, Arabadzhiev, Bauchibred, castleChain, dontonka, 33audits, simeonk, Proxy, pep7siup, tsar, Giorgio, Scoffield, MrjoryStewartBaxter, thekmj, ubermensch, Lalanda, 0xScourgedev, 0xarno, ZedBlockchain, oualidpro, honeymewn, TorpedopistolIxc41 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-08-sparkn
- **Contest**: https://www.codehawks.com/contests/cllcnja1h0001lc08z7w0orxx

### Keywords for Search

`vulnerability`

