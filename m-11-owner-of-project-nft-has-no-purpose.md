---
# Core Classification
protocol: Rigor Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3115
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-08-rigor-protocol-contest
source_link: https://code4rena.com/reports/2022-08-rigor
github_link: https://github.com/code-423n4/2022-08-rigor-findings/issues/413

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
  - dexes
  - cdp
  - yield
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - byndooa  rbserver
  - berndartmueller
---

## Vulnerability Title

[M-11] Owner of project NFT has no purpose

### Overview


This bug report is about the project NFT (non-fungible token) in Rigor, a blockchain-based platform. When creating a new project, a NFT is minted to the sender (builder). The builder has special permissions to access authorized functions in Rigor. However, if the NFT is transferred to a different address, the builder stays the same and the new owner has no purpose and no permissions. This means funds could be locked in the project contract if the current builder address is unable to perform any more actions. The bug was identified through manual review. To mitigate this issue, it is recommended to prevent transferring the project NFT to a different address or use the actual NFT owner as the builder of a project.

### Original Finding Content

_Submitted by berndartmueller, also found by byndooa and rbserver_

Creating a new project mints a NFT to the `_sender` (builder). The `builder` of a project has special permissions and is required to perform various tasks.

However, if the minted NFT is transferred to a different address, the `builder` of a project stays the same and the new owner of the transferred NFT has no purpose and no permissions to access authorized functions in Rigor.

If real-world use-cases require a change of the `builder` address, there is currently no way to do so. Funds could be locked in the project contract if the current `builder` address is unable to perform any more actions.

### Proof of Concept

[HomeFi.sol#L225](https://github.com/code-423n4/2022-08-rigor/blob/5ab7ea84a1516cb726421ef690af5bc41029f88f/contracts/HomeFi.sol#L225)<br>

```solidity
function createProject(bytes memory _hash, address _currency)
    external
    override
    nonReentrant
{
    // Revert if currency not supported by HomeFi
    validCurrency(_currency);

    address _sender = _msgSender();

    // Create a new project Clone and mint a new NFT for it
    address _project = projectFactoryInstance.createProject(
        _currency,
        _sender
    );
    mintNFT(_sender, string(_hash));

    // Update project related mappings
    projects[projectCount] = _project;
    projectTokenId[_project] = projectCount;

    emit ProjectAdded(projectCount, _project, _sender, _currency, _hash);
}
```

### Recommended Mitigation Steps

Consider preventing transferring the project NFT to a different address for now as long as there is no use-case for the NFT owner/holder or use the actual NFT owner as the `builder` of a project.

**[zgorizzo69 (Rigor) disputed and commented](https://github.com/code-423n4/2022-08-rigor-findings/issues/413#issuecomment-1207294173):**
 > Builders are kyc'ed that's why just by transferring the NFT you don't get any of the builder privileges. 

**[parv3213 (Rigor) commented](https://github.com/code-423n4/2022-08-rigor-findings/issues/413#issuecomment-1207340273):**
 > As the warden said, `Owner of project NFT has no purpose` is true and is the intended behavior. Owning this NFT does not change anything.

**[Jack the Pug (judge) confirmed as valid](https://github.com/code-423n4/2022-08-rigor-findings/issues/413)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Rigor Protocol |
| Report Date | N/A |
| Finders | byndooa  rbserver, berndartmueller |

### Source Links

- **Source**: https://code4rena.com/reports/2022-08-rigor
- **GitHub**: https://github.com/code-423n4/2022-08-rigor-findings/issues/413
- **Contest**: https://code4rena.com/contests/2022-08-rigor-protocol-contest

### Keywords for Search

`vulnerability`

