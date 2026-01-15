---
# Core Classification
protocol: PoolTogether - LootBox and MultipleWinners Strategy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13587
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/11/pooltogether-lootbox-and-multiplewinners-strategy/
github_link: none

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
  - liquid_staking
  - cdp
  - services
  - yield_aggregator
  - launchpad

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

PeriodicPrizeStrategy - Token with callback related warnings (ERC777 a.o.)

### Overview


This bug report is about an issue that is dependent on the configuration of the system. If an admin allows callback enabled tokens (such as ERC20 compliant ERC777 or other ERC721/ERC20 extensions) to be used as awards, one recipient may be able to block the payout for everyone by forcing a revert in the callback when accepting token awards. Additionally, the recipient may be able to use the callback to siphon gas, mint gas token, or similar activities. Furthermore, the recipient may be able to re-enter the PrizeStrategy contract in an attempt to manipulate the payout.

It is highly recommended to not allow tokens with callback functionality into the system. Document and/or implement safeguards that disallow the use of callback enabled tokens. Additionally, consider implementing means for the “other winners” to withdraw their share of the rewards independently from others.

### Original Finding Content

#### Description


This issue is highly dependent on the configuration of the system. If an admin decides to allow callback enabled token (e.g. `ERC20` compliant `ERC777` or other `ERC721`/`ERC20` extensions) as awards then one recipient may be able to


* block the payout for everyone by forcing a revert in the callback when accepting token awards
* use the callback to siphon gas, mint gas token, or similar activities
* potentially re-enter the `PrizeStrategy` contract in an attempt to manipulate the payout (e.g. by immediately withdrawing from the pool to manipulate the 2nd `ticket.draw()`)


#### Examples


**code/pool/contracts/prize-strategy/PeriodicPrizeStrategy.sol:L252-L263**



```
function \_awardExternalErc721s(address winner) internal {
  address currentToken = externalErc721s.start();
  while (currentToken != address(0) && currentToken != externalErc721s.end()) {
    uint256 balance = IERC721(currentToken).balanceOf(address(prizePool));
    if (balance > 0) {
      prizePool.awardExternalERC721(winner, currentToken, externalErc721TokenIds[currentToken]);
      delete externalErc721TokenIds[currentToken];
    }
    currentToken = externalErc721s.next(currentToken);
  }
  externalErc721s.clearAll();
}

```
#### Recommendation


It is highly recommended to not allow tokens with callback functionality into the system. Document and/or implement safeguards that disallow the use of callback enabled tokens. Consider implementing means for the “other winners” to withdraw their share of the rewards independently from others.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | PoolTogether - LootBox and MultipleWinners Strategy |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/11/pooltogether-lootbox-and-multiplewinners-strategy/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

