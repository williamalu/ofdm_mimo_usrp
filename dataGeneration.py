import numpy as np

data_length = 1000

data = np.random.randint(2, size=data_length)
data = np.array_str(data, max_line_width=2*data_length)

data = data.replace("[", "")
data = data.replace("]", "")
data = data.replace(" ", "")

with open("data.txt", "w") as f:
    f.write(data)
