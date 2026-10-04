---
# Core Classification
protocol: GTE
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64864
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-08-gte-perps-and-launchpad
source_link: https://code4rena.com/reports/2025-08-gte-perps-and-launchpad
github_link: https://code4rena.com/audits/2025-08-gte-perps-and-launchpad/submissions/F-59

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
  - codegpt
  - romans
  - dimulski
  - Web3Vikings
  - Bale
---

## Vulnerability Title

[M-21] Bypass of recipient check allows pre-seeding the real pair and manipulating initial AMM price

### Overview


The Launchpad system has a bug where it is unable to prevent attackers from donating tokens to the AMM during bonding, which can manipulate the initial price and reserves. This is due to the `Launchpad.pairFor()` function using the wrong address when comparing the recipient, allowing the attacker to bypass the donation guard. The bug also affects other functions such as `endRewards()` and `skim()` by operating on the wrong address. To fix this, the `pairFor()` function should be updated to use the correct address and keep the `uniV2InitCodeHash` in sync with the actual pair bytecode in use.

### Original Finding Content



* `launchpad/Launchpad.sol` [# L800-L842](https://github.com/code-423n4/2025-08-gte-perps/blob/f43e1eedb65e7e0327cfaf4d7608a37d85d2fae7/contracts/launchpad/Launchpad.sol# L800-L842)
* `launchpad/uniswap/GTELaunchpadV2PairFactory.sol` [# L43-L82](https://github.com/code-423n4/2025-08-gte-perps/blob/f43e1eedb65e7e0327cfaf4d7608a37d85d2fae7/contracts/launchpad/uniswap/GTELaunchpadV2PairFactory.sol# L43-L82)

The Launchpad system bonds a new `LaunchToken` against a quote asset on a bonding curve. Upon graduation, the Launchpad adds initial liquidity to a Uniswap V2 pair and locks the LP to a vault so that subsequent trading can begin. To prevent attackers from donating tokens to the AMM during bonding (which would set the initial AMM price), Launchpad attempts to block buys that send base tokens directly to the AMM pair by checking the `recipient` against the computed pair address.

Core actors and responsibilities:

* `Launchpad.sol`: runs the bonding curve lifecycle (`buy()`, `sell()`), creates pairs on graduation, and guards against donations during bonding via `_assertValidRecipient()`. It also calls `endRewards()`.
* `GTELaunchpadV2PairFactory`: deploys `GTELaunchpadV2Pair` and embeds both `launchpadLp` (vault) and `launchpadFeeDistributor` into the CREATE2 salt and into pair initialization.
* `GTELaunchpadV2Pair`: the AMM pair that accrues protocol fees to the distributor, parameterized via the factory.
* `Distributor` and `LaunchpadLPVault`: receive accrued rewards and custody of initial LP respectively.

Root cause - [`Launchpad.pairFor()`](https://github.com/code-423n4/2025-08-gte-perps/blob/f43e1eedb65e7e0327cfaf4d7608a37d85d2fae7/contracts/launchpad/Launchpad.sol# L800-L842) computes a pair address using the standard Uniswap formula but only hashes `(token0, token1) + initCodeHash`:
```

pair = IUniswapV2Pair(
    address(
        uint160(
            uint256(
                keccak256(
                    abi.encodePacked(
                        hex"ff",
                        factory,
                        keccak256(abi.encodePacked(token0, token1)), // <-- here we are missing lp and distributor
                        uniV2InitCodeHash // init code hash
                    )
                )
            )
        )
    )
);
```

The custom [factory’s CREATE2 salt](https://github.com/code-423n4/2025-08-gte-perps/blob/f43e1eedb65e7e0327cfaf4d7608a37d85d2fae7/contracts/launchpad/uniswap/GTELaunchpadV2PairFactory.sol# L61-L71) additionally includes `launchpadLp` and `launchpadFeeDistributor`. The Launchpad’s computed address therefore diverges from the factory-deployed pair address:
```

bytes32 salt = keccak256(
    abi.encodePacked(
        token0,
        token1,
        _launchpadLp, // <-- here
        _launchpadFeeDistributor // <-- here
    )
);
assembly {
    pair := create2(0, add(bytecode, 32), mload(bytecode), salt)
}
```

The donation guard `_assertValidRecipient()` compares `recipient` to this wrong address, so passing the real pair as recipient will not trip the check and donations are allowed during bonding.
```

 function _assertValidRecipient(
    address recipient,
    address baseToken
) internal view returns (IUniswapV2Pair pair) {
    pair = pairFor(
        address(uniV2Factory),
        baseToken,
        _launches[baseToken].quote
    );

    if (address(pair) == recipient) revert InvalidRecipient();
}
```

> [!NOTE]
> The previous mitigation attempted to forbid donations by checking `recipient != pairFor(...)` during bonding. Because `pairFor()` is wrong for this custom factory, the check can be bypassed by supplying the real pair address as the `recipient`.

Detailed consequences:

* **Root cause** - [pairFor](https://github.com/code-423n4/2025-08-gte-perps/blob/f43e1eedb65e7e0327cfaf4d7608a37d85d2fae7/contracts/launchpad/Launchpad.sol# L800-L842) function - wrong address derivation:

  + In `pairFor()`, the salt is computed as:
    `keccak256(abi.encodePacked(token0, token1))`
  + The custom factory actually uses:
    `keccak256(abi.encodePacked(token0, token1, launchpadLp, launchpadFeeDistributor))`
  + Result: Launchpad’s locally computed address differs from the factory’s actual pair, making any downstream logic relying on `pairFor()` incorrect.
* **First vulnerable place** - recipient check bypass in [`_assertValidRecipient()`](https://github.com/code-423n4/2025-08-gte-perps/blob/f43e1eedb65e7e0327cfaf4d7608a37d85d2fae7/contracts/launchpad/Launchpad.sol# L782-L798):

  + The donation guard compares `recipient` to `pairFor(factory, baseToken, quote)`. Because `pairFor()` is wrong, an attacker can pass the real pair as `recipient`, and the equality check will be false, allowing base tokens to be sent to the real pair during bonding.
  + This enables pre-seeding reserves before graduation, setting initial AMM price arbitrarily and breaking the assumption that Launchpad controls the initial price by calling `addLiquidity()` after bonding.
  + [`buy()`](https://github.com/code-423n4/2025-08-gte-perps/blob/f43e1eedb65e7e0327cfaf4d7608a37d85d2fae7/contracts/launchpad/Launchpad.sol# L319-L377) invokes `_assertValidRecipient()` to prevent donations. Due to the first vulnerable place, `buy()` succeeds with `recipient=realPair`, transferring purchased `LaunchToken` straight into the AMM pair during bonding.
  + With sufficient preparation, the attacker can then add quote tokens and mint LP to lock in manipulated reserves/price before launchpad’s graduation adds its intended liquidity.
  + **Or with other words, the fix of the critical vulnerability from the previous [audit](https://github.com/Zellic/publications/blob/master/GTE%20Launchpad-%20Zellic%20Audit%20Report.pdf), is not well implemented**
* **Second vulnerable place** - rewards finalization misdirection in `endRewards()`:

  + [`endRewards()`](https://github.com/code-423n4/2025-08-gte-perps/blob/f43e1eedb65e7e0327cfaf4d7608a37d85d2fae7/contracts/launchpad/Launchpad.sol# L617-L624) uses the same miscomputed address to target the pair when calling into the distributor/pair to end accrual. Post-graduation, this can result in a silent DoS (targeting an EOA/no-code) or acting on an unrelated pair if an address collision exists, leaving the real market’s rewards active or incorrectly affected.

    
```

    function endRewards() external onlyLaunchAsset {
    address quote = _launches[msg.sender].quote;
    IGTELaunchpadV2Pair pair = IGTELaunchpadV2Pair(
    address(pairFor(address(uniV2Factory), msg.sender, quote))
    );
    
```

  distributor.endRewards(pair);
  }
* **Third vulnerable place** - post-graduation skim path and ops on wrong address:

  + In [`_createPairAndSwapRemaining()`](https://github.com/code-423n4/2025-08-gte-perps/blob/f43e1eedb65e7e0327cfaf4d7608a37d85d2fae7/contracts/launchpad/Launchpad.sol# L658-L729), Launchpad may call `pair.skim(owner())`. If the pair already exists and Launchpad’s `pairFor()` is wrong, it will operate on the wrong address.

    
```

    IUniswapV2Pair pair = _assertValidRecipient(
    buyData.recipient,
    buyData.token
    );
    ...
    ...
    function _graduate(
    BuyData calldata buyData,
    IUniswapV2Pair pair,
    LaunchData memory data,
    uint256 amountOutBaseActual,
    uint256 amountInQuote
    )
    internal
    returns (uint256 finalAmountOutBaseActual, uint256 finalAmountInQuote)
    {
    LaunchToken(buyData.token).unlock();
    _launches[buyData.token].active = false;
    emit BondingLocked(buyData.token, pair, LaunchpadEventNonce.inc());
    
```

  uint256 additionalQuote = \_createPairAndSwapRemaining({
  token: buyData.token,
  pair: pair,
  …
  …

function \_createPairAndSwapRemaining(
address token,
IUniswapV2Pair pair,
LaunchData memory data,
uint256 remainingBase,
uint256 remainingQuote,
address recipient
) internal returns (uint256 additionalQuoteUsed) {
…
…
pair.skim(owner());
```

Highest-impact scenario (replicates the old report’s flow with current code):
- During bonding, a user buys base and sets the `recipient` to the real Uniswap V2 pair address. Since `_assertValidRecipient()` compares against the wrong address, the buy succeeds and base tokens are transferred into the AMM pair.
- The attacker adds quote liquidity and mints LP to fix the reserves ratio and effectively set the initial AMM price.
- When bonding completes and Launchpad calls `addLiquidity()`, it will no longer be able to inject its intended liquidity ratio; instead, Uniswap’s `_addLiquidity()` uses current reserves to compute optimal amounts, preserving the attacker’s chosen price. The attacker can then immediately sell launch tokens at favorable prices to extract excess quote tokens.

### Recommended mitigation steps

Update `pairFor()` to replicate the factory salt and avoid mismatch:
  - Build salt as `keccak256(abi.encodePacked(token0, token1, address(launchpadLPVault), address(distributor)))`.
  - Keep `uniV2InitCodeHash` in sync with the actual pair bytecode in use. Prefer immutable configuration or rotate router/factory alongside the hash.
  - Still prefer `getPair()` for safety and simplicity.

[View detailed Proof of Concept](https://code4rena.com/audits/2025-08-gte-perps-and-launchpad/submissions/F-59)

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | GTE |
| Report Date | N/A |
| Finders | codegpt, romans, dimulski, Web3Vikings, Bale, nem0TheFinder, nuthan2x, 0xsagetony, roccomania, 0xMilenov |

### Source Links

- **Source**: https://code4rena.com/reports/2025-08-gte-perps-and-launchpad
- **GitHub**: https://code4rena.com/audits/2025-08-gte-perps-and-launchpad/submissions/F-59
- **Contest**: https://code4rena.com/reports/2025-08-gte-perps-and-launchpad

### Keywords for Search

`vulnerability`

