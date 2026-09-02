from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from schemas import AuditPayload
from services import AuditService

app = FastAPI(
    title="ML/XAI Audit Metrics API",
    description="API para ingestão e monitoramento de explicabilidade de ML (XAI)",
    version="1.0.0"
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    messages = []
    for err in errors:
        msg = err.get("msg")
        loc_path = ".".join(map(str, err.get("loc", [])))
        
        # Pydantic adiciona "body." no loc quando é validação de body. Limpamos para melhor leitura.
        if loc_path.startswith("body."):
            loc_path = loc_path[5:]
            
        messages.append(f"Erro no campo '{loc_path}': {msg}")
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Erro de validação nos dados fornecidos", "errors": messages}
    )

@app.post("/api/v1/audit/metrics", status_code=status.HTTP_201_CREATED)
async def create_audit_metrics(payload: AuditPayload):
    result = AuditService.process_audit_metrics(payload)
    return result
