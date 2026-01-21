---
# Core Classification
protocol: Olas
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49360
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/ff3a291b-4cdd-4ebb-9828-c0ebc7f21edf
source_link: https://cdn.cantina.xyz/reports/cantina_valory_january2025.pdf
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
finders_count: 2
finders:
  - Saw-mon and Natalie
  - slowfi
---

## Vulnerability Title

Multiple Mech Marketplace proxies using the same implementation have the same domain separators 

### Overview


This bug report is about a variable called domainSeparator in a code called MechMarketplace. The variable is currently set in the constructor, which causes all proxies using this code to have the same domainSeparator. This allows for signature replays on multiple proxies, which can be a security issue. A test has been added to check for this and a recommendation has been made to fix the issue by initiating the domainSeparator during initialization instead of in the constructor. The bug has been fixed in a pull request and verified by the team.

### Original Finding Content

## MechMarketplace Issue Report

## Context
`MechMarketplace.sol#L152-L167`

## Description
Currently in MechMarketplace, the immutable variable `domainSeparator` is set in the constructor. This causes all the proxies using this implementation to have the same `domainSeparator`, which would allow signature replays across multiple mech marketplace proxies on the same chain.

## Proof of Concept
Add the following test to `test/MechMarketplace.js` and run the command:
```
npm exec hardhat test -- --grep "Multiple Mech"
```

```javascript
context("Multiple Mech Market Proxies with the same original implementation", async function () {
    let m1;
    let m2;
    beforeEach(async function () {
        const MechMarketplace = await ethers.getContractFactory("MechMarketplace");
        const mechMarketplace = await MechMarketplace.deploy(serviceRegistry.address, karma.address);
        await mechMarketplace.deployed();
        
        async function deployMechMarketplaceProxy() {
            // Deploy and initialize marketplace proxy
            const proxyData = MechMarketplace.interface.encodeFunctionData("initialize",
                [fee, minResponseTimeout, maxResponseTimeout]);
            const MechMarketplaceProxy = await ethers.getContractFactory("MechMarketplaceProxy");
            const mechMarketplaceProxy = await MechMarketplaceProxy.deploy(mechMarketplace.address, proxyData);
            await mechMarketplaceProxy.deployed();
            return ethers.getContractAt("MechMarketplace", mechMarketplaceProxy.address);
        }

        m1 = await deployMechMarketplaceProxy();
        m2 = await deployMechMarketplaceProxy();
    });

    it("Domain Separators should not match", async function() {
        const d1 = await m1.getDomainSeparator();
        const d2 = await m2.getDomainSeparator();
        // two different mech markets proxies with the same shared original implementation
        // should not have the same domain separators
        expect(d1).not.to.equal(d2);
    });
});
```

## Recommendation
Make sure `domainSeparator` is initiated during initialization and not in the constructor. Also, initialization for proxy contracts is recommended to be blocked.

## Valory
Fixed on PR 93.

## Cantina Managed
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Olas |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, slowfi |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_valory_january2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/ff3a291b-4cdd-4ebb-9828-c0ebc7f21edf

### Keywords for Search

`vulnerability`

