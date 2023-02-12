
def check():
    prohibited_list = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '.', '+', '-', ' ', ',']
    surname = 'sdfdf$#'
    print(surname)
    for item in prohibited_list:
        print(item)
        if item in surname:
            print('yes')
            return True
        else:
            pass

check()