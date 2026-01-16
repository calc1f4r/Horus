---
# Core Classification
protocol: NetMind
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59209
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/net-mind/e7dfdc3c-7589-4fc8-b3d8-4872c783a735/index.html
source_link: https://certificate.quantstamp.com/full/net-mind/e7dfdc3c-7589-4fc8-b3d8-4872c783a735/index.html
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
  - Jennifer Wu
  - Cameron Biniamow
  - Jonathan Mevs
---

## Vulnerability Title

Proposal Parameters Are Susceptible to Slippage and Sandwich Attacks

### Overview


The report discusses a bug in the `LiquidityFundsManage.sol` file where certain functions, such as `buy_P()` and `sell_P()`, can be manipulated by external actors. This makes the proposal parameters vulnerable to slippage and sandwich attacks. The report recommends adding a new input parameter for minimum amount to prevent manipulation, enhancing slippage protection, and introducing a mechanism to reject proposals based on manipulated parameters. 

### Original Finding Content

**Update**
The client acknowledged the issue and provided the following explanation:

> In this case, setting specific values and calculating them during proposal execution are essentially the same, as the final decision is made by the last vote cast. Therefore, whether specific values are written in or the current method is used to execute with slippage, the issue remains. It just requires each administrator to check the minimum parameters when voting.

**File(s) affected:**`LiquidityFundsManage.sol`

**Description:** The functions `buy_P()`, `sell_P()`, `addLiquidity_P()`, and `removeLiquidity_P()` allow the manager to create proposals for liquidity operations. However, these proposals are based on parameters that can be manipulated through changes in the Pancake pair pool, making the proposal parameters vulnerable to slippage and sandwich attacks.

Key issues include:

1.   Parameter Manipulation: The calculation of `amountMinOut` for `buy_P()` and `sell_P()`, and liquidity proportions in `removeLiquidity_P()` and `addLiquidity_P()` , can be manipulated by external actors. 
2.   Inadequate Slippage Protection: The slippage parameter is a percentage of potentially manipulated values, providing insufficient protection.
3.   Lack of Proposal Rejection Mechanism: There is no mechanism to reject a proposal based on manipulated parameters; the manager can only wait for the proposal to expire.

**Recommendation:**

1.   Introduce Minimum Amount Parameter: Add a new input parameter for the minimum amount that is not susceptible to on-chain manipulation. This will help in ensuring that the parameters used in proposals are within acceptable ranges and not easily manipulated.

2.   Enhance Slippage Protection: With the new minimum amount parameter, ensure that slippage is calculated based on this parameter rather than manipulatable values.

3.   Proposal Rejection Mechanism: Introduce a mechanism that allows the rejection of proposals if they are found to be based on manipulated parameters. This can involve additional validation steps or community voting to approve or reject proposals before execution.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | NetMind |
| Report Date | N/A |
| Finders | Jennifer Wu, Cameron Biniamow, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/net-mind/e7dfdc3c-7589-4fc8-b3d8-4872c783a735/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/net-mind/e7dfdc3c-7589-4fc8-b3d8-4872c783a735/index.html

### Keywords for Search

`vulnerability`

