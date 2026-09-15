---
# Core Classification
protocol: Curve DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17765
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/CurveDAO.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/CurveDAO.pdf
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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Gustavo Grieco
  - Josselin Feist
  - Michael Colburn
---

## Vulnerability Title

Early users will have a unfair advantage

### Overview


This bug report is about the data validation of the GaugeController.vy in the VotingEscrow. The bug is of low difficulty and it gives an unfair advantage to early users. This happens because the LiquidityGauge distributes a bonus based on the user's VotingEscrow token percentage. When the ERC20CRV contract is launched, it has 100% of the token supply, which allows the first token receivers to receive a significant and unfair bonus on their interest. The exploit scenario is that Eve deploys the system, locks half of the supply, and only puts the other half in distribution, thus earning significantly more interest than any other user. 

The short-term recommendation is to either remove the bonus based on the locked tokens or clearly document that early users will have an advantage in the system. The issues TOB-CURVE-DAO-001 and TOB-CURVE-DAO-002 must be considered when implementing the fix. The long-term recommendation is to write clear documentation of the different components' interactions and the asset dependencies and to consider an economical assessment.

### Original Finding Content

## Data Validation

**Type:** Data Validation  
**Target:** GaugeController.vy  

**Difficulty:** Low  

## Description

The VotingEscrow’s bonus for earned interest gives an unfair advantage to early users. LiquidityGauge distributes a bonus based on the user’s VotingEscrow token percentage:

```python
def _update_liquidity_limit(addr: address, l: uint256, L: uint256):
    # To be called after totalSupply is updated
    _voting_escrow: address = self.voting_escrow
    voting_balance: uint256 = ERC20(_voting_escrow).balanceOf(addr)
    voting_total: uint256 = ERC20(_voting_escrow).totalSupply()
    lim: uint256 = l * 20 / 100
    if voting_total > 0:
        lim += L * voting_balance / voting_total * 80 / 100
    lim = min(l, lim)
```

*Figure 3.1: LiquidityGauge.vy#L75-L88* 

At launch, the ERC20CRV contract has 100% of the token supply, so it and the first token receivers can receive a significant and unfair bonus on their interest. Combined with TOB-CURVE-DAO-001, this issue will allow early users to earn significant profits.  

## Exploit Scenario

Eve deploys the system, locks half of the supply, and only puts the other half in distribution. As a result, Eve earns significantly more interest than any other user.

## Recommendation

Short term, consider either:
- Removing the bonus based on the locked tokens, or
- Clearly documenting that early users will have an advantage in the system.

Issues TOB-CURVE-DAO-001 and TOB-CURVE-DAO-002 must be considered when implementing the fix.  

Long term, write clear documentation of the different components’ interactions and the asset dependencies. Consider an economical assessment.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Curve DAO |
| Report Date | N/A |
| Finders | Gustavo Grieco, Josselin Feist, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/CurveDAO.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/CurveDAO.pdf

### Keywords for Search

`vulnerability`

