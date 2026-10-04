---
# Core Classification
protocol: Berachain Honey
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52855
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Honey-Spearbit-Security-Review-October-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Honey-Spearbit-Security-Review-October-2024.pdf
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
finders_count: 3
finders:
  - Rvierdiiev
  - 0xLadboy
  - Noah Marconi
---

## Vulnerability Title

V2: Single bad collateral block HoneyFactory#mint in basket mode forever

### Overview


The report discusses a bug in the HoneyFactory contract where the minting function is blocked if there is a single bad collateral. This is because the code does not skip the bad collateral and continues to loop through each registered asset, causing the function to fail. A proof of concept is provided to show how the bug can be replicated. The recommendation is to skip the minting process if the asset is a bad collateral or if the amount is 0. The bug has been fixed in a new version of the contract.

### Original Finding Content

Severity: Medium Risk
Context: HoneyFactory#mint
Description: If there is a single bad collateral, the HoneyFactory#mint is blocked forever.
This is because as long as the asset depegs and the admin has to set the asset as bad collateral there is no way
to remove a collateral.
Further, when minting in basket mode, the for loop at HoneyFactory.sol#L272 always loops through each registered
asset.
for (uint256 i = 0; i < registeredAssets.length; i++) {
amount = refAmount * weights[i] / 1e18;
decimals = ERC20(registeredAssets[i]).decimals();
amount = Utils.changeDecimals(amount, 18, decimals);
honeyToMint += _mint(registeredAssets[i], amount, receiver, true);
}
Proof of Concept:
function test_mint_poc_one_bad_collateral_block_all_mint() external {
uint256 _daiToMint = 100e18;
uint256 mintedHoneys = (_daiToMint * daiMintRate) / 1e18;
dai.approve(address(factory), _daiToMint);
dai.approve(address(factory), _daiToMint);
mintedHoneys = factory.mint(address(dai), _daiToMint, receiver);
vm.prank(governance);
bytes32 MANAGER_ROLE = keccak256("MANAGER_ROLE");
factory.grantRole(MANAGER_ROLE, governance);
vm.prank(governance);
factory.setForcedBasketMode(true);
vm.prank(governance);
factory.setCollateralAssetStatus(address(usdt), true);
dai.approve(address(factory), _daiToMint);
mintedHoneys = factory.mint(address(dai), _daiToMint, receiver);
// uint256 _usdtToMint = 10e6;
// usdt.approve(address(factory), 10e6);
// mintedHoneys = factory.mint(address(usdt), _usdtToMint, receiver);
}
The proof of concept reverts with the following error:
Ran 1 test suite in 157.23ms (9.56ms CPU time): 0 tests passed, 1 failed, 0 skipped (1 total tests)
Failing tests:
Encountered 1 failing test in test/honey/HoneyFactory.t.sol:HoneyFactoryTest
[FAIL: AssetIsBadCollateral(0x2e234DAe75C793f67A35089C9d99245E1C58470b)]
Recommendation: Skip the mint inside the for loop if the registeredAssets[i] is bad collateral or if the amount is
0.
Berachain: Fixed in PR 481, because honey switches as emergency in basket mode.
Spearbit: In the current version, if basket mode is entered, the code not check if the asset is bad collateral, thus
not blocking mint in the basket mode.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Berachain Honey |
| Report Date | N/A |
| Finders | Rvierdiiev, 0xLadboy, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Honey-Spearbit-Security-Review-October-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Honey-Spearbit-Security-Review-October-2024.pdf

### Keywords for Search

`vulnerability`

