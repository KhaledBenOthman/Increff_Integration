from datetime import date

today = date.today()
def log(text):
    with open("log.txt", "a") as myfile:
        myfile.write(f"{today}: {text} \n")