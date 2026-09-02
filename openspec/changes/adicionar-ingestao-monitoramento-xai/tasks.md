# Plano de Tarefas: Registry de Auditoria (ML/XAI)

- [ ] **Tarefa 1: Setup da Infraestrutura Base**
  - Inicializar projeto Python com FastAPI e Pydantic.
  - Configurar o framework de testes (Pytest).
- [ ] **Tarefa 2: Modelagem de Dados e Validação (Pydantic)**
  - Criar schema `ConfidenceScoreValidator` restringindo valores ao intervalo [0.0, 1.0].
  - Criar schema principal `AuditPayload` contemplando a classificação de risco e o array de explicabilidade.
  - Implementar validador de raiz (`@model_validator`) para garantir que o objeto XAI não seja nulo ou vazio quando o risco for "Crítico".
- [ ] **Tarefa 3: Camada de Negócio e Roteamento**
  - Implementar a lógica de serviço para recepção dos dados.
  - Desenvolver o endpoint `POST /api/v1/audit/metrics`.
  - Mapear os erros de validação do Pydantic para retornar o status `400 Bad Request` com mensagens descritivas de violação matemática.
- [ ] **Tarefa 4: Implementação da Suíte de Testes (BDD)**
  - Escrever teste unitário para o caminho feliz (risco crítico + XAI preenchido).
  - Escrever testes unitários para o caso de borda 1 (confidence score 1.5 e -0.1).
  - Escrever teste unitário para o caso de borda 2 (risco crítico com array XAI ausente).

## Justificativa da revisão
A ordem inicial proposta por agentes costuma colocar a criação do endpoint (rota) antes da criação dos esquemas de validação de dados. A ordem foi invertida manualmente para garantir que o contrato de entrada (Pydantic/Type Hints) barre dados inválidos antes que qualquer lógica de processamento seja escrita, reduzindo o risco de *overengineering* no controlador.