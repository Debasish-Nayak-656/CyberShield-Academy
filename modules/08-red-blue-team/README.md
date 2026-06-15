# Module 08 — Red Team vs Blue Team Capstone

**Duration:** Week 14 | **Difficulty:** 🔴 Advanced | **Status:** 🔒 Final Project

---

## Overview

This is the capstone of CyberShield Academy. The team splits into two groups:

- **Red Team** (Attackers) — conduct a realistic attack simulation
- **Blue Team** (Defenders) — detect, contain, and respond

---

## Scenario

> A mid-sized e-commerce company suspects they are under attack. The Red Team will simulate an advanced threat actor trying to steal customer credit card data. The Blue Team will monitor, detect, and respond.

**Environment:** Isolated virtual lab network  
**Duration:** 4 hours attack / 4 hours response

---

## Red Team Objectives

```
Phase 1: Reconnaissance (45 min)
  - OSINT on the company
  - Port scan the DMZ
  - Identify public-facing services

Phase 2: Initial Access (60 min)
  - Exploit web application vulnerability
  - Establish foothold

Phase 3: Lateral Movement (60 min)
  - Escalate privileges
  - Move from DMZ to internal network
  - Reach the database server

Phase 4: Exfiltration (30 min)
  - Extract "credit card data" (simulated flag file)
  - Cover tracks
```

## Blue Team Objectives

```
- Monitor SIEM for alerts
- Identify attack timeline
- Contain compromised systems
- Eradicate malware/backdoors
- Write Incident Report
- Implement lessons learned
```

---

## Deliverables

**Red Team:**
- [ ] Attack playbook (pre-engagement)
- [ ] Proof of exploitation screenshots
- [ ] Captured flags/flags.txt
- [ ] Red team report

**Blue Team:**
- [ ] Incident Response report (template in reports/templates/)
- [ ] Attack timeline reconstruction
- [ ] List of IOCs discovered
- [ ] Remediation steps taken

**Both Teams:**
- [ ] Lessons learned presentation (10 min)

---

## Scoring

| Task | Red Team | Blue Team |
|------|----------|-----------|
| Gain initial access | +50 pts | — |
| Reach internal network | +100 pts | — |
| Capture the flag | +150 pts | — |
| Detect initial access | — | +50 pts |
| Contain attack | — | +100 pts |
| Identify all IOCs | — | +75 pts |
| Complete IR report | — | +75 pts |

---

*Congratulations on completing CyberShield Academy!*
