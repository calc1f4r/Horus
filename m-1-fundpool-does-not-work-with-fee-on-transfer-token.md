---
# Core Classification
protocol: Allo V2
chain: everychain
category: uncategorized
vulnerability_type: fee_on_transfer

# Attack Vector Details
attack_type: fee_on_transfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27133
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/109
source_link: none
github_link: https://github.com/sherlock-audit/2023-09-Gitcoin-judging/issues/19

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
  - fee_on_transfer

protocol_categories:
  - services

# Audit Details
report_date: unknown
finders_count: 54
finders:
  - JP\_Courses
  - inspecktor
  - 0xdeadbeef
  - imsrybr0
  - inzinko
---

## Vulnerability Title

M-1: `fundPool` does not work with fee-on-transfer token

### Overview


A bug was found in the `fundPool` function of the Allo Protocol, which does not work with fee-on-transfer tokens. The bug was found by a group of people including 0x1337, 0x180db, 0x6980, 0xHelium, 0xMosh, 0xbepresent, 0xdeadbeef, 0xgoat, Aamirusmani1552, ArmedGoose, AsenXDeth, BenRai, DevABDee, Inspex, JP_Courses, Kodyvim, Kow, Martians, Proxy, Tri-pathi, Vagner, WATCHPUG, ace13567, adeolu, alexzoid, ashirleyshe, ast3ros, cats, detectiveking, foresthalberd, grearlake, imsrybr0, inspecktor, inzinko, lealCodes, lemonmon, lil.eth, marchev, nobody2018, osmanozdemir1, p0wd3r, parsely, pavankv241, pengun, pontifex, qbs, rvierdiiev, seeques, shtesesamoubiq, theclonedtyroneidgafmf, trevorjudice, tsvetanovv, vagrant, xAriextz.

The bug is related to the parameter for `increasePoolAmount` in `_fundPool`, which is directly the amount used in the `transferFrom` call. This means that when the `_token` is a fee-on-transfer token, the actual amount transferred to `_strategy` will be less than `amountAfterFee`. This can lead to a recorded balance that is greater than the actual balance.

The bug was identified through Manual Review and the code snippet can be found at https://github.com/sherlock-audit/2023-09-Gitcoin/blob/main/allo-v2/contracts/core/Allo.sol#L516-L517.

The recommended solution to this bug is to use the change in `_token` balance as the parameter for `increasePoolAmount`. This was fixed by the user MLON33 in https://github.com/allo-protocol/allo-v2/pull

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-09-Gitcoin-judging/issues/19 

## Found by 
0x1337, 0x180db, 0x6980, 0xHelium, 0xMosh, 0xbepresent, 0xdeadbeef, 0xgoat, Aamirusmani1552, ArmedGoose, AsenXDeth, BenRai, DevABDee, Inspex, JP\_Courses, Kodyvim, Kow, Martians, Proxy, Tri-pathi, Vagner, WATCHPUG, ace13567, adeolu, alexzoid, ashirleyshe, ast3ros, cats, detectiveking, foresthalberd, grearlake, imsrybr0, inspecktor, inzinko, lealCodes, lemonmon, lil.eth, marchev, nobody2018, osmanozdemir1, p0wd3r, parsely, pavankv241, pengun, pontifex, qbs, rvierdiiev, seeques, shtesesamoubiq, theclonedtyroneidgafmf, trevorjudice, tsvetanovv, vagrant, xAriextz
## Vulnerability Detail
In `_fundPool`, the parameter for `increasePoolAmount` is directly the amount used in the `transferFrom` call.

https://github.com/sherlock-audit/2023-09-Gitcoin/blob/main/allo-v2/contracts/core/Allo.sol#L516-L517
```solidity
        _transferAmountFrom(_token, TransferData({from: msg.sender, to: address(_strategy), amount: amountAfterFee}));
        _strategy.increasePoolAmount(amountAfterFee);
```

When `_token` is a fee-on-transfer token, the actual amount transferred to `_strategy` will be less than `amountAfterFee`. Therefore, the current approach could lead to a recorded balance that is greater than the actual balance.
## Impact
`fundPool` does not work with fee-on-transfer token
## Code Snippet
https://github.com/sherlock-audit/2023-09-Gitcoin/blob/main/allo-v2/contracts/core/Allo.sol#L516-L517
## Tool used

Manual Review

## Recommendation
Use the change in `_token` balance as the parameter for `increasePoolAmount`.



## Discussion

**MLON33**

https://github.com/allo-protocol/allo-v2/pull/355

**quentin-abei**

Should consider choosing this issue for report : 
[30](https://github.com/sherlock-audit/2023-09-Gitcoin-judging/issues/30)
It's better detailed and have an actual working coded PoC

**jack-the-pug**

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Allo V2 |
| Report Date | N/A |
| Finders | JP\_Courses, inspecktor, 0xdeadbeef, imsrybr0, inzinko, Aamirusmani1552, p0wd3r, Inspex, theclonedtyroneidgafmf, lealCodes, pontifex, seeques, ace13567, trevorjudice, DevABDee, WATCHPUG, tsvetanovv, 0x180db, qbs, nobody2018, lil.eth, detectiveking, cats, grearlake, Tri-pathi, Martians, vagrant, 0xHelium, marchev, lemonmon, Vagner, 0xMosh, pavankv241, ast3ros, 0xgoat, ashirleyshe, 0x6980, 0xbepresent, parsely, Kodyvim, alexzoid, 0x1337, osmanozdemir1, ArmedGoose, shtesesamoubiq, Proxy, pengun, adeolu, Kow, foresthalberd, AsenXDeth, xAriextz, rvierdiiev, BenRai |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-09-Gitcoin-judging/issues/19
- **Contest**: https://app.sherlock.xyz/audits/contests/109

### Keywords for Search

`Fee On Transfer`

