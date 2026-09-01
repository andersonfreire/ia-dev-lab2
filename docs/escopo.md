# Escopo do Projeto: Registry de Auditoria e Explicabilidade (ML/XAI)

## Funcionalidades Escolhidas
1. **Ingestão e Validação de Métricas de Explicabilidade:** Um endpoint que recebe, valida a dimensionalidade e armazena os valores de explicabilidade (ex: SHAP/LIME) atrelados a cada decisão crítica tomada por um modelo de Machine Learning em produção.
2. **Monitoramento e Bloqueio por Degradação de Confiança:** Uma rotina assíncrona que avalia o *confidence score* das predições e aciona um bloqueio preventivo do modelo caso a confiança média caia abaixo de um limite aceitável em uma janela de tempo específica.

## Justificativa para o uso de SDD
A implementação de um Registry de Auditoria para modelos de Machine Learning é ideal para o Spec-Driven Development devido à sua complexidade lógica e a necessidade de validações matemáticas estritas (como limites de *confidence score* e dimensionalidade de matrizes). A funcionalidade envolve casos de borda como a ausência condicional de explicabilidade em predições de alto risco e o tratamento de *payloads* numéricos malformados. Como a solução exigirá a manipulação de dados complexos em múltiplos arquivos (rotas, esquemas de validação e serviços de negócio), a ausência de uma especificação formal induziria a IA a gerar pipelines limitados (Vibe Coding) que tenderiam a falhariam em um ambiente de produção.