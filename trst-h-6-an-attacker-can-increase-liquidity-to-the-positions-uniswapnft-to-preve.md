---
# Core Classification
protocol: Stella
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19050
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-29-Stella.md
github_link: none

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
  - business_logic

protocol_categories:
  - lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-H-6 An attacker can increase liquidity to the position's UniswapNFT to prevent the position from being closed

### Overview


This bug report describes an issue in UniswapV3NPM where an attacker can add liquidity to any NFT and prevent a position from being closed. This is possible because when closing a position, only the initial liquidity of the NFT is decreased, and then the NFT is burned. If the liquidity of the NFT is not 0, burning will fail.

The recommended mitigation for this issue was to consider decreasing the actual liquidity of the NFT in `_redeemPosition()` instead of the initial liquidity.

The team responded by fixing the issue, and the mitigation review determined that the team addressed the issue by decreasing the NFT's latest liquidity in `_redeemPosition()`.

### Original Finding Content

**Description:**
UniswapV3NPM allows the user to increase liquidity to any NFT.
```solidity
            function increaseLiquidity(IncreaseLiquidityParams calldata params)
                 external payable override checkDeadline(params.deadline)
                    returns (
                     uint128 liquidity, uint256 amount0, uint256 amount1)
            {
            Position storage position = _positions[params.tokenId];
                PoolAddress.PoolKey memory poolKey = _poolIdToPoolKey[position.poolId];
                    IUniswapV3Pool pool;
                        (liquidity, amount0, amount1, pool) = addLiquidity(
 ```
When closing a position, in `_redeemPosition()`, only the initial liquidity of the NFT will be 
decreased, and then the NFT will be burned.
```solidity
             function _redeemPosition(
                    address _user, uint _posId
                     ) internal override returns (address[] memory rewardTokens, uint[] memory rewardAmts) {
                        address _positionManager = positionManager;
                    uint128 collAmt = IUniswapV3PositionManager(_positionManager).getPositionCollAmt(_user, 
                    _posId);
                    // 1. take lp & extra coll tokens from lending proxy
                    _takeAllCollTokens(_positionManager, _user, _posId, address(this));
                         UniV3ExtraPosInfo memory extraPosInfo = IUniswapV3PositionManager(_positionManager)
                             .getDecodedExtraPosInfo(_user, _posId);
                        address _uniswapV3NPM = uniswapV3NPM; // gas saving
                    // 2. remove underlying tokens from lp (internal remove in NPM)
                    IUniswapV3NPM(_uniswapV3NPM).decreaseLiquidity(
                        IUniswapV3NPM.DecreaseLiquidityParams({
                            tokenId: extraPosInfo.uniV3PositionId,liquidity: collAmt, amount0Min: 0,
                    amount1Min: 0,
                         deadline: block.timestamp
                    })
                    );
                    ...
                    // 4. burn LP position
                          IUniswapV3NPM(_uniswapV3NPM).burn(extraPosInfo.uniV3PositionId);
                      }
```
 If the liquidity of the NFT is not 0, burning will fail.

```solidity
        function burn(uint256 tokenId) external payable override isAuthorizedForToken(tokenId) {
            Position storage position = _positions[tokenId];
                require(position.liquidity == 0 && position.tokensOwed0 == 0 && position.tokensOwed1 == 0,'Not cleared');
             delete _positions[tokenId];
        _burn(tokenId);
        }
```    
 This allows an attacker to add 1 wei liquidity to the position's NFT to prevent the position from 
being closed, and later when the position expires, the attacker can liquidate it.

**Recommended Mitigation:**
Consider decreasing the actual liquidity(using uniswapV3NPM.positions to get it) of the NFT 
in `_redeemPosition()`, instead of the initial liquidity

**Team response:**
Fixed.

**Mitigation Review:**
The team addressed this issue by decreasing NFT's latest liquidity in `_redeemPosition()`

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Stella |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-29-Stella.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Business Logic`

