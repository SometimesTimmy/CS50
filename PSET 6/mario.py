import cs50

def main():
    while True:
            print("Height: ", end="")
            h = cs50.get_int()
            if h > 0 and h <= 23:
                break

    for i in range(h):
        for j in range(h - i - 1):
            print(" ", end = "")
        for k in range(i+1):
            print("#", end = "")
        print("  ", end = "")
        for l in range(i+1):
            print("#", end = "")
        print("")

if __name__ == "__main__":
    main()