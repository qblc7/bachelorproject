# executable
from SSEendpoint import SSEendpoint

if __name__ == '__main__':
    server = SSEendpoint(8080)
    server.startServer()
    #server.robotConnect(host='172.17.0.2', port=30004, frequency=50, config='recipe.xml', buffered=True, output='robot_data.csv', binary=False)