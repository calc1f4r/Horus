---
# Core Classification
protocol: eBTC Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30159
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-10-badger
source_link: https://code4rena.com/reports/2023-10-badger
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

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[N-01] Typos, wrong comments and naming

### Overview

See description below for full details.

### Original Finding Content

1. These comments are copy-pasted from Auth.sol, we don't check the owner here

https://github.com/code-423n4/2023-10-badger/blob/main/packages/contracts/contracts/Dependencies/AuthNoOwner.sol#L33-L34

https://github.com/code-423n4/2023-10-badger/blob/main/packages/contracts/contracts/Dependencies/AuthNoOwner.sol#L39-L40

2. Fee floor is actually 0%

https://github.com/code-423n4/2023-10-badger/blob/main/packages/contracts/contracts/Dependencies/EbtcBase.sol#L35

3. Entire system debt

https://github.com/code-423n4/2023-10-badger/blob/main/packages/contracts/contracts/Dependencies/EbtcBase.sol#L73

4. Memorizing typo

https://github.com/code-423n4/2023-10-badger/blob/main/packages/contracts/contracts/Dependencies/Auth.sol#L33

5. `sending EBTC directly to a Liquity`

https://github.com/code-423n4/2023-10-badger/blob/main/packages/contracts/contracts/EBTCToken.sol#L22

6. \_NICR would be more appropriate name

https://github.com/code-423n4/2023-10-badger/blob/main/packages/contracts/contracts/HintHelpers.sol#L165

CR is associated with collateral ratio, however in this function we use NICR values to find a hint

7. Wrong pair names in comments

https://github.com/code-423n4/2023-10-badger/blob/main/packages/contracts/contracts/PriceFeed.sol#L784

https://github.com/code-423n4/2023-10-badger/blob/main/packages/contracts/contracts/PriceFeed.sol#L786
should be stETH-ETH feed

8. ETH-USD comment from Liquity

https://github.com/code-423n4/2023-10-badger/blob/main/packages/contracts/contracts/CdpManager.sol#L594

should be stETH-BTC

**[ronnyx2017 (Judge) commented](https://github.com/code-423n4/2023-10-badger-findings/issues/67#issuecomment-1829519278):**
> There are some other Low/Non-Critical issues downgraded from High/Medium that are also worth noting:

- [Not having a borrowing fee can weaken the peg stability.](https://github.com/code-423n4/2023-10-badger-findings/issues/159)
- [RolesAuthority: Incorrectly removing the function signature from the target.](https://github.com/code-423n4/2023-10-badger-findings/issues/244)
- [`LeverageMacroFactory` is susceptible to chain reorganization events.](https://github.com/code-423n4/2023-10-badger-findings/issues/224)
- [Incorrect calculations in `_chainlinkPriceChangeAboveMax`.](https://github.com/code-423n4/2023-10-badger-findings/issues/73)
- [`FeeRecipient` address is inconsistent through multiple contracts.](https://github.com/code-423n4/2023-10-badger-findings/issues/70)
- [`Governor.getUsersByRole` and `Governor.getRolesForUser` return 255 results at most.](https://github.com/code-423n4/2023-10-badger-findings/issues/185) 
- [`LeverageMacroBase.doOperation` being used by openCdp may cause OOG in some cases.](https://github.com/code-423n4/2023-10-badger-findings/issues/151)
- [Unnecessary restrictions make functions unavailable.](https://github.com/code-423n4/2023-10-badger-findings/issues/112)
- [Inconsistency in the `feeRecipientAddress` variable setting.](https://github.com/code-423n4/2023-10-badger-findings/issues/17) 
- [`fetchPrice` returns a staler price when oracle is frozen.](https://github.com/code-423n4/2023-10-badger-findings/issues/261)
- [`CollSurplusPool`'s `FeeRecipientAddress` is defined as immutable and will be out of sync.](https://github.com/code-423n4/2023-10-badger-findings/issues/150)

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | eBTC Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-10-badger
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2023-10-badger

### Keywords for Search

`vulnerability`

