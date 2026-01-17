---
# Core Classification
protocol: Yieldy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2899
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-06-yieldy-contest
source_link: https://code4rena.com/reports/2022-06-yieldy
github_link: https://github.com/code-423n4/2022-06-yieldy-findings/issues/172

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Alex the Entreprenerd
---

## Vulnerability Title

[M-24] Staking `preSign` could use some basic validations

### Overview


This bug report concerns the function `preSign` in the Staking.sol contract in the 2022-06-yieldy repository on GitHub. This function accepts any `orderUid` without any validation. This can be exploited as a rug-vector, as the orderData contains a `receiver` address that can be any address without validation. The recommended mitigation steps are to add basic validation for tokenOut, minOut, and receiver. The code from Badger can be used for validation, which has been validated by the original Cowswap / GPv2 Developers. Additionally, code can be reused from the original Cowswap / GPv2 Developers to reconstruct the `orderUid`.

### Original Finding Content

_Submitted by Alex the Entreprenerd_

The function `preSign` accepts any `orderUid`.<br>
`function preSign(bytes calldata orderUid) external onlyOwner`

Because of how Cowswap works, accepting any `orderUid` can be used as a rug-vector.

This is because the orderData contains a `receiver` which in lack of validation could be any address.

You'd also be signing other parameters such as minOut and how long the order could be filled for, which you may or may not want to validate to give stronger security guarantees to end users.

### Recomended Mitigation Steps

I'd recommend adding basic validation for tokenOut, minOut and receiver.

Feel free to check the work we've done at Badger to validate order parameters, giving way stronger guarantees to end users.
<https://github.com/GalloDaSballo/fair-selling/blob/44c0c0629289a0c4ccb3ca971cc5cd665ce5cb82/contracts/CowSwapSeller.sol#L194>

Also notice how through the code above we are able to re-construct the `orderUid`, feel free to re-use that code which has been validated by the original Cowswap / GPv2 Developers.

**[toshiSat (Yieldy) confirmed, resolved and commented](https://github.com/code-423n4/2022-06-yieldy-findings/issues/172#issuecomment-1201510899):**
 > Thanks for the functions, I like what you guys did.  Our cowswap function is only called using the `onlyOwner` modifier, so I think it's pretty safe, but I agree some validation would be better than none.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Yieldy |
| Report Date | N/A |
| Finders | Alex the Entreprenerd |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-yieldy
- **GitHub**: https://github.com/code-423n4/2022-06-yieldy-findings/issues/172
- **Contest**: https://code4rena.com/contests/2022-06-yieldy-contest

### Keywords for Search

`vulnerability`

