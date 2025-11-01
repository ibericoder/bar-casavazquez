# Casa Vazquez Backend Upgrade - Master Plan

**Project Goal:** Transform frontend-only portfolio into full-stack application demonstrating backend, deployment, and DevOps skills for job applications.

**Timeline:** Oct 27 - Nov 5, 2025 (10 days)  
**Branch:** `fastapi-backend-upgrade`  
**Target:** Multiple daily commits, production-ready code

---

## Current State

### ✅ Already Implemented (Before Plan)
- FastAPI backend with SQLAlchemy ORM
- JWT authentication (admin/manager/staff roles)
- Full CRUD APIs (wines, drinks, snacks, notifications)
- Vue.js admin panel with login
- SQLite database with migration scripts
- Basic Pydantic validation
- CORS configuration
- MCP Wine Recommender (chatbot - currently hidden)

### 📍 Current Infrastructure
- **Frontend:** Vue 3 + Vite
- **Backend:** FastAPI + Python 3.11
- **Database:** SQLite (dev) → PostgreSQL (planned)
- **Current Deployment:** Google Cloud Run
- **CI/CD:** None yet (manual gcloud deploy)

---

## Deployment Strategy

### **DECISION: Google Cloud Run with Multi-Environment Setup**

#### Current Setup (Production)
- **Service Name:** `casavazquez-website-update`
- **Region:** europe-central2
- **Database:** Currently embedded (will migrate to Cloud SQL)
- **URL:** Production URL (live site)
- **Branch:** `main`

#### New Setup (Staging) - Starting Day 6
- **Service Name:** `casavazquez-staging`
- **Region:** europe-central2
- **Database:** Separate Cloud SQL instance (staging)
- **URL:** Separate staging URL
- **Branch:** `staging`

**Two completely separate Cloud Run services = No risk to production!**

---

### CI/CD Pipeline Strategy

#### Phase 1: Automated Testing (Days 3-5)
**Trigger:** Every commit/PR to any branch
```
┌─────────────────┐
│ Push to Branch  │
└────────┬────────┘
         ▼
    ┌────────┐
    │ GitHub │
    │ Actions│
    └───┬────┘
        ▼
   Run Tests
   Build Docker
   Lint Code
        │
        ├─ PASS ──→ ✅ Can merge
        └─ FAIL ──→ ❌ Block PR
```

**What happens:**
- Automated tests run
- Docker build validates
- No deployment yet
- Fast feedback (2-3 minutes)

#### Phase 2: Staging Auto-Deploy (Days 6-8)
**Trigger:** Merge to `staging` branch
```
┌──────────────────┐
│ Merge to staging │
└────────┬─────────┘
         ▼
    Run Tests
         ▼
    Build Image
         ▼
  Push to Registry
         ▼
┌─────────────────────┐
│ Deploy to           │
│ casavazquez-staging │
│ (separate instance) │
└─────────────────────┘
```

**What happens:**
- Automatically deploys to staging Cloud Run
- Separate database (staging)
- Separate URL for testing
- Production untouched

#### Phase 3: Production Manual Deploy (Days 9-10)
**Trigger:** Manual approval only
```
┌──────────────┐
│ Merge to main│
└──────┬───────┘
       ▼
   Wait for
   Manual Click
       ▼
┌─────────────────────────┐
│ Deploy to Production    │
│ casavazquez-website-... │
│ (live site)             │
└─────────────────────────┘
```

**What happens:**
- Tests must pass
- Requires manual approval
- Deploys to production
- Safe, controlled release

---

### Cost Breakdown

**Current (Production only):**
- Cloud Run: ~$5/month
- **Total: ~$5/month**

**After Setup (Production + Staging):**
- Cloud Run Production: ~$5/month
- Cloud Run Staging: ~$2/month (lower traffic)
- Cloud SQL Production: ~$10/month
- Cloud SQL Staging: ~$7/month (smaller instance)
- **Total: ~$24/month**

**Why Worth It:**
- Professional setup for portfolio
- Safe testing environment
- Industry-standard practices
- Impresses employers
- Can pause staging when not in use

---

### Timeline Clarification

**Days 1-2 (Oct 27-28):** Local Docker setup only
**Days 3-5 (Oct 29-31):** Testing + docs (no deployment changes)
**Day 6 (Nov 1):** Create staging Cloud Run + Cloud SQL
**Day 7 (Nov 2):** Deploy staging branch to staging instance
**Day 8 (Nov 3):** Add automated CI/CD
**Days 9-10 (Nov 4-5):** Production migration + polish

---

### Environment Architecture

```
┌─────────────────────────────────────────┐
│           GitHub Repository             │
│  ┌──────────┐  ┌──────────┐            │
│  │  main    │  │ staging  │            │
│  │  branch  │  │  branch  │            │
│  └────┬─────┘  └────┬─────┘            │
└───────┼─────────────┼──────────────────┘
        │             │
        │             │
        ▼             ▼
┌──────────────┐  ┌──────────────┐
│ Production   │  │  Staging     │
│ Cloud Run    │  │  Cloud Run   │
│              │  │              │
│ URL: live    │  │ URL: staging │
└──────┬───────┘  └──────┬───────┘
       │                 │
       ▼                 ▼
┌──────────────┐  ┌──────────────┐
│ Cloud SQL    │  │ Cloud SQL    │
│ (production) │  │ (staging)    │
└──────────────┘  └──────────────┘
```

**Key Points:**
- ✅ Two separate Cloud Run services
- ✅ Two separate databases
- ✅ Zero risk to production
- ✅ Can test changes safely
- ✅ Industry best practice

---

## 10-Day Implementation Plan

### ✅ Day 1: Environment & PostgreSQL Prep (Oct 27) - COMPLETED
- [x] Created `.env.example`
- [x] Enhanced PostgreSQL URL handling  
- [x] Added connection pool health checks
- [x] Documentation started

**Commits (3):**
- `hide sommelier chat for now (WIP)=`
- `add env example file`
- `prep for postgres switch`

---

### ✅ Day 2-3: Docker & Testing (Oct 28) - COMPLETED
**Goals:**
- [x] Create `docker-compose.yml` with postgres service
- [x] Update backend Dockerfile
- [x] Add docker ignore file
- [x] Install pytest dependencies
- [x] Create test structure with fixtures
- [x] Write API tests (main, wines, auth)
- [x] Add pytest configuration
- [x] Clean up pycache files
- [x] Mobile admin improvements
- [x] Bulk price update endpoint

**Commits (9):**
- `add docker compose`
- `update dockerfile for compose`
- `add dockerignore`
- `add pytest deps`
- `add tests - inti` (typo)
- `fix test client`
- `remove pycache files`
- `wine api tests`
- `auth tests`
- `pytest config`
- `mobile admin improvements`
- `add bulk wine price update function`

**Status:** ✅ AHEAD OF SCHEDULE - Completed Day 3 work on Day 2!

---

### ✅ Day 4: API Improvements & Security (Oct 29) - COMPLETED
**Goals:**
- [x] Add image upload endpoint
- [x] Field validation for schemas
- [x] Error handling middleware
- [x] Rate limiting

**Commits (4):**
- `add image upload ep`
- `add validation wine schema`
- `improve exception handling`
- `add rate limiting middleware`

**Philosophy Applied:** Make it work → Make it pretty → Make it secure
- First: Basic upload functionality (works)
- Then: Input validation (cleaner)
- Finally: Error handling + rate limiting (secure)

**Status:** ✅ COMPLETED

---

### Day 5: API Documentation & Standards (Oct 30)
**Goals:**
- Install pytest and testing dependencies
- Create `tests/` folder structure
- Write basic API tests (health, wines endpoint)
- Test authentication flow
- Add test database configuration

**Planned Commits:**
- `add pytest dependencies`
- `setup test structure`
- `add wine api tests`
- `fix test db setup`

**Technologies Demonstrated:**
- pytest, pytest-asyncio
- Test fixtures
- API testing
- Async testing patterns

---

### Day 4: Mobile-Friendly Admin (Oct 30)
**Goals:**
- Make admin panel responsive (CSS media queries)
- Add bulk price update endpoint
- Improve mobile UX (larger buttons, better forms)
- Add image upload endpoint stub

**Planned Commits:**
- `mobile admin css`
- `bulk update endpoint`
- `admin ui improvements`

**Technologies Demonstrated:**
- Responsive design
- Mobile-first approach
- Batch operations API

---

### Day 5: API Documentation & Standards (Oct 31)
**Goals:**
- Enhance OpenAPI/Swagger docs
- Add request/response examples
- Document all endpoints
- Create API usage guide
- Add API versioning headers

**Planned Commits:**
- `improve api docs`
- `add endpoint examples`
- `api documentation update`

**Technologies Demonstrated:**
- OpenAPI specification
- API documentation best practices
- API versioning

---

### Day 6: Cloud SQL PostgreSQL (Nov 1)
**Goals:**
- Set up Google Cloud SQL PostgreSQL instance
- Configure connection from Cloud Run
- Update environment variables
- Test connection with Cloud SQL Proxy
- Create staging database

**Planned Commits:**
- `cloud sql config`
- `staging db setup`
- `connection pooling for cloud`

**Technologies Demonstrated:**
- Google Cloud SQL
- Cloud infrastructure
- Database migration
- Environment management

---

### Day 7: Staging Environment (Nov 2)
**Goals:**
- Create `staging` branch
- Deploy to separate Cloud Run service
- Configure staging environment variables
- Set up staging database
- Test full stack on staging

**Planned Commits:**
- `staging branch setup`
- `staging env config`
- `deploy to staging`
- `fix staging cors`

**Technologies Demonstrated:**
- Multi-environment deployment
- Environment separation
- Staging best practices

---

### Day 8: CI/CD with Cloud Build (Nov 3)
**Goals:**
- Create `cloudbuild.yaml`
- Auto-run tests on PR
- Auto-deploy staging on push to staging branch
- Add build badges to README
- Set up GitHub integration

**Planned Commits:**
- `add cloud build config`
- `auto test workflow`
- `auto deploy staging`
- `update readme with badges`

**Technologies Demonstrated:**
- CI/CD pipelines
- Google Cloud Build
- Automated testing
- Automated deployment

---

### Day 9: Production Deployment (Nov 4)
**Goals:**
- Migrate production data to Cloud SQL
- Update production Cloud Run service
- Configure production environment
- Set up health monitoring
- Create backup script

**Planned Commits:**
- `prod db migration`
- `prod deployment config`
- `backup automation`
- `monitoring setup`

**Technologies Demonstrated:**
- Production deployment
- Data migration
- Backup strategies
- Monitoring

---

### Day 10: Polish & Portfolio (Nov 5)
**Goals:**
- Add logging (structured logs)
- Performance monitoring setup
- Final documentation
- Create impressive README
- Screenshot admin panel for portfolio

**Planned Commits:**
- `add structured logging`
- `performance monitoring`
- `final docs`
- `portfolio ready`

**Technologies Demonstrated:**
- Production logging
- Performance monitoring
- Documentation
- Portfolio presentation

---

## Technologies Covered

### Backend
- ✅ FastAPI (async Python web framework)
- ✅ SQLAlchemy (ORM)
- ✅ Pydantic (validation)
- ✅ JWT Authentication
- 🔄 PostgreSQL (production database)
- 🔄 pytest (testing)

### DevOps
- 🔄 Docker & Docker Compose
- 🔄 Google Cloud Run (serverless)
- 🔄 Google Cloud SQL (managed PostgreSQL)
- 🔄 Cloud Build (CI/CD)
- ⏳ Monitoring & Logging

### Architecture
- ✅ REST API design
- ✅ Database migrations
- ✅ Environment configuration
- 🔄 Multi-environment deployment
- 🔄 Testing strategy

---

## Success Metrics

### For Job Applications
- ✅ Shows backend development (not just frontend)
- ✅ Demonstrates cloud deployment
- ✅ CI/CD pipeline
- ✅ Testing knowledge
- ✅ Production-ready code
- ✅ Security best practices
- ✅ Documentation

### Technical Achievements
- RESTful API with 20+ endpoints
- JWT authentication with role-based access
- PostgreSQL database in production
- Docker containerization
- Automated testing
- CI/CD pipeline
- Mobile-responsive admin panel
- Multi-environment deployment

---

## Interview Talking Points

**"Walk me through your backend architecture"**
→ FastAPI with async SQLAlchemy, PostgreSQL on Google Cloud SQL, deployed via Cloud Run with Docker

**"How do you handle deployments?"**
→ CI/CD with Cloud Build - auto-tests on PR, auto-deploy staging on merge, manual production deployment

**"What about testing?"**
→ pytest with async support, API endpoint testing, test database isolation

**"Security considerations?"**
→ JWT auth, role-based access, environment variables, SQL injection prevention via ORM, CORS configuration

**"Scalability?"**
→ Cloud Run auto-scaling, connection pooling, async endpoints, PostgreSQL with proper indexing

---

## Current Status

**Last Updated:** October 29, 2025  
**Current Day:** Day 4 (COMPLETED)  
**Commits Today:** 4  
**Total Commits This Branch:** 16

**Next Steps:**
1. Day 5: API documentation enhancements
2. Day 6+: Cloud deployment prep

**Achievement:** Completed Days 1-4 in just 3 days! 🚀

**Development Philosophy:**
Following "Make it work → Make it pretty → Make it fast/secure"
- Get features working first
- Refine and polish iteratively
- Add security and performance last
Real devs iterate - perfection comes in stages!

---

## Repository Structure

```
casavazquez/
├── backend/
│   ├── app/
│   │   ├── api/          # Endpoint routers
│   │   ├── core/         # Config, database, auth
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── mcp/          # Wine recommender
│   ├── tests/            # [TO ADD]
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── website/              # Vue.js frontend
├── docs/                 # Interview prep (gitignored)
├── docker-compose.yml
└── cloudbuild.yaml       # [TO ADD]
```

---

## Links & Resources

- **Repo:** https://github.com/ibericoder/bar-casavazquez
- **Branch:** fastapi-backend-upgrade
- **Current Prod:** Google Cloud Run (casavazquez-website-update)
- **Staging:** [TO BE CREATED]

---

**Legend:**
- ✅ Completed
- 🔄 In Progress  
- ⏳ Planned
- ❌ Blocked/Changed
