---
# Core Classification
protocol: Renzo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33502
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-renzo
source_link: https://code4rena.com/reports/2024-04-renzo
github_link: https://github.com/code-423n4/2024-04-renzo-findings/issues/484

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

protocol_categories:
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 30
finders:
  - honey-k12
  - atoko
  - ladboy233
  - 0xDemon
  - t0x1c
---

## Vulnerability Title

[M-07] Lack of slippage and deadline during withdraw and deposit

### Overview


The `withdraw()` function in the `ezETH` contract does not have the option for users to set slippage and deadline parameters. This can result in users receiving a lower redemption amount than expected due to fluctuations in the oracle values. The same issue can also be seen in the `deposit()` and `depositETH()` functions. It is recommended to allow users to pass these parameters to avoid potential losses. The warden and judge have disputed whether this is necessary, as the oracle values are fair and cannot be manipulated by users. However, it is important to note that Renzo uses market oracles, which can fluctuate more than the actual exchange rate. Therefore, it is suggested to add slippage controls and give users the option to disable them in volatile conditions.

### Original Finding Content


When users call `withdraw()` to burn their `ezETH` and receive redemption amount in return, there is no provision to provide any slippage & deadline params. This is necessary because the `withdraw()` function [uses values from the oracle](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/Withdraw/WithdrawQueue.sol#L229) and the users may get a worse rate than they planned for.

Additionally, the `withdraw()` function also makes use of calls to `calculateTVLs()` to fetch the current `totalTVL`. The `calculateTVLs()` function [makes use of oracle prices too](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/RestakeManager.sol#L317). Note that though there is a `MAX_TIME_WINDOW` inside these oracle lookup functions, the users are forced to rely on this hardcoded value & can't provide a deadline from their side.
These facts are apart from the consideration that users' call to `withdraw()` could very well be unintentionally/intentionally front-run which causes a drop in `totalTVL`. <br>

In all of these situations, users receive less than they bargained for and, hence, a slippage and deadline parameter is necessary.

Similar issue can be seen inside [`deposit()`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/RestakeManager.sol#L565) and [`depositETH()`](https://github.com/code-423n4/2024-04-renzo/blob/main/contracts/RestakeManager.sol#L605).

### Recommended Mitigation Steps

Allow users to pass a slippage tolerance value and a deadline parameter while calling these functions.

**[jatinj615 (Renzo) disputed and commented](https://github.com/code-423n4/2024-04-renzo-findings/issues/484#issuecomment-2110339545):**
 > Oracle updates the value every 24 hours and technically, it creates an arbitrage opportunity which will not be beneficial to users as they will arbitraging 1 days reward share and losing on 7 days rewards due to `coolDownPeriod`. 
>
> We need the warden to provide a POC of delta around `deposit` and `withdraw` considering we will be implementing slashing pricing mechanism at the time of claim specified in [#326](https://github.com/code-423n4/2024-04-renzo-findings/issues/326).  

**[sin1st3r\_\_ (warden) commented](https://github.com/code-423n4/2024-04-renzo-findings/issues/484#issuecomment-2132184938):**
 > @alcueca - I believe this should be a QA rather than a Med. You need slippage and deadline when the price can be manipulated like in an AMM. Here, since the price of the exchange is always fair because it can’t be moved by however large user operation, but only by changes in oracle price (that is fair by definition), there is no strong case for the same of level of protection as in AMMs.
 >
> Staking on Lido for example doesn't have slippage or deadline either. See [here](https://etherscan.io/address/0x17144556fd3424edc8fc8a4c940b2d04936d17eb#code).

**[alcueca (judge) commented](https://github.com/code-423n4/2024-04-renzo-findings/issues/484#issuecomment-2133087448):**
 > The thing is that Renzo is using market oracles, as stated in [#13](https://github.com/code-423n4/2024-04-renzo-findings/issues/13). These oracles can fluctuate more than the actual exchange rate, due to market forces. In some situations the users might be displeased that their withdrawals rended less value because of a temporary spike in the oracle.
> 
> It is quite borderline, because it needs the oracles to have jumps large enough to bother users. However, I do see value to add slippage controls, and let users disable them in volatile conditions when they just want to dump.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Renzo |
| Report Date | N/A |
| Finders | honey-k12, atoko, ladboy233, 0xDemon, t0x1c, SBSecurity, Rhaydden, MSaptarshi, Maroutis, ZanyBonzy, rbserver, PNS, twcctop, NentoR, btk, DanielArmstrong, crypticdefense, jokr, Bauchibred, ilchovski, Ocean\_Sky, FastChecker, 1, Shaheen, 2, hunter\_w3b, Tigerfrake, 0xCiphky |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-renzo
- **GitHub**: https://github.com/code-423n4/2024-04-renzo-findings/issues/484
- **Contest**: https://code4rena.com/reports/2024-04-renzo

### Keywords for Search

`vulnerability`

