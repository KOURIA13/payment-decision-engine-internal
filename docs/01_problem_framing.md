# Problem Framing: PSD3 / PSR as a Product Redesign

> A strategic memo on why treating PSD3 as a compliance program is the single largest product risk facing European PSPs over the next 24 months.

---

## 1. The regulatory shift

The Council of the EU published the final compromise texts for PSD3 and the Payment Services Regulation on **23 April 2026** (PSR: ST-8221-2026-INIT, PSD3: ST-8222-2026-INIT). Publication in the Official Journal is expected in Q2 2026, with general application approximately 21 months later — late 2027 to early 2028.

The package replaces PSD2 and the second E-Money Directive with a dual-instrument architecture: PSD3 governs authorisation, supervision, and prudential matters at member-state level; the PSR is directly applicable across the Union for conduct, transparency, open banking, and — critically for this memo — **fraud liability allocation**.

The mainstream analysis frames the reform as an evolution: stronger SCA, Verification of Payee, real-time monitoring obligations, harmonised open banking. All accurate. All incomplete.

The deeper shift is architectural.

---

## 2. From rules to objective function

PSD2 was a *rules regime*. It told Payment Service Providers what to do: apply Strong Customer Authentication on remote transactions, support open banking via dedicated interfaces, monitor transactions for fraud signals, maintain incident reporting. Compliance was demonstrable by completing a checklist.

PSD3/PSR is an *objective function regime*. It does not just tell PSPs what to do — it tells PSPs **what they will be financially liable for**, and lets them optimise accordingly:

- Fail to apply Verification of Payee → reimburse the victim.
- Fail to monitor in real time with appropriate environmental and device signals → reimburse the victim.
- Fail to block a transaction where strong fraud evidence existed → reimburse the victim.
- Apply controls correctly but cannot demonstrate the decision rationale → lose the dispute, reimburse the victim.
- Block legitimate transactions excessively → absorb conversion loss and merchant churn.

For the first time in EU payments regulation, every action the PSP takes carries an **explicit expected cost** under the regulatory framework. The right strategic response is not to build a feature for each obligation. It is to **rebuild the risk decisioning layer around expected liability cost minimisation** — and let the features fall out of that optimisation.

PSPs that miss this distinction will deliver compliant-but-expensive products. PSPs that grasp it will free meaningful budget while improving both fraud outcomes and merchant economics.

---

## 3. The dissolution of domain boundaries

Under PSD2, most large PSPs organised their product surface into clean verticals: Fraud, Authentication, Acquiring, Issuing, Open Banking. Each domain had its own roadmap, its own KPIs, its own Product Manager, often its own Group PM.

PSD3/PSR ties these surfaces through a single liability framework. Concretely:

- A **Verification of Payee** failure (Acquiring domain) cascades into an **authorisation liability** that the Risk team must absorb.
- A missed **transaction monitoring signal** (Risk domain) cascades into an **APP fraud reimbursement** obligation that the Customer Operations and Legal teams must process.
- An **SCA exemption** misapplied (Authentication domain) cascades into the issuer's **recourse rights** that the Acquiring team must reconcile.

The roadmap dependencies between these domains were already high under PSD2. Under PSD3/PSR, they become tight enough that domain-by-domain prioritisation produces locally optimal but globally expensive outcomes.

The implication for product organisations is uncomfortable: **the org charts that have served European PSPs for the past decade will quietly stop working over the next 24 months**. Group Product Managers who own a single vertical will find themselves making decisions that increase liability in a peer's domain. The structural answer is a **cross-domain liability owner** — a role that does not exist on most PSP org charts today.

This is not a hypothetical reorganisation problem. It is the operating model question that boards will be asking their Heads of Product within the next year.

---

## 4. The audit trail becomes a product surface

PSR explicitly links the failure to monitor in real time to refund outcomes. In plain language: in any dispute over fraud reimbursement, **the PSP that can demonstrate a reasoned, contemporaneous decision wins. The PSP that cannot, pays.**

This shifts decision logging from an operational concern to a product requirement of the first order.

The current state of the industry, observed across multiple platforms, is that fraud and risk systems log **outcomes**: approved, declined, challenged, refunded. They very rarely log **decisions** with their full input vector, the model versions involved, the rule weights, the alternative actions considered, and the rationale for the chosen action.

Under PSR, that gap is a liability gap. Reconstructing why a decision was made three months after the fact, in front of a regulator or a court, is not feasible without purpose-built decision logging.

The product work this implies is substantial:

- **Schema design** for decision logs that capture features, scores, model versions, rule weights, alternative actions, and final selection.
- **Storage and retrieval architecture** sized for years of high-volume decision records, with sub-second retrieval for dispute investigation.
- **Reconstruction interfaces** that let Customer Operations, Legal, and Compliance reproduce a historical decision and its rationale.
- **Cross-domain decision joining** so that an APP fraud reimbursement claim can be traced through the Verification of Payee decision, the monitoring decision, and the authorisation decision in a single coherent record.

This is at least a multi-quarter, multi-team build. PSPs that begin this work in 2026 will be ready when the rules apply. PSPs that begin it after Official Journal publication will be late.

---

## 5. What this repository attempts

This repository is not a production-ready risk engine. It is a **product specification, written in code**, that works through what a PSD3/PSR-aware risk decisioning layer would actually need to do.

It is structured the way a Group Product Manager would structure a multi-quarter domain redesign:

1. **Problem framing** — this document.
2. **Decision framework** — the expected-cost model formalised, with worked examples.
3. **PSR article mapping** — each obligation in the regulation traced to a product capability and a decision the engine has to make.
4. **Reference implementation** — illustrative code that demonstrates the decision flow.
5. **Dashboard** — a Streamlit interface showing decisions, costs, and audit trails in motion.

The goal is not to prescribe an implementation. The goal is to demonstrate that the regulatory shift can — and should — be approached with the same rigour as any other multi-quarter product redesign.

For Heads of Product, Group PMs, and risk leads framing this work internally over the next 24 months, the question is not *whether* PSD3/PSR requires a product redesign. The question is whether your organisation will frame it that way before or after the deadline forces it to.

---

*Karim Ouriachi — Senior Product Manager, Payments & Risk. 15 years across acquiring, in-store devices, and multi-country payment platform deployments.*

*linkedin.com/in/karim-ouriachi-a7217127*
