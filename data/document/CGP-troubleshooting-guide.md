# CGP Workflow — Design & Troubleshooting Manual

A step-by-step operations guide for the Comprehensive Genomic Profiling (CGP)
bioinformatics workflow. Use this manual to understand the system architecture,
locate the right logs, and isolate the failing component when an error occurs.

---

## 1. System Overview

The CGP workflow turns raw sequencing output into a clinical-style genomic report.
It is made of three software modules plus the sequencer/NFS storage layer.

```
                    ┌──────────────┐
                    │  Sequencer   │  writes BCL/FASTQ + copyComplete.txt
                    └──────┬───────┘
                           │ streams data
                           ▼
                   ┌───────────────┐
                   │   NFS folder  │  shared run directories
                   └──────┬────────┘
                          │ watched for copyComplete.txt
                          ▼
          ┌───────────────────────────────┐
          │  (1) CGP Pipeline Module       │  launches & manages analysis tasks
          │      - variant analysis        │  log: data/log/CGP.log
          │      - task status mgmt        │
          │      - outbound API calls      │
          └───────────────┬───────────────┘
                          │ HTTP POST analysis result
                          ▼
          ┌───────────────────────────────┐
          │  (2) nginx Reverse Proxy       │  sits between CGP and Reporting
          │      - logs every API call     │  access + error logs
          │      - status codes, GET params│
          └───────────────┬───────────────┘
                          │ proxied request
                          ▼
          ┌───────────────────────────────┐
          │  (3) Reporting Tool            │  receives result, builds report
          │      - report generation       │  application log
          │      - report UI               │
          └───────────────────────────────┘
                          │
                          ▼
                    User views report
```

### The golden correlation key: **Illumina Run ID**

Every analysis task is uniquely identifiable by its **Illumina run ID**
(e.g. `250625_NB551234_0142_AHKVJ7BGXM`). This ID is the single thread you
follow across all three modules. When troubleshooting, **always start by
identifying the run ID**, then grep for it in every log.

Run ID format (Illumina convention):

```
250625_NB551234_0142_AHKVJ7BGXM
│      │        │    │
│      │        │    └─ Flow cell ID
│      │        └────── Run number on the instrument
│      └─────────────── Instrument serial (NB55=NextSeq, M02=MiSeq, A00=NovaSeq)
└────────────────────── Date (YYMMDD)
```

---

## 2. Components & Responsibilities

| # | Component | Responsibility | What it logs | Primary log |
|---|-----------|----------------|--------------|-------------|
| 0 | Sequencer + NFS | Streams run data; signals completeness with `copyComplete.txt` | (none — file presence is the signal) | NFS run dir |
| 1 | CGP Pipeline | Detects ready runs, launches/manages variant-analysis tasks, calls reporting tool | Task status, stage progress, errors, outbound calls | `data/log/CGP.log` |
| 2 | nginx Proxy | Forwards CGP → Reporting; records traffic | API path, HTTP status code, GET-mode parameters | nginx access/error log |
| 3 | Reporting Tool | Receives results, generates report, serves UI | Inbound API calls, report build status | Reporting app log |

---

## 3. End-to-End Data Flow (Happy Path)

1. **Sequencer streams data** to a per-run folder on the NFS share.
2. When the run is fully copied, the sequencer writes **`copyComplete.txt`**.
3. **CGP polls/watches** the NFS folder. On seeing `copyComplete.txt`, it
   **automatically launches an analysis task** for that run ID.
4. CGP runs the variant-analysis pipeline (demux → QC → align → dedup → variant
   calling → annotation). Progress and any failures are written to `CGP.log`.
5. On **successful completion**, CGP makes an **outbound API call** to the
   reporting tool endpoint, **through nginx**, sending the analysis result.
6. **nginx logs** the call (path, status code, GET params) and proxies it to the
   reporting tool.
7. The **reporting tool** receives the result, **generates the report**, and
   logs the inbound call.
8. The user **views the report** in the reporting tool UI.

A failure can occur at any of steps 1–8. Sections 4–5 walk through isolating which.

---

## 4. Triage: Where Did It Break?

Run through these gates in order. Each gate tells you which module to dig into.

### Gate A — Did the analysis task even start?
- **Check:** Does `CGP.log` contain a `Detected new run directory: <RUN_ID>` line?
  - **No** → Problem is **upstream of CGP** (sequencer / NFS / `copyComplete.txt`).
    Go to [5.1](#51-task-never-launches).
  - **Yes** → Continue to Gate B.

### Gate B — Did the analysis task finish successfully?
- **Check:** Grep `CGP.log` for the run ID and look for `ERROR` lines or a final
  `completed ... successful` line.
  - **ERROR present / no completion** → Pipeline-stage failure.
    Go to [5.2](#52-analysis-task-fails).
  - **Completed successfully** → Continue to Gate C.

### Gate C — Did CGP successfully call the reporting tool (via nginx)?
- **Check:** nginx access log for a request around the task completion time
  carrying the run ID, and its HTTP status code.
  - **No request logged** → CGP never sent it (outbound-call problem).
    Go to [5.3](#53-cgp-cannot-reach-reporting-tool-via-nginx).
  - **Request logged with 4xx/5xx** → Proxy or upstream rejected it.
    Go to [5.3](#53-cgp-cannot-reach-reporting-tool-via-nginx) /
    [5.4](#54-reporting-tool-does-not-generate-report).
  - **Request logged with 2xx** → Continue to Gate D.

### Gate D — Did the reporting tool generate the report?
- **Check:** Reporting app log for the inbound call (run ID) and a report-build
  success entry; confirm the report is visible in the UI.
  - **No build / build error** → Go to [5.4](#54-reporting-tool-does-not-generate-report).
  - **Built but not visible** → UI / report-retrieval issue, [5.4](#54-reporting-tool-does-not-generate-report).

---

## 5. Step-by-Step Troubleshooting by Symptom

### 5.1 Task never launches

**Symptom:** No report; `CGP.log` has no `Detected new run directory` entry for
the expected run ID.

**Steps:**
1. **Confirm the run ID** you expect (from the sequencer run name).
2. **Inspect the NFS run folder** for that run:
   - Is the folder present and readable by the CGP service account?
   - Does **`copyComplete.txt`** exist? CGP will not launch until it does.
     - If the sequencer never finished copying, the file is absent — wait or
       re-check the instrument. (Compare to the demux failure in 5.2 where the
       folder exists but is *incomplete*.)
3. **Check NFS mount health** on the CGP host (`mount`, `df`, read a test file).
   A stale or unmounted share looks identical to "no new runs".
4. **Check the CGP watcher/poller** is running and pointed at the correct NFS path.
5. Once `copyComplete.txt` is present and NFS is healthy, CGP should pick the run
   up on its next scan and log `Detected new run directory: <RUN_ID>`.

---

### 5.2 Analysis task fails

**Symptom:** `CGP.log` shows `ERROR` lines for the run ID and no successful
completion.

**First, isolate the failing stage and run ID:**
```bash
grep "<RUN_ID>" data/log/CGP.log | grep -E "ERROR|WARN"
```
The bracketed tag (e.g. `[Align]`, `[Demux]`, `[Variant]`) tells you the stage.

**Common, real failure modes (matched to recorded log patterns):**

| Stage | Error signature in log | Root cause | Remediation |
|-------|------------------------|------------|-------------|
| `[Align]` | `insufficient disk space on /scratch (0 bytes free)` | Scratch volume full | Free/extend `/scratch`, then CGP retries the failed stage |
| `[Demux]` | `RunInfo.xml not found, run folder may be incomplete` | Incomplete/corrupt run dir despite trigger | Verify run folder integrity on NFS; re-stage or re-copy the run |
| `[Variant]` | `OutOfMemoryError - Java heap space exceeded` | Insufficient JVM heap for sample | Increase heap allocation; requeue the quarantined sample |
| `[Align]` | `Reference index corrupted ... .bwt checksum mismatch` | Damaged reference genome index | Re-download/restore reference, verify checksum, resume |
| `[Variant]` | `Node ... lost ... jobs killed, scheduler will requeue` | Compute node failure | Confirm node health; scheduler redistributes to healthy nodes |
| `[QC]` | `failed QC: GC content ... contamination` | Sample-level quality issue | Flag sample for review; run usually continues for other samples |

**General procedure:**
1. Identify the **stage** and the **specific sample** (e.g. `CGP-0019`) from the
   ERROR line.
2. Map the error to the table above (or read the message — they are descriptive).
3. Apply the remediation. Most infrastructure errors (disk, memory, node,
   reference) are **transient**: fix the resource, then CGP **retries/requeues**.
4. **Re-check** `CGP.log` for the resumed/retry lines and a final
   `completed with N/M samples successful`.
5. If a single sample is **quarantined for manual review**, the rest of the run
   can still complete and report; handle that sample separately.

> Tip: A run can hit an error, recover, and still finish (e.g. disk freed →
> "retrying failed stages"). Don't stop at the first ERROR — read forward to see
> whether CGP recovered.

---

### 5.3 CGP cannot reach reporting tool (via nginx)

**Symptom:** Analysis completed in `CGP.log`, but no report appears.

**Steps:**
1. In `CGP.log`, confirm the **outbound call** was attempted after completion
   (look for the result-send / outbound-call entry for the run ID).
2. In the **nginx access log**, search for the request near that timestamp and
   the run ID in the GET parameters. Note the **HTTP status code**:
   - **No entry at all** → CGP never sent it, or cannot resolve/connect to nginx.
     Check CGP's endpoint config (host/port), DNS, and network/firewall from the
     CGP host to nginx.
   - **502 / 503 / 504** → nginx reached but the **upstream reporting tool is
     down/slow**. Check the reporting service is running and within timeout.
   - **401 / 403** → auth/permission rejected at proxy or upstream. Check
     credentials/tokens and nginx access rules.
   - **404** → wrong endpoint path. Verify the CGP target URL vs. nginx
     `location` routing.
3. Check the **nginx error log** for upstream connection errors corresponding to
   the same time window.
4. After fixing connectivity/config, **re-trigger** the result send (re-run the
   outbound step for that run ID) and confirm a **2xx** in nginx.

---

### 5.4 Reporting tool does not generate report

**Symptom:** nginx shows a **2xx** for the result call, but there is still no
viewable report.

**Steps:**
1. In the **reporting tool log**, confirm the **inbound API call** for the run ID
   was received (timestamp should align with the nginx 2xx).
   - **Not received** despite nginx 2xx → proxy returned success but did not
     forward correctly; re-examine nginx `location`/upstream config.
2. Check for a **report-generation** entry and its outcome:
   - **Build error** → inspect the payload/result contents CGP sent (malformed or
     incomplete analysis result), and any validation errors in the reporting log.
   - **Build success** → the report exists; the issue is **retrieval/UI**.
3. If built but **not visible in the UI**:
   - Confirm you are looking up the **correct run ID** in the UI.
   - Check report storage/permissions and the UI's backend connectivity.
4. Re-send the result from CGP if the payload was the problem, and re-verify the
   full chain (5.3 → 5.4).

---

## 6. Quick Reference — Log Locations & Searches

| Module | Log | What to search |
|--------|-----|----------------|
| CGP Pipeline | `data/log/CGP.log` | run ID, `ERROR`, `WARN`, stage tags, `Detected`, `completed` |
| nginx Proxy | nginx access log | run ID in GET params, HTTP status code, timestamp |
| nginx Proxy | nginx error log | `upstream`, connection refused/timed out |
| Reporting Tool | reporting app log | inbound run ID, report-build status |

**Always-useful commands:**
```bash
# Everything about one run across the pipeline log
grep "<RUN_ID>" data/log/CGP.log

# Just the failures for that run
grep "<RUN_ID>" data/log/CGP.log | grep ERROR

# All errors across all runs (scan for patterns)
grep ERROR data/log/CGP.log
```

---

## 7. Troubleshooting Flow (Summary)

```
Report missing?
   │
   ├─ CGP.log has "Detected new run directory: RUN_ID"? ── No ─▶ 5.1 (NFS / copyComplete.txt)
   │                                                   Yes
   ▼
   ├─ Run finished "completed ... successful"?  ── No / ERROR ─▶ 5.2 (pipeline stage)
   │                                            Yes
   ▼
   ├─ nginx logs a 2xx for the result call?     ── No / 4xx-5xx ─▶ 5.3 (outbound / proxy)
   │                                            Yes
   ▼
   └─ Reporting tool built the report?          ── No ─────────▶ 5.4 (reporting tool)
                                                Yes ─▶ Check UI / run ID
```

> Remember: the **Illumina run ID** ties the whole investigation together. Pin it
> down first, then follow it module by module.
