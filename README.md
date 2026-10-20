# Firmware Analysis Service

## Overview

This project is a Flask-based firmware analysis service that processes uploaded firmware archives, extracts their contents, performs token analysis, stores job information, and exposes REST APIs for tracking analysis status and retrieving results.

The system was built as a background-job architecture so large firmware files can be processed asynchronously without blocking API requests.

---

## Features

### Archive Processing
- Supports `.zip`, `.tar`, `.tar.gz`, and `.tgz` archives.
- Recursively processes nested archives.
- Tracks extracted files and directory structure.
- Records file metadata.

### Firmware Token Analysis
- Recursively scans extracted firmware contents.
- Detects tokens matching the pattern:

```
<TknXXXYYYYYTkn>
```

Where:
- `XXX` = 3 digits
- `YYYYY` = 5 uppercase letters

Example:

```
<Tkn123ABCDETkn>
```

### Asynchronous Job Processing
- Uses `ThreadPoolExecutor` for background execution.
- Generates a unique job ID for each analysis request.
- Tracks job lifecycle:
  - pending
  - running
  - completed
  - failed

### REST APIs
- Upload firmware for analysis.
- Check job status.
- Retrieve analysis results.

### Database Integration
- Stores job information.
- Stores extracted file metadata.
- Supports PostgreSQL through SQLAlchemy.

### Testing
- Unit tests using pytest.
- Integration tests using Flask test_client.
- Archive-processing tests.
- Nested archive validation.
- API endpoint verification.

---

## Architecture

```
Client
  |
  v
POST /analysis
  |
  v
Create Job
  |
  v
ThreadPoolExecutor
  |
  v
Extract Firmware Archive
  |
  v
Analyze Files
  |
  v
Store Results
  |
  v
Update Job Status
```

---

## Project Structure

```
project/
│
├── app.py
├── config/
│   ├── settings.py
│   └── db.py
│
├── models/
│   ├── job.py
│   └── extracted_file.py
│
├── routes/
│   └── analysis.py
│
├── services/
│   ├── archive_processor.py
│   └── firmware_analyzer.py
│
├── tests/
│   ├── unit/
│   └── integration/
│
└── uploads/
```

---

## Token Analysis Logic

The analyzer:

1. Walks through all extracted directories recursively.
2. Opens supported files.
3. Searches for tokens using the required pattern.
4. Counts occurrences.
5. Generates CSV output.
6. Stores analysis results for retrieval.

---

## API Endpoints

### Submit Firmware Analysis

```
POST /analysis
```

Request:

```
multipart/form-data
firmware=<archive file>
```

Response:

```json
{
  "job_id": "uuid",
  "status": "pending"
}
```

---

### Check Job Status

```
GET /analysis/<job_id>
```

Response:

```json
{
  "job_id": "uuid",
  "status": "completed",
  "error": null
}
```

---

### Retrieve Results

```
GET /analysis/<job_id>/results
```

---

## Security Concepts Relevant to the Project

### Asset Management
Maintain visibility into firmware contents, extracted files, software components, and analysis results.

### Assurance
Verify firmware and software assets for known issues and security concerns.

### Compliance
Support evidence generation and reporting activities required by cybersecurity processes.

### Risk Management
Help identify findings that should be prioritized for remediation.

---

## Running Tests

```
pytest
```

Run unit tests only:

```
pytest tests/unit
```

Run integration tests only:

```
pytest tests/integration
```

---

## Key Learning Concepts

- Flask APIs
- Background jobs
- ThreadPoolExecutor
- Archive extraction
- Recursive file processing
- Regular expressions
- PostgreSQL
- SQLAlchemy
- Unit testing
- Integration testing
- Firmware analysis
- Vulnerability management fundamentals

---

## Future Enhancements

- SBOM generation
- CVE correlation
- Vulnerability filtration
- Vulnerability prioritization
- Risk scoring
- Dashboard visualization
- Automated reporting
