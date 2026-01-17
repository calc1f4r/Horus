---
# Core Classification
protocol: One World Project
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41926
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
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
  - Immeas
  - Gio
---

## Vulnerability Title

DAO membership fees cannot be retrieved by the creator

### Overview


The bug report describes an issue where the membership fees paid by users to join a DAO are not accessible to the creator of the DAO. These fees are split between the One World Project and the DAO creator, but the fees sent to the DAO creator are not accessible through any method. The only way for the creator to retrieve these funds is through a complex process involving external calls and verifications. This poses a risk and the report recommends adding a method for the creator to directly retrieve the fees. The One World Project acknowledges this issue and suggests ensuring the off-chain service meets high security standards.

### Original Finding Content

**Description:** The DAO membership fee taken from users who invoke [`MembershipFactory::joinDAO`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L120-L133) is split between the One World Project and the DAO creator, being sent to the One World Project wallet and DAO `MembershipERC1155` instance respectively:

```solidity
uint256 tierPrice = daos[daoMembershipAddress].tiers[tierIndex].price;
uint256 platformFees = (20 * tierPrice) / 100;
daos[daoMembershipAddress].tiers[tierIndex].minted += 1;
IERC20(daos[daoMembershipAddress].currency).transferFrom(msg.sender, owpWallet, platformFees);
IERC20(daos[daoMembershipAddress].currency).transferFrom(msg.sender, daoMembershipAddress, tierPrice - platformFees);
```

However, the fees [sent](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L130) to the `daoMembershipAddress` are not accessible to the DAO creator as there is no method for direct retrieval. The only way these funds can be retrieved and sent to the creator is if the `MembershipFactory::EXTERNAL_CALLER` role invokes [`MembershipERC1155::callExternalContract`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/tokens/MembershipERC1155.sol#L202-L210) via [`MembershipFactory::callExternalContract`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L155-L163), allowing arbitrary external calls to be executed.

**Impact:** The DAO creator has no direct method for retrieving the membership fees paid to their `MembershipERC1155` instance, ignoring rescue initiated by the `EXTERNAL_CALLER` role.

**Proof of Concept:** The following test can be added to `describe("Create New DAO Membership")` in `MembershipFactory.test.ts`:
```javascript
it("only allows owner to recover dao membership fees", async function () {
  await currencyManager.addCurrency(testERC20.address);
  const creator = addr1;

  await membershipFactory.connect(creator).createNewDAOMembership(DAOConfig, TierConfig);

  const ensAddress = await membershipFactory.getENSAddress("testdao.eth");
  const membershipERC1155 = await MembershipERC1155.attach(ensAddress);

  await testERC20.mint(addr2.address, ethers.utils.parseEther("20"));
  await testERC20.connect(addr2).approve(membershipFactory.address, ethers.utils.parseEther("20"));
  await expect(membershipFactory.connect(addr2).joinDAO(membershipERC1155.address, 1)).to.not.be.reverted;

  // fees are in the membership token but cannot be retrieved by the creator
  const daoMembershipBalance = await testERC20.balanceOf(membershipERC1155.address);
  expect(daoMembershipBalance).to.equal(160); // minus protocol fee

  const creatorBalanceBefore = await testERC20.balanceOf(creator.address);

  // only admin can recover them
  const transferData = testERC20.interface.encodeFunctionData("transfer", [creator.address, 160]);
  const data = membershipERC1155.interface.encodeFunctionData("callExternalContract", [testERC20.address, transferData]);
  await membershipFactory.callExternalContract(membershipERC1155.address, data);

  const creatorBalanceAfter = await testERC20.balanceOf(creator.address);
  expect(creatorBalanceAfter.sub(creatorBalanceBefore)).to.equal(160);
});
```

**Recommended Mitigation:** Consider adding a method for the creator of the DAO to retrieve the membership fees paid by users upon joining the DAO.

**One World Project:** The DAO creator is deliberately, by design, not allowed to access the DAO funds. They have to be accessed through the `callExternalContract` which can only be called by the `EXTERNAL_CONTRACT` which does its own verifications in the backend.

**Cyfrin:** Acknowledged. This dependency introduces additional risks, and we recommend ensuring the off-chain service meets stringent security standards.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | One World Project |
| Report Date | N/A |
| Finders | Immeas, Gio |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

