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
solodit_id: 64856
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-08-gte-perps-and-launchpad
source_link: https://code4rena.com/reports/2025-08-gte-perps-and-launchpad
github_link: https://code4rena.com/audits/2025-08-gte-perps-and-launchpad/submissions/F-6

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

# Audit Details
report_date: unknown
finders_count: 45
finders:
  - codegpt
  - Legend
  - 0xShitgem
  - lufP
  - 0xAsen
---

## Vulnerability Title

[H-08] CREATE2 address of the uniswap pair used by `LaunchPad` does not match address of pair deployed by `GTELaunchpadV2PairFactory`

### Overview


This bug report discusses an issue with the `Launchpad.sol` contract, specifically in lines 569-587. The problem arises when a user has already called the `GTELaunchpadV2PairFactory::createPair` function for a specific token pair, but then buys enough launch tokens to consume all tokens in the bonding curve. This causes a call to `createPair` to revert, as the pair already exists. However, the `pair` variable is not assigned to the newly created pair's address, resulting in a different address than what the factory uses. This can cause transactions to be reverted and the system to be permanently stuck in the bonding state. To fix this, the code needs to be refactored so that the `Launchpad::pairFor` function returns an address matching that used by the factory. This issue also affects the end of rewards program for a token, as it uses the same incorrectly calculated pair address. 

### Original Finding Content



`launchpad/Launchpad.sol` [# L569-L587](https://github.com/code-423n4/2025-08-gte-perps/blob/f43e1eedb65e7e0327cfaf4d7608a37d85d2fae7/contracts/launchpad/Launchpad.sol# L569-L587)

Consider a situation in which a user has already called `GTELaunchpadV2PairFactory::createPair` for a quoteToken/launchToken pair, prior to the bonding curve becoming inactive. Then a user buys enough launch tokens to consume all the tokens in the bonding curve, thus we reach Launchpad.sol lines 483-489:
```

        // Create or get the pair
        try uniV2Factory.createPair(token, data.quote) returns (address p) {
            pair = IUniswapV2Pair(p);
        } catch {
            // Do nothing, pair exists
            // @todo its more gas but lets check pair exists and create if it doesn't.
            // try catch in solidity is horrible and should be avoided
        }
```

The call to `createPair` will revert because on GTELaunchpadV2PairFactory.sol:33, the pair creation reverts if it already exists. Therefore the `pair` variable is not assigned to the address of the newly created pair, but left as its original value which is computed by the `Launchpad::pairFor` function. This function determines the address on line 571:
```

pair = IUniswapV2Pair(
            address(
                uint160(
                    uint256(
                        keccak256(
                            abi.encodePacked(
                                hex"ff",
                                factory,
                                keccak256(abi.encodePacked(token0, token1)),
                                uniV2InitCodeHash // init code hash
                            )
                        )
                    )
                )
            )
        );
```

The salt used only includes `token0` and `token1`, rather than `token0`, `token1`, `_launchpadLp` and `_launchpadFeeDistributor` as used by the factory, resulting in a different address than what the factory uses.

Impact: the user attempting to buy more tokens than there are remaining in the bonding curve will have their transaction reverted on LaunchPad.sol:491 as the `pair` address will not be a contract address. The system will be permanently stuck in the bonding state as it won’t be possible to deploy a contract at the `pair` address.

There is also a second impact of this issue as it also occurs when the rewards program ends for a token. This is evident on LaunchToken.sol:147 which is executed if the token is currently locked but all buyers have since sold their tokens back to the `Launchpad`. Consequently, `Launchpad::endRewards` is called but this uses the incorrectly calculated pair address on Launchpad.sol:436:
```

IGTELaunchpadV2Pair pair = IGTELaunchpadV2Pair(address(pairFor(address(uniV2Factory), msg.sender, quote)));

distributor.endRewards(pair);
```

This will cause the transaction to revert as there will be no contract at the `pair` address.

### Recommended mitigation steps

Re-factor the code so that the `Launchpad::pairFor` function returns an address matching that used by the factory.

[View detailed Proof of Concept](https://code4rena.com/audits/2025-08-gte-perps-and-launchpad/submissions/F-6)

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | GTE |
| Report Date | N/A |
| Finders | codegpt, Legend, 0xShitgem, lufP, 0xAsen, saikumar279, agadzhalov, hgrano, 0xPhantom, Ayomiposi233, deccs, udogodwin, nem0TheFinder, JuggerNaut63, taticuvostru, 0xsagetony, magiccentaur, roccomania, zzebra83, v2110, 0xterrah, 0xanony, FalseGenius, AvantGard, MadSisyphus, Wolf\_Kalp, anchabadze, boredpukar, c0pp3rscr3w3r, gizzy, AasifUsmani, bigbear1229, nuthan2x, BlackAnon, serial-coder, lonelybones, mahdifa, SolidityScan, dimulski, lodelux, IvanAlexandur, ZeroEx, niffylord, 0xsai, max10afternoon |

### Source Links

- **Source**: https://code4rena.com/reports/2025-08-gte-perps-and-launchpad
- **GitHub**: https://code4rena.com/audits/2025-08-gte-perps-and-launchpad/submissions/F-6
- **Contest**: https://code4rena.com/reports/2025-08-gte-perps-and-launchpad

### Keywords for Search

`vulnerability`

