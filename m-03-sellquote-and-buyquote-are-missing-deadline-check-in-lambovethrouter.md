---
# Core Classification
protocol: Lambo.win
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49614
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-12-lambowin
source_link: https://code4rena.com/reports/2024-12-lambowin
github_link: https://code4rena.com/audits/2024-12-lambowin/submissions/F-16

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
  - pumba
  - KupiaSec
  - Bryan\_Conquer
  - 0xDemon
  - SpicyMeatball
---

## Vulnerability Title

[M-03] `sellQuote` and `buyQuote` are missing deadline check in `LamboVEthRouter`

### Overview


The LamboVEthRouter contract is missing a deadline check in the `sellQuote` and `buyQuote` functions. This means that transactions can be stuck in the mempool for a long time and executed at a different price than intended, making them vulnerable to sandwich attacks. The UniswapV2Pair::swap function used in the contract requires important safety checks to be performed, but the `sellQuote` and `buyQuote` functions do not have these checks. To fix this issue, a deadline parameter should be added to these functions. The team at Lambo.win has acknowledged this issue.

### Original Finding Content



<https://github.com/code-423n4/2024-12-lambowin/blob/main/src/LamboVEthRouter.sol# L102-L102>

<https://github.com/code-423n4/2024-12-lambowin/blob/main/src/LamboVEthRouter.sol# L148-L148>

`sellQuote` and `buyQuote` are missing deadline check in `LamboVEthRouter`.

Because of that, transactions can still be stuck in the mempool and be executed a long time after the transaction is initially called. During this time, the price in the Uniswap pool can change. In this case, the slippage parameters can become outdated and the swap will become vulnerable to sandwich attacks.

### Vulnerability details

The protocol has made the choice to develop its own router to swap tokens for users, which imply calling the low level [UniswapV2Pair::swap](https://github.com/Uniswap/v2-core/blob/ee547b17853e71ed4e0101ccfd52e70d5acded58/contracts/UniswapV2Pair.sol# L158) function:
```

// this low-level function should be called from a contract which performs important safety checks
function swap(uint amount0Out, uint amount1Out, address to, bytes calldata data) external lock {
	require(amount0Out > 0 || amount1Out > 0, 'UniswapV2: INSUFFICIENT_OUTPUT_AMOUNT');
	(uint112 _reserve0, uint112 _reserve1,) = getReserves(); // gas savings
	require(amount0Out < _reserve0 && amount1Out < _reserve1, 'UniswapV2: INSUFFICIENT_LIQUIDITY');
```

As the comment indicates, this function require important safety checks to be performed.

A good example of safe implementation of such call can be found in the [UniswapV2Router02::swapExactTokensForTokens](https://github.com/Uniswap/v2-periphery/blob/0335e8f7e1bd1e8d8329fd300aea2ef2f36dd19f/contracts/UniswapV2Router02.sol# L224) function:
```

function swapExactTokensForTokens(
	uint amountIn,
	uint amountOutMin,
	address[] calldata path,
	address to,
	uint deadline
) external virtual override ensure(deadline) returns (uint[] memory amounts) {
	amounts = UniswapV2Library.getAmountsOut(factory, amountIn, path);
	require(amounts[amounts.length - 1] >= amountOutMin, 'UniswapV2Router: INSUFFICIENT_OUTPUT_AMOUNT');
	TransferHelper.safeTransferFrom(
		path[0], msg.sender, UniswapV2Library.pairFor(factory, path[0], path[1]), amounts[0]
	);
	_swap(amounts, path, to);
}
```

As we can see, 2 safety parameters are present here: `amountOutMin` and `deadline`.

Now, if we look at `SellQuote` (`buyQuote` having the same issue):
```

File: src/LamboVEthRouter.sol
148:     function _buyQuote(address quoteToken, uint256 amountXIn, uint256 minReturn) internal returns (uint256 amountYOut) {
149:         require(msg.value >= amountXIn, "Insufficient msg.value");
150:
...:
...:       //* ---------- some code ---------- *//
...:
168:         require(amountYOut >= minReturn, "Insufficient output amount");
```

We can see that no `deadline` parameter is present.

### Impact

The transaction can still be stuck in the mempool and be executed a long time after the transaction is initially called. During this time, the price in the Uniswap pool can change. In this case, the slippage parameters can become outdated and the swap will become vulnerable to sandwich attacks.

### Recommended Mitigation Steps

Add a deadline parameter.

**Shaneson (Lambo.win) acknowledged**

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Lambo.win |
| Report Date | N/A |
| Finders | pumba, KupiaSec, Bryan\_Conquer, 0xDemon, SpicyMeatball, Infect3d, NexusAudits, Evo, hyuunn, OpaBatyo |

### Source Links

- **Source**: https://code4rena.com/reports/2024-12-lambowin
- **GitHub**: https://code4rena.com/audits/2024-12-lambowin/submissions/F-16
- **Contest**: https://code4rena.com/reports/2024-12-lambowin

### Keywords for Search

`vulnerability`

