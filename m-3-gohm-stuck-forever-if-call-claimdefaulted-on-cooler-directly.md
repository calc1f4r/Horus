---
# Core Classification
protocol: Cooler Update
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26359
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/107
source_link: none
github_link: https://github.com/sherlock-audit/2023-08-cooler-judging/issues/46

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
finders_count: 4
finders:
  - jkoppel
  - detectiveking
  - evilakela
  - castle\_chain
---

## Vulnerability Title

M-3: gOhm stuck forever if call claimDefaulted on Cooler directly

### Overview


This bug report is about an issue found in the codebase of the Cooler project. The issue is that anyone can call the Cooler.claimDefaulted function to transfer gOhm (a type of token) to the Clearinghouse, but there is no way to recover or burn it. This could potentially lead to the gOhm being stolen using an exploit in the code. 

The bug was found by castle_chain, detectiveking, evilakela, and jkoppel. The code snippet provided in the report shows the Cooler.claimDefaulted sending the collateral to the lender, and the Clearinghouse.onDefault doing nothing. The Clearinghouse.defund() function cannot be used to send the gOhm back to the treasury.

The impact of the bug is that anyone can easily make all defaulted gOhm get stuck forever.

The discussion section of the report shows that the bug is not a duplicate of another bug, but it is not considered to be a big deal. 0xRusowsky suggested that the severity should be at max a medium and proposed to add a permissionless burn function. Finally, jkoppel approved the fix.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-08-cooler-judging/issues/46 

## Found by 
castle\_chain, detectiveking, evilakela, jkoppel

Anyone can call Cooler.claimDefaulted. If this is done for a loan owned by the Clearinghouse, the gOhm is sent to the Clearinghouse, but there is no way to recover or burn it.

## Vulnerability Detail

1. Bob calls `Clearinghouse.lendToCooler` to make a loan collateralized by 1000 gOhm.
2. Bob defaults on the loan
3.  Immediately after default, Eve calls `Cooler.claimDefaulted` on Bob's loan.
4. The gOhm is transferred to the Clearinghouse
5. There is no way to burn or transfer it. (In fact,  `defund()` can be used to transfer literally any token *except* gOhm back to the treasury.)

However, the gOhm can now be stolen using the exploit in #1, potentially in the same transaction as when Eve called `Cooler.claimDefaulted()`.

## Impact

Anyone can very easily make all defaulted gOhm get stuck forever.

## Code Snippet

`Cooler.claimDefaulted` sends the collateral to the lender, calls `onDefault`

https://github.com/sherlock-audit/2023-08-cooler/blob/main/Cooler/src/Cooler.sol#L325

`Clearinghouse.onDefault` does nothing

https://github.com/sherlock-audit/2023-08-cooler/blob/main/Cooler/src/Clearinghouse.sol#L265

Although `Clearinghouse.defund()` can be used to send any other token back to the treasury, it cannot do so for gOhm

https://github.com/sherlock-audit/2023-08-cooler/blob/main/Cooler/src/Clearinghouse.sol#L340

## Tool used

Manual Review

## Recommendation

Unsure. Perhaps add a flag disabling claiming by anyone other than `loan.lender`? Or just allow `defund()` to be called on gOhm?




## Discussion

**jkoppel**

This is not a duplicate of #28. #28 involves Clearinghouse.claimDefaulted, but this involves Cooler.claimDefaulted.

**Oot2k**

Not a duplicate

**0xRusowsky**

Despite it is not a duplicate, since gOHM would be stuck in CH instead of the being OHM burn. It wouldn't be a big deal (we could ammend the calculations based on that) because it doesn't have any operational/economical impact as long as that supply is removed from the backing calculations.

On top of that, there is an economical incentive to call it from the CH, as the caller is rewarded.

Disagree with severity, imo at max it should be a medium.

Will think about how to deal with it.

**0xRusowsky**

we will finally add a permissionless `burn` function despite this logic is unlikely to happen

**0xRusowsky**

- https://github.com/ohmzeus/Cooler/pull/57

**jkoppel**

Fix approved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Cooler Update |
| Report Date | N/A |
| Finders | jkoppel, detectiveking, evilakela, castle\_chain |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-08-cooler-judging/issues/46
- **Contest**: https://app.sherlock.xyz/audits/contests/107

### Keywords for Search

`vulnerability`

