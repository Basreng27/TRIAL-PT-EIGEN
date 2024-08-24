def reverse_alphabet(input_str):
    letters = ''.join(
        [
            c 
            for c in input_str 
                if c.isalpha()
        ]
    )
    reversed_letters = letters[::-1]
    
    return reversed_letters + ''.join(
        [
            c 
            for c in input_str 
                if not c.isalpha()
        ]
    )

print(reverse_alphabet("NEGIE1")) 
