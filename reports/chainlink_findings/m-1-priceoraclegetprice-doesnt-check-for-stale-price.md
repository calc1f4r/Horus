---
# Core Classification
protocol: Iron Bank
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19170
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/84
source_link: none
github_link: https://github.com/sherlock-audit/2023-05-ironbank-judging/issues/9

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
finders_count: 69
finders:
  - 0xStalin
  - josephdara
  - ni8mare
  - 0x52
  - santipu\_
---

## Vulnerability Title

M-1: PriceOracle.getPrice doesn't check for stale price

### Overview


This bug report is about the PriceOracle.getPrice function in the IronBank protocol not checking for stale prices. This could cause the protocol to make decisions based on outdated prices, resulting in financial losses. The issue was identified by a group of bug hunters, including 0x3b, 0x52, 0x8chars, 0xHati, 0xStalin, 0xpinky, 3agle, Angry_Mustache_Man, Arabadzhiev, Aymen0909, Bauchibred, BenRai, Bozho, Breeje, Brenzee, BugBusters, CMierez, Delvir0, Diana, Hama, HexHackers, IceBear, Ignite, Jaraxxus, Kodyvim, Kose, Madalad, MohammedRizwan, Norah, Ocean_Sky, Pheonix, Proxy, R-Nemes, Ruhum, Schpiel, SovaSlava, anthony, berlin-101, bin2chen, bitsurfer, branch_indigo, devScrooge, evilakela, gkrastenov, harisnabeel, holyhansss, jayphbee, josephdara, kn0t, kutugu, lil.eth, martin, n33k, ni8mare, plainshift-2, qbs, qpzm, rvierdiiev, saidam017, santipu_, sashik_eth, shaka, shealtielanz, simon135, sl1, thekmj, toshii, tsvetanovv, vagrant. 

The code snippet provided in the report showed that the PriceOracle.getPrice function did not check for freshness of data, which could lead to the protocol making decisions based on outdated prices. The impact of this issue could be bad debt for the protocol. The team used manual review as a tool to identify the issue. 

The recommendation for fixing this issue was to check the round timestamp to make sure the price is not outdated. In the discussion, it was stated that it would not be practical to set up different heartbeats for individual markets, and that the team had a backend to monitor price deviation. It was also suggested that the issue be classified as invalid due to the off-chain system. However, it was pointed

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-05-ironbank-judging/issues/9 

## Found by 
0x3b, 0x52, 0x8chars, 0xHati, 0xStalin, 0xpinky, 3agle, Angry\_Mustache\_Man, Arabadzhiev, Aymen0909, Bauchibred, BenRai, Bozho, Breeje, Brenzee, BugBusters, CMierez, Delvir0, Diana, Hama, HexHackers, IceBear, Ignite, Jaraxxus, Kodyvim, Kose, Madalad, MohammedRizwan, Norah, Ocean\_Sky, Pheonix, Proxy, R-Nemes, Ruhum, Schpiel, SovaSlava, anthony, berlin-101, bin2chen, bitsurfer, branch\_indigo, devScrooge, evilakela, gkrastenov, harisnabeel, holyhansss, jayphbee, josephdara, kn0t, kutugu, lil.eth, martin, n33k, ni8mare, plainshift-2, qbs, qpzm, rvierdiiev, saidam017, santipu\_, sashik\_eth, shaka, shealtielanz, simon135, sl1, thekmj, toshii, tsvetanovv, vagrant
## Summary
PriceOracle.getPrice doesn't check for stale price. As result protocol can make decisions based on not up to date prices, which can cause loses.
## Vulnerability Detail
`PriceOracle.getPrice` function is going to provide asset price using chain link price feeds.
https://github.com/sherlock-audit/2023-05-ironbank/blob/main/ib-v2/src/protocol/oracle/PriceOracle.sol#L66-L72
```soldiity
    function getPriceFromChainlink(address base, address quote) internal view returns (uint256) {
        (, int256 price,,,) = registry.latestRoundData(base, quote);
        require(price > 0, "invalid price");

        // Extend the decimals to 1e18.
        return uint256(price) * 10 ** (18 - uint256(registry.decimals(base, quote)));
    }
```
This function doesn't check that prices are up to date. Because of that it's possible that price is not outdated which can cause financial loses for protocol.
## Impact
Protocol can face bad debt.
## Code Snippet
Provided above
## Tool used

Manual Review

## Recommendation
You need to check that price is not outdated by checking round timestamp.



## Discussion

**ibsunhub**

Same with the answer to #25.
It's not practical to setup different heartbeat for individual markets. And we have a backend to monitor the price deviation.

**0xffff11**

Due to the off-chain system by Iron, issue can be a low. (Does not really affect the current state of the contracts) @ibsunhub Is it the right resolution, or thinking more about invalid?

**ib-tycho**

We still think this is invalid, thanks

**0xffff11**

Because Iron's off-chain safeguard, invalid

**bzpassersby**

Escalate for 10 USDC
I think this is wrongly classified as invalid. 
(1) It's impossible for Watsons to know that the protocol has off-chain safeguards because the protocol explicitly said there are no off-chain mechanisms in the contest info. It's unfair for Watsons who might be misled by this answer.
```
Q: Are there any off-chain mechanisms or off-chain procedures for the protocol (keeper bots, input validation expectations, etc)?
nope
```
(2)It's right and should be encouraged for Watsons to point-out insufficient on-chain checks. The current code ignores any data freshness-related variables when consuming chainlink data, which is clearly not the best practice. 

And it's understandable that the protocol chose to implement such checks off-chain. But since Watsons wouldn't have known about this and that the code itself clearly has flaws. This should be at least low/informational. It's unfair for Watsons to be punished because of this. 

**sherlock-admin**

 > Escalate for 10 USDC
> I think this is wrongly classified as invalid. 
> (1) It's impossible for Watsons to know that the protocol has off-chain safeguards because the protocol explicitly said there are no off-chain mechanisms in the contest info. It's unfair for Watsons who might be misled by this answer.
> ```
> Q: Are there any off-chain mechanisms or off-chain procedures for the protocol (keeper bots, input validation expectations, etc)?
> nope
> ```
> (2)It's right and should be encouraged for Watsons to point-out insufficient on-chain checks. The current code ignores any data freshness-related variables when consuming chainlink data, which is clearly not the best practice. 
> 
> And it's understandable that the protocol chose to implement such checks off-chain. But since Watsons wouldn't have known about this and that the code itself clearly has flaws. This should be at least low/informational. It's unfair for Watsons to be punished because of this. 

You've created a valid escalation for 10 USDC!

To remove the escalation from consideration: Delete your comment.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**hrishibhat**

Result:
Medium
Has Duplicates
Considering this a valid medium 

**sherlock-admin**

Escalations have been resolved successfully!

Escalation status:
- [bzpassersby](https://github.com/sherlock-audit/2023-05-ironbank-judging/issues/9/#issuecomment-1608200147): accepted

**Josephdara**

Hi @hrishibhat @sherlock-admin 
I believe my issue has been omitted
https://github.com/sherlock-audit/2023-05-ironbank-judging/issues/471#issue-1751647942

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Iron Bank |
| Report Date | N/A |
| Finders | 0xStalin, josephdara, ni8mare, 0x52, santipu\_, CMierez, qpzm, toshii, tsvetanovv, 0xHati, branch\_indigo, shaka, qbs, lil.eth, Breeje, SovaSlava, Delvir0, vagrant, R-Nemes, Pheonix, MohammedRizwan, saidam017, BugBusters, Norah, Brenzee, Angry\_Mustache\_Man, Schpiel, shealtielanz, simon135, jayphbee, Kose, Diana, Kodyvim, Ruhum, Aymen0909, anthony, 0xpinky, harisnabeel, Madalad, 0x3b, Arabadzhiev, Hama, sl1, gkrastenov, plainshift-2, Bauchibred, 0x8chars, Ocean\_Sky, kn0t, Ignite, 3agle, IceBear, devScrooge, Proxy, martin, kutugu, n33k, HexHackers, bin2chen, berlin-101, Bozho, Jaraxxus, bitsurfer, holyhansss, thekmj, evilakela, sashik\_eth, rvierdiiev, BenRai |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-05-ironbank-judging/issues/9
- **Contest**: https://app.sherlock.xyz/audits/contests/84

### Keywords for Search

`vulnerability`

