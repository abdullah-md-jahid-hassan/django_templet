import fakeredis

def main():
    print("Starting in-memory Redis TCP server on 127.0.0.1:6379...")
    server = fakeredis.TcpFakeServer(("127.0.0.1", 6379))
    server.serve_forever()

if __name__ == "__main__":
    main()
