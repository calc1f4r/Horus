---
# Core Classification
protocol: Sparkn
chain: everychain
category: uncategorized
vulnerability_type: admin

# Attack Vector Details
attack_type: admin
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27424
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/cllcnja1h0001lc08z7w0orxx
source_link: none
github_link: https://github.com/Cyfrin/2023-08-sparkn

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
  - admin

# Audit Details
report_date: unknown
finders_count: 43
finders:
  - Aamirusmani1552
  - KiteWeb3
  - Mlome
  - DevABDee
  - t0x1c
---

## Vulnerability Title

Malicious/Compromised organiser can reclaw all funds, stealing work from supporters

### Overview


This bug report is about a vulnerability in the "Distributor" contract which allows malicious or compromised organizers to reclaim all of the funds from a contest, stealing work from supporters. The vulnerability lies in the fact that there is no input validation on the `winners` array in the `Distributor#_distribute` function, allowing the organizer to pass an array of length one containing a wallet address that they control as the `winners` parameter, and `[10000]` as the `percentages` parameter in order to receive 100% of the funds initially deposited to the contract.

The impact of this vulnerability is that malicious/compromised organizers can refund 100% of the contest funds, stealing work from sponsors. The tools used to identify this vulnerability were manual review.

The recommendation to mitigate this vulnerability is to use a two step procedure for distributing funds. The organizer submits an array of winners and percentages to the `Proxy` contract and they are cached using storage variables. The owner of `ProxyFactor` (a trusted admin) checks the arrays to ensure the organizer is not distributing all of the money to themselves, and if satisfied, triggers the distribution of funds. This removes the risk of having to trust the organizer, and although it requires the trust of the admin, they were already a required trusted party and so the mitigation is beneficial overall.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-08-sparkn/blob/main/src/Distributor.sol#L116">https://github.com/Cyfrin/2023-08-sparkn/blob/main/src/Distributor.sol#L116</a>


## Summary

The contest details state that 'If a contest is created and funded, there is no way to refund. All the funds belong to the persons who wants to help solve the problem, we call them "supporters".' (see More Context section). This is untrue, as the organizer is able to refund all of the contest funds.

## Vulnerability Details

In `Distributor#_distribute`, there is no input validation on the `winners` array. A malicious or compromised organizer can, with little effort, simply pass an array of length one containing a wallet address that they control as the `winners` parameter, and `[10000]` as the `percentages` parameter in order to receive 100% of the funds initially deposited to the contract. Due to the design of the protocol, they would have 7 days after the contest ends (the value of the `EXPIRATION_TIME` constant in the `ProxyFactory` contract) to perform this action without the owner being able to prevent it.

## Impact

Malicious/Compromised organizer can refund 100% of the contest funds, stealing work from sponsors.

## Tools Used

Manual review

## Recommendations

Use a two step procedure for distributing funds:
1. The organizer submits an array of winners and percentages to the `Proxy` contract and they are cached using storage variables
2. The owner of `ProxyFactor` (a trusted admin) checks the arrays to ensure the organizer is not distributing all of the money to themselves, and if satisfied, triggers the distribution of funds

This removes the risk of having to trust the organizer, and although it requires the trust of the admin, they were already a required trusted party and so the mitigation is beneficial overall. Also, this new system adds more truth to the statement from the contest details mentioned in the summary section of this report.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Sparkn |
| Report Date | N/A |
| Finders | Aamirusmani1552, KiteWeb3, Mlome, DevABDee, t0x1c, nisedo, arnie, Phantasmagoria, cats, FalconHoof, Breeje, 0x11singh99, savi0ur, AkiraKodo, InAllHonesty, Maroutis, ke1caM, Bughunter101, SAAJ, VanGrim, 0xnevi, 0xMosh, shikhar229169, y4y, TheSchnilch, 0xDetermination, Stoicov, coolboymsk, 0xdeth, Madalad, 0x3b, GoSoul22, zigtur, 0xch13fd357r0y3r, Slavchew, owade, ABA, MrjoryStewartBaxter, 0xScourgedev, supernovahs, 0xanmol, honeymewn |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-08-sparkn
- **Contest**: https://www.codehawks.com/contests/cllcnja1h0001lc08z7w0orxx

### Keywords for Search

`Admin`

