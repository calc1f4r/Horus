---
# Core Classification
protocol: Golom
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8755
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-golom-contest
source_link: https://code4rena.com/reports/2022-07-golom
github_link: https://github.com/code-423n4/2022-07-golom-findings/issues/75

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - nft_marketplace
  - options_vault

# Audit Details
report_date: unknown
finders_count: 28
finders:
  - codexploder
  - scaraven
  - cryptonue
  - GiveMeTestEther
  - rbserver
---

## Vulnerability Title

[M-18] `fillAsk()` Allows for `msg.value` to be larger than require locking the excess in the contract

### Overview


A bug was discovered in the GolomTrader.sol contract, which is part of the 2022-07-golom GitHub repository. This bug could allow someone to send a higher `msg.value` than is required to `fillAsk()`. The excess value that is sent will be permanently locked in the contract, meaning the funds are not retrievable. To mitigate this issue, the code should be updated to enforce a strict equality for the `msg.value` parameter, instead of just a greater-than comparison. This would ensure that the exact amount required is sent, and no excess funds are locked in the contract.

### Original Finding Content


[GolomTrader.sol#L217](https://github.com/code-423n4/2022-07-golom/blob/e5efa8f9d6dda92a90b8b2c4902320acf0c26816/contracts/core/GolomTrader.sol#L217)<br>

It is possible to send a higher `msg.value` than is required to `fillAsk()`. The excess value that is sent will be permanently locked in the contract.

### Proof of Concept

There is only one check over `msg.value` and it is that it's greater than `o.totalAmt * amount + p.paymentAmt`. As seen in the following code snippet from #217.

```solidity
        require(msg.value >= o.totalAmt * amount + p.paymentAmt, 'mgmtm');
```

The issue here is that the contract will only ever spend exactly `o.totalAmt * amount + p.paymentAmt`. Hence if `msg.value` is greater than this then the excess value will be permanently locked in the contract.

### Recommended Mitigation Steps

To avoid this issue consider enforcing a strict equality.

```solidity
        require(msg.value == o.totalAmt * amount + p.paymentAmt, 'mgmtm');
```

**[0xsaruman (Golom) confirmed](https://github.com/code-423n4/2022-07-golom-findings/issues/75)**

**[0xsaruman (Golom) disagreed with severity and commented](https://github.com/code-423n4/2022-07-golom-findings/issues/75#issuecomment-1236313317):**
 > Resolved: https://github.com/golom-protocol/contracts/commit/366c0455547041003c28f21b9afba48dc33dc5c7#diff-63895480b947c0761eff64ee21deb26847f597ebee3c024fb5aa3124ff78f6ccR217
> 
> Disagree with severity cause it's user choice to send more.

**[LSDan (judge) commented](https://github.com/code-423n4/2022-07-golom-findings/issues/75#issuecomment-1276385424):**
 > I agree with this being a medium. It opens up the potential for griefing attacks and all sorts of other issues that may be beyond the scope of "the user decided to send excess funds". Further, it's common for contracts to return excess funds, so the user may reasonably expect this behaviour.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Golom |
| Report Date | N/A |
| Finders | codexploder, scaraven, cryptonue, GiveMeTestEther, rbserver, arcoun, minhquanym, joestakey, Twpony, Lambda, peritoflores, Green, reassor, jayphbee, cccz, rotcivegaf, Ruhum, 0xSky, Treasure-Seeker, horsefacts, ych18, RustyRabbit, CertoraInc, bin2chen, AuditsAreUS, dipp, obront, GimelSec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-golom
- **GitHub**: https://github.com/code-423n4/2022-07-golom-findings/issues/75
- **Contest**: https://code4rena.com/contests/2022-07-golom-contest

### Keywords for Search

`vulnerability`

