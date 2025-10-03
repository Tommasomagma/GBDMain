import re
from collections import defaultdict
from constants import getConstans, getOpsLs

# Define global variable opsLs
mistrans,replacements,varsLs = getConstans()

def clean_string(string, clean_answer, problem, opsLs):

    new_string = re.sub(r'n', ' ', string)
    new_string = re.sub(r'dfrac\{([^}]+)\}\{([^}]+)\}', r'\1/\2', new_string)

    if '{,}' not in problem and '.' not in clean_answer:
        new_string = re.sub(r'\.(\d)', r'*\1', new_string)
    new_string = new_string.replace(',', '.')

    for key, value in mistrans.items():
        if value in new_string and value not in problem:
            new_string = new_string.replace(value, key)

    for pattern, replacement in replacements.items():
        try:
            new_string = re.sub(pattern, replacement, new_string)
        except:
            continue

    cleaned_string = ''.join([
        char for i, char in enumerate(new_string)
        if re.match(r'[\d\s.]', char) or
           char in opsLs or
           (char in varsLs and
            (i == 0 or not new_string[i - 1].isalpha()) and
            (i == len(new_string) - 1 or not new_string[i + 1].isalpha()))
    ])

    new_string = ' '.join(cleaned_string.split())
    if new_string.endswith('.'):
        new_string = new_string[:-1]

    return new_string

def clean_answer(answer):
    new_answer = re.sub(r'[\[\]",]', '', answer.replace(',', '.'))
    new_answer = re.sub(r'([a-zA-Z])\^.*$', r'\1', new_answer)

    new_answer = ''.join([
        char for char in new_answer
        if char.isdigit() or char in varsLs or char in {'.', '-', '+', '*', '/', '='}
    ]).strip()

    return new_answer

def clean_problem(problem):
    new_problem = problem
    for pattern, replacement in replacements.items():
        try:
            new_problem = re.sub(pattern, replacement, new_problem)
        except re.error:
            continue
    return new_problem.strip()

def get_problem_ratio(sol_ls, problem_ls, answer_ls):
    if not sol_ls:
        return 0.0
    
    filtered_problem_ls = [item for item in problem_ls if item != '=']
    filtered_sol_ls = [item for item in sol_ls if item != '=']
    
    if '/' not in filtered_problem_ls:
        filtered_sol_ls = [item for item in filtered_sol_ls if item != '/']
    
    if '*' in filtered_problem_ls and '+' not in filtered_problem_ls:
        filtered_sol_ls = [item for item in filtered_sol_ls if item != '+']
    
    sol_for_ratio = filtered_sol_ls.copy()
    for element in answer_ls:
        if element in sol_for_ratio:
            sol_for_ratio.remove(element)
    
    problem_set = set(filtered_problem_ls)
    overlap_count = sum(1 for item in sol_for_ratio if item in problem_set)
    
    return overlap_count / len(sol_for_ratio) if sol_for_ratio else 0

def get_math_ratio(string, problem, opsLs, varLs):

    new_string = re.sub(r'n', ' ', string)
    new_string = re.sub(r'"', ' ', new_string)
    new_string = re.sub(r'dfrac\{([^}]+)\}\{([^}]+)\}', r'\1/\2', new_string)

    for key, value in mistrans.items():
        if value in new_string and value not in problem:
            new_string = new_string.replace(value, key)

    for pattern, replacement in replacements.items():
        try:
            new_string = re.sub(pattern, replacement, new_string)
        except:
            continue

    new_string = ' '.join(new_string.split())
    if new_string.endswith('.'):
        new_string = new_string[:-1]

    mathRatio = round(len([x for x in new_string if x.isdigit() or x in opsLs or x in varLs]) / len(new_string), 2) if new_string else 0

    return mathRatio

def count_vars(problem, vars_string, ops_ls):
    count = count_common = 0
    
    for i, char in enumerate(problem):
        prev_char = problem[i - 1] if i > 0 else ''
        next_char = problem[i + 1] if i < len(problem) - 1 else ''
        
        if (char in varsLs and (
            prev_char.isdigit() or prev_char in ops_ls or
            next_char.isdigit() or next_char in ops_ls or (next_char == ' ' and prev_char == ' '))):
            count += 1
            if char in vars_string:
                count_common += 1
    
    return count, count_common

def get_ratio_format(string_ls, opsLs):
    total_elements = len(string_ls)
    valid_elements = 0
    expecting_digit_or_var = True
    prev_element = None

    for element in string_ls:
        if expecting_digit_or_var:
            if (re.match(r'^\d+\.?\d*$', element) or element in varsLs) and element != prev_element:
                valid_elements += 1
                expecting_digit_or_var = False
        else:
            if element in opsLs:
                valid_elements += 1
                expecting_digit_or_var = True
        prev_element = element

    return valid_elements / total_elements if total_elements > 0 else 0

def get_math(string, opsLs):

    digits = re.findall(r'\d+(?:\.\d+)?', string)
    single_digits = list(re.sub(r'\D', '', string))
    ops = [char for char in string if char in opsLs]
    all_elements = re.findall(r'\d+(?:\.\d+)?|[' + re.escape(''.join(opsLs) + ''.join(varsLs)) + r']', string)

    return digits, single_digits, ops, all_elements

def check_for_answer(string, answer):
    
    string_lower = string.lower()
    answer_lower = answer.lower()
    answer_in_string = any(
        ans == answer_lower or ans == answer_lower.replace('-', '') or ans == answer_lower.replace('.', '')
        for ans in re.split(r'[\s+\-*/]', string_lower)
    )
    parts = re.split(r'=|/', string_lower)
    answer_after_equals = any(answer_lower in part for part in parts[1:])
    last_chars = string_lower[-len(answer_lower):]
    match_length = len(answer_lower) * 2 // 3

    return last_chars[-match_length:] == answer_lower[-match_length:] and len(answer_lower) > 2 or answer_after_equals or answer_in_string

def addStrokeFeatures(features):

    features['mean_w'] = 0
    features['mean_h'] = 50
    features['std_w'] = 0
    features['std_h'] = 50
    features['dense'] = 0.1
    features['mean_t'] = 300
    features['mean_diffs'] = 2000
    features['std_t'] = 1000
    features['std_diff_t'] = 30000
    features['max_min_diff'] = 0
    features['free'] = 10
    features['erase'] = 0
    features['clear'] = 0

    return features

def stringFeatures(string_raw, answer_raw, problem_raw):
    
    features = defaultdict(int)
    problem = clean_problem(problem_raw)
    opsLs = getOpsLs(problem)
    varLs = ['y', 'x', 'z']

    answer = clean_answer(answer_raw)
    string = clean_string(string_raw, answer, problem, opsLs)
    
    digits, single_digits, ops, all_math = get_math(string, opsLs)
    features['digits'] = len(digits)
    features['singleDigits'] = len(single_digits)
    features['uniqueDigits'] = len(set(single_digits))
    features['ops'] = len(ops)
    features['ratioFormat'] = round(get_ratio_format(all_math, opsLs), 1)
    features['ratioMath'] = get_math_ratio(string_raw, problem, opsLs, varLs)
    
    digits_answer, single_digits_answer, ops_answer, _ = get_math(answer, opsLs)
    vars_problem, vars_common = count_vars(problem, all_math, opsLs)
    features['varsProblem'] = vars_problem
    features['ratioVars'] = 1 if vars_common > 0 else 0
    features['ans'] = 1 if check_for_answer(string, answer) else 0
    
    if features['ans'] and ops_answer:
        features['ops'] -= len(ops_answer)
    
    digits_problem, single_digits_problem, ops_problem, _ = get_math(problem, opsLs)
    features['digitsProblem'] = len(digits_problem)
    features['opsProblem'] = len(ops_problem)
    
    if digits_problem:
        features['problemExpected'] = 1
        features['ratioDigits'] = round(get_problem_ratio(digits, digits_problem, digits_answer), 2)
        features['ratioSingleDigits'] = round(get_problem_ratio(single_digits, single_digits_problem, single_digits_answer), 2)
    else:
        features['ratioDigits'] = 1
        features['ratioSingleDigits'] = 1
    
    features['ratioOps'] = round(get_problem_ratio(ops, ops_problem, ops_answer), 1) if ops_problem else 1
    features['ratioProblem'] = round((features['ratioOps'] + features['ratioDigits']) / 2, 1) if ops_problem else features['ratioDigits']

    features = addStrokeFeatures(features)
    
    return features