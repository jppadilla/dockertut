from re import sub

def remove_unicode(text):
    return sub(r'[^\x00-\x7F]+', '', text)
    
def remove_colon(text):
    return sub(':', '', text)

def replace_space_with_minus(text):
    return sub(' ', '-', text)

def replace_minus_with_space(text):
    return sub('-', ' ', text)

def replace_space_with_urlspace(text):
    return sub(' ', '%20', text)

def better_strip(text, text_to_remove):
    return sub(text_to_remove, '', text)

def remove_parentheses(text):
    return sub(r"[()]", '', text)

def clean_text(text):
    text = remove_parentheses(text)
    text = remove_unicode(text)
    text = remove_colon(text)
    return text