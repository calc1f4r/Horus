---
# Core Classification
protocol: Hyperdrive February 2024
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35823
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-February-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-February-2024.pdf
github_link: none

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
finders_count: 4
finders:
  - Saw-Mon and Natalie
  - Christoph Michel
  - Deivitto
  - M4rio.eth
---

## Vulnerability Title

Large vault share price updates can be captured by open/close short

### Overview


This bug report discusses a medium risk bug in the HyperdriveShort.sol code. The bug occurs when a user opens a short and deposits c / c0 * dy - dz * c, and then closes the short in the same transaction and receives base proceeds of c' / c0 * dy - dz * c'. This can lead to a profit for the trader, causing a loss for the LPs. The bug can only occur in certain situations and there is currently no simple solution. The developers are aware of the issue and plan to document it and avoid using problematic yield sources in the future.

### Original Finding Content

## Severity: Medium Risk

## Context
- HyperdriveShort.sol#L597
- HyperdriveShort.sol#L447-L459

## Description
When opening a short, the user deposits \( \frac{c}{c_0} \times dy - dz \times c \). When closing in the same transaction, they receive base proceeds which are also \( \frac{c'}{c_0} \times dy - dz \times c' \), where \( dz \times c' \) represents the bond sell and buyback part of the short. This can lead to a profit when a vault share price transaction increases, as this is sandwiched. The trader makes a profit, and the loss must therefore come from the LPs in equal terms.

## Recommendation
As fees and gas fees eat into the profits, this only becomes a problem for vaults that don't linearly increase the vault share price, but instead rely on fewer, larger share price update events. There's currently no simple mitigation, as Hyperdrive's design always directly uses the underlying vault price instead of smoothing it out.

## Proof of Concept
```solidity
function test_sandwich_vault_share_price_update() external {
    uint256 apr = 0.1e18;
    // Deploy the pool and initialize the market
    {
        uint256 timeStretchApr = 0.02e18;
        deploy(alice, timeStretchApr, 0, 0, 0, 0);
    }
    uint256 contribution = 500e18;
    uint256 lpShares = initialize(alice, apr, contribution);
    contribution -= 2 * hyperdrive.getPoolConfig().minimumShareReserves;
    
    // sandwich vault price update
    // 1. open short
    uint256 shorts = 10e18;
    (uint256 maturityTime, uint256 baseDeposit) = openShort(celine, shorts);
    console2.log("opened shorts, paid ", baseDeposit);
    
    // 2. simulate vault share price increase
    int256 c1c0Growth = 0.01e18;
    MockHyperdrive(address(hyperdrive)).accrue(365 days, c1c0Growth);
    
    // 3. close short
    uint256 baseProceeds = closeShort(celine, maturityTime, shorts);
    console2.log("closed shorts, got ", baseProceeds);
    
    // 4. profit
    int256 profit = int256(baseProceeds) - int256(baseDeposit);
    console2.log("profit: %se16", profit / 1e16);
    assertGe(profit, 0);
}
```

## DELV
Acknowledged. This is reasonable, and we were aware of this problem. Our mitigation for this will be to clearly document this in the factory documentation and to avoid using yield sources that would be problematic.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Hyperdrive February 2024 |
| Report Date | N/A |
| Finders | Saw-Mon and Natalie, Christoph Michel, Deivitto, M4rio.eth |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-February-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-February-2024.pdf

### Keywords for Search

`vulnerability`

