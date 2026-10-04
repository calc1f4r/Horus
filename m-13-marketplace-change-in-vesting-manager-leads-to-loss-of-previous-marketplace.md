---
# Core Classification
protocol: SecondSwap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49549
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-12-secondswap
source_link: https://code4rena.com/reports/2024-12-secondswap
github_link: https://code4rena.com/audits/2024-12-secondswap/submissions/F-36

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
finders_count: 6
finders:
  - EPSec
  - BenRai
  - 0xLasadie
  - franfran20
---

## Vulnerability Title

[M-13] MarketPlace Change In Vesting Manager, Leads To Loss Of Previous MarketPlace Listing

### Overview


This bug report discusses an issue with the `VestingManager` contract in the `SecondSwap` project. When a new `MarketPlace` contract is set, all previous listings in the marketplace become stuck and inaccessible, leading to loss of vested assets. This is because the `VestingManager` contract is no longer connected to the previous marketplace. The report recommends providing a way for users to remove their vested listings and transfer them back to their address after a change in the marketplace contract. The project team has acknowledged the issue and is working on a solution.

### Original Finding Content



<https://github.com/code-423n4/2024-12-secondswap/blob/214849c3517eb26b31fe194bceae65cb0f52d2c0/contracts/SecondSwap_VestingManager.sol# L204>

<https://github.com/code-423n4/2024-12-secondswap/blob/214849c3517eb26b31fe194bceae65cb0f52d2c0/contracts/SecondSwap_VestingManager.sol# L121>

<https://github.com/code-423n4/2024-12-secondswap/blob/214849c3517eb26b31fe194bceae65cb0f52d2c0/contracts/SecondSwap_VestingManager.sol# L149>

<https://github.com/code-423n4/2024-12-secondswap/blob/214849c3517eb26b31fe194bceae65cb0f52d2c0/contracts/SecondSwap_VestingManager.sol# L161>

When interacting with the `MarketPlace` contract and vesting listings, the `MarketPlace` contract calls the `VestingManager` contract (using the address gotten from the `MarketplaceSetting` contract) which calls the `StepVesting` contract itself to transfer vestings from one address to another.

The `VestingManager` contract contains the `setMarketplace` function which is in place in case the `MarketPlace` contract needs to be changed and redeployed instead of an upgrade (upgrades to the MarketPlace contract occur through the proxy admin, so this function is to change the proxy entirely). When a new MarketPlace contract is set, all previous listings in the marketplace remain stuck, unlistable or inaccessible by the user who listed them, leading to loss of vested assets, simply because the VestingManager is no longer connected to that instance of the marketplace.

### Proof of Concept

Let’s take a user who has a total amount of 1000 `Token F` vested. The user decides to list 200 of these tokens on the marketplace. After this period that the listing is active, the `VestingManager` contract updates the MarketPlace contract(not an upgrade, a complete change of the proxy).

The function that changes the marketplace address in the `VestingManager`
```

   function setMarketplace(address _marketplace) external onlyAdmin {
        marketplace = _marketplace;
    }
```

The issue lies in the fact that the `VestingManager` no longer points to the previous marketplace were the listing was made. So those listings that existed in the former marketplace can no longer be unlisted or purchased by another user. Simply because the functions `listVesting` and `unlistVesting` in the MarketPlace contract rely on calling the `VestingManager` contract, which no longer recognizes the old marketplace, only the new one.

There is a freeze function that should supposedly stop all actions on the marketplace to give enough time for users to unlist their listed vestings but when the marketplace is frozen, unlisting and purchasing listings are also frozen. See below:
```

    function unlistVesting(address _vestingPlan, uint256 _listingId) external isFreeze { // <== contains the isFreeze modfiier
        // .... some code here .....
    }

    function spotPurchase(
        address _vestingPlan,
        uint256 _listingId,
        uint256 _amount,
        address _referral
    ) external isFreeze  { // <= contains the isFreeze modifier
        // .... some code here .....
    }
```

So when the old marketplace with users listings tries to call the `VestingManager` contract, it reverts simply because the marketplace recognized in the Vesting manager is not the same as the Old marketplace that contained all previous listings.
```

    // the onlyMarketplace modifier recognizes the new marketplace and not the old marketplace and results in a revert
    function unlistVesting(address seller, address plan, uint256 amount) external onlyMarketplace {}
    function completePurchase(address buyer, address vesting, uint256 amount) external onlyMarketplace {}

// The modifier check
    modifier onlyMarketplace() {
        require(msg.sender == marketplace, "SS_VestingManager: caller is not marketplace");
        _;
    }
```

This leads to the vestings that were in the previous `MarketPlace` becoming inaccessible, unlistable or unpurchaseable.

Major impact would be that all the vestings that were listed in the old marketplace would no longer be accessible because the vesting manager is pointing to a new marketplace contract, leading to loss of vestings listed before the change happened due to them being inaccessible via unlisting or purchasing.

### Recommended mitigation steps

Provide a way to allow after a change in the marketplace contract, the user to be able to remove their vested listings and transfer it back to their address from the previous marketplace.

**TechticalRAM (SecondSwap) acknowledged**

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | SecondSwap |
| Report Date | N/A |
| Finders | EPSec, BenRai, 0xLasadie, franfran20 |

### Source Links

- **Source**: https://code4rena.com/reports/2024-12-secondswap
- **GitHub**: https://code4rena.com/audits/2024-12-secondswap/submissions/F-36
- **Contest**: https://code4rena.com/reports/2024-12-secondswap

### Keywords for Search

`vulnerability`

