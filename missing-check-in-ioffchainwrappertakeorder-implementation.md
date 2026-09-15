---
# Core Classification
protocol: DeFi Saver
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13480
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/03/defi-saver/
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
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - David Oz Kashi
  - Shayan Eskandari
---

## Vulnerability Title

Missing check in IOffchainWrapper.takeOrder implementation

### Overview

See description below for full details.

### Original Finding Content

#### Description


`IOffchainWrapper.takeOrder` wraps an external call that is supposed to perform a token swap. As for the two different implementations `ZeroxWrapper` and `ScpWrapper` this function validates that the destination token balance after the swap is greater than the value before. However, it is not sufficient, and the user-provided minimum amount for swap should be taken in consideration as well. Besides, the external contract should not be trusted upon, and `SafeMath` should be used for the subtraction operation.


#### Examples


**code/contracts/exchangeV3/offchainWrappersV3/ZeroxWrapper.sol:L42-L50**



```
uint256 tokensBefore = \_exData.destAddr.getBalance(address(this));
(success, ) = \_exData.offchainData.exchangeAddr.call{value: \_exData.offchainData.protocolFee}(\_exData.offchainData.callData);
uint256 tokensSwaped = 0;

if (success) {
    // get the current balance of the swaped tokens
    tokensSwaped = \_exData.destAddr.getBalance(address(this)) - tokensBefore;
    require(tokensSwaped > 0, ERR\_TOKENS\_SWAPED\_ZERO);
}

```
**code/contracts/exchangeV3/offchainWrappersV3/ScpWrapper.sol:L43-L51**



```
uint256 tokensBefore = \_exData.destAddr.getBalance(address(this));
(success, ) = \_exData.offchainData.exchangeAddr.call{value: \_exData.offchainData.protocolFee}(\_exData.offchainData.callData);
uint256 tokensSwaped = 0;

if (success) {
    // get the current balance of the swaped tokens
    tokensSwaped = \_exData.destAddr.getBalance(address(this)) - tokensBefore;
    require(tokensSwaped > 0, ERR\_TOKENS\_SWAPED\_ZERO);
}

```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | DeFi Saver |
| Report Date | N/A |
| Finders | David Oz Kashi, Shayan Eskandari |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/03/defi-saver/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

