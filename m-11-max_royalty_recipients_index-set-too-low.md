---
# Core Classification
protocol: Foundation
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42492
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-02-foundation
source_link: https://code4rena.com/reports/2022-02-foundation
github_link: https://github.com/code-423n4/2022-02-foundation-findings/issues/45

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
  - dexes
  - cdp
  - services
  - indexes
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-11] `MAX_ROYALTY_RECIPIENTS_INDEX` set too low

### Overview


The bug report is about a limitation in the NFTMarketFees.sol code, which is used for paying creators of NFTs. Currently, the code is set to only pay out to a maximum of 5 creators, even if there are more than 5 involved. This means that any additional creators will not receive any payment. The person who submitted the report suggests increasing this limit, as it is possible for there to be more than 5 creators involved in the creation of an NFT. The person who manages the code has acknowledged this issue and suggests documenting the limitation and providing a workaround for users who may encounter this problem. 

### Original Finding Content

_Submitted by cmichel_

[NFTMarketFees.sol#L78](https://github.com/code-423n4/2022-02-foundation/blob/4d8c8931baffae31c7506872bf1100e1598f2754/contracts/mixins/NFTMarketFees.sol#L78)<br>

The creator payouts are capped at `MAX_ROYALTY_RECIPIENTS_INDEX`. It's currently set to `4` and only 5 creators are paid out.<br>
Other creators are ignored.

### Recommended Mitigation Steps

I don't think cases with more than 5 creators / royalty receivers are unlikely.<br>
It can and should probably be increased, especially as the transfers are already gas restricted.

**[NickCuso (Foundation) acknowledged and commented](https://github.com/code-423n4/2022-02-foundation-findings/issues/45#issuecomment-1057382530):**
 > Yes this is a fair point. The limit we put in place is arbitrary. We want some limit in order to ensure that the gas costs (which are often pushed to users other than the original creator) never get to be very expensive.
> 
> What we can and should do is document this limitation so that it's more clear what exactly will happen when too many recipients are defined. Additionally we should comment on a possible workaround: If you have a contract that splits with too many participants you could use the Royalty Override in order to define a single contract recipient instead to handle the splits - e.g. https://www.0xsplits.xyz/



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Foundation |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-foundation
- **GitHub**: https://github.com/code-423n4/2022-02-foundation-findings/issues/45
- **Contest**: https://code4rena.com/reports/2022-02-foundation

### Keywords for Search

`vulnerability`

