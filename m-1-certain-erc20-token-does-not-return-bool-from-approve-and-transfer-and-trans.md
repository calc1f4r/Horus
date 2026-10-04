---
# Core Classification
protocol: Footium
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18602
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/71
source_link: none
github_link: https://github.com/sherlock-audit/2023-04-footium-judging/issues/14

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
finders_count: 10
finders:
  - 0xGoodess
  - juancito
  - n1punp
  - innertia
  - Dug
---

## Vulnerability Title

M-1: Certain ERC20 token does not return bool from approve and transfer and transaction revert

### Overview


This bug report is about certain ERC20 tokens not returning a bool from approve and transfer and causing the transaction to revert. This was found manually by 0xGoodess, Dug, GalloDaSballo, TheNaubit, ctf\_sec, deadrxsezzz, innertia, juancito, mstpr-brainbot, n1punp. The issue is that some tokens do not return a bool on ERC20 methods and using the IERC20 token interface will cause the transaction to revert. This could have an impact on the transactions and the code snippets that are related to this issue can be found on the provided Github link. The recommendation is to use Openzeppelin SafeTransfer / SafeApprove for this issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-04-footium-judging/issues/14 

## Found by 
0xGoodess, Dug, GalloDaSballo, TheNaubit, ctf\_sec, deadrxsezzz, innertia, juancito, mstpr-brainbot, n1punp
## Summary

Certain ERC20 token does not return bool from approve and transfer and transaction revert

## Vulnerability Detail

According to

https://github.com/d-xo/weird-erc20#missing-return-values

Some tokens do not return a bool on ERC20 methods and use IERC20 token interface will revert transaction

Certain ERC20 token does not return bool from approve and transfer and transaction revert

```solidity
   function setApprovalForERC20(
        IERC20 erc20Contract,
        address to,
        uint256 amount
    ) external onlyClubOwner {
        erc20Contract.approve(to, amount);
    }
```

and

```solidity
function transferERC20(
	IERC20 erc20Contract,
	address to,
	uint256 amount
) external onlyClubOwner {
	erc20Contract.transfer(to, amount);
}
```

the transfer / approve can fail slienlty

## Impact

Some tokens do not return a bool on ERC20 methods and use IERC20 token interface will revert transaction

## Code Snippet

https://github.com/sherlock-audit/2023-04-footium/blob/11736f3f7f7efa88cb99ee98b04b85a46621347c/footium-eth-shareable/contracts/FootiumEscrow.sol#L80

https://github.com/sherlock-audit/2023-04-footium/blob/11736f3f7f7efa88cb99ee98b04b85a46621347c/footium-eth-shareable/contracts/FootiumEscrow.sol#L95

## Tool used

Manual Review

## Recommendation

Use Openzeppelin SafeTransfer / SafeApprove

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Footium |
| Report Date | N/A |
| Finders | 0xGoodess, juancito, n1punp, innertia, Dug, GalloDaSballo, deadrxsezzz, mstpr-brainbot, TheNaubit, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-04-footium-judging/issues/14
- **Contest**: https://app.sherlock.xyz/audits/contests/71

### Keywords for Search

`vulnerability`

