from Client import Clientside

if __name__ == '__main__':
    client = Clientside(url="127.0.0.1:8000", action="poll", target="listen")
    # print(client.c._url)
    client.processData()
    print("5")
