**Plano de Implementação DevOps — Tech**  
Ivan de Souza Neto \- 17/11/2026

**0\. Método**   
Avaliei cada processo da Tech com base nas cinco dimensões do CALMS. Para cada situação, identifiquei o fato, o problema causado, a proposta de melhoria e a métrica de acompanhamento.

**1\. Diagnóstico cultural** 

Segue o diagnóstico encontrado com base no relato da Tech.

| Lente | Fato | Problema |
| :---: | ----- | :---: |
| C | Dev encaminha o pacote para operações. | Entrega sem responsabilidade. |
| A | Deploy manual, sem padrão. | 20% de falha ocasionada no deploy. |
| L | 2 dias entre o código pronto e o deploy. | Atraso na resolução dos problemas relatados na plataforma, gerando uma demora de 2 dias para qualquer deploy da plataforma. |
| M | Testes e monitoramento só depois do deploy. | Impacto direto no cliente, devido ao deploy ser em produção, sendo 2 incidentes por semana com média de 4 horas de resolução. |
| S | Só uma pessoa sabe Delphi. | Centralização e sobrecarga da operação em apenas 1 ponto focal. |

**Riscos do sistema legado:**  
	Nesse sistema está centralizado todo o processo de controle de estoque, emissão de notas fiscais e relatórios de vendas, além da centralização e sobrecarga dos processos em apenas uma pessoa.   
	Isso se torna um risco muito grande caso a empresa precise abrir mão deste funcionário (seja por falecimento, doença, demissão ou algo que faça com que ele se ausente de alguma forma). Vale ressaltar que atualmente o time é de 14 desenvolvedores, sendo que apenas 1 deles conhece Delphi.   
	Atualmente, a Tech se encontra totalmente dependente deste funcionário para manter o fluxo atual de funcionamento. Se o sistema parar, a empresa fica sem emitir nota (o que é algo obrigatório) e também sem o controle do estoque, sendo um risco muito alto.

**2\. Automação (A)**

A primeira viabilização seria o deploy automático para o e-commerce após a validação dos testes e homologação. Com isso, o trabalho manual de deploy diminui de forma geral para qualquer atualização ou também para resolução de problemas, reduzido o tempo entre o código pronto e o deploy de 2 dias para menos de 1 dia.  
	O primeiro processo a se automatizar seria o e-commerce, já que todo o time domina as linguagens usadas nele. Se a automação der problema, o time inteiro consegue corrigir. Como o sistema legado é de alto risco, ele entraria após o primeiro projeto já ter melhorias no processo e quando ocorrer a descentralização do conhecimento em Delphi \- tanto na aprendizagem do time quanto na documentação.

**Plano em fases:**  
	Até 30 dias: colocar o código do e-commerce no Git, para controle de versionamento, e criar os primeiros testes automáticos.  
	Até 60 dias: criar o ambiente de homologação, a fim de validar todos os deploys antes de entrarem em produção.  
	Até 90 dias: ativar o deploy automático em produção e começar a acompanhar semanalmente as métricas da seção 3\.

**Redução de resistência:**  
	Para evitar resistência, a equipe de operações participará da construção da esteira desde o início, porque é quem mais conhece os problemas de produção, e isso melhora a comunicação entre os times. O papel dela deixa de ser executar deploys e testes manuais e passa a ser cuidar da esteira e do monitoramento. Os desenvolvedores, por sua vez, passam a acompanhar o comportamento do código em produção, encerrando a "entrega sem responsabilidade".

**3\. Medição e compartilhamento (M e S)**

| Métrica | O que mede | Hoje | Meta | Prazo |
| :---: | :---: | :---: | :---: | :---: |
| Lead time | Tempo do código pronto até o deploy | 2 dias | Menos de 1 dia | 90 dias |
| Taxa de sucesso dos deploys | Quantos deploys dão certo | 80% | 95% | 90 dias |
| Incidentes após o deploy | Quantos problemas por semana | 2 por semana | 1 a cada 15 dias | 90 dias |
| MTTR | Tempo médio para resolver um incidente | 4 horas | Menos de 2 horas | 90 dias |

**3.2 A métrica que falta:**  
O cenário não informa a frequência de deploy, quarta métrica do padrão DORA. Ela importa porque mostra o ritmo de entregas da empresa: deploys frequentes são menores, mais fáceis de testar e, se falharem, mais rápidos de corrigir. A Tech deve começar a medir agora e, após a automação, buscar pelo menos 1 deploy por dia no e-commerce.

**3.3 Plano de compartilhamento:**

* Documentação: o passo a passo do deploy (runbook) ficará no GitHub, junto do código, e cada deploy terá o registro do que mudou, seja uma correção ou uma novidade.  
* Post-mortem: após cada incidente, o time registra o que aconteceu, a causa e como evitar que se repita, sem procurar culpados, focando no processo.  
* Delphi: o desenvolvedor que conhece Delphi trabalhará em dupla com outros 2 desenvolvedores nas tarefas do legado, enquanto documenta o sistema. Assim, o conhecimento deixa de depender de uma pessoa só.

**4\. As Três Maneiras**

* Primeira (fluxo): a esteira automática reduz o lead time de 2 dias para menos de 1 dia.  
* Segunda (feedback): os testes automáticos e o ambiente de homologação avisam o erro antes do cliente, e o monitoramento com alertas detecta rapidamente o que escapar, reduzindo o MTTR.  
* Terceira (aprender): o post-mortem sem culpados transforma cada falha em aprendizado, e o piloto no e-commerce funciona como experimento: o que der certo será levado ao legado.

**5\. Resumo** 

A Tech precisa sair de um processo manual e concentrado em poucas pessoas para um fluxo automatizado e compartilhado. Hoje, 20% dos deploys falham, os testes e o monitoramento só acontecem depois que o código já está em produção, o que gera 2 incidentes por semana com 4 horas de resolução, e todo o sistema legado depende de um único desenvolvedor que conhece Delphi.

A proposta é implantar uma esteira automática no e-commerce, com testes, ambiente de homologação e deploy automático, para reduzir as falhas e o tempo de entrega. Em paralelo, o conhecimento do legado será compartilhado com o restante do time, por meio de trabalho em dupla e documentação, e um monitoramento com alertas passará a detectar rapidamente os erros que escaparem dos testes.

O primeiro passo, nos próximos 30 dias, é versionar o código do e-commerce no Git e criar os primeiros testes automáticos, acompanhando a evolução semanalmente pelas métricas da seção 3\.

