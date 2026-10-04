---
# Core Classification
protocol: Blueberry
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6665
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/41
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/9

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
  - leveraged_farming
  - dexes
  - cdp
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x52
---

## Vulnerability Title

M-18: ChainlinkAdapterOracle use BTC/USD chainlink oracle to price WBTC which is problematic if WBTC depegs

### Overview


This bug report is about an issue found in the ChainlinkAdapterOracle code which uses a BTC/USD chainlink oracle to price WBTC. This is problematic because if the bridge connecting WBTC to BTC is compromised or fails, WBTC will no longer be equivalent to BTC and the protocol will take on a large amount of bad debt from outstanding loans. The code snippet linked in the report is from the ChainlinkAdapterOracle.sol file on line 47 to 59. The tool used to find this issue was manual review. The recommendation given is to use a double oracle setup with both a Chainlink and an on-chain liquidity base oracle, such as UniV3 TWAP. If the price of the on-chain liquidity oracle drops below a certain threshold of the Chainlink oracles, any borrowing should be immediately halted. This will prevent price manipulation and safeguard against the asset depegging.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/9 

## Found by 
0x52

## Summary

The chainlink BTC/USD oracle is used to price WBTC ([docs](https://docs.blueberry.garden/lending-protocol/price-oracle#price-feed-alternative)). WBTC is basically a bridged asset and if the bridge is compromised/fails then WBTC will depeg and will no longer be equivalent to BTC. This will lead to large amounts of borrowing against an asset that is now effectively worthless. Since the protocol still values it via BTC/USD the protocol will not only be stuck with the bad debt caused by the currently outstanding loans but they will also continue to give out bad loans and increase the amount of bad debt further

## Vulnerability Detail

See summary.

## Impact

Protocol will take on a large amount of bad debt should WBTC bridge become compromised and WBTC depegs

## Code Snippet

https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/oracle/ChainlinkAdapterOracle.sol#L47-L59

## Tool used

Manual Review

## Recommendation

I would recommend using a double oracle setup. Use both the Chainlink and another on-chain liquidity base oracle (i.e. UniV3 TWAP). If the price of the on-chain liquidity oracle drops below a certain threshold of the Chainlink oracles (i.e. 2% lower), any borrowing should be immediately halted. The chainlink oracle will prevent price manipulation and the liquidity oracle will safeguard against the asset depegging.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry |
| Report Date | N/A |
| Finders | 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/9
- **Contest**: https://app.sherlock.xyz/audits/contests/41

### Keywords for Search

`vulnerability`

