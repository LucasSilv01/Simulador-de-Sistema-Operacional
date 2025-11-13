
#  Simulador de Sistema Operacional em Python

**Autor:** José Lucas da Silva Cardoso  
**Disciplina:** Sistemas Operacionais  
**Ano:** 2025  

---

## Descrição do Projeto

Este projeto implementa um **simulador de Sistema Operacional (SO)** desenvolvido em **Python**, com foco no **gerenciamento de processos e algoritmos de escalonamento de CPU**.

O simulador permite **criar, listar, bloquear, desbloquear e finalizar processos**, além de executar a simulação dos seguintes **algoritmos de escalonamento**:

- **FIFO (First In, First Out)**
- **SJF (Shortest Job First)**
- **Round Robin (quantum = 2)**
- **Prioridades (1 = mais alta)**

Este projeto tem fins **didáticos**, servindo como ferramenta de apoio ao ensino de **Sistemas Operacionais**.


O terminal entrará no modo interativo:

```
SO>
```

A partir daí, você pode digitar comandos para **criar, listar ou executar processos**.

---

## Exemplo de Uso

### Criando processos

```bash
SO> create Chrome
SO> create Word
SO> create VSCode
```

### Listando processos

```bash
SO> list
```

Saída esperada:

```
PID  Nome     Estado       CPU  Memória  Prioridade
1    Chrome   Pronto        5      32        3
2    Word     Pronto        7      28        1
3    VSCode   Pronto        4      36        2
```

### Executando simulação com Round Robin

```bash
SO> run rr
```

Saída exemplo:

```
Executando Chrome (PID 1)
Quantum expirou! Chrome retornou à fila.
Executando Word (PID 2)
Executando VSCode (PID 3)
Processo 1 finalizado!
Todos os processos finalizados!
```

---

## Tabela de Comandos

| Comando | Sintaxe | Descrição |
|----------|----------|-----------|
| `create` | `create <nome>` | Cria um novo processo. O nome é obrigatório. |
| `list` | `list` | Lista todos os processos e seus estados atuais. |
| `block` | `block <PID>` | Bloqueia o processo com o PID indicado. |
| `unblock` | `unblock <PID>` | Desbloqueia o processo indicado. |
| `kill` | `kill <PID>` | Finaliza imediatamente o processo. |
| `run` | `run <algoritmo>` | Executa a simulação (`fifo`, `sjf`, `rr`, `prio`). |
| `exit` | `exit` | Encerra o simulador. |

---

## Algoritmos de Escalonamento Implementados

### FIFO — *First In, First Out*
O processo **primeiro a chegar** é o **primeiro a ser executado**.  
Não há preempção: o processo roda até terminar.  
Simples, porém pouco eficiente em cenários com processos longos.

<img width="1192" height="444" alt="image" src="https://github.com/user-attachments/assets/ee04c16d-88ea-42b1-a17a-54b69b2f4223" />


### SJF — *Shortest Job First*
O processo com **menor tempo de CPU restante** é escolhido primeiro.  
Reduz o tempo médio de espera, mas pode causar **starvation** (bloqueio) de processos longos.

<img width="1496" height="406" alt="image" src="https://github.com/user-attachments/assets/4d9f1a2d-f090-44c2-a104-4c62717b1530" />


### RR — *Round Robin*
Usa um **quantum fixo (2 ciclos)**.  
Cada processo recebe um pequeno intervalo de CPU antes de retornar à fila.  
Garante **justiça** na distribuição do tempo de CPU entre todos os processos.

<img width="1192" height="520" alt="image" src="https://github.com/user-attachments/assets/4d2543ce-4ee4-4efd-94e0-18e82a4a7dc8" />


### PRIO — *Prioridades*
Cada processo possui uma **prioridade numérica** (1 = mais alta).  
O sistema sempre escolhe o processo de **maior prioridade**.  
Ideal para sistemas com **tarefas críticas**.

<img width="1416" height="406" alt="image" src="https://github.com/user-attachments/assets/ee3e147a-1920-4f75-8a8d-d563a702b7a5" />


---

## Estados dos Processos

| Estado | Descrição |
|---------|------------|
| `Pronto` | Aguardando na fila de execução. |
| `Executando` | Atualmente usando a CPU. |
| `Bloqueado` | Esperando um evento externo (E/S, desbloqueio, etc). |
| `Finalizado` | Processo concluído. |

---

## Objetivos Didáticos

- Demonstrar o funcionamento dos **principais algoritmos de escalonamento de CPU**.
- Simular o **ciclo de vida dos processos** em um ambiente controlado.
- Servir como ferramenta para **estudo e experimentação** de conceitos de **Sistemas Operacionais**.

---

## Conclusão

O simulador cumpre o papel de representar de forma prática e acessível os **conceitos fundamentais de escalonamento de processos**.  
Por meio da interação no terminal, é possível compreender **como diferentes algoritmos afetam o desempenho e a ordem de execução** dos processos em um sistema operacional.

---

> Desenvolvido por **José Lucas da Silva Cardoso** – 2025
