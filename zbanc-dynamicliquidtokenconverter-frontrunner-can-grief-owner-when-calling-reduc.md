---
# Core Classification
protocol: Zer0 - zBanc
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13396
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/05/zer0-zbanc/
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
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - David Oz Kashi
  - Martin Ortner
---

## Vulnerability Title

zBanc - DynamicLiquidTokenConverter frontrunner can grief owner when calling reduceWeight  Acknowledged

### Overview


This bug report describes an issue with the Dynamic Liquid Token Converter contract. The contract allows the owner to reduce the converter weights once the marketcap surpasses a configured threshold. The marketcap at the beginning of the call is calculated and stored. However, a malicious actor could attempt to grief calls made by the owner by sandwiching them with buy and sell calls in an attempt to raise the barrier for the next valid payout marketcap or temporarily lower the marketcap if they are a major token holder. To mitigate this, the client suggested that having an admin by a DAO will help to reduce the owner risks here.

### Original Finding Content

#### Resolution



The client acknowledged this issue by providing the following statement:



> 
> 5.12 - admin by a DAO will mitigate the owner risks here
> 
> 
> 




#### Description


The owner of the converter is allowed to reduce the converters weights once the marketcap surpasses a configured threshhold. The thresshold is configured on first deployment. The marketcap at the beginning of the call is calculated as `reserveBalance / reserve.weight` and stored as `lastWeightAdjustmentMarketCap` after reducing the weight.


**zBanc/solidity/contracts/converter/types/liquid-token/DynamicLiquidTokenConverter.sol:L130-L138**



```
    function reduceWeight(IERC20Token \_reserveToken)
        public
        validReserve(\_reserveToken)
        ownerOnly
    {
        \_protected();
        uint256 currentMarketCap = getMarketCap(\_reserveToken);
        require(currentMarketCap > (lastWeightAdjustmentMarketCap.add(marketCapThreshold)), "ERR\_MARKET\_CAP\_BELOW\_THRESHOLD");


```
The reserveBalance can be manipulated by buying (adding reserve token) or selling liquidity tokens (removing reserve token). The success of a call to `reduceWeight` is highly dependant on the marketcap. A malicious actor may, therefore, attempt to grief calls made by the owner by sandwiching them with `buy` and sell `calls` in an attempt to (a) raise the barrier for the next valid payout marketcap or (b) temporarily lower the marketcap if they are a major token holder in an attempt to fail the `reduceWeights` call.


In both cases the griefer may incur some losses due to conversion errors, bancor fees if they are set, and gas spent. It is, therefore, unlikely that a third party may spend funds on these kinds of activities. However, the owner as a potential major liquid token holder may use this to their own benefit by artificially lowering the marketcap to the absolute minimum (old+threshold) by selling liquidity and buying it back right after reducing weights.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Zer0 - zBanc |
| Report Date | N/A |
| Finders | David Oz Kashi, Martin Ortner |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/05/zer0-zbanc/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

