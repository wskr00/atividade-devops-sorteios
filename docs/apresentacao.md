# Roteiro de apresentação — até 10 minutos

- **0:00–1:00 — Conceitos:** relação entre DevOps e ágil; CI, Delivery e Deployment; diferença entre VM e container.
- **1:00–2:00 — API e testes:** mostrar os três endpoints, uma requisição válida e outra inválida; explicar testes e campos dos logs.
- **2:00–4:00 — Actions e GHCR:** abrir uma execução real na aba Actions; mostrar testes, build, publicação e tag do commit. Capturar print da execução.
- **4:00–6:00 — Helm e Kind:** mostrar chart, Service NodePort e, no log do job, `helm status`, pods/services, rollout e respostas HTTP. Explicar que o Kind é efêmero e não representa um deploy em produção. Capturar print dos comandos e respostas.
- **6:00–8:30 — Observabilidade local:** mostrar serviços do Compose, gerar tráfego válido e inválido, abrir dashboard do Kibana com logs, contagem por status e tempo médio. Explicar que Filebeat lê o volume compartilhado. Capturar print do dashboard.
- **8:30–10:00 — Reflexão:** explicar feedback rápido, repetibilidade e limites; comentar dificuldades reais e solução.

Se a execução ao vivo falhar, mostre o estado real e relate o que faltou validar; não apresente evidências inventadas.
