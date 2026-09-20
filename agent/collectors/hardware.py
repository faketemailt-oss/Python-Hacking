import platform,psutil
def collect():
 m=psutil.virtual_memory(); return {"cpu_logical":psutil.cpu_count(),"cpu_physical":psutil.cpu_count(logical=False),"cpu_percent":psutil.cpu_percent(interval=0.1),"memory_total":m.total,"memory_available":m.available,"machine":platform.machine(),"processor":platform.processor()}
