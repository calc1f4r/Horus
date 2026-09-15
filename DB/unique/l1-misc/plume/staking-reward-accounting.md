---
# Core Classification
protocol: generic
chain: plume
category: staking
vulnerability_type: staking_rewards_plume
root_cause_family: see pattern_key

# Pattern Identity
pattern_key: staking-rewards-plume | staking rewards plume | varies by finding | see references

# Interaction Scope
interaction_scope: varies
involved_contracts:
  - staking rewards plume

# Attack Vector Details
attack_type: varies
affected_component: staking rewards plume

# Technical Primitives
primitives:
  - able
  - access
  - accounting
  - accrual
  - accrue
  - accrued

# Grep / Hunt-Card Seeds
code_keywords:
  - able
  - access
  - accounting
  - accrual
  - accrue
  - accrued
  - accruing
  - across

severity: high
impact: varies
language: varies
tags:
  - plume
  - l1
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [p1] | reports/plume-l1_findings/49616-sc-high-user-can-steal-rewards.md | HIGH | Immunefi (shadowHunter) | sc high user can steal rewards |
| [p2] | reports/plume-l1_findings/49700-sc-high-validator-commission-can-be-blocked.md | HIGH | Immunefi (Blobism) | sc high validator commission can be blocked |
| [p3] | reports/plume-l1_findings/49817-sc-medium-inactive-validators-are-prevented-to-claim-to-eligible-commission-rewards.md | MEDIUM | Immunefi (warden) | sc medium inactive validators are prevented to claim to eligible commission rewards |
| [p4] | reports/plume-l1_findings/50167-sc-high-retroactive-reward-drain-via-incomplete-reward-debt-reset.md | HIGH | Immunefi (BeastBoy) | sc high retroactive reward drain via incomplete reward debt reset |
| [p5] | reports/plume-l1_findings/50350-sc-high-stakingfacet-stakeonbehalf-allows-to-prevent-withdraws.md | HIGH | Immunefi (max10afternoon) | sc high stakingfacet stakeonbehalf allows to prevent withdraws |
| [p6] | reports/plume-l1_findings/50409-sc-high-validator-will-lose-comission.md | HIGH | Immunefi (shadowHunter) | sc high validator will lose comission |
| [p7] | reports/plume-l1_findings/50412-sc-high-illegitimate-reward-claim-after-unstake-due-to-overlapping-reward-rate-checkpoints.md | HIGH | Immunefi (GeorgeMichael) | sc high illegitimate reward claim after unstake due to overlapping reward rate checkpoints |
| [p8] | reports/plume-l1_findings/50425-sc-high-active-non-slashed-validators-cannot-claim-rewards-when-a-reward-token-is-disabled.md | HIGH | Immunefi (oxrex) | sc high active non slashed validators cannot claim rewards when a reward token is disabled |
| [p9] | reports/plume-l1_findings/50433-sc-high-validator-list-griefing-unrestricted-stakeonbehalf-allows-user-asset-freeze-permanentl.md | HIGH | Immunefi (farman1094) | sc high validator list griefing unrestricted stakeonbehalf allows user asset freeze permanently |
| [p10] | reports/plume-l1_findings/50450-sc-high-logic-error-in-streak-validation-causes-legitimate-jackpot-wins-to-be-denied-violating.md | HIGH | Immunefi (Bug82427) | sc high logic error in streak validation causes legitimate jackpot wins to be denied violating reward contract expectations |
| [p11] | reports/plume-l1_findings/50477-sc-high-validator-loses-all-accrued-commission-when-reward-token-is-removed.md | HIGH | Immunefi (holydevoti0n) | sc high validator loses all accrued commission when reward token is removed |
| [p12] | reports/plume-l1_findings/50490-sc-high-user-loses-reward-tokens-during-validator-user-relationship-clearing.md | HIGH | Immunefi (oxrex) | sc high user loses reward tokens during validator user relationship clearing |
| [p13] | reports/plume-l1_findings/50519-sc-high-rewardsfacet-reintroducing-an-old-reward-token-will-result-in-wrong-accounting-leading.md | HIGH | Immunefi (max10afternoon) | sc high rewardsfacet reintroducing an old reward token will result in wrong accounting leading to theft of yield |
| [p14] | reports/plume-l1_findings/50560-sc-high-inconsistent-commission-rounding-traps-user-validator-funds.md | HIGH | Immunefi (Sharky) | sc high inconsistent commission rounding traps user validator funds |
| [p15] | reports/plume-l1_findings/50860-sc-high-logic-error-in-jackpot-eligibility-check-leads-to-systematic-theft-of-user-rewards.md | HIGH | Immunefi (AlertBasilisk56249) | sc high logic error in jackpot eligibility check leads to systematic theft of user rewards |
| [p16] | reports/plume-l1_findings/51051-sc-high-inactive-validator-reward-accrual-bypass.md | HIGH | Immunefi (light279) | sc high inactive validator reward accrual bypass |
| [p17] | reports/plume-l1_findings/51124-sc-high-validator-would-loss-commission-fee-if-the-rewards-token-are-removed.md | HIGH | Immunefi (pks271) | sc high validator would loss commission fee if the rewards token are removed |
| [p18] | reports/plume-l1_findings/51324-sc-high-rounding-in-commission-accounting-burns-delegator-rewards.md | HIGH | Immunefi (Rhaydden) | sc high rounding in commission accounting burns delegator rewards |
| [p19] | reports/plume-l1_findings/51452-sc-high-stakeonbehalf-function-enables-out-of-gas-dos.md | HIGH | Immunefi (KlosMitSoss) | sc high stakeonbehalf function enables out of gas dos |
| [p20] | reports/plume-l1_findings/51476-sc-medium-validators-can-t-claim-their-accrued-commission-if-they-are-made-inactive.md | MEDIUM | Immunefi (WinSec) | sc medium validators can t claim their accrued commission if they are made inactive |
| [p21] | reports/plume-l1_findings/51479-sc-high-inaccurate-reward-calculation-post-validator-slashing-due-to-premature-timestamp-updat.md | HIGH | Immunefi (light279) | sc high inaccurate reward calculation post validator slashing due to premature timestamp update on token removal |
| [p22] | reports/plume-l1_findings/51530-sc-high-validators-can-not-claim-pending-accrued-commission-when-reward-tokens-have-been-remov.md | HIGH | Immunefi (Outliers) | sc high validators can not claim pending accrued commission when reward tokens have been removed from the isrewardtoken mapping&#x20; |
| [p23] | reports/plume-l1_findings/51653-sc-high-permanent-loss-of-staker-rewards-after-slashing-when-validator-records-are-cleared.md | HIGH | Immunefi (wellbyt3) | sc high permanent loss of staker rewards after slashing when validator records are cleared |
| [p24] | reports/plume-l1_findings/51658-sc-high-yield-distribution-in-batches-let-the-same-tokens-collect-rewards-in-multiple-batches.md | HIGH | Immunefi (jovi) | sc high yield distribution in batches let the same tokens collect rewards in multiple batches stealing yield from other users |
| [p25] | reports/plume-l1_findings/51666-sc-medium-inactive-validators-blocked-from-claiming-accrued-commission.md | MEDIUM | Immunefi (farman1094) | sc medium inactive validators blocked from claiming accrued commission |
| [p51] | reports/plume-l1_findings/51684-sc-medium-unbounded-gas-consumption-in-removestakerfromallvalidators-leads-to-denial-of-servic.md | MEDIUM | Immunefi (drdee) | sc medium unbounded gas consumption in removestakerfromallvalidators leads to denial of service preventing users with large validator counts from remo |
| [p52] | reports/plume-l1_findings/51728-sc-high-users-can-claim-rewards-for-inactive-validator-periods-due-to-incorrect-checkpoint-acc.md | HIGH | Immunefi (farman1094) | sc high users can claim rewards for inactive validator periods due to incorrect checkpoint accrual&#x20; |
| [p53] | reports/plume-l1_findings/51813-sc-high-malicious-user-can-grief-victims-by-staking-them-across-many-validators-leading-to-fun.md | HIGH | Immunefi (ihtishamsudo) | sc high malicious user can grief victims by staking them across many validators leading to fund freezing |
| [p54] | reports/plume-l1_findings/51842-sc-high-unclaimed-staker-rewards-lost-when-admin-clears-validator-records-without-checking-pen.md | HIGH | Immunefi (farman1094) | sc high unclaimed staker rewards lost when admin clears validator records without checking pending rewards |
| [p55] | reports/plume-l1_findings/51860-sc-high-missing-access-control-in-stakeonbehalf-lets-anyone-bloat-another-user-s-validator-lis.md | HIGH | Immunefi (manvi) | sc high missing access control in stakeonbehalf lets anyone bloat another user s validator list leading to permanent fund lock via gas exhaustion dos |
| [p56] | reports/plume-l1_findings/51909-sc-medium-inconsistent-commission-claim-logic-denies-legitimate-claims-for-inactive-validators.md | MEDIUM | Immunefi (Outliers) | sc medium inconsistent commission claim logic denies legitimate claims for inactive validators |
| [p57] | reports/plume-l1_findings/51912-sc-high-mismatched-rounding-rules-in-reward-logic-library-results-in-two-fold-loss-of-earnings.md | HIGH | Immunefi (jovi) | sc high mismatched rounding rules in reward logic library results in two fold loss of earnings |
| [p58] | reports/plume-l1_findings/51946-sc-high-commission-claims-fail-for-removed-reward-tokens.md | HIGH | Immunefi (aksoy) | sc high commission claims fail for removed reward tokens |
| [p59] | reports/plume-l1_findings/51987-sc-high-validators-will-be-able-to-steal-more-commission-from-users-that-isn-t-the-commission.md | HIGH | Immunefi (oxrex) | sc high validators will be able to steal more commission from users that isn t the commission to be charged |
| [p60] | reports/plume-l1_findings/51988-sc-medium-plumerewardlogic-calculaterewardswithcheckpointsview-lacking-of-checking-if-the-vali.md | MEDIUM | Immunefi (jasonxiale) | sc medium plumerewardlogic calculaterewardswithcheckpointsview lacking of checking if the validator is inactive but not slashed&#x20; |
| [p61] | reports/plume-l1_findings/51994-sc-high-permanent-loss-of-validator-commission-upon-reward-token-removal.md | HIGH | Immunefi (light279) | sc high permanent loss of validator commission upon reward token removal |
| [p62] | reports/plume-l1_findings/51999-sc-high-logical-flaw-in-validator-reactivation-and-addrewardtoken-allows-claiming-rewards-for.md | HIGH | Immunefi (perseverance) | sc high logical flaw in validator reactivation and addrewardtoken allows claiming rewards for validators in inactive periods |
| [p63] | reports/plume-l1_findings/52084-sc-high-unstaking-before-reward-token-removal-leads-to-incorrect-reward-accrual-on-re-addition.md | HIGH | Immunefi (light279) | sc high unstaking before reward token removal leads to incorrect reward accrual on re addition |
| [p64] | reports/plume-l1_findings/52104-sc-high-removed-reward-tokens-block-validator-commission-claims.md | HIGH | Immunefi (jovi) | sc high removed reward tokens block validator commission claims |
| [p65] | reports/plume-l1_findings/52165-sc-high-user-can-t-claim-reward-erc20-tokens-since-rewards-transfer-will-revert.md | HIGH | Immunefi (WinSec) | sc high user can t claim reward erc20 tokens since rewards transfer will revert |
| [p66] | reports/plume-l1_findings/52278-sc-high-incorrect-streak-check-in-jackpot-eligibility-leads-to-unfair-reward-denial.md | HIGH | Immunefi (godwinudo) | sc high incorrect streak check in jackpot eligibility leads to unfair reward denial |
| [p67] | reports/plume-l1_findings/52286-sc-high-off-by-one-error-in-jackpot-eligibility-check-leads-to-denial-of-legitimate-rewards.md | HIGH | Immunefi (OxPrince) | sc high off by one error in jackpot eligibility check leads to denial of legitimate rewards |
| [p68] | reports/plume-l1_findings/52390-sc-high-validateistoken-blocks-validators-from-claiming-earned-rewards-from-removed-tokens.md | HIGH | Immunefi (kaysoft) | sc high validateistoken blocks validators from claiming earned rewards from removed tokens&#x20; |
| [p69] | reports/plume-l1_findings/52500-sc-high-missing-commission-checkpoint-initialization-leads-to-retroactive-commission-theft-of.md | HIGH | Immunefi (ZeroExRes) | sc high missing commission checkpoint initialization leads to retroactive commission theft of user rewards |
| [p70] | reports/plume-l1_findings/52527-sc-high-the-validator-admin-might-claim-less-commission-token-when-validatorfacet-requestcommi.md | HIGH | Immunefi (jasonxiale) | sc high the validator admin might claim less commission token when validatorfacet requestcommissionclaim is called&#x20; |
| [p71] | reports/plume-l1_findings/52573-sc-high-unconsented-stakeonbehalf-enables-unbounded-gas-consumption-via-uservalidators-growth.md | HIGH | Immunefi (wylis) | sc high unconsented stakeonbehalf enables unbounded gas consumption via uservalidators growth causing dos at scale in claimall withdraw&#x20; |
| [p72] | reports/plume-l1_findings/52588-sc-high-retroactive-reward-accrual-for-newly-added-tokens-when-validator-was-inactive.md | HIGH | Immunefi (light279) | sc high retroactive reward accrual for newly added tokens when validator was inactive&#x20; |
| [p73] | reports/plume-l1_findings/52667-sc-high-commission-is-not-added-at-point-of-adding-validator-hence-stakers-that-stake-before-t.md | HIGH | Immunefi (warden) | sc high commission is not added at point of adding validator hence stakers that stake before the first checkpoint would always use the current commiss |
| [p74] | reports/plume-l1_findings/52711-sc-high-in-validatorfacet-validator-cannot-claims-commissions-of-removed-tokens.md | HIGH | Immunefi (Paludo0x) | sc high in validatorfacet validator cannot claims commissions of removed tokens |
| [p75] | reports/plume-l1_findings/52719-sc-medium-inactive-validators-blocked-from-claiming-commissions-despite-passed-timelock.md | MEDIUM | Immunefi (warden) | sc medium inactive validators blocked from claiming commissions despite passed timelock |
| [p76] | reports/plume-l1_findings/52770-sc-high-unbounded-gas-consumption-via-stakeonbehalf-manipulation.md | HIGH | Immunefi (bl4ck4non) | sc high unbounded gas consumption via stakeonbehalf manipulation |
| [p77] | reports/plume-l1_findings/52780-sc-high-timestamp-manipulation-in-forcesettlevalidatorcommission-leads-to-permanent-loss-of-st.md | HIGH | Immunefi (ZeroExRes) | sc high timestamp manipulation in forcesettlevalidatorcommission leads to permanent loss of staker rewards |
| [p78] | reports/plume-l1_findings/52849-sc-high-claimers-who-claim-after-slash-inactive-updaterewardpertokenforvalidator-which-advance.md | HIGH | Immunefi (IronsideSec) | sc high claimers who claim after slash inactive updaterewardpertokenforvalidator which advances validatorlastupdatetimes to be more than slashtimestam |
| [p79] | reports/plume-l1_findings/52865-sc-high-inconsistency-in-how-stake-cooldown-is-handled-due-to-off-by-one-error.md | HIGH | Immunefi (warden) | sc high inconsistency in how stake cooldown is handled due to off by one error&#x20; |
| [p80] | reports/plume-l1_findings/52889-sc-high-inactive-validators-accrue-rewards-for-new-tokens.md | HIGH | Immunefi (KlosMitSoss) | sc high inactive validators accrue rewards for new tokens |
| [p81] | reports/plume-l1_findings/52931-sc-high-validators-can-not-claim-their-commissions-after-the-reward-token-removal.md | HIGH | Immunefi (Slayer) | sc high validators can not claim their commissions after the reward token removal&#x20; |
| [p82] | reports/plume-l1_findings/52944-sc-high-the-requestcommisionclaim-function-can-only-claim-commission-on-tokens-that-are-curren.md | HIGH | Immunefi (frolic) | sc high the requestcommisionclaim function can only claim commission on tokens that are currently reward tokens |
| [p83] | reports/plume-l1_findings/52955-sc-high-a-commission-rate-checkpoint-is-not-created-when-adding-a-validator-despite-the-commis.md | HIGH | Immunefi (frolic) | sc high a commission rate checkpoint is not created when adding a validator despite the commission rate being set leading to loss of validator commiss |
| [p84] | reports/plume-l1_findings/52964-sc-high-if-a-new-reward-token-is-added-during-a-the-period-a-validator-is-inactive-the-validat.md | HIGH | Immunefi (warden) | sc high if a new reward token is added during a the period a validator is inactive the validator will still earn rewards commission for some of the du |
| [p85] | reports/plume-l1_findings/52983-sc-high-validator-will-loose-commission-for-the-tokens-which-are-removed-from-the-reward-token.md | HIGH | Immunefi (swarun) | sc high validator will loose commission for the tokens which are removed from the reward tokens but they still have commission left to be claimed&#x20 |
| [p86] | reports/plume-l1_findings/52995-sc-high-validators-lose-access-to-historical-reward-tokens-when-tokens-are-removed.md | HIGH | Immunefi (warden) | sc high validators lose access to historical reward tokens when tokens are removed |
| [p87] | reports/plume-l1_findings/52996-sc-high-users-can-claim-rewards-for-newly-added-reward-tokens-even-when-the-validator-they-sta.md | HIGH | Immunefi (swarun) | sc high users can claim rewards for newly added reward tokens even when the validator they staked for was inactive during some time interval&#x20; |
| [p88] | reports/plume-l1_findings/53018-sc-high-owed-rewards-could-be-lost-for-some-users-for-periods-before-slashing-time-due-to-inco.md | HIGH | Immunefi (valkvalue) | sc high owed rewards could be lost for some users for periods before slashing time due to incorrect logic&#x20; |
| [p89] | reports/plume-l1_findings/53020-sc-high-there-are-functions-which-when-inevitably-used-could-result-in-wrongly-accruing-yield.md | HIGH | Immunefi (valkvalue) | sc high there are functions which when inevitably used could result in wrongly accruing yield for inactive validators which can make the protocol inso |
| [p90] | reports/plume-l1_findings/53028-sc-high-there-is-an-asymmetric-rounding-issue-that-is-can-cause-a-theft-of-unclaimed-yield-in.md | HIGH | Immunefi (XDZIBECX) | sc high there is an asymmetric rounding issue that is can cause a theft of unclaimed yield in reward or commission accounting |
| [p91] | reports/plume-l1_findings/53039-sc-high-rewards-and-commissions-accrued-in-the-interval-before-a-slash-might-be-lost.md | HIGH | Immunefi (a16) | sc high rewards and commissions accrued in the interval before a slash might be lost |
| [p92] | reports/plume-l1_findings/53051-sc-high-unconsented-stakeonbehalf-enables-third-party-gas-griefing-dos-by-bloating-uservalidat.md | HIGH | Immunefi (tansegv) | sc high unconsented stakeonbehalf enables third party gas griefing dos by bloating uservalidators breaking withdraw claimall |
| [p93] | reports/plume-l1_findings/53061-sc-high-asymmetric-rounding-in-commission-ceil-for-users-floor-for-validators-enables-per-segm.md | HIGH | Immunefi (tansegv) | sc high asymmetric rounding in commission ceil for users floor for validators enables per segment rounding loss validators can amplify via frequent co |
| [q94] | reports/plume-l1_findings/49623-sc-low-unstaking-allows-going-below-minimum-stake.md | LOW | Immunefi (Blobism) | sc low unstaking allows going below minimum stake |
| [q95] | reports/plume-l1_findings/49668-sc-insight-validator-status-function-emit-misleading-event.md | INFO | Immunefi (holydevoti0n) | sc insight validator status function emit misleading event&#x20; |
| [q96] | reports/plume-l1_findings/49671-sc-insight-wrong-emission-in-stake.md | INFO | Immunefi (holydevoti0n) | sc insight wrong emission in stake |
| [q97] | reports/plume-l1_findings/49698-sc-low-coordinated-validator-attack-delays-slashing-and-enables-commission-theft.md | LOW | Immunefi (shadowHunter) | sc low coordinated validator attack delays slashing and enables commission theft |
| [q98] | reports/plume-l1_findings/49726-sc-insight-there-is-a-redundant-zero-address-check-in-the-validatorfacet-sol-that-is-obsolete.md | INFO | Immunefi (avoloder) | sc insight there is a redundant zero address check in the validatorfacet sol that is obsolete and could never be true |
| [q99] | reports/plume-l1_findings/49919-sc-insight-unstake-function-does-not-unstake-all-as-mentioned-in-the-natspec.md | INFO | Immunefi (holydevoti0n) | sc insight unstake function does not unstake all as mentioned in the natspec |
| [q100] | reports/plume-l1_findings/50082-sc-low-protocol-lets-validators-operate-with-dust-amounts-making-attacks-risk-free.md | LOW | Immunefi (holydevoti0n) | sc low protocol lets validators operate with dust amounts making attacks risk free |
| [q101] | reports/plume-l1_findings/50168-sc-insight-unused-and-duplicated-functions-should-be-removed-from-rewardsfacet-and-stakingface.md | INFO | Immunefi (Vanshika) | sc insight unused and duplicated functions should be removed from rewardsfacet and stakingfacet |
| [q102] | reports/plume-l1_findings/50212-sc-insight-validators-without-staked-funds-can-control-slashing-decisions-leading-to-protocol.md | INFO | Immunefi (holydevoti0n) | sc insight validators without staked funds can control slashing decisions leading to protocol insolvency |
| [q103] | reports/plume-l1_findings/50312-sc-insight-validator-can-steal-user-rewards-due-to-a-lack-of-cooldown-when-validator-increases.md | INFO | Immunefi (holydevoti0n) | sc insight validator can steal user rewards due to a lack of cooldown when validator increases commission |
| [q104] | reports/plume-l1_findings/50436-sc-low-votetoslashvalidator-prevents-malicious-inactive-validators-to-be-slashed.md | LOW | Immunefi (holydevoti0n) | sc low votetoslashvalidator prevents malicious inactive validators to be slashed&#x20; |
| [q105] | reports/plume-l1_findings/50506-sc-insight-stakingfacet-missing-event-emission-on-any-unstaking-operations.md | INFO | Immunefi (blackgrease) | sc insight stakingfacet missing event emission on any unstaking operations |
| [q106] | reports/plume-l1_findings/50551-sc-low-staked-dust-positions-are-not-properly-prevented.md | LOW | Immunefi (a16) | sc low staked dust positions are not properly prevented |
| [q107] | reports/plume-l1_findings/50691-sc-insight-no-validator-limit-can-lead-to-dos.md | INFO | Immunefi (PotEater) | sc insight no validator limit can lead to dos |
| [q108] | reports/plume-l1_findings/50745-sc-low-single-cooldown-entry-design-causes-timer-reset-on-multiple-unstakes-leading-to-extende.md | LOW | Immunefi (Bluedragon) | sc low single cooldown entry design causes timer reset on multiple unstakes leading to extended lock periods |
| [q109] | reports/plume-l1_findings/50783-sc-low-validator-percentage-cap-does-not-work-properly.md | LOW | Immunefi (holydevoti0n) | sc low validator percentage cap does not work properly |
| [q110] | reports/plume-l1_findings/50914-sc-low-bypass-of-minimum-stake-enforcement-via-partial-unstake.md | LOW | Immunefi (light279) | sc low bypass of minimum stake enforcement via partial unstake |
| [q111] | reports/plume-l1_findings/50922-sc-low-unstaking-partially-will-extend-the-cooldown-time-for-previously-unstaked-amount-too.md | LOW | Immunefi (WinSec) | sc low unstaking partially will extend the cooldown time for previously unstaked amount too |
| [q112] | reports/plume-l1_findings/51083-sc-insight-claimall-only-loops-over-active-reward-tokens-and-ignores-historical-tokens.md | INFO | Immunefi (KlosMitSoss) | sc insight claimall only loops over active reward tokens and ignores historical tokens |
| [q113] | reports/plume-l1_findings/51171-sc-insight-redundant-storage-reads-and-unnecessary-checks-in-reward-rate-checkpoint-logic-lead.md | INFO | Immunefi (farman1094) | sc insight redundant storage reads and unnecessary checks in reward rate checkpoint logic lead to inefficient gas usage |
| [q114] | reports/plume-l1_findings/51201-sc-low-contracts-without-payable-entry-points-cannot-withdraw-nor-claim-rewards.md | LOW | Immunefi (jovi) | sc low contracts without payable entry points cannot withdraw nor claim rewards |
| [q115] | reports/plume-l1_findings/51288-sc-insight-validators-commission-can-be-permanently-lost.md | INFO | Immunefi (Outliers) | sc insight validators commission can be permanently lost |
| [q116] | reports/plume-l1_findings/51455-sc-low-inflated-earned-ui-rewards-when-validator-stake-is-zero-due-to-missing-totalstaked-guar.md | LOW | Immunefi (Rhaydden) | sc low inflated earned ui rewards when validator stake is zero due to missing totalstaked guard in view logic |
| [q117] | reports/plume-l1_findings/51510-sc-low-bypass-of-maxvalidatorpercentage-allows-a-validator-to-exceed-the-decentralisation-cap.md | LOW | Immunefi (Rhaydden) | sc low bypass of maxvalidatorpercentage allows a validator to exceed the decentralisation cap |
| [q118] | reports/plume-l1_findings/51519-sc-low-unstake-does-not-validate-users-remaing-stake.md | LOW | Immunefi (funkornaut) | sc low unstake does not validate users remaing stake |
| [q119] | reports/plume-l1_findings/51713-sc-low-missing-minimum-stake-validation-in-unstake-operations.md | LOW | Immunefi (rilwan99) | sc low missing minimum stake validation in unstake operations |
| [q120] | reports/plume-l1_findings/51802-sc-low-temporary-freeze-of-rewards-is-possible-if-efficientsupply-0.md | LOW | Immunefi (Santi) | sc low temporary freeze of rewards is possible if efficientsupply 0 |
| [q121] | reports/plume-l1_findings/51966-sc-low-totalamountclaimable-reverts-instead-of-returning-the-claimable-reward-for-historical-t.md | LOW | Immunefi (holydevoti0n) | sc low totalamountclaimable reverts instead of returning the claimable reward for historical tokens |
| [q122] | reports/plume-l1_findings/51980-sc-low-unstake-cooldown-period-is-mistakenly-reset-on-each-claim-resulting-in-temporary-frozen.md | LOW | Immunefi (ZeroXGondar) | sc low unstake cooldown period is mistakenly reset on each claim resulting in temporary frozen funds |
| [q123] | reports/plume-l1_findings/52113-sc-low-stakingfacet-unstake-uint16-validatorid-uint256-amount-can-be-abused-to-bypass-minstake.md | LOW | Immunefi (jasonxiale) | sc low stakingfacet unstake uint16 validatorid uint256 amount can be abused to bypass minstakeamount&#x20; |
| [q124] | reports/plume-l1_findings/52186-sc-low-incorrect-reward-calculation-for-slashed-validators-due-to-single-segment-time-handling.md | LOW | Immunefi (DSbeX) | sc low incorrect reward calculation for slashed validators due to single segment time handling&#x20; |
| [q125] | reports/plume-l1_findings/52248-sc-insight-lack-of-initialization-check-in-staking-allows-users-to-stake-without-reward-token.md | INFO | Immunefi (wylis) | sc insight lack of initialization check in staking allows users to stake without reward token configured causing permanent loss of yield |
| [q126] | reports/plume-l1_findings/52312-sc-low-cooldown-coalescing-bug-unintended-cooldown-extension-for-prior-unstakes.md | LOW | Immunefi (warden) | sc low cooldown coalescing bug unintended cooldown extension for prior unstakes |
| [q127] | reports/plume-l1_findings/52422-sc-low-using-the-current-time-in-geteffectiverewardrateat-will-result-in-incorrect-reward-calc.md | LOW | Immunefi (WinSec) | sc low using the current time in geteffectiverewardrateat will result in incorrect reward calculation for an entire duration of a time segment |
| [q128] | reports/plume-l1_findings/52489-sc-low-when-users-perform-unstake-operations-in-batches-it-may-cause-some-funds-to-be-frozen-f.md | LOW | Immunefi (Lin511) | sc low when users perform unstake operations in batches it may cause some funds to be frozen for an additional period of time&#x20; |
| [q129] | reports/plume-l1_findings/52750-sc-low-percentage-limit-bypass-via-unstaking-from-other-validators.md | LOW | Immunefi (EFCCWEB3) | sc low percentage limit bypass via unstaking from other validators |
| [q130] | reports/plume-l1_findings/52837-sc-insight-gas-heavy-repeated-binary-search-increases-reward-calculation-gas-costs.md | INFO | Immunefi (Khay3) | sc insight gas heavy repeated binary search increases reward calculation gas costs |
| [q131] | reports/plume-l1_findings/52891-sc-low-staking-and-unstaking-immediately-an-amount-little-less-than-the-original-staked-amount.md | LOW | Immunefi (WinSec) | sc low staking and unstaking immediately an amount little less than the original staked amount leaves dust stake amounts in the system&#x20; |
| [q132] | reports/plume-l1_findings/52948-sc-low-jackpot-reward-rejected-at-exact-threshold.md | LOW | Immunefi (Am3nh3l) | sc low jackpot reward rejected at exact threshold |
| [q133] | reports/plume-l1_findings/53038-sc-low-distributeyield-can-be-frontrun-to-sandwich-rewards-we-can-force-ourselves-to-be-the-la.md | LOW | Immunefi (valkvalue) | sc low distributeyield can be frontrun to sandwich rewards we can force ourselves to be the last holder and get unfairly big bonuses |
| [q134] | reports/plume-l1_findings/53056-sc-low-native-withdraw-to-msg-sender-only-non-payable-contract-stakers-cannot-withdraw-permane.md | LOW | Immunefi (tansegv) | sc low native withdraw to msg sender only non payable contract stakers cannot withdraw permanent funds lock&#x20; |
| [q135] | reports/plume-l1_findings/53059-sc-low-reward-rate-checkpoints-are-used-but-are-never-set.md | LOW | Immunefi (a16) | sc low reward rate checkpoints are used but are never set |
| [q136] | reports/plume-l1_findings/53063-sc-low-maxvalidatorpercentage-can-be-used-to-dos-protocol-staking.md | LOW | Immunefi (heeze) | sc low maxvalidatorpercentage can be used to dos protocol staking&#x20; |

## Staking Rewards Plume

**staking-rewards-plume patterns mined from uncited L1 audit reports** - 68 sec-tier findings (0 critical / 61 high / 7 medium) across 68 files from Immunefi (AlertBasilisk56249), Immunefi (BeastBoy), Immunefi (Blobism), Immunefi (Bug82427), Immunefi (GeorgeMichael), Immunefi (IronsideSec).

### Overview

Titles in the references table are verbatim from source reports. Route to the exact report file for full PoC detail. Validation strength: `unassessed` (evidence rows only).

### Detection Patterns

#### High-Signal Grep Seeds
```
- able
- access
- accounting
- accrual
- accrue
- accrued
- accruing
- across
```

### Vulnerability Description

#### Root Cause

The cited reports describe staking rewards plume paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `staking-rewards-plume | staking rewards plume | varies by finding | see references`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `staking-rewards-plume | staking rewards plume | varies by finding | see references | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `staking-rewards-plume | staking rewards plume | varies by finding | see references | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: sc high user can steal rewards** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// sc high user can steal rewards
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: sc high user can steal rewards
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: sc high validator commission can be blocked** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// sc high validator commission can be blocked
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: sc high validator commission can be blocked
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: sc high retroactive reward drain via incomplete reward debt reset** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// sc high retroactive reward drain via incomplete reward debt reset
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: sc high retroactive reward drain via incomplete reward debt reset
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```

### Impact Analysis

#### Technical Impact
- Wrong accounting / reward misallocation / stuck or double-counted funds (fund-loss class rows above)
- State inconsistency after partial failure (see error-handling references)
- Chain halt or node crash from unbounded work (see DoS rows)

#### Business Impact
- User fund loss and withdrawal freezes; validator downtime; consensus/partition risk for client-level bugs.

### Secure Implementation

**Fix 1: [Bound and validate at the entry surface]**
```rust
// ✅ SECURE: explicit bounds + validation before state mutation
fn handler(input: UntrustedInput) -> Result<(), Error> {
    ensure!(input.len() <= T::MaxInput::get(), Error::TooLarge);
    ensure!(is_valid(&input), Error::Invalid);
    state.update_checked(&input)?;
    Ok(())
}
```

**Fix 2: [Aggregate instead of iterate; cap growth]**
```rust
// ✅ SECURE: keep block-time work O(1) and cap attacker growth
fn on_block_end() {
    let aggregate = Aggregates::get();          // maintained incrementally
    distribute(&aggregate);                      // no unbounded iteration
}
fn create_plan(p: Plan) -> Result<(), Error> {
    ensure!(PlansCount::get() < T::MaxPlans::get(), Error::TooManyPlans);
    Ok(())
}
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Entry surface writes state before validating attacker-controlled fields
- Block-time hooks iterate collections whose size is attacker-influenceable
- Multi-step handlers where a mid-step failure leaves earlier writes committed
- Config setters without role checks or bounds
```

#### Audit Checklist
- [ ] Verify every attacker-reachable input is length/bounds-checked before state writes
- [ ] Verify block-time (end-blocker / on_finalize) iteration is O(1) or capped
- [ ] Verify failure paths roll back partial state mutations
- [ ] Cross-check the cited reports' fix status before re-reporting

### Keywords for Search

`able, access, accounting, accrual, accrue, accrued, accruing, across, active, added`

### Related Vulnerabilities

- Sibling entries under the same category folder
