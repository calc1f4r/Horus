---
# Core Classification
protocol: yAxis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42289
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-09-yaxis
source_link: https://code4rena.com/reports/2021-09-yaxis
github_link: https://github.com/code-423n4/2021-09-yaxis-findings/issues/113

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
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-10] `YAxisVotePower.balanceOf` can be manipulated

### Overview


The YAxisVotePower.balanceOf contract uses the Uniswap pool reserves to calculate rewards. However, the pool can be manipulated to increase the reserves, allowing an attacker to increase their voting power and pass a proposal. A solution would be to implement a TWAP-style contract that tracks a time-weighted-average reserve amount to prevent manipulation. The severity of this issue has been debated, with some saying it is a valid concern while others argue it can be mitigated by only allowing trusted accounts to call balanceOf during governance votes. However, it is still possible for an attacker to frontrun the voting power by buying and selling their position on the same block as the vote count. Therefore, the severity of this issue has been classified as medium.

### Original Finding Content

_Submitted by cmichel_

The `YAxisVotePower.balanceOf` contract uses the Uniswap pool reserves to compute a `_lpStakingYax` reward:

```solidity
(uint256 _yaxReserves,,) = yaxisEthUniswapV2Pair.getReserves();
int256 _lpStakingYax = _yaxReserves
    .mul(_stakeAmount)
    .div(_supply)
    .add(rewardsYaxisEth.earned(_voter));
```

The pool can be temporarily manipulated to increase the `_yaxReserves` amount.

#### Impact
If this voting power is used for governance proposals, an attacker can increase their voting power and pass a proposal.

#### Recommended Mitigation Steps
One could build a TWAP-style contract that tracks a time-weighted-average reserve amount (instead of the price in traditional TWAPs).
This can then not be manipulated by flashloans.

**[uN2RVw5q commented](https://github.com/code-423n4/2021-09-yaxis-findings/issues/113#issuecomment-932350186):**
 > I disagree with the "sponsor disputed" tag.
>
> I think this is a valid issue and makes `balanceOf(_voter)` susceptible to flashloan attacks. However, as long as `balanceOf(_voter)` is always called by a trusted EOA during governance vote counts, this should not be a problem. I assume this is the case for governance proposals. If that is not the case, I would recommend changing the code. Otherwise, changing the risk to "documentation" would be reasonable.

**[GalloDaSballo (judge) commented](https://github.com/code-423n4/2021-09-yaxis-findings/issues/113#issuecomment-943463853):**
 > Agree with original warden finding, as well as severity
>
> The ability to trigger the count at any time does prevent a flashloan attack (as flashloans are atomic)
> It would allow the privilege of the flashloan attack to the trusted EOA (admin privilege)
>
> Additionally the voting power can still be frontrun, while you cannot manipulate that voting power via a flashloan, you can just buy and sell your position on the same block as when the count is being taken
>
> Due to this I will up the severity back to medium as this is a legitimate vector to extract value



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | yAxis |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-yaxis
- **GitHub**: https://github.com/code-423n4/2021-09-yaxis-findings/issues/113
- **Contest**: https://code4rena.com/reports/2021-09-yaxis

### Keywords for Search

`vulnerability`

