import random
ASCII_LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# --- Functions ---
def get_random_string(length):
    out = ""
    for i in range(length):
        out += random.choice(ASCII_LETTERS)
    return out


def generate_final_expression(preset,data):
    for block in data:
        preset = preset.replace(block[0],block[1])


def get_random_python():
    out = "error"
    statement_type = random.randint(0,4)
    if statement_type == 0:
        out = get_random_string(random.randint(5,10))+" "+random.choice("+-*/%")+"= "+str(random.randint(100, 999999))
    elif statement_type == 1:
        out = get_random_string(random.randint(5,10))+" = "+str(random.randint(100, 999999))+random.choice("+-*/%")
        out += str(random.randint(100, 999999))
    else:
        args = ""
        for i in range(random.randint(0,5)):
            if random.randint(0,1) == 0:
                args += str(random.randint(100, 999999))+","
            else:
                args += "'"+get_random_string(random.randint(5,20))+"',"
        out = random.choice(py_functions)+"("+args+")"
    return out


# load python_functions file
with open("python_functions.txt","r") as f:
    py_functions = f.readlines()
# remove newlines
for tid in range(len(py_functions)):
    py_functions[tid] = py_functions[tid].rstrip().lower()

if __name__ == '__main__':
    for i in range(100):
        print(get_random_python())
