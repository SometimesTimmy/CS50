import cs50

def main():
    print("Number: ", end="")
    Number = cs50.get_int()
    if Number < 0:
        print("INVALID")

    n_count = Number # n_count is a dummy copy for counting digit length
    digits = 0 # digits is the counter

    while n_count >= 1:
        n_count = n_count/10
        digits += 1

    if not digits == 13 and not digits == 15 and not digits == 16:
        print("INVALID")

    n2 = 0 # n2 is the individual ever other digit starting with the second to last digit
    sum_n2 = 0
    Number2 = Number/10 # Number2 is the dummy copy for n2

    while Number2 > 10:
        n2 = Number2%10
        Number2 = Number2/100

        if n2*2 == 10:
            sum_n2 += 1

        if n2*2 < 10:
            sum_n2 = sum_n2 + n2*2

        if n2*2 > 10:
            sum_n2 = sum_n2 + n2*2%10 + 1

    n1 = 0 # n1 is the individual ever other digit starting with the last digit
    Number1 = Number; #Number 1 is the dummy copy for n1

    sum_n1 = 0
    while Number1 > 0:
        n1 = Number1%10
        Number1 = Number1/100
        sum_n1 = sum_n1 + n1

    # the below two lines were written for testing purpose
    # if (sum_n1+sum_n2)%10 == 0:
        # print("This is a valid card, and you have finished the HW!")

    # American Express uses 15-digit numbers,
    # MasterCard uses 16-digit numbers,
    # and Visa uses 13- and 16-digit numbers
    if digits == 15:
        print("AMEX")
    if digits == 16:
        if Number/1000000000000000 == 5:
            print("MASTERCARD")
        if Number/1000000000000000 < 5:
            print("VISA")
    if digits == 13:
        print("VISA")

if __name__ == "__main__":
    main()