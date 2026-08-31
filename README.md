# Costa Rica ID and Name Checker

A small Python command-line utility that looks up a list of identification numbers through Costa Rica's Ministry of Finance public API and reports records whose returned names match a supplied list.

> **Project status:** functional utility / prototype. It performs sequential read-only lookups and prints results to the terminal. It is not a registry, identity-verification service, or production-grade batch processing system.

## What It Does

For each non-empty line in `ids.txt`, the script requests:

```text
https://api.hacienda.go.cr/fe/ae?identificacion=<ID>
```

It reads the `nombre` returned by the API, normalizes accents, case, and whitespace, and compares it with every target in `names.txt`. A target matches only when all of its name tokens appear as complete tokens in the returned name.

Example:

```text
names.txt:  MARIA LOPEZ
API name:   MARIA ELENA LOPEZ RODRIGUEZ
result:     match
```

## Current Behavior

- Uses only Python's standard library.
- Reads identification numbers from `ids.txt`.
- Reads target names from `names.txt`.
- Normalizes accents and letter case before comparison.
- Uses a 10-second HTTP timeout.
- Waits one second between requests to reduce load on the public service.
- Handles common HTTP and connection errors without stopping the full run.
- Writes progress and matches to standard output; it does not create a report file or database.

## Requirements

- Python 3.6 or newer
- Internet access to `api.hacienda.go.cr`
- Permission and a legitimate purpose to process the input data

No third-party Python packages are required.

## Setup

```bash
git clone https://github.com/jrodriguezes/costa-rica-id-verifier.git
cd costa-rica-id-verifier
```

Create the two input files in the repository root.

`names.txt`:

```text
PERSONA DE EJEMPLO
OTRO NOMBRE DE EJEMPLO
```

`ids.txt`:

```text
000000000
111111111
```

Use only synthetic examples or data that you are explicitly authorized to process. Then run:

```bash
python checker.py
```

On systems where Python 3 uses a separate executable:

```bash
python3 checker.py
```

## Matching Rules

The comparison intentionally ignores:

- Uppercase versus lowercase.
- Diacritics such as `Á` versus `A`.
- Repeated whitespace.
- The order and presence of additional name tokens in the API response.

The comparison does **not** implement fuzzy matching, typo correction, phonetic matching, or identity confirmation. A name match is only a text-processing result and can produce false positives when names are common or incomplete.

## Data Flow

```text
ids.txt
   │
   ├─ one HTTPS request per ID ──> Hacienda public API
   │                                  │
names.txt ── normalize targets        └─ returned nombre
   │                                      │
   └──────────────── compare complete tokens
                                          │
                                          └─ terminal output
```

## Privacy and Responsible Use

Identification numbers and names are personal data. Before using this project:

- Obtain a lawful basis and authorization for the intended processing.
- Do not commit real identification numbers or personal names to a public repository.
- Replace repository samples with synthetic data.
- Limit access to input files and terminal output.
- Do not use a textual match as proof of identity, eligibility, legal status, or ownership.
- Review the public API's current terms, availability, and acceptable-use requirements.

The repository currently treats `ids.txt` and `names.txt` as ordinary files. If real data must be used locally, add them to `.gitignore` before populating them and verify that they have never been committed.

## Known Limitations

- Requests are sequential, so large lists are slow.
- There is no retry or exponential-backoff strategy.
- Output is console-only and is not machine-readable.
- The external API can change, throttle requests, become unavailable, or return incomplete data.
- Matching is token-based and does not establish that two people are the same person.
- There are no automated tests or CI workflow.

## Possible Improvements

- [ ] Replace tracked input examples with clearly synthetic fixtures.
- [ ] Add command-line arguments for input and output paths.
- [ ] Add CSV or JSON report export.
- [ ] Add structured logging and resumable runs.
- [ ] Add configurable delay, timeout, and retry behavior.
- [ ] Add unit tests for normalization and matching.
- [ ] Add integration tests with mocked API responses.

## License

No open-source license is currently included. Unless a license is added, all rights are reserved.

## Author

[Jeremy Rodriguez](https://github.com/jrodriguezes)
