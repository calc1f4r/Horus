---
# Core Classification
protocol: ReyaNetwork-April
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37835
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/ReyaNetwork-security-review-April.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-01] Missing validation of non-zero value

### Overview

See description below for full details.

### Original Finding Content

Within `ConfigurationModule::setMarketConfiguration`, there is no validation that `MarketConfigurationData.maxSlippage` is not zero:

```solidity
File: ConfigurationModule.sol
55:     function setMarketConfiguration(uint128 marketId, MarketConfigurationData memory config) external override {
56:         if (config.oracleNodeId == 0) {
57:             revert Errors.InvalidMarketConfiguration(marketId, config, "ORCLN");
58:         }
59:
60:         if (config.baseSpacing.eq(ZERO_ud)) {
61:             revert Errors.InvalidMarketConfiguration(marketId, config, "BSSP");
62:         }
63:
64:         NodeOutput.Data memory node =
65:             INodeModule(GlobalConfiguration.getOracleManagerAddress()).process(config.oracleNodeId);
66:         UD60x18 oraclePrice = UD60x18.wrap(node.price);
67:
68:         if (config.priceSpacing.eq(ZERO_ud) || oraclePrice.lte(config.priceSpacing.mul(ud(1000e18)))) {
69:             revert Errors.InvalidMarketConfiguration(marketId, config, "PRCSP");
70:         }
71:
72:         if (!config.minimumOrderBase.mod(config.baseSpacing).eq(ZERO_ud)) {
73:             revert Errors.InvalidMarketConfiguration(marketId, config, "MNOB");
74:         }
75:
76:         // TODO: it should be less or equal than 0.01 but it breaks a lot of testing doing so
77:         if (config.velocityMultiplier.gt(ud(1e18))) {
78:             revert Errors.InvalidMarketConfiguration(marketId, config, "VLCTM");
79:         }
80:
81:         if (config.depthFactor.eq(ZERO_ud)) {
82:             revert Errors.InvalidMarketConfiguration(marketId, config, "DPTHF");
83:         }
84:
85:         if (config.maxExposureFactor.gt(ONE_ud)) {
86:             revert Errors.InvalidMarketConfiguration(marketId, config, "MXEXF");
87:         }
88:
89:         Market.Data storage market = Market.exists(marketId);
90:         market.onlyAuthorized(Permissions.PASSIVE_PERP_MARKET_CONFIGURATOR);
91:
92:         MarketConfiguration.set(marketId, config);
93:     }
```

This could affect the calculation of `pSlippage` within the `Market::getPSlippage` function, as any non-zero value of `pSlippage` would cause the function to revert with an `ExceededPSlippage` error if `maxPSlippage` is zero (lines 301-303).

```solidity
File: Market.sol
272:
273:     function getPSlippage(
274:         Data storage self,
275:         SD59x18 deltaBase,
276:         UD60x18 oraclePrice
277:     )
278:         internal
279:         view
280:         returns (SD59x18 pSlippage)
281:     {
282:         MarketConfigurationData memory marketConfig = getConfig(self);
283:
284:         uint256 riskMatrixIndex = marketConfig.riskMatrixIndex;
285:         UD60x18 depthFactor = marketConfig.depthFactor;
286:         UD60x18 maxExposureFactor = marketConfig.maxExposureFactor;
287:         UD60x18 maxPSlippage = marketConfig.maxPSlippage;
288:
289:         (UD60x18 maxExposureShort, UD60x18 maxExposureLong, SD59x18[] memory exposures) = getPoolMaxExposures(self);
290:         SD59x18 deltaExposure = convertBaseToExposure(deltaBase, oraclePrice);
291:
292:         SD59x18 netExposure = exposures[riskMatrixIndex].add(deltaExposure);
293:         UD60x18 maxExposure = netExposure.lt(ZERO_sd) ? maxExposureShort : maxExposureLong;
294:
295:         if (netExposure.abs().intoUD60x18().gte(maxExposure.mul(maxExposureFactor))) {
296:             revert Errors.ExceededMaxExposure(netExposure, maxExposure);
297:         }
298:
299:         pSlippage = computePSlippage({ netExposure: netExposure, maxExposure: maxExposure, depthFactor: depthFactor });
300:
301:         if (pSlippage.abs().intoUD60x18().gt(maxPSlippage)) {
302:             revert Errors.ExceededPSlippage(pSlippage, maxPSlippage);
303:         }
304:     }
```

It is advisable to evaluate that `maxSlippage` is not zero within the `ConfigurationModule::setMarketConfiguration` function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | ReyaNetwork-April |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/ReyaNetwork-security-review-April.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

