import math

vectors = [
    [44.55, 0, 21, 6.24],
    [6.6, 53.46, 0, 68.64],
    [39.6, 46.98, 25.5, 0]
]

s = '{:.4f}'

for vec in vectors:
    sum = 0

    for element in vec:
        sum += math.pow(element, 2)

    euclidean_len = math.sqrt(sum)
    print(f"Euclidean length of {vec}: {math.sqrt(sum)}")

    for i in range(len(vec)):
        vec[i] = float(s.format(vec[i] / euclidean_len))

    print(f"New vector: {vec}")

print("\n\n")

# raw query vector
car_insurance = [1.65, 1.62, 0, 0]

sum = 0

for element in car_insurance:
    sum += math.pow(element, 2)

length = math.sqrt(sum)
print(f"Euclidean length of {car_insurance}: {float(s.format(math.sqrt(sum)))}")

for i in range(len(car_insurance)):
    car_insurance[i] = float(s.format(car_insurance[i] / length))

print(f"New car insurance vector: {car_insurance}")

# vector now normalized

document = 1
for vec in vectors:
    weight = 0

    print(f"Doc{document}: ", end=" ")

    for i in range(len(vec)):
        print(f"({vec[i]} x {car_insurance[i]})", end=" ")
        if i < len(vec) - 1:
            print(" + ", end=" ")
        weight += vec[i] * car_insurance[i]

    print(f"= {s.format(weight)}")
    
    document += 1