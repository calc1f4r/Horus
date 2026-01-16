---
# Core Classification
protocol: Golom
chain: everychain
category: uncategorized
vulnerability_type: call_vs_transfer

# Attack Vector Details
attack_type: call_vs_transfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8738
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-golom-contest
source_link: https://code4rena.com/reports/2022-07-golom
github_link: https://github.com/code-423n4/2022-07-golom-findings/issues/343

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.20
financial_impact: medium

# Scoring
quality_score: 1.0014334963240574
rarity_score: 1.001075122243043

# Context Tags
tags:
  - call_vs_transfer

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - nft_marketplace
  - options_vault

# Audit Details
report_date: unknown
finders_count: 85
finders:
  - codexploder
  - 0x52
  - scaraven
  - brgltd
  - cryptonue
---

## Vulnerability Title

[M-01] Use `call()` rather than `transfer()` on address payable

### Overview


This bug report is about a vulnerability found in the code of GolomTrader.sol, a smart contract. The vulnerability is related to the use of the `.transfer()` function to send ether to other addresses. This function can fail for a number of reasons, such as if the destination is a smart contract that doesn’t implement a `payable` function, or if it implements a `payable` function but that function uses more than 2300 gas units. It can also fail if the destination is a smart contract but that smart contract is called via an intermediate proxy contract, or if future changes or forks in Ethereum result in higher gas fees than transfer provides. To remediate this issue, the recommended solution is to use the `.call()` function instead of `.transfer()`, and to pass the gas units as a variable to the `.call()` function. This will help to avoid some of the limitations of `.transfer()`.

### Original Finding Content


[L154](https://github.com/code-423n4/2022-07-golom/blob/main/contracts/core/GolomTrader.sol#L154) in [GolomTrader.sol](https://github.com/code-423n4/2022-07-golom/blob/main/contracts/core/GolomTrader.sol) uses `.transfer()` to send ether to other addresses. There are a number of issues with using `.transfer()`, as it can fail for a number of reasons (specified in the Proof of Concept).

### Proof of Concept

1.  The destination is a smart contract that doesn’t implement a `payable` function or it implements a `payable` function but that function uses more than 2300 gas units.
2.  The destination is a smart contract that doesn’t implement a `payable` `fallback` function or it implements a `payable` `fallback` function but that function uses more than 2300 gas units.
3.  The destination is a smart contract but that smart contract is called via an intermediate proxy contract increasing the case requirements to more than 2300 gas units. A further example of unknown destination complexity is that of a multisig wallet that as part of its operation uses more than 2300 gas units.
4.  Future changes or forks in Ethereum result in higher gas fees than transfer provides. The `.transfer()` creates a hard dependency on 2300 gas units being appropriate now and into the future.

### Tools Used

Vim

### Recommended Remediation Steps

Instead use the `.call()` function to transfer ether and avoid some of the limitations of `.transfer()`. This would be accomplished by changing `payEther()` to something like;

```solidity
(bool success, ) = payable(payAddress).call{value: payAmt}(""); // royalty transfer to royaltyaddress
require(success, "Transfer failed.");
```

Gas units can also be passed to the `.call()` function as a variable to accomodate any uses edge cases. Gas could be a mutable state variable that can be set by the contract owner.

**[0xsaruman (Golom) confirmed](https://github.com/code-423n4/2022-07-golom-findings/issues/343)**

**[0xsaruman (Golom) resolved and commented](https://github.com/code-423n4/2022-07-golom-findings/issues/343#issuecomment-1236301220):**
 > Resolved https://github.com/golom-protocol/contracts/commit/366c0455547041003c28f21b9afba48dc33dc5c7#diff-63895480b947c0761eff64ee21deb26847f597ebee3c024fb5aa3124ff78f6ccR154

**[LSDan (judge) commented](https://github.com/code-423n4/2022-07-golom-findings/issues/343#issuecomment-1287092544):**
 > Given how many upgrades I'm making on this, I figured a comment on my reasoning was in order. In many contests, this would be considered low risk. While unlikely to occur without warning, it is well-documented and so very well might occur at some point in the foreseeable future. With Golom's implementation, the entire functionality of the protocol would break if the gas price were to rise, resulting in a need to relaunch/redeploy. The extreme nature of this disruption offsets the other factors normally considered and is why I consider it to be a medium risk in this contest.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 1.0014334963240574/5 |
| Rarity Score | 1.001075122243043/5 |
| Audit Firm | Code4rena |
| Protocol | Golom |
| Report Date | N/A |
| Finders | codexploder, 0x52, scaraven, brgltd, cryptonue, Bnke0x0, saian, giovannidisiena, 0xNazgul, arcoun, minhquanym, joestakey, Chom, Lambda, peritoflores, 0x1f8b, MEP, Noah3o6, IllIllI, reassor, immeas, Ruhum, ellahi, oyc_109, Treasure-Seeker, StyxRave, 0xNineDec, durianSausage, CertoraInc, cthulhu_cult, Dravee, GalloDaSballo, 0xHarry, dharma09, JohnSmith, navinavu, bulej93, Jmaxmanblue, Jujic, Krow10, rbserver, bardamu, kenzo, Deivitto, cccz, rotcivegaf, hansfriese, cloudjunky, bin2chen, shenwilly, RedOneN, indijanc, GimelSec, 0xf15ers, _Adam, TomJ, 0xDjango, Kenshin, simon135, jayphbee, bearonbike, 0xsolstars, kyteg, zzzitron, sseefried, TrungOre, 8olidity, __141345__, StErMi, dipp, obront, rokinot, ladboy233, cryptphi, djxploit, asutorufos, teddav, c3phas, 0x4non, 0xsanson, horsefacts, jayjonah8, carlitox477, hyh, cRat1st0s |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-golom
- **GitHub**: https://github.com/code-423n4/2022-07-golom-findings/issues/343
- **Contest**: https://code4rena.com/contests/2022-07-golom-contest

### Keywords for Search

`call vs transfer`

