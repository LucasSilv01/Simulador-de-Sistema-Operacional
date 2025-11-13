from enum import Enum
from typing import List, Optional
from collections import deque
import random
import time


class ProcessState(Enum):
    """Estados possíveis de um processo."""
    PRONTO = "Pronto"
    EXECUTANDO = "Executando"
    BLOQUEADO = "Bloqueado"
    FINALIZADO = "Finalizado"


class Process:
    """Representa um processo no sistema operacional."""
    
    def __init__(self, pid: int, name: str, cpu_time: int, memory: int, priority: int):
        self.pid = pid
        self.name = name
        self.cpu_time = max(1, cpu_time)
        self.cpu_remaining = self.cpu_time
        self.memory = memory
        self.priority = priority
        self.state = ProcessState.PRONTO
        self.arrival_time = time.time()
        self.finish_time: Optional[float] = None

    def __repr__(self):
        return f"<Process pid={self.pid} name={self.name} state={self.state.value}>"

    @property
    def turnaround_time(self) -> Optional[float]:
        """Tempo total até finalização."""
        if self.finish_time:
            return self.finish_time - self.arrival_time
        return None

    @property
    def waiting_time(self) -> Optional[float]:
        """Tempo de espera (turnaround - CPU real)."""
        if self.turnaround_time:
            return self.turnaround_time - self.cpu_time
        return None


class OperatingSystem:
    """Simulador de um Sistema Operacional didático."""
    
    def __init__(self, quantum: int = 2):
        self.processes: List[Process] = []
        self.next_pid = 1
        self.quantum = quantum
        self.rr_queue = deque()  # fila persistente de Round Robin

    # -------------------------------
    # CRUD de Processos
    # -------------------------------

    def create_process(self, name: str, cpu_time: int = 5, memory: int = 100, priority: int = 3) -> Process:
        """Cria um novo processo e adiciona à fila RR."""
        process = Process(self.next_pid, name, cpu_time, memory, priority)
        self.processes.append(process)
        self.rr_queue.append(process)
        self.next_pid += 1
        print(f"Processo criado: PID={process.pid}, Nome={process.name}, CPU={cpu_time}, MEM={memory}, PRIO={priority}")
        return process

    def list_processes(self):
        """Lista todos os processos e seus estados."""
        if not self.processes:
            print("Nenhum processo criado.")
            return
        
        print("\nPID | Nome           | CPU (restante/total) | MEM | PRIO | Estado")
        print("-" * 65)
        for p in self.processes:
            print(f"{p.pid:3} | {p.name:14} | {p.cpu_remaining:2}/{p.cpu_time:2}               | "
                  f"{p.memory:3} | {p.priority:4} | {p.state.value}")

    def get_process_by_pid(self, pid: int) -> Optional[Process]:
        """Busca um processo pelo PID."""
        return next((p for p in self.processes if p.pid == pid), None)

    # -------------------------------
    # Controle de Estado
    # -------------------------------

    def block_process(self, pid: int):
        """Bloqueia um processo."""
        process = self.get_process_by_pid(pid)
        if not process:
            print(f"Processo {pid} não encontrado.")
            return
        if process.state == ProcessState.FINALIZADO:
            print(f"Processo {pid} já está finalizado.")
            return
        process.state = ProcessState.BLOQUEADO
        print(f"Processo {pid} bloqueado.")

    def unblock_process(self, pid: int):
        """Desbloqueia um processo."""
        process = self.get_process_by_pid(pid)
        if not process:
            print(f"Processo {pid} não encontrado.")
            return
        if process.state == ProcessState.BLOQUEADO:
            process.state = ProcessState.PRONTO
            print(f"Processo {pid} desbloqueado.")
        else:
            print(f"Processo {pid} não está bloqueado.")

    def kill_process(self, pid: int):
        """Encerra um processo."""
        process = self.get_process_by_pid(pid)
        if not process:
            print(f"Processo {pid} não encontrado.")
            return
        process.state = ProcessState.FINALIZADO
        process.cpu_remaining = 0
        process.finish_time = time.time()
        print(f"Processo {pid} encerrado.")

    # -------------------------------
    # Seleção de Processos
    # -------------------------------

    def get_ready_processes(self) -> List[Process]:
        return [p for p in self.processes if p.state == ProcessState.PRONTO]

    def select_next_process_fifo(self) -> Optional[Process]:
        ready = self.get_ready_processes()
        return ready[0] if ready else None

    def select_next_process_sjf(self) -> Optional[Process]:
        ready = self.get_ready_processes()
        return min(ready, key=lambda p: p.cpu_remaining) if ready else None

    def select_next_process_prio(self) -> Optional[Process]:
        ready = self.get_ready_processes()
        return min(ready, key=lambda p: p.priority) if ready else None

    def select_next_process_rr(self) -> Optional[Process]:
        """Round Robin persistente com fila rotativa."""
        while self.rr_queue:
            proc = self.rr_queue.popleft()
            if proc.state == ProcessState.PRONTO:
                return proc
        return None

    # -------------------------------
    # Execução da Simulação
    # -------------------------------

    def run_simulation(self, algorithm: str = "fifo"):
        """Executa a simulação com o algoritmo escolhido."""
        algorithm = algorithm.lower()
        print(f"\nExecutando simulação por {algorithm.upper()}...\n")

        cycle = 0

        while True:
            ready = self.get_ready_processes()

            if not ready:
                non_finalized = [p for p in self.processes if p.state != ProcessState.FINALIZADO]
                if not non_finalized:
                    print("\n✓ Todos os processos finalizados!")
                else:
                    print("\n⚠ Nenhum processo PRONTO. Existem processos bloqueados ou em espera.")
                break

            # Seleciona processo
            if algorithm == "fifo":
                current = self.select_next_process_fifo()
            elif algorithm == "sjf":
                current = self.select_next_process_sjf()
            elif algorithm == "prio":
                current = self.select_next_process_prio()
            elif algorithm == "rr":
                current = self.select_next_process_rr()
                if current:
                    self.rr_queue.append(current)  # reenqueue para o final
            else:
                print(f"Algoritmo '{algorithm}' inválido.")
                return

            if not current:
                break

            # Executa uma unidade de CPU
            current.state = ProcessState.EXECUTANDO
            current.cpu_remaining -= 1
            cycle += 1
            print(f"→ Ciclo {cycle}: Executando {current.name} (PID {current.pid}) | Restante: {current.cpu_remaining}")

            # Finaliza se necessário
            if current.cpu_remaining <= 0:
                current.state = ProcessState.FINALIZADO
                current.finish_time = time.time()
                print(f"   ✓ Processo {current.pid} finalizado!")
            else:
                current.state = ProcessState.PRONTO

        print(f"\nSimulação concluída em {cycle} ciclos!\n")
        self.show_metrics()

    # -------------------------------
    # Métricas
    # -------------------------------

    def show_metrics(self):
        """Exibe métricas de desempenho."""
        print("\n--- Métricas de Processos ---")
        for p in self.processes:
            t = p.turnaround_time
            w = p.waiting_time
            print(f"PID {p.pid:2} | {p.name:10} | Estado: {p.state.value:11} | "
                  f"Turnaround: {t:.2f}s | Espera: {w:.2f}s" if t else
                  f"PID {p.pid:2} | {p.name:10} | Estado: {p.state.value}")


# -------------------------------
# Interface CLI
# -------------------------------

def main():
    os_sim = OperatingSystem()

    print("=" * 60)
    print("  SIMULADOR DE SISTEMA OPERACIONAL - VERSÃO MELHORADA")
    print("=" * 60)
    print("\nComandos disponíveis:")
    print("  create <nome> [cpu] [mem] [prio]  - Cria um processo")
    print("  list                              - Lista todos os processos")
    print("  run <algoritmo>                   - Executa escalonamento (fifo, sjf, rr, prio)")
    print("  block <PID>                       - Bloqueia um processo")
    print("  unblock <PID>                     - Desbloqueia um processo")
    print("  kill <PID>                        - Encerra um processo")
    print("  exit                              - Encerra o sistema\n")

    while True:
        try:
            command = input("SO> ").strip()
            if not command:
                continue

            parts = command.split()
            cmd = parts[0].lower()

            if cmd == "create":
                if len(parts) < 2:
                    print("Uso: create <nome> [cpu] [mem] [prio]")
                    continue
                name = " ".join(parts[1:-3]) if len(parts) > 4 else parts[1]
                try:
                    cpu = int(parts[-3]) if len(parts) >= 4 else random.randint(3, 8)
                    mem = int(parts[-2]) if len(parts) >= 5 else random.randint(50, 200)
                    prio = int(parts[-1]) if len(parts) >= 6 else random.randint(1, 5)
                except ValueError:
                    cpu, mem, prio = random.randint(3, 8), random.randint(50, 200), random.randint(1, 5)
                os_sim.create_process(name, cpu, mem, prio)

            elif cmd == "list":
                os_sim.list_processes()

            elif cmd == "run":
                if len(parts) < 2:
                    print("Uso: run <fifo|sjf|rr|prio>")
                    continue
                os_sim.run_simulation(parts[1])

            elif cmd == "block":
                os_sim.block_process(int(parts[1]))

            elif cmd == "unblock":
                os_sim.unblock_process(int(parts[1]))

            elif cmd == "kill":
                os_sim.kill_process(int(parts[1]))

            elif cmd == "exit":
                print("Encerrando o sistema...")
                break

            else:
                print(f"Comando '{cmd}' não reconhecido.")

        except Exception as e:
            print(f"Erro: {e}")


if __name__ == "__main__":
    main()