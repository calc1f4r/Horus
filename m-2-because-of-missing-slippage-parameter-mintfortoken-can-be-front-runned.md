---
# Core Classification
protocol: USSD - Autonomous Secure Dollar
chain: everychain
category: economic
vulnerability_type: front-running

# Attack Vector Details
attack_type: front-running
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19142
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/82
source_link: none
github_link: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/97

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
  - front-running

protocol_categories:
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - shealtielanz
  - cryptostellar5
  - Kose
  - Aymen0909
  - 0xRobocop
---

## Vulnerability Title

M-2: Because of missing slippage parameter, mintForToken() can be front-runned

### Overview


A bug report has been filed for the missing slippage parameter in the ```mintForToken()``` function of the USSD contract. This lack of a parameter makes it vulnerable to front-run attacks, allowing a frontrunner to manipulate the reserves of the pool and make the transferred token appear more valuable than its actual worth. Consequently, users minting USSD may receive USSD that are worth significantly less than the value of their real worth. The issue was found by 0xRobocop, Aymen0909, GimelSec, Kose, cryptostellar5, qbs, and shealtielanz and was identified using manual review. 

The recommended solution is to add a ```minAmountOut``` parameter. This would help protect users from front-run attacks and ensure that they receive the full value of USSD they were expecting. 

The discussion around this issue included a comment from sherlock-admin that weighted average prices should be enough to prevent front-run attacks, to which kosedogus responded that weighted average prices do not guarantee that trades will be free from slippage. Shogoki then removed the escalation.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/97 

## Found by 
0xRobocop, Aymen0909, GimelSec, Kose, cryptostellar5, qbs, shealtielanz
## Summary
Missing slippage parameter in ```mintForToken()``` makes it vulnerable to front-run attacks and exposes users to unwanted slippage.
## Vulnerability Detail
The current implementation of the ```mintForToken()``` function lacks a parameter for controlling slippage, which makes it vulnerable to front-run attacks. Transactions involving large volumes are particularly at risk, as the minting process can be manipulated, resulting in price impact. This manipulation allows the reserves of the pool to be controlled, enabling a frontrunner to make the transferred token to appear more valuable than its actual worth. Consequently, when users mint USSD, they may receive USSD that are worth significantly less than the value of their real worth. This lack of slippage control resembles a swap without a limit on value manipulation.

## Impact
User will be vulnerable to front-run attacks and receive less USSD from their expectation.
## Code Snippet
[USSD.sol#L150-L167](https://github.com/USSDofficial/ussd-contracts/blob/f44c726371f3152634bcf0a3e630802e39dec49c/contracts/USSD.sol#L150-L167)
```solidity
/// Mint specific AMOUNT OF STABLE by giving token
    function mintForToken(
        address token,
        uint256 tokenAmount,
        address to
    ) public returns (uint256 stableCoinAmount) {
        require(hasCollateralMint(token), "unsupported token");

        IERC20Upgradeable(token).safeTransferFrom(
            msg.sender,
            address(this),
            tokenAmount
        );
        stableCoinAmount = calculateMint(token, tokenAmount);
        _mint(to, stableCoinAmount);

        emit Mint(msg.sender, to, token, tokenAmount, stableCoinAmount);
    }
```
## Tool used

Manual Review

## Recommendation
Consider adding a ```minAmountOut``` parameter.



## Discussion

**sherlock-admin**

> Removed: comment left for traceability 
> I think this is not a valid medium. 
> As the mintForToken function uses oracle prices, which return a weighted average price, it should not be that easy manipulated by Frontrunning.

    You've deleted an escalation for this issue.

**kosedogus**

> Escalate for 10USDC I think this is not a valid medium. As the mintForToken function uses oracle prices, which return a weighted average price, it should not be that easy manipulated by Frontrunning.

Weighted average prices does not guarantee that trades (minting in this case)  executed based on the average price will be free from slippage. TWAP's are obviously vulnerable to slippage attacks. I also would like to remind that there is another valid issue due to the lack of slippage parameter in uniRouter. (That function also uses TWAP) 

**Shogoki**

Okay, I think you are right.
I removed the escalation

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | USSD - Autonomous Secure Dollar |
| Report Date | N/A |
| Finders | shealtielanz, cryptostellar5, Kose, Aymen0909, 0xRobocop, qbs, GimelSec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/97
- **Contest**: https://app.sherlock.xyz/audits/contests/82

### Keywords for Search

`Front-Running`

