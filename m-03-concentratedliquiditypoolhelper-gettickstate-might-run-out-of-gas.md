---
# Core Classification
protocol: Sushi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25580
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-09-sushitrident-2
source_link: https://code4rena.com/reports/2021-09-sushitrident-2
github_link: https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/17

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
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-03] `ConcentratedLiquidityPoolHelper`: `getTickState()` might run out of gas

### Overview


This bug report is about the `getTickState()` function in the IConcentratedLiquidityPool pool. This function attempts to fetch the state of all inserted ticks, including `MIN_TICK` and `MAX_TICK`, but depending on the tick spacing, it may run out of gas. The recommended mitigation steps are to have a starting index parameter to start the iteration from and to make use of the `tickCount` parameter more meaningfully to limit the number of iterations performed. Sarangparikh22 (Sushi) acknowledged the bug and alcueca (judge) commented that the functionality is affected and the severity is 2.

### Original Finding Content

_Submitted by hickuphh3, also found by cmichel_

##### Impact
`getTickState()` attempts to fetch the state of all inserted ticks (including `MIN_TICK` and `MAX_TICK`) of a pool. Depending on the tick spacing, this function may run out of gas.

##### Recommended Mitigation Steps
Have a starting index parameter to start the iteration from. Also, `tickCount` can be made use of more meaningfully to limit the number of iterations performed.

```jsx
function getTickState(
	IConcentratedLiquidityPool pool,
	int24 startIndex,
	uint24 tickCount
) external view returns (SimpleTick[] memory) {
  SimpleTick[] memory ticks = new SimpleTick[](tickCount);

  IConcentratedLiquidityPool.Tick memory tick;
	int24 current = startIndex;

	for (uint24 i; i < tickCount; i++) {
		tick = pool.ticks(current);
		ticks[i] = SimpleTick({index: current, liquidity: tick.liquidity});
		// reached end of linked list, exit loop
		if (current == TickMath.MAX_TICK) break;
		// else, continue with next iteration
		current = tick.nextTick;
	}

  return ticks;
}
```

**[sarangparikh22 (Sushi) acknowledged](https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/17)**

**[alcueca (judge) commented](https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/17#issuecomment-967004172):**
 > Functionality is affected, severity 2.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sushi |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-sushitrident-2
- **GitHub**: https://github.com/code-423n4/2021-09-sushitrident-2-findings/issues/17
- **Contest**: https://code4rena.com/reports/2021-09-sushitrident-2

### Keywords for Search

`vulnerability`

