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
solodit_id: 25269
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-illuminate
source_link: https://code4rena.com/reports/2022-06-illuminate
github_link: https://github.com/code-423n4/2022-06-illuminate-findings/issues/37

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

[H-01] The lend function for tempus uses the wrong return value of depositAndFix

### Overview



A bug has been reported in the TempusController contract of the Tempus Protocol, which is used to mint IlluminateTokens. The depositAndFix function of the contract returns two uint256 data, the first is the number of shares exchanged for the underlying token, the second is the number of principalToken exchanged for the shares. The second return value should be used in the lend function for tempus. However, due to an error, the second return value is not being used, which causes the contract to mint an incorrect number of IlluminateTokens to the user. 

To verify the bug, the code can be seen at the Github link provided. The recommended mitigation steps to fix the bug include adding a line of code to the interfaces.sol file and the Lender.sol file. In the interfaces.sol file, the ITEMPUS interface should be added, which includes the depositAndFix function. In the Lender.sol file, the code should be amended to subtract the IlluminateToken balance from the returned value of the depositAndFix function. This will ensure that the correct number of IlluminateTokens are minted to the user. The bug has been confirmed by Sourabhmarathe (Illuminate).

### Original Finding Content

_Submitted by cccz, also found by 0x52 and datapunk_

The depositAndFix function of the TempusController contract returns two uint256 data, the first is the number of shares exchanged for the underlying token, the second is the number of principalToken exchanged for the shares, the second return value should be used in the lend function for tempus.

This will cause the contract to mint an incorrect number of illuminateTokens to the user.

### Proof of Concept

<https://github.com/code-423n4/2022-06-illuminate/blob/92cbb0724e594ce025d6b6ed050d3548a38c264b/lender/Lender.sol#L452-L453>

<https://github.com/tempus-finance/tempus-protocol/blob/master/contracts/TempusController.sol#L52-L76>

### Recommended Mitigation Steps

interfaces.sol

    interface ITempus {
        function maturityTime() external view returns (uint256);

        function yieldBearingToken() external view returns (IERC20Metadata);

        function depositAndFix(
            Any,
            Any,
            uint256,
            bool,
            uint256,
            uint256
        ) external returns (uint256, uint256);
    }

Lender.sol

            (,uint256 returned) = ITempus(tempusAddr).depositAndFix(Any(x), Any(t), a - fee, true, r, d);
            returned -= illuminateToken.balanceOf(address(this));

**[sourabhmarathe (Illuminate) confirmed](https://github.com/code-423n4/2022-06-illuminate-findings/issues/37)**



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
- **GitHub**: https://github.com/code-423n4/2022-06-illuminate-findings/issues/37
- **Contest**: https://code4rena.com/reports/2022-06-illuminate

### Keywords for Search

`vulnerability`

