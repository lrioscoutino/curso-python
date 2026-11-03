import psutil  # Librería para obtener información de procesos del sistema
import time    # Para manejar intervalos de tiempo
from tabulate import tabulate  # Para crear tablas formateadas en consola
from datetime import datetime  # Para timestamp de los procesos


class ProcessManager:
    def __init__(self):
        self.process_history = []

    def get_process_info(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                process_info = proc.info
                process_info['timestamp'] = datetime.now()
                processes.append(process_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return processes

    def monitor(self, duration=10, interval=1):
        """Monitorea procesos por una duración específica"""
        end_time = time.time() + duration
        while time.time() < end_time:
            self.process_history.append(self.get_process_info())
            time.sleep(interval)

    def get_top_cpu_processes(self, n=5):
        """Obtiene los n procesos con mayor uso de CPU"""
        if not self.process_history:
            return []

        latest_snapshot = self.process_history[-1]
        sorted_processes = sorted(latest_snapshot,
                                  key=lambda x: x['cpu_percent'],
                                  reverse=True)
        return sorted_processes[:n]

    def display_top_processes(self, n=5):
        top_processes = self.get_top_cpu_processes(n)
        headers = ['PID', 'Name', 'CPU %', 'Memory %']
        table_data = [[p['pid'], p['name'],
                       f"{p['cpu_percent']:.1f}",
                       f"{p['memory_percent']:.1f}"]
                      for p in top_processes]

        print("\nTop Procesos por Uso de CPU:")
        print(tabulate(table_data, headers=headers, tablefmt='grid'))

    def measure_cpu_time(self, pid):
        """
        TODO: Implementar medición de tiempo de CPU para un proceso específico
        - Usar psutil.Process(pid)
        - Calcular tiempo de usuario y sistema
        - Retornar resultados en formato legible
        """
        pass


    def analyze_memory_usage(self, pid):
        """
        TODO: Implementar análisis detallado de uso de memoria
        - Medir RSS y VSZ
        - Calcular páginas en memoria
        - Detectar posibles memory leaks
        """
        pass