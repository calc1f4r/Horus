---
# Core Classification
protocol: Backd
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24395
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-05-backd
source_link: https://code4rena.com/reports/2022-05-backd
github_link: none

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[N-13] Typos

### Overview

See description below for full details.

### Original Finding Content


*There are 6 instances of this issue:*
```solidity
File: protocol/contracts/BkdLocker.sol

/// @audit invlude
173:       * @dev This does not invlude the gov. tokens queued for withdrawal.
```
https://github.com/code-423n4/2022-05-backd/blob/2a5664d35cde5b036074edef3c1369b984d10010/protocol/contracts/BkdLocker.sol#L173

```solidity
File: protocol/contracts/tokenomics/InflationManager.sol

/// @audit TOOD
532:      //TOOD: See if this is still needed somewhere
```
https://github.com/code-423n4/2022-05-backd/blob/2a5664d35cde5b036074edef3c1369b984d10010/protocol/contracts/tokenomics/InflationManager.sol#L532

```solidity
File: protocol/contracts/tokenomics/FeeBurner.sol

/// @audit Emmited
29:       event Burned(address targetLpToken, uint256 amountBurned); // Emmited after a successfull burn to target lp token

/// @audit successfull
29:       event Burned(address targetLpToken, uint256 amountBurned); // Emmited after a successfull burn to target lp token

/// @audit Recieve
35:       receive() external payable {} // Recieve function for withdrawing from Backd ETH Pool

/// @audit Transfering
84:           // Transfering LP tokens back to sender
```
https://github.com/code-423n4/2022-05-backd/blob/2a5664d35cde5b036074edef3c1369b984d10010/protocol/contracts/tokenomics/FeeBurner.sol#L29

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-05-backd-findings/issues/109#issuecomment-1159843872):**
> **1. migrate() still does transfers when the transfer is to the same pool, and this can be done multiple times**<br>
>Interesting finding, also wonder if this could cause issues with fees, but in lack of POC, I think this is a valid Low Severity finding

> **2. Non-exploitable reentrancy**<br>
>Agree with severity and finding, would rephrase to "code doesn't conform to CEI"

> **3. Users can DOS themselves by executing prepareUnlock(0) many times**<br>
>This should be downgraded to non-critical because it probably requires tens of thousands of calls, that said the finding is valid

> **4. Unused/empty receive()/fallback() function**<br>
>I fail to see the need for the extra checks given that the contracts are meant to handle ETH

> **5. safeApprove() is deprecated**<br>
>Technically valid, however the code is using `safeApprove` correctly, only once, from zero to X

> **6. Missing checks for address(0x0) when assigning values to address state variables**<br>
>Valid

> **7. _prepareDeadline(), _setConfig(), and _executeDeadline() should be private**<br>
>Disagree with the alarmist side, but there's validity to this finding.

> **Non-critical Issues**<br>
>Agree with the findings although it feels like a bot wrote this.

>Overall a really exhaustive report, 3 findings are interesting the rest doesn't stand out, however the thoroughness of the report does.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Backd |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-backd
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-05-backd

### Keywords for Search

`vulnerability`

