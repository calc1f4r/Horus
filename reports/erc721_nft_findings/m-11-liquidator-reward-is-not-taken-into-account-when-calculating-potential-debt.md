---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25827
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-astaria
source_link: https://code4rena.com/reports/2023-01-astaria
github_link: https://github.com/code-423n4/2023-01-astaria-findings/issues/400

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
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - evan
  - ladboy233
---

## Vulnerability Title

[M-11] Liquidator reward is not taken into account when calculating potential debt

### Overview


Bug Report Summary:

This bug report concerns the Astaria protocol, where liquidator reward is not taken into account when calculating potential debt. When liquidationInitialAsk is set to the bare minimum, liquidator reward will always come at the expense of vaults late on in the stack. The bug was tested using a Solidity contract, where a vault loses more than 3 tokens and the liquidator reward was not taken into account. 

The bug was disputed by androolloyd (Astaria), who commented that this was working as intended. Picodes (judge) then commented that it would be safer and avoid eventual loss of funds to ensure that the eventual liquidator reward is included in liquidationInitialAsk.

### Original Finding Content


Liquidator reward is not taken into account when calculating potential debt. When liquidationInitialAsk is set to the bare minimum, liquidator reward will always come at the expense of vaults late on in the stack.

### Proof of Concept

Consider the following test where the vault loses more than 3 tokens.

    pragma solidity =0.8.17;

    import "forge-std/Test.sol";

    import {Authority} from "solmate/auth/Auth.sol";
    import {FixedPointMathLib} from "solmate/utils/FixedPointMathLib.sol";
    import {MockERC721} from "solmate/test/utils/mocks/MockERC721.sol";
    import {
      MultiRolesAuthority
    } from "solmate/auth/authorities/MultiRolesAuthority.sol";

    import {ERC721} from "gpl/ERC721.sol";
    import {SafeCastLib} from "gpl/utils/SafeCastLib.sol";

    import {IAstariaRouter, AstariaRouter} from "../AstariaRouter.sol";
    import {VaultImplementation} from "../VaultImplementation.sol";
    import {PublicVault} from "../PublicVault.sol";
    import {TransferProxy} from "../TransferProxy.sol";
    import {WithdrawProxy} from "../WithdrawProxy.sol";
    import {Vault} from "../Vault.sol";

    import {Strings2} from "./utils/Strings2.sol";

    import "./TestHelpers.t.sol";
    import {OrderParameters} from "seaport/lib/ConsiderationStructs.sol";

    contract AstariaTest is TestHelpers {
      using FixedPointMathLib for uint256;
      using CollateralLookup for address;
      using SafeCastLib for uint256;

      event NonceUpdated(uint256 nonce);
      event VaultShutdown();

      function testProfitFromLiquidatorFee() public {

        TestNFT nft = new TestNFT(1);
        address tokenContract = address(nft);
        uint256 tokenId = uint256(0);

        address publicVault = _createPublicVault({
          strategist: strategistOne,
          delegate: strategistTwo,
          epochLength: 7 days
        });
        _lendToVault(
          Lender({addr: address(1), amountToLend: 60 ether}),
          publicVault
        );

        (, ILienToken.Stack[] memory stack) = _commitToLien({
          vault: publicVault,
          strategist: strategistOne,
          strategistPK: strategistOnePK,
          tokenContract: tokenContract,
          tokenId: tokenId,
          lienDetails: ILienToken.Details({
            maxAmount: 50 ether,
            rate: (uint256(1e16) * 150) / (365 days),
            duration: 10 days,
            maxPotentialDebt: 0 ether,
            liquidationInitialAsk: 42 ether
          }),
          amount: 40 ether,
          isFirstLien: true
        });

        vm.warp(block.timestamp + 10 days);
        OrderParameters memory listedOrder = ASTARIA_ROUTER.liquidate(
          stack,
          uint8(0)
        );

        _bid(Bidder(bidder, bidderPK), listedOrder, 42 ether);
        assertTrue(WETH9.balanceOf(publicVault) < 57 ether);
      }
    }

### Tools Used

VSCode, Foundry

### Recommended Mitigation Steps

Include liquidator reward in the calculation of potential debt.

**[androolloyd (Astaria) disputed and commented](https://github.com/code-423n4/2023-01-astaria-findings/issues/400#issuecomment-1416270111):**
 > This is working as intended.

**[Picodes (judge) commented](https://github.com/code-423n4/2023-01-astaria-findings/issues/400#issuecomment-1441302402):**
 > @androolloyd could you expand on this? Wouldn't it be safer and avoid eventual loss of funds to ensure that the eventual liquidator reward is included in `liquidationInitialAsk`?



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | evan, ladboy233 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-astaria
- **GitHub**: https://github.com/code-423n4/2023-01-astaria-findings/issues/400
- **Contest**: https://code4rena.com/reports/2023-01-astaria

### Keywords for Search

`vulnerability`

