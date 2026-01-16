---
# Core Classification
protocol: Blueberry Update #3
chain: everychain
category: uncategorized
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24322
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/104
source_link: none
github_link: https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/18

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - wrong_math

protocol_categories:
  - rwa
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Vagner
---

## Vulnerability Title

M-2: `getPrice` in `WeightedBPTOracle.sol`  uses `totalSupply` for price calculations which can lead to wrong results

### Overview


This bug report is about the `getPrice` function in the `WeightedBPTOracle.sol` contract which is used to calculate the price of a given Balancer LP. The function is using `totalSupply` for every LP calculation which can lead to wrong results and assumptions. This is because, according to Balancer docs, there are three potential functions to query when determining the BPT supply depending on pool type, one of them being `getActualSupply`, which is used by the most recent Weighted and Stable Pools and it accounts for pre-minted BPT as well as due protocol fees. Using `totalSupply` for these pools can lead to very wrong calculations because of all the pre-minted BPT. The impact of this vulnerability is medium, since it can lead to wrong price assumptions. The code snippet of this bug can be found at https://github.com/sherlock-audit/2023-07-blueberry/blob/main/blueberry-core/contracts/oracle/WeightedBPTOracle.sol#L71-L73. The recommendation is to consider implementing the more recent `getActualSupply` even if older pools doesn't have this functions, because it can lead to wrong assumptions and calculations. During the judging contest, one comment was left on this issue, which stated that this could be a factor to exploit the pool in future.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/18 

## Found by 
Vagner
`getPrice` is used to calculate the price in USD of a given balancer LP, and it respects the recommendations  of Balancer docs by calculating the invariant and using it to protect from manipulations, but it uses `totalSupply` for every LP calculated which can lead to wrong results and assumptions.
## Vulnerability Detail
In the Balancer docs it is specified that `There are three potential functions to query when determining the BPT supply depending on pool type.` https://docs.balancer.fi/concepts/advanced/valuing-bpt/valuing-bpt.html#getting-bpt-supply
- `getActualSupply` : which is used by the most recent Weighted and Stable Pools and it accounts for pre-minted BPT as well as due protocol fees:
- `getVirtualSupply` : which is used by Linear Pools and "legacy" Stable Phantom Pools and it accounts just for pre-minted BPT
- `totalSupply` : which makes sense to be called only by older `legacy` pools since those doesn't have pre-minted BPT
The `getPrice` uses every time `totalSupply`
https://github.com/sherlock-audit/2023-07-blueberry/blob/main/blueberry-core/contracts/oracle/WeightedBPTOracle.sol#L71-L73
which in the case of most recent pools can lead to very wrong calculations because of all the pre-minted BPT.
## Impact
Impact is a medium one, since it can lead to wrong price assumptions
## Code Snippet
https://github.com/sherlock-audit/2023-07-blueberry/blob/main/blueberry-core/contracts/oracle/WeightedBPTOracle.sol#L71-L73
## Tool used

Manual Review

## Recommendation
Consider implementing the more recent `getActualSupply` even if older pools doesn't have this functions , because it can lead to wrong assumptions and calculations.



## Discussion

**sherlock-admin2**

1 comment(s) were left on this issue during the judging contest.

**YakuzaKiawe** commented:
>  invalid as this could be a factor to exploit the pool in future

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry Update #3 |
| Report Date | N/A |
| Finders | Vagner |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-07-blueberry-judging/issues/18
- **Contest**: https://app.sherlock.xyz/audits/contests/104

### Keywords for Search

`Wrong Math`

