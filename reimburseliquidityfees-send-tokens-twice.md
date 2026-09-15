---
# Core Classification
protocol: Connext
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7228
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - business_logic

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0xLeastwood
  - Jonah1005
---

## Vulnerability Title

reimburseLiquidityFees send tokens twice

### Overview


This bug report is about the function reimburseLiquidityFees() which is called from the BridgeFacet. When using tokenExchanges viaswapExactIn(), tokens are sent to msg.sender, which is the BridgeFacet, and then sent again to msg.sender viasafeTransfer(), which is also the BridgeFacet. Therefore, tokens end up being sent to the BridgeFacet twice. This bug was introduced with the fix in C4.

The recommendation is to double check the code to see what the intended behavior is. The bug has been solved in PR 1551 and verified by Spearbit.

### Original Finding Content

## High Risk Report

## Severity 
High Risk

## Context 
- **Files**: 
  - BridgeFacet.sol (Lines 644-675)
  - SponsorVault.sol (Lines 197-226)
  - ITokenExchange.sol (Lines 18-24)

## Description 
The function `reimburseLiquidityFees()` is called from the `BridgeFacet`, making the `msg.sender` within this function to be the `BridgeFacet`. 

When using token exchanges via `swapExactIn()`, tokens are sent to `msg.sender`, which is the `BridgeFacet`. Then, tokens are sent again to `msg.sender` via `safeTransfer()`, which is also the `BridgeFacet`. Therefore, tokens end up being sent to the `BridgeFacet` twice.

**Note:** The check `...balanceOf(...) != starting + sponsored` should fail too.

**Note:** The fix in C4 seems to introduce this issue: `code4rena-246`.

### Code Snippet
```solidity
contract BridgeFacet is BaseConnextFacet {
    function _handleExecuteTransaction(...) ... {
        ...
        uint256 starting = IERC20(_asset).balanceOf(address(this));
        ...
        (bool success, bytes memory data) = address(s.sponsorVault).call(
            abi.encodeWithSelector(s.sponsorVault.reimburseLiquidityFees.selector, _asset, _args.amount, _args.params.to)
        );
        if (success) {
            uint256 sponsored = abi.decode(data, (uint256));
            // Validate correct amounts are transferred
            if (IERC20(_asset).balanceOf(address(this)) != starting + sponsored) { // this should fail now
                revert BridgeFacet__handleExecuteTransaction_invalidSponsoredAmount();
            }
        }
        ...
    }
}
```

```solidity
contract SponsorVault is ISponsorVault, ReentrancyGuard, Ownable {
    function reimburseLiquidityFees(...) {
        if (address(tokenExchanges[_token]) != address(0)) {
            ...
            sponsoredFee = tokenExchange.swapExactIn{value: amountIn}(_token, msg.sender); // send to msg.sender
        } else {
            ...
        }
        ...
        IERC20(_token).safeTransfer(msg.sender, sponsoredFee); // send again to msg.sender
    }
}
```

### Interface
```solidity
interface ITokenExchange {
    /**
     * @notice Swaps the exact amount of native token being sent for a given token.
     * @param token The token to receive
     * @param recipient The recipient of the token
     * @return The amount of tokens resulting from the swap
     */
    function swapExactIn(address token, address recipient) external payable returns (uint256);
}
```

## Recommendation 
Doublecheck the code to see what the intended behavior is.

## Connext 
Solved in PR 1551.

## Spearbit 
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | 0xLeastwood, Jonah1005 |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf

### Keywords for Search

`Business Logic`

