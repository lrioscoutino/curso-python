from process_manager import ProcessManager


if __name__ == "__main__":
    process_manager = ProcessManager()
    monitor = ProcessManager()
    # Monitorear procesos por 10 segundos
    monitor.monitor(duration=10)
    # Mostrar los 5 procesos que más CPU usan
    monitor.display_top_processes(5)
