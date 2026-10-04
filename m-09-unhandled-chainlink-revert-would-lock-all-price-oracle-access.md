---
# Core Classification
protocol: Juicebox
chain: everychain
category: oracle
vulnerability_type: oracle

# Attack Vector Details
attack_type: oracle
affected_component: oracle

# Source Information
source: solodit
solodit_id: 2967
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-juicebox-v2-contest
source_link: https://code4rena.com/reports/2022-07-juicebox
github_link: https://github.com/code-423n4/2022-07-juicebox-findings/issues/59

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.75
financial_impact: medium

# Scoring
quality_score: 3.75
rarity_score: 3.333333333333333

# Context Tags
tags:
  - oracle
  - dos

protocol_categories:
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - codexploder
  - berndartmueller
  - bardamu
  - Alex the Entreprenerd
  - horsefacts
---

## Vulnerability Title

[M-09] Unhandled chainlink revert would lock all price oracle access

### Overview


This bug report is about a vulnerability found in the JBChainlinkV3PriceFeed.sol smart contract. The vulnerability could potentially lead to a permanent denial of service if the call to the `latestRoundData` function reverts. The proof of concept for this vulnerability involves Chainlink's multisigs which can block access to price feeds at will. To prevent denial of service scenarios, it is recommended to use a defensive approach with Solidity's try/catch structure. This way, if the call to the price feed fails, the caller contract is still in control and can handle any errors safely and explicitly. The recommended mitigation steps for this vulnerability include surrounding the call to `latestRoundData()` with `try/catch` instead of calling it directly. In a scenario where the call reverts, the catch block can be used to call a fallback oracle or handle the error in any other suitable way.

### Original Finding Content

_Submitted by bardamu, also found by berndartmueller, codexploder, Alex the Entreprenerd, and horsefacts_

Call to `latestRoundData` could potentially revert and make it impossible to query any prices. Feeds cannot be changed after they are configured (<https://github.com/jbx-protocol/juice-contracts-v2-code4rena/blob/828bf2f3e719873daa08081cfa0d0a6deaa5ace5/contracts/JBPrices.sol#L115>) so this would result in a permanent denial of service.

### Proof of Concept

Chainlink's multisigs can immediately block access to price feeds at will. Therefore, to prevent denial of service scenarios, it is recommended to query Chainlink price feeds using a defensive approach with Solidity’s try/catch structure. In this way, if the call to the price feed fails, the caller contract is still in control and can handle any errors safely and explicitly.

<https://github.com/jbx-protocol/juice-contracts-v2-code4rena/blob/828bf2f3e719873daa08081cfa0d0a6deaa5ace5/contracts/JBPrices.sol#L69>

    if (_feed != IJBPriceFeed(address(0))) return _feed.currentPrice(_decimals);

<https://github.com/jbx-protocol/juice-contracts-v2-code4rena/blob/828bf2f3e719873daa08081cfa0d0a6deaa5ace5/contracts/JBChainlinkV3PriceFeed.sol#L42-L44>

    function currentPrice(uint256 _decimals) external view override returns (uint256) {
      // Get the latest round information. Only need the price is needed.
      (, int256 _price, , , ) = feed.latestRoundData();

Refer to <https://blog.openzeppelin.com/secure-smart-contract-guidelines-the-dangers-of-price-oracles/> for more information regarding potential risks to account for when relying on external price feed providers.

### Tools Used

VIM

### Recommended Mitigation Steps

Surround the call to `latestRoundData()` with `try/catch` instead of calling it directly. In a scenario where the call reverts, the catch block can be used to call a fallback oracle or handle the error in any other suitable way.

**[mejango (Juicebox) acknowledged](https://github.com/code-423n4/2022-07-juicebox-findings/issues/59)**

**[jack-the-pug (judge) commented](https://github.com/code-423n4/2022-07-juicebox-findings/issues/59#issuecomment-1200414043):**
 > Good catch! Seems like we should update this function to allow changing the feed contract:
> 
> https://github.com/jbx-protocol/juice-contracts-v2-code4rena/blob/828bf2f3e719873daa08081cfa0d0a6deaa5ace5/contracts/JBPrices.sol#L109-L121



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3.75/5 |
| Rarity Score | 3.333333333333333/5 |
| Audit Firm | Code4rena |
| Protocol | Juicebox |
| Report Date | N/A |
| Finders | codexploder, berndartmueller, bardamu, Alex the Entreprenerd, horsefacts |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-juicebox
- **GitHub**: https://github.com/code-423n4/2022-07-juicebox-findings/issues/59
- **Contest**: https://code4rena.com/contests/2022-07-juicebox-v2-contest

### Keywords for Search

`Oracle, DOS`

