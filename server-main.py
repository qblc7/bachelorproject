# executable
from SSEendpoint import SSEendpoint

if __name__ == '__main__':
    server = SSEendpoint(8000)
    print("1")
    server.startServer()
    print("3")
