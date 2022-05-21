from flask import flash

def validate_pass(password):
    if len(password) < 8:
        return False
        
    requirements = {}
    for char in password:
        if not (char.isalpha() or char.isdigit() or char.isspace()):
            requirements['special_characters'] = True
        if char.isdigit():
            requirements['numbers'] = True
        if char.islower():
            requirements['lower case'] = True
        if char.isupper():
            requirements['upper case'] = True


    if len(requirements) < 2:
        return False
