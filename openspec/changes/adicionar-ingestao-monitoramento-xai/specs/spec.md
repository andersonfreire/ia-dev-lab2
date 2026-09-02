# Especificação Técnica

## Requisitos (PRD)
- O sistema deve expor um endpoint para ingestão de métricas de ML.
- O sistema deve validar estritamente se o `confidence_score` está no intervalo [0.0, 1.0].
- O payload deve conter a classificação de risco ("Baixo", "Médio", "Crítico").
- Se a classificação de risco for "Crítico", o objeto de explicabilidade (SHAP/LIME) é obrigatório.

## Critérios de Aceite

**Cenário 1: Caminho Feliz - Ingestão válida**
- **Dado** que o payload contém uma predição de risco "Crítico" e um array de explicabilidade preenchido
- **Quando** o endpoint de ingestão for acionado
- **Então** o sistema deve registrar a métrica e retornar status 201 (Created)

**Cenário 2: Caso de Borda - Score anômalo**
- **Dado** que o payload informa um `confidence_score` de 1.5 ou -0.1
- **Quando** o endpoint de ingestão for acionado
- **Então** o sistema deve rejeitar a requisição com status 400 (Bad Request) informando violação de limite matemático

**Cenário 3: Caso de Borda - Ausência condicional de XAI**
- **Dado** que o payload contém uma predição de risco "Crítico"
- **Quando** o array de explicabilidade vier nulo ou vazio
- **Então** o sistema deve rejeitar a requisição com status 400 (Bad Request) exigindo a justificativa