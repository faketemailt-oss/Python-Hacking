import platform,socket,time,psutil
def collect(): return {"os":platform.system(),"os_release":platform.release(),"architecture":platform.machine(),"hostname":socket.gethostname(),"python":platform.python_version(),"boot_time":psutil.boot_time(),"collected_at":time.time()}
