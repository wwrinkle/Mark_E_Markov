def log(message, data=None):
    line = "=" * (len(message) + 4)
    print(line)
    print(f"= {message} =")

    if data is not None:
        print("DATA:")
        print(data)

    print(line)
