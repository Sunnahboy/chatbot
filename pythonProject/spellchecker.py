from fuzzywuzzy import process

def correct_sentence(sentence, agriculture_keywords):
    corrected_sentence = []
    for word in sentence.split():
        closest_match = process.extractOne(word, agriculture_keywords)
        if closest_match[1] >= 80:  # Adjust the threshold as needed
            corrected_sentence.append(closest_match[0])
        else:
            corrected_sentence.append(word)
    return " ".join(corrected_sentence)

#sample
agriculture_keywords = ["crop", "farm", "harvest", "agriculture"]
sentence = "I have a cropp on my frm"
corrected = correct_sentence(sentence, agriculture_keywords)
print(corrected)
