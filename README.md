# Atividade DevOps: API de sorteios

Projeto simples em Python/FastAPI com testes, imagem Docker, GitHub Actions, Helm/Kind e observabilidade local com Elastic Stack. Não usa banco, frontend ou autenticação.

## 1. Conceitos fundamentais

DevOps aproxima desenvolvimento e operações por meio de colaboração, automação e feedback rápido. Complementa metodologias ágeis: entregas pequenas e frequentes são construídas, testadas e observadas continuamente. **CI** integra alterações com build e testes automáticos. **Continuous Delivery** mantém a aplicação pronta para uma liberação, que pode exigir decisão humana. **Continuous Deployment** libera automaticamente cada alteração aprovada pelos testes para o ambiente de destino.

Uma máquina virtual inclui um sistema operacional convidado completo sobre um hypervisor; é útil para isolar sistemas operacionais diferentes, mas tende a consumir mais recursos. Um container compartilha o kernel do host e empacota aplicação e dependências, iniciando geralmente mais rápido e de forma reproduzível. Aqui a API é empacotada em container e executada no Kind e no Compose.

## 2. Executar e testar localmente

Requisitos: Python 3.12, Docker com Compose; para o deploy de demonstração, conta GitHub com Actions e GHCR habilitados. Na raiz do projeto:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest -q
uvicorn app.main:app --host 127.0.0.1 --port 8000 --no-access-log
```

Em outro terminal:

```bash
curl http://localhost:8000/
curl http://localhost:8000/health
curl 'http://localhost:8000/sortear?min=1&max=100'
curl -i 'http://localhost:8000/sortear?min=10&max=1'
```

Os limites são inclusivos; `min > max` retorna 400 e valores não inteiros retornam 422. `min` e `max` são opcionais e valem 1 e 100 por padrão. Pare o uvicorn com Ctrl+C antes de iniciar a API do Compose na mesma porta.

## 3. GitHub Actions, GHCR e Kind

Crie um repositório GitHub vazio e, dentro desta pasta, execute (substitua a URL):

```bash
git init -b main
git add .
git commit -m "Implementa atividade DevOps"
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

Na aba **Actions**, abra a execução `Testar, publicar e demonstrar deploy`. O workflow também pode ser iniciado em **Run workflow**. Em Settings → Actions → General, permita o uso do Actions; a política da organização precisa permitir as ações utilizadas e a publicação de packages. O workflow solicita somente `contents: read` e `packages: write` e usa `GITHUB_TOKEN`, sem token pessoal no código. Se o pacote GHCR já existir e pertencer a outro repositório, ajuste o acesso do repositório ao pacote em Package settings → Manage Actions access. A imagem usa `ghcr.io/<dono>/<repositório>:<SHA-do-commit>` em minúsculas no nome. A visibilidade pública do pacote não é necessária.

O job executa testes, cria e publica a imagem e faz `docker pull` autenticado. Cria um Kind **no runner**, carrega essa imagem no cluster e instala o chart com `IfNotPresent`. O Service é NodePort; o smoke test acessa o Service com port-forward. Veja no passo **Instalar aplicação e verificar deploy** a saída de `helm status`, `kubectl get pods,svc`, `kubectl rollout status` e as respostas de `/health` e `/sortear`. Capture um print real desses trechos e outro da execução concluída.

**Limitação:** o cluster é descartado ao final do job. Cada push cria outro cluster e instala novamente; não há atualização de cluster persistente nem deploy contínuo em produção. A stack Compose abaixo é uma demonstração independente da mesma API; ela não coleta logs do Kind no Actions.

## 4. Observabilidade local

Docker/Compose e recursos suficientes para Elasticsearch e Kibana são necessários. A configuração desativa a segurança do Elasticsearch **apenas para esta demonstração local**; Elasticsearch e Kibana são publicados somente no localhost. Na raiz do projeto:

```bash
docker compose up -d --build
docker compose ps
```

Aguarde o Kibana ficar pronto em http://localhost:5601 (pode levar alguns minutos). Gere tráfego real:

```bash
for i in $(seq 1 20); do curl -s 'http://localhost:8000/sortear?min=1&max=100' > /dev/null; done
for i in $(seq 1 5); do curl -s 'http://localhost:8000/sortear?min=10&max=1' > /dev/null; done
for i in $(seq 1 5); do curl -s 'http://localhost:8000/sortear?min=abc' > /dev/null; done
curl -s 'http://localhost:9200/sorteios-*/_count?pretty'
```

A API grava uma linha JSON por requisição em um volume compartilhado; o Filebeat lê esse arquivo, interpreta o JSON e envia os eventos ao Elasticsearch. Cada linha contém `timestamp`, `method`, `route`, `status`, `duration_ms` e `version`. O stdout também recebe os mesmos eventos. O Filebeat mantém sua posição em um volume para evitar reler tudo a cada reinício.

### Dashboard no Kibana

1. Abra **Stack Management → Data Views → Create data view**. Nome e padrão: `sorteios-*`; campo de tempo: `timestamp`. Salve. Se o padrão não aparecer, gere tráfego, aguarde alguns segundos e verifique `docker compose logs filebeat` e o `_count` acima.
2. Em **Discover**, escolha `sorteios-*`, período **Last 15 minutes** e adicione as colunas `timestamp`, `method`, `route`, `status`, `duration_ms` e `version`. Clique **Save**, nomeie `Logs recentes`.
3. Em **Dashboard → Create dashboard → Add from library**, adicione `Logs recentes`.
4. Clique **Create visualization** (Lens); selecione o data view `sorteios-*`. Para contagem por status, escolha gráfico de barras, eixo horizontal `status` com agregação **Top values**, eixo vertical **Count of records**. Salve como `Requisições por status` e retorne ao dashboard.
5. Crie outra visualização Lens: gráfico de linha, eixo horizontal `timestamp` com **Date histogram**, eixo vertical `duration_ms` com agregação **Average**. Salve como `Tempo médio de resposta (ms)` e adicione ao dashboard.
6. Ajuste o período para **Last 15 minutes**, clique em **Save**, nomeie `Observabilidade de sorteios` e capture um print real mostrando os três painéis e os eventos 200, 400 e 422. Se necessário, atualize o dashboard depois de gerar tráfego novamente.

Para parar os serviços sem apagar dados: `docker compose down`. Para apagar também logs e índices desta demonstração: `docker compose down -v`. Para diagnosticar: `docker compose logs --tail=100 api filebeat elasticsearch kibana`.

## 5. Entrega e apresentação

Veja [docs/relatorio.md](docs/relatorio.md) e [docs/apresentacao.md](docs/apresentacao.md). Insira prints reais após executar as demonstrações; não há evidências fabricadas neste projeto.
