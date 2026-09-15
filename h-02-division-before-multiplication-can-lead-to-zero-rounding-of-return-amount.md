---
# Core Classification
protocol: Illuminate
chain: everychain
category: arithmetic
vulnerability_type: rounding

# Attack Vector Details
attack_type: rounding
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25270
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-illuminate
source_link: https://code4rena.com/reports/2022-06-illuminate
github_link: https://github.com/code-423n4/2022-06-illuminate-findings/issues/48

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
  - rounding
  - precision_loss

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

[H-02] Division Before Multiplication Can Lead To Zero Rounding Of Return Amount

### Overview


A bug has been identified in the `lend()` function of the 2022-06-illuminate codebase, which could potentially lead to users losing their funds. This bug occurs when the `order.premium` is less than `order.principal`. This bug is due to the code performing division before multiplication, which can lead to integer rounding and a resulting `returned` value of zero. If this occurs, the user’s funds will be transferred but the amount sent to `yield(u, y, returned, address(this))` will be zero.

The recommended mitigation steps are for the multiplication to occur before division, that is `((a[i] - fee) * order.premium) / order.principal);`. This has been confirmed by JTraversa (Illuminate) and Alex the Entreprenerd (warden) has suggested looking at how Swivel Calculates it.

### Original Finding Content

_Submitted by kirk-baird, also found by csanuragjain, datapunk, and ladboy233_

There is a division before multiplication bug that exists in [`lend()`](https://github.com/code-423n4/2022-06-illuminate/blob/92cbb0724e594ce025d6b6ed050d3548a38c264b/lender/Lender.sol#L280) for the Swivel case.

If `order.premium` is less than `order.principal` then `returned` will round to zero due to the integer rounding.

When this occurs the user's funds are essentially lost. That is because they transfer in the underlying tokens but the amount sent to `yield(u, y, returned, address(this))` will be zero.

### Proof of Concept

```solidity
    function lend(
        uint8 p,
        address u,
        uint256 m,
        uint256[] calldata a,
        address y,
        Swivel.Order[] calldata o,
        Swivel.Components[] calldata s
    ) public unpaused(p) returns (uint256) {

        // lent represents the number of underlying tokens lent
        uint256 lent;
        // returned represents the number of underlying tokens to lend to yield
        uint256 returned;

        {
            uint256 totalFee;
            // iterate through each order a calculate the total lent and returned
            for (uint256 i = 0; i < o.length; ) {
                Swivel.Order memory order = o[i];
                // Require the Swivel order provided matches the underlying and maturity market provided
                if (order.underlying != u) {
                    revert NotEqual('underlying');
                } else if (order.maturity > m) {
                    revert NotEqual('maturity');
                }
                // Determine the fee
                uint256 fee = calculateFee(a[i]);
                // Track accumulated fees
                totalFee += fee;
                // Sum the total amount lent to Swivel (amount of ERC5095 tokens to mint) minus fees
                lent += a[i] - fee;
                // Sum the total amount of premium paid from Swivel (amount of underlying to lend to yield)
                returned += (a[i] - fee) * (order.premium / order.principal);

                unchecked {
                    i++;
                }
            }
            // Track accumulated fee
            fees[u] += totalFee;

            // transfer underlying tokens from user to illuminate
            Safe.transferFrom(IERC20(u), msg.sender, address(this), lent);
            // fill the orders on swivel protocol
            ISwivel(swivelAddr).initiate(o, a, s);

            yield(u, y, returned, address(this));
        }

        emit Lend(p, u, m, lent);
        return lent;
    }
```

Specifically the function `returned += (a[i] - fee) * (order.premium / order.principal);`

### Recommended Mitigation Steps

The multiplication should occur before division, that is `((a[i] - fee) * order.premium) / order.principal);`.

**[JTraversa (Illuminate) confirmed](https://github.com/code-423n4/2022-06-illuminate-findings/issues/48)** 

**[Alex the Entreprenerd (warden) commented](https://github.com/code-423n4/2022-06-illuminate-findings/issues/48#issuecomment-1195909365):**
 > Also see how [Swivel Calculates it](https://github.com/Swivel-Finance/swivel/blob/0ce3edfd05e3546a10ff9d751ead219c0ba35d21/contracts/v2/swivel/Swivel.sol#L131)



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
- **GitHub**: https://github.com/code-423n4/2022-06-illuminate-findings/issues/48
- **Contest**: https://code4rena.com/reports/2022-06-illuminate

### Keywords for Search

`Rounding, Precision Loss`

