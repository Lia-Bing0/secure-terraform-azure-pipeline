from fastapi import FastAPI

app = FastAPI(
    title="Secure Terraform Delivery Pipeline Demo API",
    description="Demo API used for OWASP ZAP runtime security testing.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Secure Terraform Delivery Pipeline Demo API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/api/status")
def api_status():
    return {
        "service": "demo-api",
        "environment": "ci",
        "security_scan": "ready"
    }


@app.get("/api/version")
def version():
    return {
        "version": "1.0.0",
        "framework": "fastapi"
    }