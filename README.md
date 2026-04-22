# CMSC 471 Final Project - Image-to-Text Application

A serverless, 4-tier AWS application that extracts text from images using Amazon Textract, built with Infrastructure as Code using AWS SAM.

## Project Overview

This project demonstrates a production-grade serverless architecture deployed entirely through AWS SAM templates, with BDD acceptance tests, DevOps traceability, and cost optimization strategies.

**Key Technologies:**
- AWS Lambda (compute)
- Amazon Textract (OCR)
- AWS Step Functions (orchestration)
- DynamoDB (NoSQL state)
- S3 (object storage with lifecycle policies)
- API Gateway (REST API)
- CloudWatch (monitoring)
- AWS SAM (Infrastructure as Code)

**Constraints (AWS Academy Learner Lab):**
- Uses `LabRole` only (no custom IAM roles)
- Textract instead of Bedrock (per Learner Lab allowlist)
- API Gateway instead of CloudFront for edge traffic

## Architecture

```mermaid
graph TD
    User[User browser] --> APIG[API Gateway<br/>Public entry point]
    APIG -->|GET /| L0[Lambda<br/>Fetch and return index.html]
    APIG -->|POST /api/inbox| LInbox[Lambda<br/>Manage S3 inbox files]
    APIG -->|POST /api/jobs| LSubmit[Lambda<br/>StartExecution]
    APIG -->|GET /api/jobs/:id| LPoll[Lambda<br/>Poll job status]
    APIG -->|GET,DELETE /api/records| LRecords[Lambda<br/>Fetch and delete results]

    L0 -.-> S3Web[S3 Bucket<br/>index.html, JS, CSS]
    LInbox -.-> S3Store[S3 Bucket<br/>Inbox images]
    LSubmit --> SF[Step Functions State Machine]
    LPoll -.-> DDB[DynamoDB<br/>Job state and metadata]
    LRecords -.-> DDB

    subgraph Serverless[Async Orchestration Domain]
        SF --> L1[Lambda<br/>Fetch image from S3]
        SF --> L2[Lambda<br/>Call Textract]
        SF --> L3[Lambda<br/>Save Results]
        L2 -.-> Textract[Amazon Textract<br/>OCR Engine]
    end

    L1 -.-> S3Store
    L3 -.-> DDB
    CW[CloudWatch] -.-> SF

    style User fill:#e1f5ff
    style APIG fill:#fff9c4
    style SF fill:#c8e6c9
    style Textract fill:#ffccbc
    style DDB fill:#f0f4c3
```

## Getting Started

```bash
# Build and deploy
sam build --use-container
sam deploy --guided --profile lab

# Run tests
pytest tests/acceptance -v
```

## Documentation

- [Architecture Details](docs/architecture.md)
- [Cost Analysis](docs/tco.md)
- [Well-Architected Review](docs/well-architected.md)