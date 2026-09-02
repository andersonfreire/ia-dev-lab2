import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_caminho_feliz_risco_critico_xai_preenchido():
    """
    Testa o caminho feliz: risco crítico e array de explicabilidade (XAI) preenchido.
    Deve retornar HTTP 201 Created.
    """
    payload = {
        "confidence_score": 0.85,
        "risk_classification": "Crítico",
        "explanations": [{"feature": "age", "importance": 0.45}, {"feature": "income", "importance": 0.30}]
    }
    response = client.post("/api/v1/audit/metrics", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Métricas de auditoria recebidas e processadas com sucesso"
    assert data["data"]["risk_classification"] == "Crítico"


def test_caso_de_borda_1_confidence_score_acima_do_limite():
    """
    Testa o caso de borda 1: confidence score 1.5 (maior que 1.0).
    Deve retornar HTTP 400 Bad Request com erro de validação.
    """
    payload = {
        "confidence_score": 1.5,
        "risk_classification": "Baixo"
    }
    response = client.post("/api/v1/audit/metrics", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Erro de validação nos dados fornecidos"
    
    # Verifica se a mensagem de erro apropriada para limite superior está presente
    error_messages = " ".join(data["errors"])
    assert "confidence_score" in error_messages


def test_caso_de_borda_1_confidence_score_abaixo_do_limite():
    """
    Testa o caso de borda 1: confidence score -0.1 (menor que 0.0).
    Deve retornar HTTP 400 Bad Request com erro de validação.
    """
    payload = {
        "confidence_score": -0.1,
        "risk_classification": "Médio"
    }
    response = client.post("/api/v1/audit/metrics", json=payload)
    assert response.status_code == 400
    data = response.json()
    
    error_messages = " ".join(data["errors"])
    assert "confidence_score" in error_messages


def test_caso_de_borda_2_risco_critico_xai_ausente():
    """
    Testa o caso de borda 2: risco crítico sem o array de XAI (explanations).
    Deve retornar HTTP 400 Bad Request.
    """
    payload = {
        "confidence_score": 0.9,
        "risk_classification": "Crítico"
    }
    response = client.post("/api/v1/audit/metrics", json=payload)
    assert response.status_code == 400
    data = response.json()
    error_messages = " ".join(data["errors"])
    assert "não pode ser nulo ou vazio quando o risco for \"Crítico\"" in error_messages


def test_caso_de_borda_2_risco_critico_xai_vazio():
    """
    Testa o caso de borda 2: risco crítico com o array de XAI vazio.
    Deve retornar HTTP 400 Bad Request.
    """
    payload = {
        "confidence_score": 0.9,
        "risk_classification": "Crítico",
        "explanations": []
    }
    response = client.post("/api/v1/audit/metrics", json=payload)
    assert response.status_code == 400
    data = response.json()
    error_messages = " ".join(data["errors"])
    assert "não pode ser nulo ou vazio quando o risco for \"Crítico\"" in error_messages
