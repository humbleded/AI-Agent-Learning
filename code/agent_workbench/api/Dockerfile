FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app/code

RUN apt-get update \
    && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# The local document reader uses PyTorch. This deployment runs on CPU.
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --index-url https://download.pytorch.org/whl/cpu \
        torch==2.14.0+cpu torchvision==0.29.0+cpu

COPY agent_workbench/api/requirements.txt agent_workbench/api/
COPY stage6/engineering_docs_rag/*requirements.txt stage6/engineering_docs_rag/
COPY stage8/incident_change_review_agent/requirements.txt stage8/incident_change_review_agent/
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -r agent_workbench/api/requirements.txt && python -m pip check

COPY agent_workbench/api/main.py agent_workbench/api/
COPY stage6/engineering_docs_rag/ingest.py stage6/engineering_docs_rag/knowledge_agent.py stage6/engineering_docs_rag/
COPY stage6/engineering_docs_rag/sample_docs/ stage6/engineering_docs_rag/sample_docs/
COPY stage8/incident_change_review_agent/incident_graph.py stage8/incident_change_review_agent/

RUN useradd --create-home --uid 10001 workbench \
    && install -d -o workbench -g workbench /app/code/stage6/engineering_docs_rag/.ingest_store
USER workbench

CMD ["python", "-m", "uvicorn", "main:app", "--app-dir", "agent_workbench/api", "--host", "0.0.0.0", "--port", "8765"]
