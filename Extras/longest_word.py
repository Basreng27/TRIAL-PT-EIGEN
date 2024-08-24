def longest(sentence):
    words = sentence.split()
    longest_word = max(words, key=len)
    
    return f"{longest_word}: {len(longest_word)} character"

print(longest("Saya sangat senang mengerjakan soal algoritma"))
