# TECHNOVA REST API Reference

All endpoints return JSON responses. Interactive OpenAPI docs are available at `/docs`.

## Health
- `GET /api/health` -> System health and backend status.

## Datasets
- `POST /api/datasets/upload` -> Multipart file upload (CSV, XLSX, JSON). Returns dataset metadata & quality report.
- `GET /api/datasets` -> List all uploaded datasets.
- `GET /api/datasets/{id}` -> Get dataset details & column profiling.
- `DELETE /api/datasets/{id}` -> Delete dataset.
- `GET /api/datasets/relationships` -> Multi-table relationship detection.

## Analysis
- `POST /api/analysis` -> Execute analysis pipeline (`question`, `dataset_ids`). Returns full analysis & proof.
- `GET /api/analysis/history` -> Get analysis trajectory history.
- `GET /api/analysis/{id}` -> Get analysis status & answer.

## Proof & Evidence
- `GET /api/analysis/{id}/proof` -> Get executable proof card & generated code.
- `GET /api/analysis/{id}/evidence` -> Get verification evidence items.

## Reports & Demo
- `GET /api/reports/{id}` -> Export analysis report JSON.
- `GET /api/demo/questions` -> List built-in demonstration questions.
