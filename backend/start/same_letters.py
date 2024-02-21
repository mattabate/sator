import json

with open("4_letter_words.json") as f:
    words = json.load(f)

print(words)

alp = {}

for word in words:
    alphabetized_string = "".join(sorted(word))
    if alphabetized_string in alp:
        alp[alphabetized_string]["num"] += 1
        alp[alphabetized_string]["words"].append(word)
    else:
        alp[alphabetized_string] = {}
        alp[alphabetized_string]["num"] = 1
        alp[alphabetized_string]["words"] = [word]

# print top ten
sorted_alp = sorted(alp.items(), key=lambda x: x[1]["num"], reverse=True)

for i in range(10):
    print(sorted_alp[i])
