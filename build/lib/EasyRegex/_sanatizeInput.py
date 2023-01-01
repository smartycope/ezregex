
escapeChars = (r'\)', r'\(', r'\[', r'\]', r'\{', r'\}', r'\+', r'\*', r'\$', r'\@', r'\^', r'\:', r'\=', r'\-', r'\/', r'\?', r'\|')
def _sanitizeInput(i):
    """ Instead of rasising an error if passed a strange datatype, it now trys to cast it to a string """
    # r'\<', r'\>', r'//'

    # If it's another chain, compile it
    if type(i) is EasyRegexMember:
        return str(i)
    elif isinstance(i, str):
        for part in escapeChars:
            i = re.sub(r'(?<!\\)' + part, part, i)
        return i
    else:
        return str(i)
        # raise TypeError(f'Incorrect type {type(i)} given to EasyRegex parameter: Must be string or another EasyRegex chain.')
