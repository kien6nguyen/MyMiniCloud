# MyMiniCloud - Simulated Cloud Infrastructure

A mini cloud system with 9 standard server types, containerized with Docker and interconnected via `cloud-net`.

## 🚀 Getting Started

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed on Windows.
- [Docker Compose](https://docs.docker.com/compose/install/) (comes with Docker Desktop).

### Deployment
1.  Open terminal in this directory.
2.  Run the command:
    ```bash
    docker-compose up --build -d
    ```

### 🌍 Accessing Services

| Service | Port | URL |
|---------|------|-----|
| **Web Dashboard** (STT 1) | 80 | `http://localhost/` |
| **App API** (STT 2) | 80 (via Proxy) | `http://localhost/api/status` |
| **MinIO UI** (STT 5) | 9001 | `http://localhost:9001` |
| **Grafana** (STT 8) | 3000 | `http://localhost:3000` (User: admin, Pass: admin) |
| **Prometheus** (STT 7) | 9090 | `http://monitoring-server:9090` (internal) |

## 🏗️ Architecture

- **Web Server**: Nginx serving a modern HTML dashboard.
- **Application Server**: Flask API for cloud orchestration logic.
- **Database**: PostgreSQL storing user and node metadata.
- **Authentication**: Custom JWT-based Auth service.
- **Storage**: MinIO (S3-compatible).
- **DNS**: CoreDNS for internal simulated name resolution.
- **Monitoring**: Prometheus scraping metrics from services.
- **Logging**: Grafana for visualizing system health.
- **Proxy/LB**: Nginx routing external traffic.

## 🛠️ Internal DNS Mapping
The `dns-server` simulates the following mappings:
- `m-web.cloud.local` -> Web Server 
- `m-app.cloud.local` -> App Server
- `m-db.cloud.local` -> DB Server