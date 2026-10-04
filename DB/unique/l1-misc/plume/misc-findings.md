---
# Core Classification
protocol: generic
chain: plume
category: misc
vulnerability_type: misc_plume
root_cause_family: see pattern_key

# Pattern Identity
pattern_key: misc-plume | misc plume | varies by finding | see references

# Interaction Scope
interaction_scope: varies
involved_contracts:
  - misc plume

# Attack Vector Details
attack_type: varies
affected_component: misc plume

# Technical Primitives
primitives:
  - able
  - account
  - accounting
  - accumulation
  - after
  - aggregator

# Grep / Hunt-Card Seeds
code_keywords:
  - able
  - account
  - accounting
  - accumulation
  - after
  - aggregator
  - allowance
  - allowances

severity: critical
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
| [p1] | reports/plume-l1_findings/49705-sc-medium-two-vectors-for-unbounded-gas-consumption-due-to-the-normal-raffle-operations.md | MEDIUM | Immunefi (blackgrease) | sc medium two vectors for unbounded gas consumption due to the normal raffle operations |
| [p2] | reports/plume-l1_findings/49787-sc-high-batched-yield-distribution-doesn-t-account-for-transfers-purchases-between-batches-1.md | HIGH | Immunefi (Vanshika) | sc high batched yield distribution doesn t account for transfers purchases between batches |
| [p3] | reports/plume-l1_findings/49787-sc-high-batched-yield-distribution-doesn-t-account-for-transfers-purchases-between-batches.md | HIGH | Immunefi (Vanshika) | sc high batched yield distribution doesn t account for transfers purchases between batches |
| [p4] | reports/plume-l1_findings/49939-sc-high-initial-timestamp-mismatch-might-lead-to-users-being-able-to-spin-twice-in-the-same-da.md | HIGH | Immunefi (a16) | sc high initial timestamp mismatch might lead to users being able to spin twice in the same day |
| [p5] | reports/plume-l1_findings/49963-sc-medium-anyone-can-create-an-arctoken-and-block-the-setpurchasetoken-function.md | MEDIUM | Immunefi (KlosMitSoss) | sc medium anyone can create an arctoken and block the setpurchasetoken function |
| [p6] | reports/plume-l1_findings/50275-sc-high-eligible-user-loses-jackpot.md | HIGH | Immunefi (shadowHunter) | sc high eligible user loses jackpot |
| [p7] | reports/plume-l1_findings/50428-sc-medium-reverting-on-callback-increases-chances-of-winning.md | MEDIUM | Immunefi (Oppi992) | sc medium reverting on callback increases chances of winning |
| [p8] | reports/plume-l1_findings/50507-sc-high-non-atomic-yield-distribution-may-lead-to-theft-of-yield.md | HIGH | Immunefi (a16) | sc high non atomic yield distribution may lead to theft of yield |
| [p9] | reports/plume-l1_findings/50527-sc-high-attacker-can-steal-yield-during-batch-distribution.md | HIGH | Immunefi (wellbyt3) | sc high attacker can steal yield during batch distribution |
| [p10] | reports/plume-l1_findings/50796-sc-high-jackpot-eligibility-uses-stale-streak.md | HIGH | Immunefi (BeastBoy) | sc high jackpot eligibility uses stale streak |
| [p11] | reports/plume-l1_findings/50822-sc-high-deployer-can-cpgrade-arctoken-to-malicious-implementation-and-steal-all-user-funds.md | HIGH | Immunefi (holydevoti0n) | sc high deployer can cpgrade arctoken to malicious implementation and steal all user funds |
| [p12] | reports/plume-l1_findings/50951-sc-high-inconsistent-streak-count-usage-between-jackpot-and-raffle-ticket-calculations.md | HIGH | Immunefi (KlosMitSoss) | sc high inconsistent streak count usage between jackpot and raffle ticket calculations |
| [p13] | reports/plume-l1_findings/51041-sc-high-streak-count-misuse-in-jackpot-eligibility-allows-theft-of-user-funds.md | HIGH | Immunefi (warden) | sc high streak count misuse in jackpot eligibility allows theft of user funds |
| [p14] | reports/plume-l1_findings/51090-sc-high-malicious-user-can-steal-yields-when-arctoken-distributeyieldwithlimit-is-used.md | HIGH | Immunefi (jasonxiale) | sc high malicious user can steal yields when arctoken distributeyieldwithlimit is used&#x20; |
| [p15] | reports/plume-l1_findings/51180-sc-medium-function-is-vulnerable-to-gas-griefing.md | MEDIUM | Immunefi (PotEater) | sc medium function is vulnerable to gas griefing |
| [p16] | reports/plume-l1_findings/51369-sc-high-unbounded-iteration-gas-dos-in-validatetokenforclaim.md | HIGH | Immunefi (BeastBoy) | sc high unbounded iteration gas dos in validatetokenforclaim&#x20; |
| [p17] | reports/plume-l1_findings/51547-sc-medium-approval-race-condition-with-safeapprove-leads-to-transaction-reverts.md | MEDIUM | Immunefi (Tomioka) | sc medium approval race condition with safeapprove leads to transaction reverts |
| [p18] | reports/plume-l1_findings/51801-sc-medium-supra-callback-allows-for-theft-of-gas.md | MEDIUM | Immunefi (arnie) | sc medium supra callback allows for theft of gas |
| [p19] | reports/plume-l1_findings/51847-sc-critical-dos-via-dust-leftover-in-erc-20-approvals.md | CRITICAL | Immunefi (BeastBoy) | sc critical dos via dust leftover in erc 20 approvals |
| [p20] | reports/plume-l1_findings/51878-sc-high-timing-misalignment-between-campaign-days-and-calendar-days-allows-double-spinning-on.md | HIGH | Immunefi (vivekd) | sc high timing misalignment between campaign days and calendar days allows double spinning on high probability jackpot days |
| [p21] | reports/plume-l1_findings/51899-sc-medium-partial-distribution-of-yield-will-fail-if-the-totalefficentive-supply-increases.md | MEDIUM | Immunefi (TeamJosh) | sc medium partial distribution of yield will fail if the totalefficentive supply increases&#x20; |
| [p22] | reports/plume-l1_findings/51992-sc-high-dust-accumulation-in-arctoken-during-yield-distribution.md | HIGH | Immunefi (Killua) | sc high dust accumulation in arctoken during yield distribution&#x20; |
| [p23] | reports/plume-l1_findings/52026-sc-medium-claimall-could-revert-because-of-unbounded-gas-consumptions.md | MEDIUM | Immunefi (WinSec) | sc medium claimall could revert because of unbounded gas consumptions |
| [p24] | reports/plume-l1_findings/52198-sc-high-balance-manipulation-between-batches-leading-to-inflated-payout-and-dos.md | HIGH | Immunefi (farman1094) | sc high balance manipulation between batches leading to inflated payout and dos |
| [p25] | reports/plume-l1_findings/52203-sc-medium-griefing-attack-on-arctokenpurchase-setpurchasetoken-function-via-front-running.md | MEDIUM | Immunefi (thesvn) | sc medium griefing attack on arctokenpurchase setpurchasetoken function via front running |
| [p51] | reports/plume-l1_findings/52254-sc-high-arctoken-theft-beyond-unclaimed-yield-during-distribution.md | HIGH | Immunefi (Blobism) | sc high arctoken theft beyond unclaimed yield during distribution |
| [p52] | reports/plume-l1_findings/52285-sc-high-incorrect-dust-handling-in-yield-distribution-leads-to-permanent-fund-lock.md | HIGH | Immunefi (vivekd) | sc high incorrect dust handling in yield distribution leads to permanent fund lock |
| [p53] | reports/plume-l1_findings/52347-sc-high-improper-handling-of-yield-distribution-state-in-distributeyieldwithlimit-leads-to-rev.md | HIGH | Immunefi (oluwaseyisekoni) | sc high improper handling of yield distribution state in distributeyieldwithlimit leads to revert freezing users yield&#x20; |
| [p54] | reports/plume-l1_findings/52409-sc-high-asymmetric-commission-rounding-creates-systematic-accounting-drift.md | HIGH | Immunefi (spongebob) | sc high asymmetric commission rounding creates systematic accounting drift |
| [p55] | reports/plume-l1_findings/52424-sc-high-there-is-a-retroactive-commission-miscalculation-in-plumerewardlogic.md | HIGH | Immunefi (XDZIBECX) | sc high there is a retroactive commission miscalculation in plumerewardlogic |
| [p56] | reports/plume-l1_findings/52449-sc-high-broken-streaks-still-pass-jackpot-eligibility-in-spin-contract.md | HIGH | Immunefi (farman1094) | sc high broken streaks still pass jackpot eligibility in spin contract |
| [p57] | reports/plume-l1_findings/52464-sc-high-commission-rounding-mismatch-under-payment-bug.md | HIGH | Immunefi (BeastBoy) | sc high commission rounding mismatch under payment bug |
| [p58] | reports/plume-l1_findings/52517-sc-high-missing-point-in-time-snapshot-in-batched-yield-distribution-enables-double-claims-and.md | HIGH | Immunefi (vivekd) | sc high missing point in time snapshot in batched yield distribution enables double claims and permanent fund lock |
| [p59] | reports/plume-l1_findings/52560-sc-high-incorrect-current-streak-used-when-calculating-whether-the-jackpot-should-be-awarded-o.md | HIGH | Immunefi (swarun) | sc high incorrect current streak used when calculating whether the jackpot should be awarded or not |
| [p60] | reports/plume-l1_findings/52576-sc-high-flaw-in-raffle-determinereward-in-jackpot-prize-calculation-after-week-12.md | HIGH | Immunefi (Paludo0x) | sc high flaw in raffle determinereward in jackpot prize calculation after week 12 |
| [p61] | reports/plume-l1_findings/52601-sc-high-in-spin-handlerandomness-jackpot-eligibility-uses-outdated-streakcount-instead-of-upda.md | HIGH | Immunefi (Paludo0x) | sc high in spin handlerandomness jackpot eligibility uses outdated streakcount instead of updated streak |
| [p62] | reports/plume-l1_findings/52620-sc-medium-permanently-dos-to-arctokenpurchase-contract.md | MEDIUM | Immunefi (IronsideSec) | sc medium permanently dos to arctokenpurchase contract |
| [p63] | reports/plume-l1_findings/52634-sc-high-batch-yield-distribution-has-a-mathematical-flaw-that-enables-economic-manipulation.md | HIGH | Immunefi (spongebob) | sc high batch yield distribution has a mathematical flaw that enables economic manipulation |
| [p64] | reports/plume-l1_findings/52680-sc-high-holders-length-changing-when-distributing-limit-with-limit-could-lead-to-case-where-ne.md | HIGH | Immunefi (warden) | sc high holders length changing when distributing limit with limit could lead to case where new holders unfairly claim yield and yield is permanently  |
| [p65] | reports/plume-l1_findings/52690-sc-medium-dos-of-smart-contracts-on-bridging-functions.md | MEDIUM | Immunefi (funkornaut) | sc medium dos of smart contracts on bridging functions |
| [p66] | reports/plume-l1_findings/52787-sc-high-batched-yield-distribution-rounding-in-arctoken-permanently-freezes-unclaimed-funds-an.md | HIGH | Immunefi (manvi) | sc high batched yield distribution rounding in arctoken permanently freezes unclaimed funds and misreports payouts |
| [p67] | reports/plume-l1_findings/52803-sc-high-canrecoverfromcooldown-is-inconsistent-when-slash-and-cooldown-maturity-occur-in-the-s.md | HIGH | Immunefi (Paludo0x) | sc high canrecoverfromcooldown is inconsistent when slash and cooldown maturity occur in the same block |
| [p68] | reports/plume-l1_findings/52845-sc-high-distributeyieldwithlimit-lacks-snapshot-between-batches-allowing-state-changes-to-brea.md | HIGH | Immunefi (warden) | sc high distributeyieldwithlimit lacks snapshot between batches allowing state changes to break distribution and lock yield |
| [p69] | reports/plume-l1_findings/52847-sc-high-no-function-to-recover-the-remained-yield-by-distributeyieldwithlimit.md | HIGH | Immunefi (ubl4nk) | sc high no function to recover the remained yield by distributeyieldwithlimit&#x20; |
| [p70] | reports/plume-l1_findings/52925-sc-medium-usdt-like-approval-hygiene-can-block-subsequent-operations-after-partial-fill-leaves.md | MEDIUM | Immunefi (LoopGhost007) | sc medium usdt like approval hygiene can block subsequent operations after partial fill leaves non zero allowance |
| [p71] | reports/plume-l1_findings/52956-sc-high-state-inconsistency-in-batched-yield-distribution-leads-to-direct-theft-of-user-funds.md | HIGH | Immunefi (Nuesayo) | sc high state inconsistency in batched yield distribution leads to direct theft of user funds and protocol insolvency |
| [p72] | reports/plume-l1_findings/52961-sc-high-theft-of-yield-from-the-distributor.md | HIGH | Immunefi (heeze) | sc high theft of yield from the distributor&#x20; |
| [p73] | reports/plume-l1_findings/52982-sc-medium-non-standard-erc20-approvals-usdt-like-cause-repeat-call-failures-after-partial-fill.md | MEDIUM | Immunefi (RevertLord) | sc medium non standard erc20 approvals usdt like cause repeat call failures after partial fills |
| [p74] | reports/plume-l1_findings/52986-sc-high-jackpot-check-uses-previous-streakcount-instead-of-current-computed-streak-denying-jac.md | HIGH | Immunefi (daxun) | sc high jackpot check uses previous streakcount instead of current computed streak denying jackpot on first eligible day |
| [p75] | reports/plume-l1_findings/53011-sc-critical-uncleaned-partial-approval-consumption-in-dex-aggregator-integration-leads-to-perm.md | CRITICAL | Immunefi (vivekd) | sc critical uncleaned partial approval consumption in dex aggregator integration leads to permanent dos |
| [p76] | reports/plume-l1_findings/53035-sc-medium-share-lock-applied-to-wrapper-instead-of-end-user-breaks-transfers-or-bypasses-lock.md | MEDIUM | Immunefi (Afriauditor) | sc medium share lock applied to wrapper instead of end user breaks transfers or bypasses lock |
| [p77] | reports/plume-l1_findings/53043-sc-high-handlerandomness-doesn-t-properly-account-for-current-streak-which-could-result-in-the.md | HIGH | Immunefi (valkvalue) | sc high handlerandomness doesn t properly account for current streak which could result in the user spinning losing a jackpot |
| [p78] | reports/plume-l1_findings/53047-sc-high-the-jackpot-eligibility-check-uses-stale-storage-data-instead-of-the-freshly-calculate.md | HIGH | Immunefi (warden) | sc high the jackpot eligibility check uses stale storage data instead of the freshly calculated streak&#x20; |
| [p79] | reports/plume-l1_findings/53048-sc-medium-approval-logic-can-break-on-non-standard-erc-20s-usdt-style-and-leave-allowances-loo.md | MEDIUM | Immunefi (jpmendes) | sc medium approval logic can break on non standard erc 20s usdt style and leave allowances loose |
| [p80] | reports/plume-l1_findings/53077-sc-high-permanent-fund-lock-due-to-flawed-remainder-logic-in-distributeyield.md | HIGH | Immunefi (Alem) | sc high permanent fund lock due to flawed remainder logic in distributeyield |
| [w81] | reports/plume-l1_findings/49798-sc-insight-invalid-holder-set-initialization-bypasses-modular-restrictions-corrupting-yield-di.md | HIGH | Immunefi (warden) | sc insight invalid holder set initialization bypasses modular restrictions corrupting yield distribution |
| [w82] | reports/plume-l1_findings/49941-sc-low-permanent-freezing-of-yield-tokens-due-to-flawed-check-in-distribution-logic.md | MEDIUM | Immunefi (warden) | sc low permanent freezing of yield tokens due to flawed check in distribution logic |
| [w83] | reports/plume-l1_findings/50713-sc-high-deployer-s-default-admin-role-enables-self-grant-of-upgrader-role-bypassing-implementa.md | HIGH | Immunefi (warden) | sc high deployer s default admin role enables self grant of upgrader role bypassing implementation whitelist |
| [w84] | reports/plume-l1_findings/52027-sc-low-whitelistrestrictions-sol-mint-burn-operations-blocked-when-transfers-disabled.md | MEDIUM | Immunefi (warden) | sc low whitelistrestrictions sol mint burn operations blocked when transfers disabled |
| [w85] | reports/plume-l1_findings/52178-sc-critical-user-will-lose-the-unspent-amount-when-executing-partial-swaps-via-okxrouter.md | CRITICAL | Immunefi (warden) | sc critical user will lose the unspent amount when executing partial swaps via okxrouter |
| [w86] | reports/plume-l1_findings/52218-sc-high-creator-retains-default-admin-role-allowing-bypass-of-upgrade-restrictions.md | HIGH | Immunefi (warden) | sc high creator retains default admin role allowing bypass of upgrade restrictions |
| [w87] | reports/plume-l1_findings/52339-sc-low-loss-of-daily-streak-and-jackpot-eligibility-due-to-supra-generator-callback-delay-and.md | HIGH | Immunefi (warden) | sc low loss of daily streak and jackpot eligibility due to supra generator callback delay and on callback time usage in spin sol&#x20; |
| [w88] | reports/plume-l1_findings/52499-sc-high-arctoken-factory-s-admin-cannot-upgrade-an-arctoken.md | HIGH | Immunefi (warden) | sc high arctoken factory s admin cannot upgrade an arctoken |
| [w89] | reports/plume-l1_findings/52979-sc-low-whitelistrestrictions-unintentionally-disables-mint-and-burn-when-transfers-are-restric.md | CRITICAL | Immunefi (warden) | sc low whitelistrestrictions unintentionally disables mint and burn when transfers are restricted |
| [w90] | reports/plume-l1_findings/53022-sc-critical-funds-are-not-properly-refunded-to-user-which-calls-for-swap-on-the-dex-aggregator.md | CRITICAL | Immunefi (warden) | sc critical funds are not properly refunded to user which calls for swap on the dex aggregator |
| [w91] | reports/plume-l1_findings/53034-sc-high-arctokenfactory-doesn-t-properly-handle-role-management-which-allows-users-to-arbitrar.md | HIGH | Immunefi (warden) | sc high arctokenfactory doesn t properly handle role management which allows users to arbitrary upgrade their arctoken s implementation |
| [q92] | reports/plume-l1_findings/49626-sc-insight-modulo-bias-in-winner-selection-in-raffle.md | INFO | Immunefi (Opzteam) | sc insight modulo bias in winner selection in raffle |
| [q93] | reports/plume-l1_findings/49639-sc-insight-gas-inefficiency-in-loop-storage-reads-processmaturedcooldowns.md | INFO | Immunefi (Opzteam) | sc insight gas inefficiency in loop storage reads processmaturedcooldowns |
| [q94] | reports/plume-l1_findings/49647-sc-low-pausable-functions-are-not-exposed.md | LOW | Immunefi (rajkaur) | sc low pausable functions are not exposed |
| [q95] | reports/plume-l1_findings/49738-sc-insight-active-users-in-prize-pool-loose-invested-raffle-tickets-when-raffle-removeprize-is.md | INFO | Immunefi (blackgrease) | sc insight active users in prize pool loose invested raffle tickets when raffle removeprize is called&#x20; |
| [q96] | reports/plume-l1_findings/49768-sc-insight-missing-input-validation-in-raffle-editprize-breaks-functionality.md | INFO | Immunefi (blackgrease) | sc insight missing input validation in raffle editprize breaks functionality |
| [q97] | reports/plume-l1_findings/49800-sc-insight-yield-distribution-could-encounter-an-unexpected-revert.md | INFO | Immunefi (a16) | sc insight yield distribution could encounter an unexpected revert |
| [q98] | reports/plume-l1_findings/49835-sc-insight-dex-aggregator-unused-eth-loss.md | INFO | Immunefi (Blobism) | sc insight dex aggregator unused eth loss |
| [q99] | reports/plume-l1_findings/49868-sc-insight-raffle-sol-does-not-enforce-prize-endtimestamp-allowing-user-and-admin-interactions.md | INFO | Immunefi (blackgrease) | sc insight raffle sol does not enforce prize endtimestamp allowing user and admin interactions with expired prizes |
| [q100] | reports/plume-l1_findings/49876-sc-insight-lack-of-refund-on-admin-canceled-spin-requests-leads-to-permanent-loss-of-funds.md | INFO | Immunefi (vargalove) | sc insight lack of refund on admin canceled spin requests leads to permanent loss of funds |
| [q101] | reports/plume-l1_findings/49893-sc-insight-raffle-sol-implementation-logic-allows-direct-plume-transfers-but-has-no-withdraw-l.md | INFO | Immunefi (blackgrease) | sc insight raffle sol implementation logic allows direct plume transfers but has no withdraw locking funds permanently |
| [q102] | reports/plume-l1_findings/49915-sc-low-misleading-event-emission-in-createwhitelistrestrictions-function-in-restrictionsfactor.md | LOW | Immunefi (AasifUsmani) | sc low misleading event emission in createwhitelistrestrictions function in restrictionsfactory contract |
| [q103] | reports/plume-l1_findings/49932-sc-insight-there-are-five-separate-but-similar-implementations-of-a-binary-search-that-can-be.md | INFO | Immunefi (Vanshika) | sc insight there are five separate but similar implementations of a binary search that can be condensed into one function |
| [q104] | reports/plume-l1_findings/49954-sc-insight-raffle-editprizes-lacks-logic-to-make-prizes-immutable-once-winner-selection-starts.md | INFO | Immunefi (blackgrease) | sc insight raffle editprizes lacks logic to make prizes immutable once winner selection starts or users join breaking user trust&#x20; |
| [q105] | reports/plume-l1_findings/50022-sc-low-missing-admin-pause-unpause-functions-in-tellerwithmultiassetsupportpredicateproxy-cont.md | LOW | Immunefi (honey0x0) | sc low missing admin pause unpause functions in tellerwithmultiassetsupportpredicateproxy contract |
| [q106] | reports/plume-l1_findings/50060-sc-insight-scattered-module-processing-pattern-in-arctoken-update-function.md | INFO | Immunefi (AasifUsmani) | sc insight scattered module processing pattern in arctoken update function |
| [q107] | reports/plume-l1_findings/50120-sc-low-arctokens-cannot-be-burned-or-minted-when-transfers-are-restricted.md | LOW | Immunefi (KlosMitSoss) | sc low arctokens cannot be burned or minted when transfers are restricted |
| [q108] | reports/plume-l1_findings/50187-sc-insight-yieldblacklistrestrictions-uses-slot-0-instead-of-unstructured-storage-risking-slot.md | INFO | Immunefi (Paludo0x) | sc insight yieldblacklistrestrictions uses slot 0 instead of unstructured storage risking slot collision |
| [q109] | reports/plume-l1_findings/50195-sc-low-unfair-yield-distribution-due-to-remainder-allocation-to-last-holder.md | LOW | Immunefi (AasifUsmani) | sc low unfair yield distribution due to remainder allocation to last holder |
| [q110] | reports/plume-l1_findings/50225-sc-low-user-can-bypass-minstakeamount-checking.md | LOW | Immunefi (New5paceXyz) | sc low user can bypass minstakeamount checking&#x20; |
| [q111] | reports/plume-l1_findings/50284-sc-insight-incorrect-erc7201-storage-implementation-in-core-factory-contracts.md | INFO | Immunefi (AasifUsmani) | sc insight incorrect erc7201 storage implementation in core factory contracts |
| [q112] | reports/plume-l1_findings/50343-sc-low-cooldown-reset-vulnerability.md | LOW | Immunefi (ciphermalware) | sc low cooldown reset vulnerability |
| [q113] | reports/plume-l1_findings/50380-sc-insight-redundant-use-of-allowedimplementations-mapping-in-factory-contracts-createtoken-an.md | INFO | Immunefi (AasifUsmani) | sc insight redundant use of allowedimplementations mapping in factory contracts createtoken and createwhitelistrestrictions in arctokenfactory and res |
| [q114] | reports/plume-l1_findings/50392-sc-insight-phantom-commission-burn.md | INFO | Immunefi (BeastBoy) | sc insight phantom commission burn |
| [q115] | reports/plume-l1_findings/50393-sc-insight-unused-admin-state-variable-increases-deployment-and-storage-costs.md | INFO | Immunefi (Lock0down) | sc insight unused admin state variable increases deployment and storage costs&#x20; |
| [q116] | reports/plume-l1_findings/50399-sc-low-broken-access-control-in-particular-contract-functions-due-lack-of-pause-unpause-functi.md | LOW | Immunefi (KKam86) | sc low broken access control in particular contract functions due lack of pause unpause functionality |
| [q117] | reports/plume-l1_findings/50402-sc-low-single-rate-assumption-ignores-checkpoints-in-slashed-case.md | LOW | Immunefi (BeastBoy) | sc low single rate assumption ignores checkpoints in slashed case&#x20; |
| [q118] | reports/plume-l1_findings/50415-sc-low-getmaxnumberoftokens-returns-wrong-value-when-arctokens-are-withdrawn.md | LOW | Immunefi (KlosMitSoss) | sc low getmaxnumberoftokens returns wrong value when arctokens are withdrawn |
| [q119] | reports/plume-l1_findings/50470-sc-insight-inefficient-design-in-distributeyieldwithlimit-arctoken-creates-unnecessary-gas-con.md | INFO | Immunefi (AasifUsmani) | sc insight inefficient design in distributeyieldwithlimit arctoken creates unnecessary gas consumption |
| [q120] | reports/plume-l1_findings/50487-sc-low-cross-campaign-jackpot-denial-due-to-state-pollution.md | LOW | Immunefi (IronsideSec) | sc low cross campaign jackpot denial due to state pollution |
| [q121] | reports/plume-l1_findings/50493-sc-low-immutable-proxy-implementation-mapping-in-restrictionsfactory-breaks-upgrade-logic.md | LOW | Immunefi (Paludo0x) | sc low immutable proxy implementation mapping in restrictionsfactory breaks upgrade logic |
| [q122] | reports/plume-l1_findings/50624-sc-low-there-is-a-missing-emergency-pause-in-predicate-proxy.md | LOW | Immunefi (XDZIBECX) | sc low there is a missing emergency pause in predicate proxy&#x20; |
| [q123] | reports/plume-l1_findings/50632-sc-insight-critical-timestamp-parsing-bug-in-getyear-of-datetime-contract.md | INFO | Immunefi (ubl4nk) | sc insight critical timestamp parsing bug in getyear of datetime contract |
| [q124] | reports/plume-l1_findings/50677-sc-insight-redundant-code-in-dexaggregatorwrapperwithpredicateproxy-impairs-readability-and-po.md | INFO | Immunefi (KKam86) | sc insight redundant code in dexaggregatorwrapperwithpredicateproxy impairs readability and potentially increases gas costs |
| [q125] | reports/plume-l1_findings/50694-sc-low-spins-occuring-close-to-midnight-lead-to-users-streaks-being-unfairly-broken-due-to-vrf.md | LOW | Immunefi (heavyw8t) | sc low spins occuring close to midnight lead to users streaks being unfairly broken due to vrf callback delay |
| [q126] | reports/plume-l1_findings/50721-sc-low-winners-cannot-claim-prizes-until-all-winners-have-been-drawn-in-raffle-claimprize.md | LOW | Immunefi (blackgrease) | sc low winners cannot claim prizes until all winners have been drawn in raffle claimprize&#x20; |
| [q127] | reports/plume-l1_findings/50839-sc-low-last-holder-always-gets-more-yield.md | LOW | Immunefi (funkornaut) | sc low last holder always gets more yield |
| [q128] | reports/plume-l1_findings/50887-sc-insight-arcotokenpurchase-purchasemade-event-mislabels-payment-amount-as-pricepaid-instead.md | INFO | Immunefi (Paludo0x) | sc insight arcotokenpurchase purchasemade event mislabels payment amount as pricepaid instead of unit price |
| [q129] | reports/plume-l1_findings/50889-sc-low-arctokenpurchase-withdrawunsoldarctokens-fails-to-reduce-totalamountforsale-leaving-ava.md | LOW | Immunefi (Paludo0x) | sc low arctokenpurchase withdrawunsoldarctokens fails to reduce totalamountforsale leaving availability counters wrong |
| [q130] | reports/plume-l1_findings/50949-sc-insight-no-check-if-raffle-actually-has-enough-funds.md | INFO | Immunefi (PotEater) | sc insight no check if raffle actually has enough funds |
| [q131] | reports/plume-l1_findings/50973-sc-insight-incorrect-parameter-type-in-setjackpotprobabilities.md | INFO | Immunefi (Paludo0x) | sc insight incorrect parameter type in setjackpotprobabilities |
| [q132] | reports/plume-l1_findings/50977-sc-low-tellerwithmultiassetsupportpredicateproxy-contract-cannot-be-emergency-paused.md | LOW | Immunefi (warden) | sc low tellerwithmultiassetsupportpredicateproxy contract cannot be emergency paused&#x20; |
| [q133] | reports/plume-l1_findings/51070-sc-low-winning-raffle-ticket-can-be-re-used-to-maintain-unfair-advantage-over-other-players-in.md | LOW | Immunefi (blackgrease) | sc low winning raffle ticket can be re used to maintain unfair advantage over other players in raffle&#x20; |
| [q134] | reports/plume-l1_findings/51100-sc-insight-gas-inefficiency-in-prize-removal-logic.md | INFO | Immunefi (AasifUsmani) | sc insight gas inefficiency in prize removal logic |
| [q135] | reports/plume-l1_findings/51122-sc-low-arctokenpurchase-enabletoken-can-reset-the-amountsold-to-0.md | LOW | Immunefi (pks271) | sc low arctokenpurchase enabletoken can reset the amountsold to 0 |
| [q136] | reports/plume-l1_findings/51129-sc-low-boringvault-proxies-do-not-support-smart-contract-wallets.md | LOW | Immunefi (holydevoti0n) | sc low boringvault proxies do not support smart contract wallets |
| [q137] | reports/plume-l1_findings/51132-sc-low-tellerwithmultiassetsupportpredicateproxy-cannot-be-paused-unpaused.md | LOW | Immunefi (holydevoti0n) | sc low tellerwithmultiassetsupportpredicateproxy cannot be paused unpaused |
| [q138] | reports/plume-l1_findings/51159-sc-insight-high-gas-iterative-date-calculations-in-datetime-sol.md | INFO | Immunefi (zbugs) | sc insight high gas iterative date calculations in datetime sol |
| [q139] | reports/plume-l1_findings/51162-sc-low-missing-pause-control-implementation-in-tellerwithmultiassetsupportpredicateproxy.md | LOW | Immunefi (TeamJosh) | sc low missing pause control implementation in tellerwithmultiassetsupportpredicateproxy |
| [q140] | reports/plume-l1_findings/51286-sc-low-event-restrictionscreated-uses-wrong-owner.md | LOW | Immunefi (p1ranh4) | sc low event restrictionscreated uses wrong owner |
| [q141] | reports/plume-l1_findings/51296-sc-low-arctokenpurchase-withdrawal-breaks-view-functions.md | LOW | Immunefi (funkornaut) | sc low arctokenpurchase withdrawal breaks view functions |
| [q142] | reports/plume-l1_findings/51320-sc-low-malicious-teller-parameter-allow-event-data-manipulation.md | LOW | Immunefi (holydevoti0n) | sc low malicious teller parameter allow event data manipulation |
| [q143] | reports/plume-l1_findings/51391-sc-low-enabletoken-function-overwrites-amountsold-to-zero-causing-permanent-loss-of-sales-hist.md | LOW | Immunefi (vivekd) | sc low enabletoken function overwrites amountsold to zero causing permanent loss of sales history |
| [q144] | reports/plume-l1_findings/51493-sc-insight-misleading-view-function-documentation.md | INFO | Immunefi (heavyw8t) | sc insight misleading view function documentation |
| [q145] | reports/plume-l1_findings/51502-sc-low-enabling-transfer-restrictions-permanently-blocks-minting-and-burning.md | LOW | Immunefi (rajaroy43) | sc low enabling transfer restrictions permanently blocks minting and burning |
| [q146] | reports/plume-l1_findings/51525-sc-low-unfair-yield-distribution-to-last-holder-due-to-flawed-dust-handling.md | LOW | Immunefi (rajaroy43) | sc low unfair yield distribution to last holder due to flawed dust handling |
| [q147] | reports/plume-l1_findings/51567-sc-low-contract-cannot-be-paused-missing-public-pause-and-unpause-functions.md | LOW | Immunefi (MMophule) | sc low contract cannot be paused missing public pause and unpause functions |
| [q148] | reports/plume-l1_findings/51596-sc-low-unsafe-uint256-to-uint8-downcast-causes-integer-overflow-leading-to-unauthorized-jackpo.md | LOW | Immunefi (vivekd) | sc low unsafe uint256 to uint8 downcast causes integer overflow leading to unauthorized jackpot payouts after week 255 |
| [q149] | reports/plume-l1_findings/51651-sc-insight-redundant-array-access-in-removestakerfromvalidator.md | INFO | Immunefi (AasifUsmani) | sc insight redundant array access in removestakerfromvalidator |
| [q150] | reports/plume-l1_findings/51707-sc-insight-gas-inefficiency-due-to-redundant-validatevalidatorexists-modifier-in-requestcommis.md | INFO | Immunefi (rilwan99) | sc insight gas inefficiency due to redundant validatevalidatorexists modifier in requestcommissionclaim&#x20; |
| [q151] | reports/plume-l1_findings/51712-sc-insight-yield-distribution-will-revert-if-global-module-doesn-t-implement-iyieldrestriction.md | INFO | Immunefi (WinSec) | sc insight yield distribution will revert if global module doesn t implement iyieldrestrictions |
| [q152] | reports/plume-l1_findings/51771-sc-low-unsafe-downcast-of-uint256-to-uint8-will-lead-to-silent-overflow.md | LOW | Immunefi (vielite) | sc low unsafe downcast of uint256 to uint8 will lead to silent overflow |
| [q153] | reports/plume-l1_findings/51814-sc-insight-checkpoint-cumulativeindex-returned-in-the-getrewardratecheckpoint-function-will-be.md | INFO | Immunefi (oxrex) | sc insight checkpoint cumulativeindex returned in the getrewardratecheckpoint function will be zero |
| [q154] | reports/plume-l1_findings/51816-sc-low-yield-distribution-can-be-front-run-to-steal-rounding-remainder-as-last-holder.md | LOW | Immunefi (KlosMitSoss) | sc low yield distribution can be front run to steal rounding remainder as last holder |
| [q155] | reports/plume-l1_findings/51836-sc-low-contract-cannot-be-paused-despite-inheriting-pausable.md | LOW | Immunefi (Finlooz4) | sc low contract cannot be paused despite inheriting pausable |
| [q156] | reports/plume-l1_findings/51863-sc-low-lack-of-winning-ticket-removal-in-handlewinnerselection-leads-to-unfair-prize-distribut.md | LOW | Immunefi (vivekd) | sc low lack of winning ticket removal in handlewinnerselection leads to unfair prize distribution and economic exploitation |
| [q157] | reports/plume-l1_findings/51882-sc-low-unnecessary-claiming-restriction-in-raffle-contract-prevents-winners-from-claiming-priz.md | LOW | Immunefi (vivekd) | sc low unnecessary claiming restriction in raffle contract prevents winners from claiming prizes until all winners are drawn |
| [q158] | reports/plume-l1_findings/51918-sc-insight-redundant-zero-address-checks-for-router-address.md | INFO | Immunefi (warden) | sc insight redundant zero address checks for router address&#x20; |
| [q159] | reports/plume-l1_findings/51920-sc-insight-unnecessary-second-hand-of-if-check-in-calculaterewardswithcheckpointsview.md | INFO | Immunefi (oxrex) | sc insight unnecessary second hand of if check in calculaterewardswithcheckpointsview&#x20; |
| [q160] | reports/plume-l1_findings/51929-sc-low-deactivating-istransferallowed-indirectly-doses-minting-burning-functionality.md | LOW | Immunefi (Am3nh3l) | sc low deactivating istransferallowed indirectly doses minting burning functionality |
| [q161] | reports/plume-l1_findings/51951-sc-low-a-global-blocking-check-in-claimprize-prevents-individual-winner-claims-until-all-winne.md | LOW | Immunefi (XDZIBECX) | sc low a global blocking check in claimprize prevents individual winner claims until all winners are drawn |
| [q162] | reports/plume-l1_findings/51979-sc-low-getaccruedcommission-returns-outdated-accrued-commission.md | LOW | Immunefi (holydevoti0n) | sc low getaccruedcommission returns outdated accrued commission |
| [q163] | reports/plume-l1_findings/51989-sc-low-event-restrictionscreated-always-emits-msg-sender-as-owner.md | LOW | Immunefi (Killua) | sc low event restrictionscreated always emits msg sender as owner&#x20; |
| [q164] | reports/plume-l1_findings/52041-sc-low-in-arctoken-attacker-can-reposition-to-last-holder-and-capture-entire-yield-remainder.md | LOW | Immunefi (Paludo0x) | sc low in arctoken attacker can reposition to last holder and capture entire yield remainder |
| [q165] | reports/plume-l1_findings/52137-sc-insight-silent-override-of-non-global-module-implementation-causes-stored-state-and-event-l.md | INFO | Immunefi (Sharky) | sc insight silent override of non global module implementation causes stored state and event log inconsistency |
| [q166] | reports/plume-l1_findings/52202-sc-low-failure-to-invalidate-winning-tickets-allows-multiple-wins-from-single-entry.md | LOW | Immunefi (Sharky) | sc low failure to invalidate winning tickets allows multiple wins from single entry |
| [q167] | reports/plume-l1_findings/52221-sc-insight-hardcoded-supra-subscription-wallet-can-freeze-spin.md | INFO | Immunefi (holydevoti0n) | sc insight hardcoded supra subscription wallet can freeze spin |
| [q168] | reports/plume-l1_findings/52241-sc-low-unexposed-pauseable-functionality.md | LOW | Immunefi (funkornaut) | sc low unexposed pauseable functionality |
| [q169] | reports/plume-l1_findings/52277-sc-low-race-condition-in-streak-calculation-leads-to-unfair-streak-reset-for-users-spinning-ne.md | LOW | Immunefi (Orionn) | sc low race condition in streak calculation leads to unfair streak reset for users spinning near utc day change |
| [q170] | reports/plume-l1_findings/52303-sc-insight-incorrect-yield-distribution-event-emission.md | INFO | Immunefi (TheCarrot) | sc insight incorrect yield distribution event emission |
| [q171] | reports/plume-l1_findings/52327-sc-low-unfair-yield-distribution-due-to-last-holder-bias.md | LOW | Immunefi (ZeroXGondar) | sc low unfair yield distribution due to last holder bias |
| [q172] | reports/plume-l1_findings/52393-sc-low-burns-blocked-by-both-sides-whitelist-with-zero-address-exclusion-when-restrictions-are.md | LOW | Immunefi (Khay3) | sc low burns blocked by both sides whitelist with zero address exclusion when restrictions are enabled |
| [q173] | reports/plume-l1_findings/52436-sc-low-getaccruedcommission-could-return-an-inaccurate-value.md | LOW | Immunefi (a16) | sc low getaccruedcommission could return an inaccurate value |
| [q174] | reports/plume-l1_findings/52468-sc-insight-dos-in-batch-yield-distribution-due-to-cross-batch-state-inconsistency.md | INFO | Immunefi (flora) | sc insight dos in batch yield distribution due to cross batch state inconsistency |
| [q175] | reports/plume-l1_findings/52589-sc-low-in-distribute-yield-function-if-there-are-no-legitimate-users-i-e-no-restricted-users-t.md | LOW | Immunefi (swarun) | sc low in distribute yield function if there are no legitimate users i e no restricted users the funds will remain stuck |
| [q176] | reports/plume-l1_findings/52706-sc-low-multi-quantity-prize-claims-revert-until-all-winners-are-drawn-freezing-early-winners.md | LOW | Immunefi (wellbyt3) | sc low multi quantity prize claims revert until all winners are drawn freezing early winners |
| [q177] | reports/plume-l1_findings/52710-sc-low-mint-burn-are-blocked-when-whitelist-restrictions-are-enabled.md | LOW | Immunefi (IronsideSec) | sc low mint burn are blocked when whitelist restrictions are enabled |
| [q178] | reports/plume-l1_findings/52794-sc-low-remainingforsale-not-updated-after-withdrawunsoldarctokens-will-cause-following-buy-rev.md | LOW | Immunefi (maggie) | sc low remainingforsale not updated after withdrawunsoldarctokens will cause following buy revert |
| [q179] | reports/plume-l1_findings/52796-sc-low-whitelist-restriction-in-arctoken-blocks-all-minting-and-burning.md | LOW | Immunefi (ZeroExRes) | sc low whitelist restriction in arctoken blocks all minting and burning |
| [q180] | reports/plume-l1_findings/52843-sc-low-the-zero-address-cannot-be-whitelisted-which-means-during-restrictions-minting-and-burn.md | LOW | Immunefi (heeze) | sc low the zero address cannot be whitelisted which means during restrictions minting and burning cannot work |
| [q181] | reports/plume-l1_findings/52870-sc-low-cooldown-extension-logic-may-lead-to-locked-funds.md | LOW | Immunefi (EFCCWEB3) | sc low cooldown extension logic may lead to locked funds |
| [q182] | reports/plume-l1_findings/52896-sc-low-pause-gate-is-present-but-no-way-to-pause.md | LOW | Immunefi (hulkvision) | sc low pause gate is present but no way to pause |
| [q183] | reports/plume-l1_findings/52901-sc-low-wrapped-week-index-can-mis-price-jackpot-table-after-long-uptime.md | LOW | Immunefi (spongebob) | sc low wrapped week index can mis price jackpot table after long uptime |
| [q184] | reports/plume-l1_findings/52915-sc-low-yield-are-transferred-before-eligibility-check-potentially-leading-to-freezing-of-funds.md | LOW | Immunefi (spongebob) | sc low yield are transferred before eligibility check potentially leading to freezing of funds |
| [q185] | reports/plume-l1_findings/52918-sc-insight-redundant-check-for-allwinnersdrawn-error.md | INFO | Immunefi (Finlooz4) | sc insight redundant check for allwinnersdrawn error |
| [q186] | reports/plume-l1_findings/52937-sc-insight-redundant-raffle-ticket-balance-check.md | INFO | Immunefi (Am3nh3l) | sc insight redundant raffle ticket balance check |
| [q187] | reports/plume-l1_findings/52960-sc-insight-incosistent-withdrawable-amount-calculations.md | INFO | Immunefi (holydevoti0n) | sc insight incosistent withdrawable amount calculations |
| [q188] | reports/plume-l1_findings/52976-sc-low-turning-on-transfer-restriction-permanently-blocks-minting-and-burning.md | LOW | Immunefi (warden) | sc low turning on transfer restriction permanently blocks minting and burning |
| [q189] | reports/plume-l1_findings/52990-sc-low-uint8-truncation-and-missing-cap-on-week-index-can-return-wrong-zero-jackpot-amounts-lo.md | LOW | Immunefi (daxun) | sc low uint8 truncation and missing cap on week index can return wrong zero jackpot amounts low contract fails to deliver promised returns&#x20; |
| [q190] | reports/plume-l1_findings/53015-sc-low-raffle-does-not-invalidate-used-tickets-breaking-fairness.md | LOW | Immunefi (warden) | sc low raffle does not invalidate used tickets breaking fairness |
| [q191] | reports/plume-l1_findings/53069-sc-low-dynamic-cooldown-interval-changes-cause-unexpected-fund-lockup-extensions.md | LOW | Immunefi (Outliers) | sc low dynamic cooldown interval changes cause unexpected fund lockup extensions |
| [q192] | reports/plume-l1_findings/53071-sc-insight-okxhelper-function-incompatible-with-the-uniswap-v3-swap-to-with-permit-selector.md | INFO | Immunefi (frolic) | sc insight okxhelper function incompatible with the uniswap v3 swap to with permit selector&#x20; |

## Misc Plume

**misc-plume patterns mined from uncited L1 audit reports** - 55 sec-tier findings (2 critical / 38 high / 15 medium) across 55 files from Immunefi (Afriauditor), Immunefi (Alem), Immunefi (BeastBoy), Immunefi (Blobism), Immunefi (IronsideSec), Immunefi (Killua).

### Overview

Titles in the references table are verbatim from source reports. Route to the exact report file for full PoC detail. Validation strength: `unassessed` (evidence rows only).

### Detection Patterns

#### High-Signal Grep Seeds
```
- able
- account
- accounting
- accumulation
- after
- aggregator
- allowance
- allowances
```

### Vulnerability Description

#### Root Cause

The cited reports describe misc plume paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `misc-plume | misc plume | varies by finding | see references`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `misc-plume | misc plume | varies by finding | see references | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `misc-plume | misc plume | varies by finding | see references | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: sc critical dos via dust leftover in erc 20 approvals** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// sc critical dos via dust leftover in erc 20 approvals
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: sc critical dos via dust leftover in erc 20 approvals
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: sc critical uncleaned partial approval consumption in dex aggregator integration leads to permanent dos** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// sc critical uncleaned partial approval consumption in dex aggregator integration leads to permanent dos
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: sc critical uncleaned partial approval consumption in dex aggregator integration leads to permanent 
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: sc high batched yield distribution doesn t account for transfers purchases between batches** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// sc high batched yield distribution doesn t account for transfers purchases between batches
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: sc high batched yield distribution doesn t account for transfers purchases between batches
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

`able, account, accounting, accumulation, after, aggregator, allowance, allowances, allowing, allows`

### Related Vulnerabilities

- Sibling entries under the same category folder
