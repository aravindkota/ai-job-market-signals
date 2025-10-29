"""PURPOSE: FastAPI app with routes for /health, /jobs, /stats.
"""


from fastapi import FastAPI

app = FastAPI(title="Upwork AI Job Intelligence Service")

@app.get("/health")
def health():
    return {"status": "ok"}
