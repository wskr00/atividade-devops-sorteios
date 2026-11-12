# Relatório — Atividade DevOps na prática

## Objetivo e solução

Foi preparado um projeto de API de sorteios em FastAPI para demonstrar integração, entrega, implantação e observabilidade. A API possui endpoints de identificação, saúde e sorteio, valida os parâmetros e registra cada requisição em JSON com horário, método, rota, status, duração e versão. Pytest cobre respostas válidas, inválidas e o formato essencial dos logs.

## Etapas

1. **Conceitos:** DevOps aproxima desenvolvimento e operações e apoia entregas ágeis por automação e feedback. CI testa integrações; Continuous Delivery prepara liberações e Continuous Deployment as executa automaticamente. Containers compartilham o kernel e empacotam dependências; VMs incluem sistema operacional próprio. O README detalha os exemplos.
2. **CI e imagem:** o workflow executa testes, cria uma imagem e publica no GHCR com `GITHUB_TOKEN` e tag do commit. [Execução real bem-sucedida](https://github.com/wskr00/atividade-devops-sorteios/actions/runs/43288731141). [Inserir print real da execução para a entrega.]
3. **Kubernetes e Helm:** o workflow cria Kind temporário, carrega a imagem publicada, instala o chart, verifica o rollout e testa a API via Service NodePort e port-forward. O cluster é destruído ao fim do job; não é deploy em cluster persistente ou produção. Na execução validada, o release ficou `deployed`, o pod ficou `1/1 Running`, o rollout concluiu e `/health` e `/sortear` responderam. [Inserir print real desses trechos no log do Actions.]
4. **Observabilidade:** em demonstração local independente, a mesma API escreve logs JSON em volume; Filebeat lê e envia ao Elasticsearch; Kibana mostra logs, contagens por status e tempo médio. [Captura real do dashboard](evidencias/dashboard-kibana.jpg).
5. **Apresentação:** o roteiro está em `docs/apresentacao.md` e cabe em até 10 minutos.

## Dificuldades e validação

Na preparação, os quatro testes passaram e o Helm validou o chart. O Pytest exibiu um aviso de depreciação de uma dependência indireta, sem falhar. A imagem da API foi construída e o Compose iniciado; o Filebeat enviou 18 eventos reais ao Elasticsearch (11 com status 200, 4 com 400 e 3 com 422), e a API de status do Kibana informou disponibilidade. O dashboard foi montado e conferido com logs recentes, contagem por status e tempo médio. A busca tradicional do Discover apresentou erro ao ser incorporada no Kibana 8.17.4; substituímos por uma consulta ES|QL validada. As duas primeiras publicações GHCR falharam com `denied` ao enviar um manifesto com attestation; uma imagem sem essa attestation e com metadado do repositório conseguiu publicar. O workflow foi executado com sucesso no repositório privado, incluindo publicação e deploy efêmero; os logs registram a limpeza do cluster. O Actions também emitiu aviso de depreciação do Node.js 20 para ações de terceiros, sem impedir a execução. Acrescente aqui outras dificuldades efetivamente encontradas durante a execução e os resultados reais; consulte o README para comandos e evidências.

## Reflexão

Testes, empacotamento e verificações repetíveis reduzem falhas manuais e aceleram o feedback. Logs e indicadores permitem investigar o comportamento depois da execução. O exemplo demonstra essas práticas em escala pequena; disponibilidade, segurança, retenção e operação de produção exigiriam planejamento adicional.
