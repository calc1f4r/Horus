---
# Core Classification
protocol: NFTX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42412
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-12-nftx
source_link: https://code4rena.com/reports/2021-12-nftx
github_link: https://github.com/code-423n4/2021-12-nftx-findings/issues/161

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
  - cross_chain
  - rwa
  - leveraged_farming
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-03] `NFTXMarketplaceZap.sol#buyAnd***()` should return unused weth/eth back to `msg.sender` instead of `to`

### Overview


The bug report is about a function called `buyAndSwap721WETH` in a contract called NFTXMarketplaceZap. The function is supposed to buy ERC721 tokens and send them to a specified address. However, there is a problem with the function where it does not accurately calculate the cost of the tokens being bought. This means that if a user sets a maximum amount of ETH to spend, the actual cost may be lower but the function will still spend the full maximum amount. This results in a loss of funds for the user. The severity of the bug has been rated as medium and the developers have acknowledged the issue but have not yet fixed it. 

### Original Finding Content

_Submitted by WatchPug_

<https://github.com/code-423n4/2021-12-nftx/blob/194073f750b7e2c9a886ece34b6382b4f1355f36/nftx-protocol-v2/contracts/solidity/NFTXMarketplaceZap.sol#L226-L249>

```solidity
function buyAndSwap721WETH(
  uint256 vaultId, 
  uint256[] memory idsIn, 
  uint256[] memory specificIds, 
  uint256 maxWethIn, 
  address[] calldata path,
  address to
) public nonReentrant {
  require(to != address(0));
  require(idsIn.length != 0);
  IERC20Upgradeable(address(WETH)).transferFrom(msg.sender, address(this), maxWethIn);
  INFTXVault vault = INFTXVault(nftxFactory.vault(vaultId));
  uint256 redeemFees = (vault.targetSwapFee() * specificIds.length) + (
      vault.randomSwapFee() * (idsIn.length - specificIds.length)
  );
  uint256[] memory amounts = _buyVaultToken(address(vault), redeemFees, maxWethIn, path);
  _swap721(vaultId, idsIn, specificIds, to);

  emit Swap(idsIn.length, amounts[0], to);

  // Return extras.
  uint256 remaining = WETH.balanceOf(address(this));
  WETH.transfer(to, remaining);
}
```

For example:

If Alice calls `buyAndSwap721WETH()` to buy some ERC721 and send to Bob, for slippage control, Alice put `1000 ETH` as `maxWethIn`, the actual cost should be lower.

Let's say the actual cost is `900 ETH`.

Expected Results: Alice spend only for the amount of the actual cost (`900 ETH`).

Actual Results: Alice spent `1000 ETH`.

**[0xKiwi (NFTX) acknowledged, but disagreed with medium severity and commented](https://github.com/code-423n4/2021-12-nftx-findings/issues/161#issuecomment-1003214046):**
 > I think the idea in this is that if a contract is buying for someone else, the zap handles the refund instead of the contract originating the purchase.
> But this is a valid concern, thank you

**[LSDan (judge) commented](https://github.com/code-423n4/2021-12-nftx-findings/issues/161#issuecomment-1064555316):**
 > This does result in a loss of funds if the user sends the wrong amount. I agree with the warden's severity rating.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | NFTX |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-nftx
- **GitHub**: https://github.com/code-423n4/2021-12-nftx-findings/issues/161
- **Contest**: https://code4rena.com/reports/2021-12-nftx

### Keywords for Search

`vulnerability`

