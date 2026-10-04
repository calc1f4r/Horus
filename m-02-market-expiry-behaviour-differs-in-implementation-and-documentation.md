---
# Core Classification
protocol: prePO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1660
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-03-prepo-contest
source_link: https://code4rena.com/reports/2022-03-prepo
github_link: https://github.com/code-423n4/2022-03-prepo-findings/issues/28

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
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - leastwood  rayn
  - GreyArt
---

## Vulnerability Title

[M-02] Market expiry behaviour differs in implementation and documentation

### Overview


This bug report is about a vulnerability in the PrePOMarket smart contract. The vulnerability is that the expiry date is ignored in the implementation, so the default settlement after expiry is a 1:1 ratio of long and short token for 1 collateral token instead of the lower bound of its Valuation Range as stated in the documentation. This could lead to users incurring swap fees from having to swap some short tokens back for long tokens for redemption, and also affect user funds should long tokens be repurchased at a higher price than when they were sold. 

To mitigate this issue, the logic should be added to the implementation to settle at the lower valuation after expiry, or the documentation should be updated to reflect the default behaviour of 1:1 redemption. The recommended mitigation steps are provided in the report.

### Original Finding Content

_Submitted by GreyArt, also found by leastwood and rayn_

[prePO Docs: Expiry](https://docs.prepo.io/concepts/markets#expiry)<br>
[PrePOMarket.sol#L145-L156](https://github.com/code-423n4/2022-03-prepo/blob/main/contracts/core/PrePOMarket.sol#L145-L156)<br>

The docs say that “If a market has not settled by its expiry date, it will automatically settle at the lower bound of its Valuation Range.”

However, in the implementation, the expiry date is entirely ignored. The default settlement after expiry is a 1:1 ratio of long and short token for 1 collateral token.

### Impact

Should users believe that the market will settle at the lower bound, they would swap and hold long for short tokens instead of at a 1:1 ratio upon expiry. Thereafter, they would incur swap fees from having to swap some short tokens back for long tokens for redemption. User funds are also  affected should long tokens are repurchased at a higher price than when they were sold.

### Recommended Mitigation Steps

If the market is to settle at the lower valuation after expiry, then the following logic should be added:

```jsx
// market has expired
// settle at lower bound
if (block.timestamp > _expiryTime) {
	uint256 _shortPrice = MAX_PRICE - _floorLongPrice;
	_collateralOwed =
		(_floorLongPrice * _longAmount + _shortPrice * _shortAmount) /
		MAX_PRICE;
} else if (_finalLongPrice <= MAX_PRICE) {
	...
} else {
	...
}
```

Otherwise, the documentation should be updated to reflect the default behaviour of 1:1 redemption.

**[ramenforbreakfast (prePO) disagreed with Medium severity](https://github.com/code-423n4/2022-03-prepo-findings/issues/28)**

**[ramenforbreakfast (prePO) agreed with Medium severity and commented](https://github.com/code-423n4/2022-03-prepo-findings/issues/28#issuecomment-1075730207):**
 > This is a valid submission, no longer disagreeing with severity as we clearly stated that expiry should be enforceable. 
> 
> This was a mistake on our part and I think we ended up not using `expiryTime` since the only thing that really mattered was if the `finalLongPrice` was set. We should decide whether to enforce it or remove it altogether.

**[gzeon (judge) commented](https://github.com/code-423n4/2022-03-prepo-findings/issues/28#issuecomment-1086869183):**
 > Agree with sponsor.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | prePO |
| Report Date | N/A |
| Finders | leastwood  rayn, GreyArt |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-prepo
- **GitHub**: https://github.com/code-423n4/2022-03-prepo-findings/issues/28
- **Contest**: https://code4rena.com/contests/2022-03-prepo-contest

### Keywords for Search

`vulnerability`

