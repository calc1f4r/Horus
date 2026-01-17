---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25248
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-canto
source_link: https://code4rena.com/reports/2022-06-canto
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
  - dexes
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[N-05] Events indexing

### Overview

See description below for full details.

### Original Finding Content


Events should use indexed fields

### PROOF OF CONCEPT

Instances include:

#### lending-market/Comptroller.sol

    l19 event MarketListed(CToken cToken)
    l22 event MarketEntered(CToken cToken, address account)
    l25 event MarketExited(CToken cToken, address account)
    l28 event NewCloseFactor(uint oldCloseFactorMantissa, uint newCloseFactorMantissa)
    l31 event NewCollateralFactor(CToken cToken, uint oldCollateralFactorMantissa, uint newCollateralFactorMantissa)
    l34 event NewLiquidationIncentive(uint oldLiquidationIncentiveMantissa, uint newLiquidationIncentiveMantissa)
    l37 event NewPriceOracle(PriceOracle oldPriceOracle, PriceOracle newPriceOracle)
    l40 event NewPauseGuardian(address oldPauseGuardian, address newPauseGuardian)
    l43 event ActionPaused(string action, bool pauseState)
    l46 event ActionPaused(CToken cToken, string action, bool pauseState)
    l49 event CompBorrowSpeedUpdated(CToken indexed cToken, uint newSpeed)
    l52 event CompSupplySpeedUpdated(CToken indexed cToken, uint newSpeed)
    l55 event ContributorCompSpeedUpdated(address indexed contributor, uint newSpeed)
    l58 event DistributedSupplierComp(CToken indexed cToken, address indexed supplier, uint compDelta, uint compSupplyIndex)
    l61 event DistributedBorrowerComp(CToken indexed cToken, address indexed borrower, uint compDelta, uint compBorrowIndex)
    l64 event NewBorrowCap(CToken indexed cToken, uint newBorrowCap)
    l67 event NewBorrowCapGuardian(address oldBorrowCapGuardian, address newBorrowCapGuardian)
    l70 event CompGranted(address recipient, uint amount)
    l73 event CompAccruedAdjusted(address indexed user, uint oldCompAccrued, uint newCompAccrued)
    l76 event CompReceivableUpdated(address indexed user, uint oldCompReceivable, uint newCompReceivable)

#### lending-market/AccountantInterfaces.sol

    l15 event AcctInit(address lendingMarketAddress)
    l16 event AcctSupplied(uint amount, uint err)
    l25 event NewImplementation(address oldImplementation, address newImplementation)

#### lending-market/TreasuryInterfaces.sol

    l17 event NewImplementation(address oldImplementation, address newImplementation)

#### lending-market/CNote.sol

    l10 event AccountantSet(address accountant, address accountantPrior)

#### lending-market/NoteInterest.sol

    l17 event NewInterestParams(uint baserateperblock)
    l61 event NewBaseRate(uint oldBaseRateMantissa, uint newBaseRateMantissa)
    l64 event NewAdjusterCoefficient(uint oldAdjusterCoefficient, uint newAdjusterCoefficient)
    l67 event NewUpdateFrequency(uint oldUpdateFrequency, uint newUpdateFrequency)

#### stableswap/BaseV1-core.sol

    l88 event Mint(address indexed sender, uint amount0, uint amount1);
    l89 event Burn(address indexed sender, uint amount0, uint amount1, address indexed to);
    l90 event Swap(
            address indexed sender,
            uint amount0In,
            uint amount1In,
            uint amount0Out,
            uint amount1Out,
            address indexed to
        );
    l98 event Sync(uint reserve0, uint reserve1);
    l99 event Claim(address indexed sender, address indexed recipient, uint amount0, uint amount1);
    l101 event Transfer(address indexed from, address indexed to, uint amount);
    l102 event Approval(address indexed owner, address indexed spender, uint amount)
    l486 event PairCreated(address indexed token0, address indexed token1, bool stable, address pair, uint)

### MITIGATION

Add indexed fields to these events so that they have the maximum number of indexed fields possible.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-canto
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-06-canto

### Keywords for Search

`vulnerability`

