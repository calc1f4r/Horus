---
# Core Classification
protocol: Escher
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6362
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-escher-contest
source_link: https://code4rena.com/reports/2022-12-escher
github_link: https://github.com/code-423n4/2022-12-escher-findings/issues/274

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - launchpad
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - csanuragjain
---

## Vulnerability Title

[M-05] Inconsistency in fees

### Overview


A bug report has been made regarding the FixedPrice.sol contract. The issue is that when the seller cancels a sale before the sale startTime, fees are deducted from the funds that should be moved to the saleReceiver. This could lead to a loss of funds.

The proof of concept for the bug is as follows: a new sale is started, the seller mistakenly sends ETH to the FixedPrice.sol contract, the seller realizes their mistake and tries to cancel the sale before the sale startTime, the _end function is called, and the fees are deducted from the funds that should be moved to the saleReceiver.

The recommended mitigation step to resolve this bug is to revise the cancel function. The revised code should look like this: 

```
function cancel() external onlyOwner {
        require(block.timestamp < sale.startTime, "TOO LATE");
        emit End(_sale);
        selfdestruct(_sale.saleReceiver);
    }
```

Overall, this bug report concerns the FixedPrice.sol contract and the issue of fees being deducted from funds that should be moved to the saleReceiver when the seller cancels a sale before the sale startTime. The recommended mitigation step is to revise the cancel function.

### Original Finding Content


If the seller cancels before the sale startTime then all funds should be moved to saleReceiver without any deduction (Assuming seller has sent some ETH accidentally before sell start). But in `FixedPrice.sol` contract, fees are deducted even when seller cancels before the sale startTime which could lead to loss of funds.

### Proof of Concept

1.  A new sale is started
2.  Seller selfdestructed one of his personal contracts and by mistake gave this sale contract as receiver. This forcefully sends the remaining 20 ETH to the  `FixedPrice.sol` contract.
3.  Seller realizes his mistake and tries to cancel the sale as sale as not yet started using the `cancel` function.

<!---->

    function cancel() external onlyOwner {
            require(block.timestamp < sale.startTime, "TOO LATE");
            _end(sale);
        }

4.  This internally calls the `\_end` function

<!---->

    function _end(Sale memory _sale) internal {
            emit End(_sale);
            ISaleFactory(factory).feeReceiver().transfer(address(this).balance / 20);
            selfdestruct(_sale.saleReceiver);
        }

5.  The `_end` function deducts fees of 20/20=1 ETH even though seller has cancelled before the sale starts.

### Recommended Mitigation Steps

Revise the `cancel` function

    function cancel() external onlyOwner {
            require(block.timestamp < sale.startTime, "TOO LATE");
            emit End(_sale);
            selfdestruct(_sale.saleReceiver);
        }

**[stevennevins (Escher) disagreed with severity and commented](https://github.com/code-423n4/2022-12-escher-findings/issues/274#issuecomment-1363395142):**
 > Marking as Low as it seems pretty unlikely of a scenario.

**[berndartmueller (judge) commented](https://github.com/code-423n4/2022-12-escher-findings/issues/274#issuecomment-1369770534):**
 > I consider Medium severity appropriate because fees are sent to the receiver even though a sale has not started yet. This also clearly deviates from the implementation in the `FixedPrice` contract, where fees are not sent in case the owner cancels a sale.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Escher |
| Report Date | N/A |
| Finders | csanuragjain |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-escher
- **GitHub**: https://github.com/code-423n4/2022-12-escher-findings/issues/274
- **Contest**: https://code4rena.com/contests/2022-12-escher-contest

### Keywords for Search

`vulnerability`

