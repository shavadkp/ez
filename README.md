📝 Translation Backend System — Async Job Processing with Django, Celery & Redis

This project implements an asynchronous translation processing system using Django REST Framework, Celery, and Redis.
It supports job submission, status tracking, priority queues, cancellation, and fetching translation results.

🚀 Features

Submit translation jobs (text/file/url)

Asynchronous processing using Celery workers

Real-time job status (queued → in_progress → completed/failed)

Priority queue support (urgent, normal, low)

Authentication (Token-based)

Job cancellation

Translation results stored for retrieval

Redis-backed message queue

🏗 System Architecture
Client → Django API → Redis (Broker) → Celery Worker → PostgreSQL/SQLite

Workflow:

User submits job via /jobs/

Django saves job → queues Celery task

Celery processes translation in background

Result saved in JobResult

User fetches:

GET /jobs/<id>/ → status

GET /jobs/<id>/result/ → translation

📡 API Endpoints
🔐 Authentication

Every request requires:

Authorization: Token <your_token>

1️⃣ Submit Translation Job

POST /jobs/

Request
{
  "source_type": "text",
  "source_text": "Hello world",
  "target_languages": ["fr"],
  "priority": "normal"
}

Response
{
  "id": "uuid",
  "status": "queued"
}

2️⃣ Fetch Job Status

GET /jobs/<job_id>/

Response
{
  "id": "uuid",
  "status": "in_progress",
  "progress": 60,
  "priority": "normal"
}

3️⃣ Fetch Translation Result

GET /jobs/<job_id>/result/

Response
{
  "job": "uuid",
  "result_data": {
    "fr": "part1 → translated(fr) part2 → translated(fr)"
  }
}

4️⃣ Cancel Job

POST /jobs/<job_id>/cancel/

Response
{
  "status": "cancelled"
}

🗄 Database Schema
Job Table
Field	Type	Description
id	UUID	Primary key
user	FK	Owner
source_type	text/file/url	Input type
source_text	Text	Input content
target_languages	Array	Languages to translate
priority	urgent/normal/low	Queue priority
status	queued, in_progress, completed, failed	Job state
progress	int	% of completion
submitted_at	datetime	When submitted
started_at	datetime	When processing started
finished_at	datetime	When completed
error_message	text	Failure reason
JobResult Table
Field	Type	Description
id	UUID	PK
job	FK (One-to-One)	Job reference
result_data	JSON	Translated output
created_at	datetime	Time saved
⚙️ Celery Task Workflow
Pseudocode:
1. Fetch job info
2. Mark job as in_progress
3. For each language:
      - Process text in chunks
      - Update job.progress
4. Generate final translation result
5. Save JobResult
6. Set job status to completed
7. If any error → retry up to 3 times

📈 Autoscaling Logic (Pseudocode)
while True:
    queue_length = redis.llen("celery")
    
    if queue_length > 50:
        spin_up_worker_instance()

    elif queue_length < 5:
        shut_down_idle_worker()

    sleep(10)

🔧 Local Setup
1️⃣ Clone & Create Environment
git clone <repo>
cd project
python -m venv venv
venv\Scripts\activate

2️⃣ Install Requirements
pip install -r requirements.txt

3️⃣ Run Migrations
python manage.py migrate

4️⃣ Create Superuser
python manage.py createsuperuser

5️⃣ Run Django Server
python manage.py runserver

6️⃣ Start Celery Worker (Windows)
celery -A ez worker -l info -P solo

7️⃣ Ensure Redis is Running

(Installed via Redis for Windows)
