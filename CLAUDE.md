@AGENTS.md

# Agent Reference Document: Railway Radar Enterprise Architecture

## 1. Project Context & Primary Purpose
*   **The Core Objective:** The primary purpose of this project is to simulate a high-stakes, Fortune-500-level engineering environment. It is an educational ecosystem built to allow a team of three (Saurabh, Suraj, and Kisan) to learn as a unified pod by seeing a highly scalable, enterprise-grade architecture in action.
*   **The Product:** "Railway radar" is a high-concurrency web application designed to track Indian Railways trains in real-time across a geospatial map.
*   **Target Scale:** The platform is architected to operate at massive scale, supporting 1M to 10M+ Monthly Active Users (MAU) without bottlenecks.

## 2. Team Topology & Mentorship Strategy
The project uses strict role separation to mimic how top-tier engineering pods operate, ensuring safe, parallel development and targeted upskilling:
*   **Saurabh (Tech Lead, AI Architect, DevOps):** Architect of the monorepo, sets up GitHub Actions CI/CD pipelines, designs the PostgreSQL/Redis schemas, and builds the Python FastAPI predictive engines.
*   **Suraj (Data Engineer & Frontend Integration):** Bridges data and UI. Handles data ingestion scripts (GeoJSON parsing) and Mapbox GL integration, combining his Data Science learning with real-world React execution.
*   **Kisan (Core UI Developer):** Focuses on isolated, highly structured foundational React tasks (UI atoms, Tailwind layouts, search debouncing) to build muscle memory before handling complex map state.

## 3. Technology Stack & Architectural Choices
The project utilizes an Event-Driven Microservices Architecture.
*   **Monorepo Strategy (Turborepo & pnpm):** A monorepo guarantees atomic commits. Frontend and backend API contracts can be updated in a single Pull Request, physically preventing the backend and frontend from ever being out of sync. It enables Shift-Left validation via Husky, blocking code that fails linting or type-checking.
*   **Frontend (Next.js 16, React 19, Tailwind v4):** Next.js handles optimized routing and rendering, while Mapbox GL is chosen specifically for high-performance 60fps rendering of massive geospatial datasets.
*   **Backend (Python FastAPI & Node.js):** FastAPI seamlessly handles strict data validation via Pydantic and natively supports the Python AI/ML ecosystem needed for predictive routing. Node.js is utilized alongside for handling high-concurrency WebSocket connections.
*   **Polyglot Storage Layer:** 
    *   **PostgreSQL with PostGIS:** Handles persistent state (static train routes, station coordinates). PostGIS executes native, highly efficient geospatial queries.
    *   **Redis:** Handles highly ephemeral state (volatile train GPS coordinates changing every few seconds). This prevents locking up the PostgreSQL database and enables sub-millisecond reads for millions of users.

## 4. Data Strategy: The "Why" Behind Dead Reckoning
Sourcing live train telemetry presented the largest architectural hurdle, dictating the system design.
*   **The Roadblocks:** Direct NTES scraping was blocked by TLS/session verification. Third-party aggregators (RapidAPI) enforced strict rate limits, making traditional polling (one API request per user) financially impossible at scale. 
*   **The Upstream Choice:** Open-source Datameet repositories provide the static track schemas. The RailKit REST API (`api.railkit.in`) provides live telemetry payloads.
*   **The Scalability Solution (Spatial Interpolation):** Polling APIs for 10,000 trains every 5 seconds would generate ~5 billion monthly requests. The architecture shifted to **Dead Reckoning** to drop this to under 500,000 requests:
    1.  **10-Minute Batching:** Background workers fetch bulk telemetry updates only once every 10 minutes and push the state to Redis.
    2.  **Client-Side Illusion:** The frontend calculates movement between updates using the train's velocity, heading, and the static PostGIS track line to create a smooth real-time animation.
    3.  **Cache-Aside (On-Demand Precision):** If a user explicitly clicks a train and the Redis telemetry is older than 60 seconds, FastAPI bypasses the batch, fetches the fresh coordinate on-demand, updates Redis, and snaps the UI to the exact location.

## 5. Enterprise Workflows & Methodologies
*   **Agile Management:** The team utilizes Jira for Sprint tracking (using Parent-Child sub-tasks to distribute work) and Confluence for Technical Design Documents (RFCs).
*   **Parallel Development:** Engineers code against frozen mock JSON data contracts first. This allows UI engineers to build layouts without waiting for backend APIs to be finished.
*   **Secret Management:** API keys (like the Mapbox token) are never committed to code or shared in plain text. They are passed via self-destructing links and stored locally in `.env.local` files protected by `.gitignore` rules.


## 🛑 Critical System Constraints & Rules
- **DO NOT** poll external third-party APIs directly from the Next.js frontend. 
- **API Rate Limits:** We are operating on strict free-tier limits. Do not write scripts that loop over train arrays to fetch live data.
- **Data Strategy:** Always use the **Dead Reckoning / Spatial Interpolation** pattern for live tracking. Read telemetry exclusively from the Redis cache.
- **Cache-Aside Pattern:** Only fetch from the external RailKit API on-demand if the Redis cache key `train:{train_id}:telemetry` is older than 60 seconds.
- **Tech Stack:** Use Next.js 16 (App Router), React 19, Tailwind v4, and Python FastAPI.