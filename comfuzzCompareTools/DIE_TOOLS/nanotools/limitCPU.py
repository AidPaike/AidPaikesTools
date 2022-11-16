import psutil

count = psutil.cpu_count()
p = psutil.Process()
p.cpu_affinity([11, 12, 13, 14, 15, 16])