from concurrent.futures import ThreadPoolExecutor

image_loader = ThreadPoolExecutor(max_workers=2)
