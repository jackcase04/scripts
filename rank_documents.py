import math

def calculate_document_weights(query, normalized_documents):
    document_no = 1
    for vec in normalized_documents:
        weight = 0

        print(f"Doc{document_no}: ", end=" ")

        for i in range(len(vec)):
            print(f"({query[i]} x {vec[i]})", end=" ")
            if i < len(vec) - 1:
                print(" + ", end=" ")
            weight += query[i] * vec[i]

        print(f"= {s.format(weight)}")
        
        document_no += 1

tf_values = [
    [27,0,14,3],
    [4,33,0,33],
    [24,29,17,0]
]

idf_values = [1.65,1.62,1.5,2.08]

dict = {
    0: "car",
    1: "insurance",
    2: "best",
    3: "auto"
}
s = '{:.4f}'

normalized_documents = []
document_no = 1

print("Augmented tf formula: 0.5 + 0.5 x (tf / max_tf)")
print("Aug_tf x idf\n")

for document in tf_values:
    max_tf = max(document)
    print(f"Max tf for Doc{document_no}: {max_tf}\n")
    temp_vec = []

    for i in range(len(document)):
        x = ( 0.5 + 0.5 * (document[i] / max_tf) ) * idf_values[i]
        print(f"{dict[i]}: (0.5 + 0.5 x ( {document[i]} / {max_tf}) ) x {idf_values[i]}")

        temp_vec.append(x)

    sum = 0

    for element in temp_vec:
        sum += math.pow(element, 2)

    euclidean_len = math.sqrt(sum)
    print(f"Euclidean length of {temp_vec}: {math.sqrt(sum)}")

    for i in range(len(temp_vec)):
        temp_vec[i] = float(s.format(temp_vec[i] / euclidean_len)) 

    print(f"Normalized Doc{document_no}: {temp_vec}\n")
    normalized_documents.append(temp_vec)

    document_no += 1

print(f"{normalized_documents} \n")

# nnn.atc query - raw tf, no idf, no normalization

query = [1,1,1,0] # car, insurance, best, !auto

calculate_document_weights(query, normalized_documents)

# ntc.atc query tf x idf, then normalize

print("\n\n")

query = [1,1,1,0]

for i in range(len(query)):
    x = query[i] * idf_values[i]
    print(f"{dict[i]}: {query[i]} x {idf_values[i]}")
    query[i] = x

sum = 0

for element in query:
    sum += math.pow(element, 2)

euclidean_len = math.sqrt(sum)
print(f"Euclidean length of {query}: {math.sqrt(sum)}")

for i in range(len(query)):
    query[i] = float(s.format(query[i] / euclidean_len)) 

print(f"Normalized query: {query}\n")

calculate_document_weights(query, normalized_documents)