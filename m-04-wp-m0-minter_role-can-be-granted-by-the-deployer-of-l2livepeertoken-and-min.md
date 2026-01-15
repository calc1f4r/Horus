---
# Core Classification
protocol: Livepeer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25626
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-01-livepeer
source_link: https://code4rena.com/reports/2022-01-livepeer
github_link: https://github.com/code-423n4/2022-01-livepeer-findings/issues/193

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
  - services
  - cross_chain
  - launchpad
  - payments

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-04] [WP-M0] `MINTER_ROLE` can be granted by the deployer of L2LivepeerToken and mint arbitrary amount of tokens

### Overview


This bug report is about the `L2LivepeerToken` contract which has a `mint()` function that allows an address with `MINTER_ROLE` to burn an arbitrary amount of tokens. This poses a serious centralization risk as if the private key of the deployer or an address with the `MINTER_ROLE` is compromised, the attacker will be able to mint an unlimited amount of LPT tokens.

The recommendation is to remove the `MINTER_ROLE` and make the `L2LivepeerToken` only mintable by the owner. The owner should be the `L2Minter` contract. However, the recommendation was acknowledged by Yondonfu (Livepeer) who said they are planning on keeping the role since the `L2LPTGateway` needs to be given minting rights as well in addition to the `L2Minter`.

### Original Finding Content

_Submitted by WatchPug_.

<https://github.com/livepeer/arbitrum-lpt-bridge/blob/ebf68d11879c2798c5ec0735411b08d0bea4f287/contracts/L2/token/LivepeerToken.sol#L23-L30>

```solidity
function mint(address _to, uint256 _amount)
    external
    override
    onlyRole(MINTER_ROLE)
{
    _mint(_to, _amount);
    emit Mint(_to, _amount);
}
```

Using the `mint()` function of `L2LivepeerToken`, an address with `MINTER_ROLE` can burn an arbitrary amount of tokens.

If the private key of the deployer or an address with the `MINTER_ROLE` is compromised, the attacker will be able to mint an unlimited amount of LPT tokens.

We believe this is unnecessary and poses a serious centralization risk.

#### Recommendation

Consider removing the `MINTER_ROLE`, make the `L2LivepeerToken` only mintable by the owner, and make the L2Minter contract to be the owner and therefore the only minter.

**[yondonfu (Livepeer) acknowledged](https://github.com/code-423n4/2022-01-livepeer-findings/issues/193#issuecomment-1019660423):**
 > Planning on keeping the role since the L2LPTGateway needs to be given minting rights as well in addition to the L2 Minter.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Livepeer |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-livepeer
- **GitHub**: https://github.com/code-423n4/2022-01-livepeer-findings/issues/193
- **Contest**: https://code4rena.com/reports/2022-01-livepeer

### Keywords for Search

`vulnerability`

