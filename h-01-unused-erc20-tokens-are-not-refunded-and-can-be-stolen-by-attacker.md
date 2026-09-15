---
# Core Classification
protocol: Amun
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6521
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-amun-contest
source_link: https://code4rena.com/reports/2021-12-amun
github_link: https://github.com/code-423n4/2021-12-amun-findings/issues/201

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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - WatchPug
---

## Vulnerability Title

[H-01] Unused ERC20 tokens are not refunded, and can be stolen by attacker

### Overview


A bug has been identified in the WatchPug smart contract, which is causing users to lose funds under certain circumstances. The bug is related to the `annualizedFee` being minted to `feeBeneficiary` between the time a user sends a transaction and the transaction being packed into the block, leading to a decrease in the amount of underlying tokens for each basketToken. The current implementation only refunds the leftover inputToken and does not return any leftover underlying tokens to the user. Furthermore, the leftover tokens in the `SingleTokenJoinV2` contract can be stolen by calling `joinTokenSingle()` with fake `outputBasket` contract and `swap.exchange` contract.

To address this issue, it is recommended that either `IBasketFacet.calcTokensForAmount()` be called first to only swap for the desired amounts of tokens (like `SingleTokenJoin.sol`) or that leftover tokens be refunded.

### Original Finding Content


_Submitted by WatchPug_

Under certain circumstances, e.g. `annualizedFee` being minted to `feeBeneficiary` between the time user sent the transaction and the transaction being packed into the block and causing amounts of underlying tokens for each basketToken to decrease. It's possible or even most certainly that there will be some leftover basket underlying tokens, as `BasketFacet.sol#joinPool()` will only transfer required amounts of basket tokens from Join contracts.

However, in the current implementation, only the leftover inputToken is returned.

As a result, the leftover underlying tokens won't be returned to the user, which constitutes users' fund loss.

[`SingleTokenJoinV2.sol` L57-L78](https://github.com/code-423n4/2021-12-amun/blob/cf890dedf2e43ec787e8e5df65726316fda134a1/contracts/basket/contracts/singleJoinExit/SingleTokenJoinV2.sol#L57-L78)

```solidity
function joinTokenSingle(JoinTokenStructV2 calldata _joinTokenStruct)
    external
{
    // ######## INIT TOKEN #########
    IERC20 inputToken = IERC20(_joinTokenStruct.inputToken);

    inputToken.safeTransferFrom(
        msg.sender,
        address(this),
        _joinTokenStruct.inputAmount
    );

    _joinTokenSingle(_joinTokenStruct);

    // ######## SEND TOKEN #########
    uint256 remainingIntermediateBalance = inputToken.balanceOf(
        address(this)
    );
    if (remainingIntermediateBalance > 0) {
        inputToken.safeTransfer(msg.sender, remainingIntermediateBalance);
    }
}
```

[`BasketFacet.sol` L143-L168](https://github.com/code-423n4/2021-12-amun/blob/cf890dedf2e43ec787e8e5df65726316fda134a1/contracts/basket/contracts/facets/Basket/BasketFacet.sol#L143-L168)

```solidity
function joinPool(uint256 _amount, uint16 _referral)
    external
    override
    noReentry
{
    require(!this.getLock(), "POOL_LOCKED");
    chargeOutstandingAnnualizedFee();
    LibBasketStorage.BasketStorage storage bs =
        LibBasketStorage.basketStorage();
    uint256 totalSupply = LibERC20Storage.erc20Storage().totalSupply;
    require(
        totalSupply.add(_amount) <= this.getCap(),
        "MAX_POOL_CAP_REACHED"
    );

    uint256 feeAmount = _amount.mul(bs.entryFee).div(10**18);

    for (uint256 i; i < bs.tokens.length; i++) {
        IERC20 token = bs.tokens[i];
        uint256 tokenAmount =
            balance(address(token)).mul(_amount.add(feeAmount)).div(
                totalSupply
            );
        require(tokenAmount != 0, "AMOUNT_TOO_SMALL");
        token.safeTransferFrom(msg.sender, address(this), tokenAmount);
    }
    ...
```

Furthermore, the leftover tokens in the `SingleTokenJoinV2` contract can be stolen by calling `joinTokenSingle()` with fake `outputBasket` contract and `swap.exchange` contract.

##### Recommended Mitigation Steps

Consider:

1.  Calling `IBasketFacet.calcTokensForAmount()` first and only swap for exactly the desired amounts of tokens (like `SingleTokenJoin.sol`);
2.  Or, refund leftover tokens.

**[loki-sama (Amun) acknowledged](https://github.com/code-423n4/2021-12-amun-findings/issues/201)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Amun |
| Report Date | N/A |
| Finders | WatchPug |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-amun
- **GitHub**: https://github.com/code-423n4/2021-12-amun-findings/issues/201
- **Contest**: https://code4rena.com/contests/2021-12-amun-contest

### Keywords for Search

`vulnerability`

