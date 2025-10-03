def getConstans():

    mistrans = { '4': 'y', '5': 's', '7': 'z' }
    varsLs = ['a', 'b', 'x', 'y', 'z']
    replacements = {
        r'\\Large\\frac\{([^}]+)\}\{([^}]+)\}': r'\1/\2',
        r'\\dfrac\{([^}]+)\}\{([^}]+)\}': r'\1/\2',
        r'\\frac\{([^}]+)\}\{([^}]+)\}': r'\1/\2',
        r'\\div': '/',
        r'\\hspace\{.*?\}': ' ',
        r'\\underline\{[^}]*\}': '?',
        r'\\cdot': '*',
        r'\\times': '*',
        r'\{,\}': '.',
        r',': '.',
        r'\$': '',
        r'\\Large': '',
        r'\\quad': '',
        r'\\': '',
        r'\{': '',
        r'\}': '',
        r'\s+': ' ',
        r'([0-9])\s+([0-9])': r'\1\2',
        r'n': ''
    }

    return mistrans, replacements, varsLs

def getOpsLs(problem):

    if '^' in problem:
        return ['+', '-', '*', '/', '=', '^']
    else:
        return ['+', '-', '*', '/', '=']
