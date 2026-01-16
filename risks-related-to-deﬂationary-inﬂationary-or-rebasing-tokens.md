---
# Core Classification
protocol: Atlendis Labs Loan Products
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17585
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-atlendis-atlendissmartcontracts-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-atlendis-atlendissmartcontracts-securityreview.pdf
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
finders_count: 4
finders:
  - Gustavo Grieco
  - Nat Chin
  - Justin Jacob
  - Elvis Skozdopolj
---

## Vulnerability Title

Risks related to deﬂationary, inﬂationary, or rebasing tokens

### Overview


This bug report is about a data validation issue in the TickLogic.sol contract. The loan product and pool custodian contracts do not check that the expected amount has been sent on transfer. This can lead to incorrect accounting in both contracts if they do not receive enough assets because tokens are inflationary, deflationary, or rebase. This lack of validation can cause positions to become insolvent if the tokens take a fee, as the amount transferred can be less than expected. 

The short-term recommendation is to check the custodian balance during deposits and withdraws, and adjust the expected position amounts. Additionally, prevent the usage of rebasing tokens. For the long-term, the system should be robust against edge cases to the ERC20 specification. This can be done by reviewing the token integration checklist in Appendix I.

### Original Finding Content

## Diﬃculty: Low

## Type: Data Validation

### Target: TickLogic.sol

## Description
The loan product contract and the pool custodian contract do not check that the expected amount has been sent on transfer. This can lead to incorrect accounting in both contracts if they do not receive enough assets because tokens are inflationary, deflationary, or rebase.

Each lending product uses a pool custodian contract that holds custody of all ERC20 assets and through which the product contract deposits and withdraws the assets:

```solidity
function _deposit (uint256 amount, address from) private {
    collectRewards();
    depositedBalance += amount;
    token.safeTransferFrom(from, address(this), amount);
    bytes memory returnData = adapterDelegateCall(adapter, abi.encodeWithSignature('deposit(uint256)', amount));
    if (!abi.decode(returnData, (bool))) revert DELEGATE_CALL_FAIL();
    emit Deposit(amount, from, adapter, yieldProvider);
}
```

**Figure 9.1:** deposit function in the PoolCustodian contract

`safeTransferFrom` does not check that the expected value was transferred. If the tokens take a fee, the amount transferred can be less than expected. Similarly, the product contracts assume that the received amount is the same as the inputted amount. As a result, the custodian contract may hold fewer tokens than expected, and the accounting of the product may be incorrect.

## Exploit Scenario
USDT enables a 0.5% fee on transfers. Every deposit to a product leads to the creation of positions with more tokens than received. As a result, the positions become insolvent.

---

## Recommendations
Short-term, check the custodian balance during deposits and withdrawals, and adjust the expected position amounts. Be aware that some commonly used assets, such as USDT, can enable fees in the future. Additionally, prevent the usage of rebasing tokens.

Long-term, review the token integration checklist in Appendix I, and ensure that the system is robust against edge cases to the ERC20 specification.

## References
- Incident with non-standard ERC20 deflationary tokens

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Atlendis Labs Loan Products |
| Report Date | N/A |
| Finders | Gustavo Grieco, Nat Chin, Justin Jacob, Elvis Skozdopolj |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-atlendis-atlendissmartcontracts-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2023-03-atlendis-atlendissmartcontracts-securityreview.pdf

### Keywords for Search

`vulnerability`

