import base64

f = 'FgMDAJwBAACYAwNgUrIiQ23GNQ0ypQrI2IAos8MWHzqrm2HzcpGEwJ1M/wAAFsAUADXAEwAvwCzAK8AwAJ3ALwCcAAoBAABZAAoAFgAUABcAGAAZAAkACgALAAwADQAOABYACwACAQAADQAcABoGAwYBBQMFAQQDBAEEAgMDAwEDAgIDAgECAgAAABAADgAAC3d3dy43eWlwLmNu/wEAAQA='
g = 'FgMDAKABAACcAwNgOJe74Ak3NZhxiQc+c4B1qUluUdIRuw88nYD0/GBaAAAAFsAUADXAEwAvwCzAK8AwAJ3ALwCcAAoBAABdAAoAFgAUABcAGAAZAAkACgALAAwADQAOABYACwACAQAADQAcABoGAwYBBQMFAQQDBAEEAgMDAwEDAgIDAgECAgAAABQAEgAAD3Rvb2xzLmJuc3pzLmNvbf8BAAEA'
import base64

Y_str = "ZmxhZ3ttYWZha3VhaWxhaXFpYW5kYW9ifQ=="
# Y_str = f
Y_str = g
J_str = base64.b64decode(Y_str)
print(J_str.decode(encoding='utf-8', errors='ignore'))
