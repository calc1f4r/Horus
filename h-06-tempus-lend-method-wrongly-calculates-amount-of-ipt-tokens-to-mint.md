---
# Core Classification
protocol: Illuminate
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25274
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-illuminate
source_link: https://code4rena.com/reports/2022-06-illuminate
github_link: https://github.com/code-423n4/2022-06-illuminate-findings/issues/222

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
  - yield
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-06] Tempus lend method wrongly calculates amount of iPT tokens to mint

### Overview


A bug has been reported in the Tempus `lend` method, which calculates the amount of tokens to mint as `amountReturnedFromTempus - lenderBalanceOfMetaPrincipalToken`. This calculation is incorrect as it has no relation to the iPT token. As a result, users are receiving the wrong amount of iPT tokens, or even 0 tokens if the Lender contract has an iPT balance. The issue is caused by the Tempus `depositAndFix` method, which does not return anything, leading to the calculation to revert or return 0.

The recommended mitigation steps involve checking how many Tempus principal tokens the contract has received before and after the swap, and the difference in the two amounts is the amount that was received. This has been confirmed by Illuminate.

### Original Finding Content

_Submitted by kenzo, also found by cccz, Metatron, unforgiven, and WatchPug_

The Tempus `lend` method calculates the amount of tokens to mint as `amountReturnedFromTempus - lenderBalanceOfMetaPrincipalToken`.
This seems wrong as there's no connection between the two items. Tempus has no relation to the iPT token.

### Impact

Wrong amount of iPT will be minted to the user.
If the Lender contract has iPT balance, the function will revert, otherwise, user will get minted 0 iPT tokes.

### Proof of Concept

[This](https://github.com/code-423n4/2022-06-illuminate/blob/main/lender/Lender.sol#L465:#L469) is how the `lend` method calculates the amount of iPT tokens to mint:

            uint256 returned = ITempus(tempusAddr).depositAndFix(Any(x), Any(t), a - fee, true, r, d) -
                illuminateToken.balanceOf(address(this));
            illuminateToken.mint(msg.sender, returned);

The Tempus `depositAndFix` method [does not return](https://etherscan.io/address/0xdB5fD0678eED82246b599da6BC36B56157E4beD8#code#F1#L127) anything.
Therefore this calculation will revert if `illuminateToken.balanceOf(address(this)) > 0`, or will return 0 if the balance is 0.

\[Note: there's another issue here where the depositAndFix sends wrong parameters - I will submit it in another issue.]

### Recommended Mitigation Steps

I believe that what you intended to do is to check how many Tempus principal tokens the contract received.

So you need to check Lender's `x.tempusPool().principalShare()` before and after the swap, and the delta is the amount received.

**[sourabhmarathe (Illuminate) confirmed](https://github.com/code-423n4/2022-06-illuminate-findings/issues/222)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Illuminate |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-illuminate
- **GitHub**: https://github.com/code-423n4/2022-06-illuminate-findings/issues/222
- **Contest**: https://code4rena.com/reports/2022-06-illuminate

### Keywords for Search

`vulnerability`

