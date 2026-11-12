# Relatório — Atividade DevOps na prática

## Objetivo e solução

Foi preparado um projeto de API de sorteios em FastAPI para demonstrar integração, entrega, implantação e observabilidade. A API possui endpoints de identificação, saúde e sorteio, valida os parâmetros e registra cada requisição em JSON com horário, método, rota, status, duração e versão. Pytest cobre respostas válidas, inválidas e o formato essencial dos logs.

## Etapas

1. **Conceitos:** DevOps aproxima desenvolvimento e operações e apoia entregas ágeis por automação e feedback. CI testa integrações; Continuous Delivery prepara liberações e Continuous Deployment as executa automaticamente. Containers compartilham o kernel e empacotam dependências; VMs incluem sistema operacional próprio. O README detalha os exemplos.
2. **CI e imagem:** o workflow executa testes, cria uma imagem e publica no GHCR com `GITHUB_TOKEN` e tag do commit. [Inserir print real da execução bem-sucedida.]
3. **Kubernetes e Helm:** o workflow cria Kind temporário, carrega a imagem publicada, instala o chart, verifica o rollout e testa a API via Service NodePort e port-forward. O cluster é destruído ao fim do job; não é deploy em cluster persistente ou produção. [Inserir print real de helm status, pods, service e smoke test no log do Actions.]
4. **Observabilidade:** em demonstração local independente, a mesma API escreve logs JSON em volume; Filebeat lê e envia ao Elasticsearch; Kibana mostra logs, contagens por status e tempo médio. [Inserir print real do dashboard.]
5. **Apresentação:** o roteiro está em `docs/apresentacao.md` e cabe em até 10 minutos.

## Dificuldades e validação

Na preparação, os quatro testes passaram e o Helm validou o chart. O Pytest exibiu um aviso de depreciação de uma dependência indireta, sem falhar. A imagem da API foi construída e o Compose iniciado; o Filebeat enviou 18 eventos reais ao Elasticsearch (11 com status 200, 4 com 400 e 3 com 422), e a API de status do Kibana informou disponibilidade. O dashboard ainda precisa ser montado e conferido na interface. O workflow do GitHub precisa ser executado no repositório de destino para comprovar publicação e deploy. Acrescente aqui outras dificuldades efetivamente encontradas durante a execução e os resultados reais; consulte o README para comandos e evidências.

## Reflexão

Testes, empacotamento e verificações repetíveis reduzem falhas manuais e aceleram o feedback. Logs e indicadores permitem investigar o comportamento depois da execução. O exemplo demonstra essas práticas em escala pequena; disponibilidade, segurança, retenção e operação de produção exigiriam planejamento adicional.
