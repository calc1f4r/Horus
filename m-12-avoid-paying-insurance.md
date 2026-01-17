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
solodit_id: 25500
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-06-tracer
source_link: https://code4rena.com/reports/2021-06-tracer
github_link: https://github.com/code-423n4/2021-06-tracer-findings/issues/30

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

[M-12] avoid paying insurance

### Overview


A bug has been identified in the code of a project that allows users to avoid paying insurance. This bug can be exploited by using a flash loan or large amount of tokens to call `deposit` of `Insurance.sol` to ensure the pool is sufficiently filled, followed by calling the function `executeTrade` of `Trader`.sol` with a minimal trade. This will then call `recordTrade` which calls `updateFundingRate` and `getPoolFundingRate`, resulting in the insurance rate being set to 0. The user can then withdraw from the Insurance and pay back the flash loan.

The severity of this bug has been debated, with some suggesting it is a medium risk as a front-runner could keep doing this for not paying any funding using a bot, while others disagree with the severity, noting that executing this exploit once would only cause insurance funding to not be paid for a single hour, and that for insurance funding to never be paid, the exploit would have to be timed as the first transaction on each and every hour, which would quickly be noticed.

The code referenced in the proof of concept can be found on the issue page, and it is recommended to set a timelock on withdrawing insurance.

### Original Finding Content

_Submitted by gpersoon_

It's possible to avoid paying insurance in the following way:

- once per hour (at the right moment), do the following:
1. using a flash loan, or with a large amount of tokens, call `deposit` of `Insurance.sol` to make sure that the pool is sufficiently filled (`poolHoldings` > `poolTarget`)
2. call the function `executeTrade` of Trader`.sol` with a minimal trade (possibly of value 0, see finding "`executeTrade` with same trades")
3. `executeTrade` calls `matchOrders`, which calls `recordTrade`
4. `recordTrade` calls `updateFundingRate()`;   (once per hour, so you have to be sure you do it in time before other trades trigger this)
5. `updateFundingRate` calls `getPoolFundingRate`
6. `getPoolFundingRate` determines the insurance rate, but because the insurance pool is sufficiently full (due to the flash loan), the rate is 0
7. `updateFundingRate` stores the 0 rate via `setInsuranceFundingRate`  (which is used later on to calculate the amounts for the insurances)
8. withdraw from the Insurance and pay back the flash loan

The insurance rates are 0 now and no-one pays insurance. The gas costs relative to the insurance costs + the flash loan fees determine if this is an economically viable attack. Otherwise it is still a grief attack.
This will probably be detected pretty soon because the insurance pool will stay empty. However its difficult to prevent.

See issue page for code referenced in proof of concept.

Recommend setting a timelock on withdrawing insurance.

**[raymogg (Tracer) confirmed but disagreed with severity](https://github.com/code-423n4/2021-06-tracer-findings/issues/30#issuecomment-873763520):**
 > Really like this exploit idea. Currently this is possible since the Trader is not whitelisted (eg there is no whitelisted relayer address). With this added, this exploit is no longer possible as only off chain relayers can place orders with the trader.
>
> Disagree with the severity mainly due to the fact that executing this exploit once would only cause insurance funding to not be paid for a single hour. For insurance funding to never be paid, you would have to time this transaction as the first transaction on each and every hour. This would quickly be noticed. The only affect on this would be insurance depositors miss interest payments for a few periods.

**[cemozerr (Judge) commented](https://github.com/code-423n4/2021-06-tracer-findings/issues/30#issuecomment-882109332):**
 > Marking this as medium risk as a front-runner could keep doing this for not paying any funding using a bot.



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

- **Source**: https://code4rena.com/reports/2021-06-tracer
- **GitHub**: https://github.com/code-423n4/2021-06-tracer-findings/issues/30
- **Contest**: https://code4rena.com/reports/2021-06-tracer

### Keywords for Search

`vulnerability`

