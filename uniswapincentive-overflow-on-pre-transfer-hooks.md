---
# Core Classification
protocol: Fei Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13547
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/01/fei-protocol/
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - launchpad

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Alexander Wade
  -  Sergii Kravchenko
  - Valentin Wüstholz
---

## Vulnerability Title

UniswapIncentive overflow on pre-transfer hooks

### Overview


This bug report describes a vulnerability in the Fei Protocol Core code, in which the incentivizeBuy and incentivizeSell functions perform some combination of mint/burn operations, which could lead to unintended consequences like allowing a caller to mint tokens before transferring them or burning tokens from their recipient. This is caused by the getBuyIncentive and getSellPenalty functions, which calculate price deviations after casting the amount to an int256, which may overflow. The recommended solution is to ensure casts in these functions do not overflow. This was addressed in fei-protocol/fei-protocol-core#15.

### Original Finding Content

#### Resolution



This was addressed in [fei-protocol/fei-protocol-core#15](https://github.com/fei-protocol/fei-protocol-core/pull/15).


#### Description


Before a token transfer is performed, `Fei` performs some combination of mint/burn operations via `UniswapIncentive.incentivize`:


**code/contracts/token/UniswapIncentive.sol:L49-L65**



```
function incentivize(
	address sender,
	address receiver, 
	address operator,
	uint amountIn
) external override onlyFei {
    updateOracle();

	if (isPair(sender)) {
		incentivizeBuy(receiver, amountIn);
	}

	if (isPair(receiver)) {
        require(isSellAllowlisted(sender) || isSellAllowlisted(operator), "UniswapIncentive: Blocked Fei sender or operator");
		incentivizeSell(sender, amountIn);
	}
}

```
Both `incentivizeBuy` and `incentivizeSell` calculate buy/sell incentives using overflow-prone math, then mint / burn from the target according to the results. This may have unintended consequences, like allowing a caller to mint tokens before transferring them, or burn tokens from their recipient.


#### Examples


`incentivizeBuy` calls `getBuyIncentive` to calculate the final minted value:


**code/contracts/token/UniswapIncentive.sol:L173-L186**



```
function incentivizeBuy(address target, uint amountIn) internal ifMinterSelf {
	if (isExemptAddress(target)) {
		return;
	}

    (uint incentive, uint32 weight,
    Decimal.D256 memory initialDeviation,
    Decimal.D256 memory finalDeviation) = getBuyIncentive(amountIn);

    updateTimeWeight(initialDeviation, finalDeviation, weight);
    if (incentive != 0) {
        fei().mint(target, incentive);        
    }
}

```
`getBuyIncentive` calculates price deviations after casting `amount` to an `int256`, which may overflow:


**code/contracts/token/UniswapIncentive.sol:L128-L134**



```
function getBuyIncentive(uint amount) public view override returns(
    uint incentive,
    uint32 weight,
    Decimal.D256 memory initialDeviation,
    Decimal.D256 memory finalDeviation
) {
    (initialDeviation, finalDeviation) = getPriceDeviations(-1 \* int256(amount));

```
#### Recommendation


Ensure casts in `getBuyIncentive` and `getSellPenalty` do not overflow.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Fei Protocol |
| Report Date | N/A |
| Finders | Alexander Wade,  Sergii Kravchenko, Valentin Wüstholz |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/01/fei-protocol/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

