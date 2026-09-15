---
# Core Classification
protocol: DittoETH
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34212
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-03-dittoeth
source_link: https://code4rena.com/reports/2024-03-dittoeth
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[26] Invalid NatSpec comment style

### Overview

See description below for full details.

### Original Finding Content


<details>

NatSpec comment in solidity should use `///` or `/* ... */` syntax.

There are 111 instances:

BidOrdersFacet.sol ([70-70](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/BidOrdersFacet.sol#L70-L70), [72-73](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/BidOrdersFacet.sol#L72-L73), [102-102](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/BidOrdersFacet.sol#L102-L102), [107-107](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/BidOrdersFacet.sol#L107-L107), [113-113](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/BidOrdersFacet.sol#L113-L113), [140-140](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/BidOrdersFacet.sol#L140-L140), [291-291](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/BidOrdersFacet.sol#L291-L291), [308-309](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/BidOrdersFacet.sol#L308-L309), [333-334](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/BidOrdersFacet.sol#L333-L334), [338-339](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/BidOrdersFacet.sol#L338-L339), [344-344](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/BidOrdersFacet.sol#L344-L344), [353-353](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/BidOrdersFacet.sol#L353-L353), [393-393](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/BidOrdersFacet.sol#L393-L393), [401-401](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/BidOrdersFacet.sol#L401-L401)):

```solidity
70:         // @dev leave empty, don't need hint for market buys

72: 
73:         // @dev update oracle in callers

102:         // @dev setting initial shortId to match "backwards" (See _shortDirectionHandler() below)

107:             // @dev if match and match price is gt .5% to saved oracle in either direction, update startingShortId

113:             // @dev no match, add to market if limit order

140:             // @dev Handles scenario when no sells left after partial fill

291:         // @dev needs to happen after updateSellOrdersOnMatch()

308: 
309:             // @dev Approximates the startingShortId after bid is fully executed

333: 
334:         // @dev match price is based on the order that was already on orderbook

338: 
339:     // @dev If neither conditions are true, it returns an empty Order struct

344:             // @dev Setting lowestSell after comparing short and ask prices

353:             // @dev Handles scenario when there are no shorts

393:             // @dev shortHintId should always be the first thing matched

401:             // @dev Only set to true if actually moving forward
```

BridgeRouterFacet.sol ([67-67](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/BridgeRouterFacet.sol#L67-L67), [147-147](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/BridgeRouterFacet.sol#L147-L147), [178-178](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/BridgeRouterFacet.sol#L178-L178)):

```solidity
67:         // @dev amount after deposit might be less, if bridge takes a fee

147:     // @dev Deters attempts to take advantage of long delays between updates to the yield rate, by creating large temporary positions

178:             // @dev don't use mulU88 in rare case of overflow
```

ExitShortFacet.sol ([156-157](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/ExitShortFacet.sol#L156-L157), [167-168](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/ExitShortFacet.sol#L167-L168), [202-203](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/ExitShortFacet.sol#L202-L203), [205-206](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/ExitShortFacet.sol#L205-L206)):

```solidity
156: 
157:         // @dev Must prevent forcedBid from exitShort() matching with original shortOrder

167: 
168:         // @dev if short order was cancelled, fully exit

202: 
203:             // @dev Only allow partial exit if the CR is same or better than before

205: 
206:             // @dev collateral already subtracted in exitShort()
```

PrimaryLiquidationFacet.sol ([55-55](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/PrimaryLiquidationFacet.sol#L55-L55), [57-58](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/PrimaryLiquidationFacet.sol#L57-L58), [66-67](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/PrimaryLiquidationFacet.sol#L66-L67), [71-72](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/PrimaryLiquidationFacet.sol#L71-L72), [95-95](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/PrimaryLiquidationFacet.sol#L95-L95), [157-158](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/PrimaryLiquidationFacet.sol#L157-L158), [163-164](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/PrimaryLiquidationFacet.sol#L163-L164), [177-177](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/PrimaryLiquidationFacet.sol#L177-L177), [185-186](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/PrimaryLiquidationFacet.sol#L185-L186), [191-192](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/PrimaryLiquidationFacet.sol#L191-L192), [197-197](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/PrimaryLiquidationFacet.sol#L197-L197), [198-198](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/PrimaryLiquidationFacet.sol#L198-L198), [217-217](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/PrimaryLiquidationFacet.sol#L217-L217)):

```solidity
55:         // @dev TAPP partially reimburses gas fees, capped at 10 to limit arbitrary high cost

57: 
58:         // @dev Ensures SR has enough ercDebt/collateral to make caller fee worthwhile

66: 
67:         // @dev liquidate requires more up-to-date oraclePrice

71: 
72:         // @dev Can liquidate as long as CR is low enough

95:     // @dev startingShortId is updated via updateOracleAndStartingShortViaTimeBidOnly() prior to call

157: 
158:         // @dev Provide higher price to better ensure it can fully fill the liquidation

163: 
164:         // @dev Increase ethEscrowed by shorter's full collateral for forced bid

177:             // @dev Max ethDebt can only be the ethEscrowed in the TAPP

185: 
186:         // @dev Liquidation contract will be the caller. Virtual accounting done later for shorter or TAPP

191: 
192:         // @dev virtually burning the repurchased debt

197:         // @dev manually setting basefee to 1,000,000 in foundry.toml;

198:         // @dev By basing gasFee off of baseFee instead of priority, adversaries are prevent from draining the TAPP

217:         // @dev TAPP already received the gasFee for being the forcedBid caller. tappFee nets out.
```

RedemptionFacet.sol ([36-36](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L36-L36), [37-37](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L37-L37), [71-72](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L71-L72), [82-82](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L82-L82), [91-92](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L91-L92), [94-95](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L94-L95), [100-100](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L100-L100), [107-108](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L107-L108), [109-109](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L109-L109), [126-127](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L126-L127), [144-145](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L144-L145), [156-156](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L156-L156), [157-157](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L157-L157), [261-261](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L261-L261), [262-262](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L262-L262), [277-278](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L277-L278), [282-282](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L282-L282), [286-287](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L286-L287), [288-288](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L288-L288), [294-295](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L294-L295), [355-356](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L355-L356), [372-372](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L372-L372), [375-375](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L375-L375), [380-381](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L380-L381), [391-391](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L391-L391), [393-393](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/RedemptionFacet.sol#L393-L393)):

```solidity
36:         // @dev Matches check in onlyValidShortRecord but with a more restrictive ercDebt condition

37:         // @dev Proposer can't redeem on self

71: 
72:         // @dev redeemerAssetUser.SSTORE2Pointer gets reset to address(0) after actual redemption

82:             // @dev Setting this above _onlyValidShortRecord to allow skipping

91: 
92:             // @dev Skip if proposal is not sorted correctly or if above redemption threshold

94: 
95:             // @dev totalAmountProposed tracks the actual amount that can be redeemed. totalAmountProposed <= redemptionAmount

100:                 // @dev Exit when proposal would leave less than minShortErc, proxy for nearing end of slate

107: 
108:             // @dev Cancel attached shortOrder if below minShortErc, regardless of ercDebt in SR

109:             // @dev All verified SR have ercDebt >= minShortErc so CR does not change in cancelShort()

126: 
127:             // @dev directly write the properties of MTypes.ProposalData into bytes

144: 
145:         // @dev SSTORE2 the entire proposalData after validating proposalInput

156:         // @dev Calculate the dispute period

157:         // @dev timeToDispute is immediate for shorts with CR <= 1.1x

261:             // @dev All proposals from the incorrectIndex onward will be removed

262:             // @dev Thus the proposer can only redeem a portion of their original slate

277: 
278:             // @dev Update the redeemer's SSTORE2Pointer

282:                 // @dev this implies everything in the redeemer's proposal was incorrect

286: 
287:             // @dev Penalty is based on the proposal with highest CR (decodedProposalData is sorted)

288:             // @dev PenaltyPct is bound between CallerFeePct and 33% to prevent exploiting primaryLiquidation fees

294: 
295:             // @dev Give redeemer back ercEscrowed that is no longer used to redeem (penalty applied)

355: 
356:         // @dev Only need to read up to the position of the SR to be claimed

372:             // @dev Refund shorter the remaining collateral only if fully redeemed and not claimed already

375:             // @dev Shorter shouldn't lose any unclaimed yield because dispute time > YIELD_DELAY_SECONDS

380: 
381:     // @dev inspired by https://docs.liquity.org/faq/lusd-redemptions#how-is-the-redemption-fee-calculated

391:         // @dev Calculate Asset.ercDebt prior to proposal

393:         // @dev Derived via this formula: baseRateNew = baseRateOld + redeemedLUSD / (2 * totalLUSD)
```

ShortOrdersFacet.sol ([46-47](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/ShortOrdersFacet.sol#L46-L47), [54-55](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/ShortOrdersFacet.sol#L54-L55), [74-74](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/ShortOrdersFacet.sol#L74-L74), [83-84](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/facets/ShortOrdersFacet.sol#L83-L84)):

```solidity
46: 
47:         // @dev create "empty" SR. Fail early.

54: 
55:         // @dev minShortErc needs to be modified (bigger) when cr < 1

74:         // @dev if match and match price is gt .5% to saved oracle in either direction, update startingShortId

83: 
84:         // @dev reading spot oracle price
```

LibBridgeRouter.sol ([74-74](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibBridgeRouter.sol#L74-L74), [104-104](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibBridgeRouter.sol#L104-L104), [112-112](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibBridgeRouter.sol#L112-L112), [142-143](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibBridgeRouter.sol#L142-L143)):

```solidity
74:                     // @dev Prevents abusing bridge for arbitrage

104:                     // @dev Prevents abusing bridge for arbitrage

112:     // @dev Only applicable to VAULT.ONE which has mixed LST

142: 
143:     // @dev Only relevant to NFT SR that is being transferred, used to deter workarounds to the bridge credit system
```

LibOracle.sol ([29-29](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOracle.sol#L29-L29), [81-82](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOracle.sol#L81-L82), [154-155](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOracle.sol#L154-L155), [160-161](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOracle.sol#L160-L161), [166-167](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOracle.sol#L166-L167)):

```solidity
29:                 // @dev multiply base oracle by 10**10 to give it 18 decimals of precision

81: 
82:         // @dev if there is issue with chainlink, get twap price. Verify twap and compare with chainlink

154: 
155:     // @dev Intentionally using creationTime for oracleTime.

160: 
161:     // @dev Intentionally using ercAmount for oraclePrice. Storing as price may lead to bugs in the match algos.

166: 
167:     // @dev Allows caller to save gas since reading spot price costs ~16K
```

LibOrders.sol ([28-29](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L28-L29), [42-43](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L42-L43), [137-138](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L137-L138), [171-172](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L171-L172), [188-188](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L188-L188), [237-237](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L237-L237), [267-267](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L267-L267), [294-294](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L294-L294), [331-332](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L331-L332), [418-419](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L418-L419), [507-507](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L507-L507), [508-508](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L508-L508), [511-511](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L511-L511), [518-518](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L518-L518), [640-641](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L640-L641), [723-724](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L723-L724), [760-760](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L760-L760), [769-769](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L769-L769), [781-782](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L781-L782), [790-790](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L790-L790), [801-802](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L801-L802), [846-846](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L846-L846), [899-899](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L899-L899), [900-900](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L900-L900), [905-905](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L905-L905), [906-906](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L906-L906), [927-928](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L927-L928), [931-931](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L931-L931), [961-962](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L961-L962), [964-964](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L964-L964), [966-967](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L966-L967), [970-970](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L970-L970), [974-974](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L974-L974), [980-981](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibOrders.sol#L980-L981)):

```solidity
28: 
29:     // @dev in seconds

42: 
43:         // @dev use the diff to get more time (2159), to prevent overflow at year 2106

137: 
138:         // @dev: Only need to set this when placing incomingShort onto market

171: 
172:     // @dev partial addOrder

188:         // @dev (ID) is exiting, [ID] is inserted

237:         // @dev: TAIL can't be prevId because it will always be last item in list

267:         // @dev: TAIL can't be prevId because it will always be last item in list

294:         // @dev (ID) is exiting, [ID] is inserted

331: 
332:         // @dev mark as cancelled instead of deleting the order itself

418: 
419:     // @dev not used to change state, just which methods to call

507:                 // @dev Handles only matching one thing

508:                 // @dev If does not get fully matched, b.matchedShortId == 0 and therefore not hit this block

511:                 // @dev Handles moving forward only

518:                 // @dev Handle going backward and forward

640: 
641:         // @dev match price is based on the order that was already on orderbook

723: 
724:         // @dev this happens at the end so fillErc isn't affected in previous calculations

760:                 // @dev force hint to be within 0.5% of oraclePrice

769:                     // @dev prevShortPrice >= oraclePrice

781: 
782:     // @dev Update on match if order matches and price diff between order price and oracle > chainlink threshold (i.e. eth .5%)

790:         // @dev handle .5% deviations in either directions

801: 
802:     // @dev Possible for this function to never get called if updateOracleAndStartingShortViaThreshold() gets called often enough

846:             // @dev If hint was prev matched, assume that hint was close to HEAD and therefore is reasonable to use HEAD

899:             // @dev creating shortOrder automatically creates a closed shortRecord which also sets a shortRecordId

900:             // @dev cancelling an unmatched order needs to also handle/recycle the shortRecordId

905:                 // @dev prevents leaving behind a partially filled SR is under minShortErc

906:                 // @dev if the corresponding short is cancelled, then the partially filled SR's debt will == minShortErc

927: 
928:                     // @dev update the eth refund amount

931:                 // @dev virtually mint the increased debt

961: 
962:         // @dev tithe is increased only if discount is greater than 1%

964:             // @dev bound the new tithe amount between 25% and 100%

966: 
967:             // @dev Vault.dethTitheMod is added onto Vault.dethTithePercent to get tithe amount

970:             // @dev dethTitheMod is only set when setTithe is called.

974:                 // @dev change back to original tithe percent

980: 
981:         // @dev exists because of ShortOrderFacet contract size
```

LibSRUtil.sol ([89-89](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibSRUtil.sol#L89-L89), [132-133](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/LibSRUtil.sol#L132-L133)):

```solidity
89:                     // @dev The resulting SR will not have PartialFill status after cancel

132: 
133:         // @dev shortOrderId is already validated in mintNFT
```

UniswapOracleLibrary.sol ([57-58](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/UniswapOracleLibrary.sol#L57-L58), [68-69](https://github.com/code-423n4/2024-03-dittoeth/blob/91faf46078bb6fe8ce9f55bcb717e5d2d302d22e/contracts/libraries/UniswapOracleLibrary.sol#L68-L69)):

```solidity
57: 
58:         // @dev Returns the cumulative tick and liquidity as of each timestamp secondsAgo from the current block timestamp

68: 
69:         // @dev Gets price using this formula: p(i) = 1.0001**i, where i is the tick
```

</details>



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | DittoETH |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-03-dittoeth
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-03-dittoeth

### Keywords for Search

`vulnerability`

