---
# Core Classification
protocol: Kuiper
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19845
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-12-defiProtocol
source_link: https://code4rena.com/reports/2021-12-defiProtocol
github_link: https://github.com/code-423n4/2021-12-defiprotocol-findings/issues/60

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
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-08] Lost fees due to precision loss in fees calculation

### Overview


A bug has been discovered in the fees calculation of a Solidity contract. Division is being used in the midst of the calculation, rather than at the end, leading to lost precision in the fee amount. This can cause the protocol to leak value, with tests showing that in normal usage, 1% of fees are lost, and in some cases even 7.5%. The exact amount depends on the parameters set and being tested.

To mitigate this bug, the code should be changed so that all multiplication is done first, followed by all division. This can be done by removing the usage of feePct and setting fee to be: `uint256 fee = startSupply * licenseFee * timeDiff / ONE_YEAR / (BASE - licenseFee);` This has been confirmed by two members of the team and has been deemed as a 'medium' risk due to the protocol regularly leaking value.

### Original Finding Content

_Submitted by kenzo, also found by 0v3rf10w_

In fees calculation, division is being used in the midst of the calculation, not at the end of it.
This leads to lost precision in fee amount (as solidity doesn't save remainder of division).
Division should happen at the end to maintain precision.

### Impact

Lost fees.
The exact amount depends on the parameters set and being tested.
According to a few tests I ran, it seems that in normal usage, 1% of fees are lost.
In some cases even 7.5% of fees.

### Proof of Concept

Division in the midst of a calculation:
```solidity
uint256 feePct = timeDiff * licenseFee / ONE_YEAR;
uint256 fee = startSupply * feePct / (BASE - feePct);

_mint(publisher, fee * (BASE - factory.ownerSplit()) / BASE);
_mint(Ownable(address(factory)).owner(), fee * factory.ownerSplit() / BASE);
```

[Basket.sol#L140:#L145](https://github.com/code-423n4/2021-12-defiprotocol/blob/main/contracts/contracts/Basket.sol#L140:#L145)<br>
It's a little hard to share a POC script as it involves changing the .sol file so I tested it manually. But after moving the division to the end using the mitigation below, I saw 1%-7% increases in fees minted. Usually 1%.

### Recommended Mitigation Steps

We want to firstly do all multiplication and lastly do all the division.
So remove the usage of feePct and instead set fee to be:
```solidity
uint256 fee = startSupply * licenseFee * timeDiff / ONE_YEAR / (BASE - licenseFee);
```

**[frank-beard (Kuiper) confirmed](https://github.com/code-423n4/2021-12-defiprotocol-findings/issues/60)**

**[0xleastwood (judge) commented](https://github.com/code-423n4/2021-12-defiprotocol-findings/issues/60#issuecomment-1079826919):**
 > Nice find! I think this qualifies as `medium` risk due to the protocol regularly leaking value. This can be mitigated by performing division at the very end of the fee calculation.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Kuiper |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-defiProtocol
- **GitHub**: https://github.com/code-423n4/2021-12-defiprotocol-findings/issues/60
- **Contest**: https://code4rena.com/reports/2021-12-defiProtocol

### Keywords for Search

`vulnerability`

