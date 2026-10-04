---
# Core Classification
protocol: Tracer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25590
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-10-tracer
source_link: https://code4rena.com/reports/2021-10-tracer
github_link: https://github.com/code-423n4/2021-10-tracer-findings/issues/17

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
  - yield
  - services
  - derivatives

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-02] Deposits don't work with fee-on transfer tokens

### Overview


A bug report was submitted by cmichel regarding certain ERC20 tokens that have customizations such as deflationary tokens that charge a certain fee for every `transfer()` or `transferFrom()` and rebasing tokens that increase in value over time like Aave's aTokens (`balanceOf` changes over time). This bug impacts the `PoolCommiter.commit()` function, which stores the entire `amount` in the commitment but with fee-on-transfer tokens, fewer tokens will be transferred which leads to inconsistencies with the `pool.longBalance()` and in `uncommit`.

The recommended mitigation steps for this bug are to measure the asset change right before and after the asset-transferring routines. Alex the Entreprenerd (judge) commented that this is a valid finding and the warden has shown a way to tamper with the protocol, extracting value (as such medium severity). He also suggested that not using `feeOnTransfer` or `rebasing` tokens is completely legitimate.

### Original Finding Content

_Submitted by cmichel_.

There are ERC20 tokens that may make certain customizations to their ERC20 contracts.
One type of these tokens is deflationary tokens that charge a certain fee for every `transfer()` or `transferFrom()`.
Others are rebasing tokens that increase in value over time like Aave's aTokens (`balanceOf` changes over time).

#### Impact

The `PoolCommiter.commit()` function will store the entire `amount` in the commitment but with fee-on-transfer tokens, fewer tokens will be transferred which leads to inconsistencies with the `pool.longBalance()` and in `uncommit`.

#### Recommended Mitigation Steps

One possible mitigation is to measure the asset change right before and after the asset-transferring routines


**[rogue developer (Tracer) disputed](https://github.com/code-423n4/2021-10-tracer-findings/issues/17#issuecomment-944009136):**
 > Only governance (a multisig) can deploy markets, and has complete say over what markets can be deployed (see the `onlyGov` modifier in `PoolFactory.sol#deployPool`). Because new markets being deployed would be done via proposal to the DAO, which include the collateral token being used in a proposed market, markets with fee-on transfer tokens like Aave's aTokens just won't be deployed. I think this is a fairly safe assumption to make and thus we're making it out of scope. In any case, the chances of this happening and slipping past everyone who votes in the proposals _and_ not being noticed extremely soon after a market is deployed are extremely low.

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2021-10-tracer-findings/issues/17#issuecomment-955088716):**
 > I think this is a valid finding, the warden has shown a way to tamper with the protocol, extracting value (as such medium severity)
> 
> In terms of mitigation, not using `feeOnTransfer` or `rebasing` tokens is completely legitimate.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tracer |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-tracer
- **GitHub**: https://github.com/code-423n4/2021-10-tracer-findings/issues/17
- **Contest**: https://code4rena.com/reports/2021-10-tracer

### Keywords for Search

`vulnerability`

