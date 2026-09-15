---
# Core Classification
protocol: Project
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49830
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm2mxcaoo000112pvkwt2nb8u
source_link: none
github_link: https://github.com/Cyfrin/2024-11-one-world

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

# Audit Details
report_date: unknown
finders_count: 10
finders:
  - oluwaseyisekoni
  - princekay
  - theirrationalone
  - skid0016
  - 0xkyosi
---

## Vulnerability Title

Users Can Join DAOs Using Removed Currencies Due To Missing Validation

### Overview

See description below for full details.

### Original Finding Content

**Lines of Code:**\
<https://github.com/Cyfrin/2024-11-one-world/blob/1e872c7ab393c380010a507398d4b4caca1ae32b/contracts/dao/CurrencyManager.sol#L49-L57>\
<https://github.com/Cyfrin/2024-11-one-world/blob/1e872c7ab393c380010a507398d4b4caca1ae32b/contracts/dao/MembershipFactory.sol#L140>\
\
**Summary:**

The lack of check in the `joinDAO` function can allow users to interact with a token that is not \`*whiteListed\`*.  When the `Admin_Role` calls the `removeCurrency` function in the `CurrencyManager.sol`, it removes a currency from the `whiteListed` array and not generally from the system. Users can still join an existing DAO that was created with the currency that was recently removed.

**Vulnerability Details:**
The MembershipFactory contract allows users to join DAOs by paying with whitelisted currencies. However, there is no validation in the `joinDAO` function to verify if the DAO's currency is still whitelisted when users attempt to join. When a currency is removed from the CurrencyManager's whitelist, existing DAOs that use that currency remain active and continue accepting new members using the removed currency.

This occurs because:

1. The DAO's configuration stores the currency address but doesn't track its whitelist status
2. The `joinDAO` function only validates tier availability without checking currency status
3. The CurrencyManager's `removeCurrency` function doesn't handle existing DAOs using the currency

**Impact:**

* Users can bypass the currency whitelist system by joining DAOs that use removed currencies
* Could lead to regulatory issues if currencies were removed for compliance reasons
* Platform fees and DAO payments continue in removed currencies, potentially exposing users to deprecated or unsafe tokens

**Recommended Mitigation:**

Add currency whitelist validation in `joinDAO`:

```diff
function joinDAO(address daoMembershipAddress, uint256 tierIndex) external {
        require(daos[daoMembershipAddress].noOfTiers > tierIndex, "Invalid tier.");
        require(daos[daoMembershipAddress].tiers[tierIndex].amount > daos[daoMembershipAddress].tiers[tierIndex].minted, "Tier full.");
+       address currency = daos[daoMembershipAddress].currency;
+       require(currencyManager.isCurrencyWhitelisted(currency), "Currency not whitelisted");
        uint256 tierPrice = daos[daoMembershipAddress].tiers[tierIndex].price;
        uint256 platformFees = (20 * tierPrice) / 100;
        daos[daoMembershipAddress].tiers[tierIndex].minted += 1;
        IERC20(daos[daoMembershipAddress].currency).transferFrom(_msgSender(), owpWallet, platformFees);
        IERC20(daos[daoMembershipAddress].currency).transferFrom(_msgSender(), daoMembershipAddress, tierPrice - platformFees); //my sends it to the Dao contract
        IMembershipERC1155(daoMembershipAddress).mint(_msgSender(), tierIndex, 1);
        emit UserJoinedDAO(_msgSender(), daoMembershipAddress, tierIndex);
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Project |
| Report Date | N/A |
| Finders | oluwaseyisekoni, princekay, theirrationalone, skid0016, 0xkyosi, aresaudits, 4th05, perfect871214, pro_king, jesjupyter |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-11-one-world
- **Contest**: https://codehawks.cyfrin.io/c/cm2mxcaoo000112pvkwt2nb8u

### Keywords for Search

`vulnerability`

