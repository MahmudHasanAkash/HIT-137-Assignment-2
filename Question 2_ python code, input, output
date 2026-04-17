import re
import os

#Connor's tokenizer
def tokenize_to_format(expression):
    # catch illegal chars
    raw_units = re.findall(r'\d+\.?\d*|[+/()-]|\s+|.', expression)
    
    formatted = []
    for i, t in enumerate(raw_units):
        if t.isspace():
            continue
            
        # HANDLE NUMBERS
        if t.replace('.', '', 1).isdigit():
            formatted.append(f"[NUM:{t}]")
            
        # HANDLE OPERATORS
        elif t in "+-*/":
            # Removed Connor's unary tracking here. The assignment says tokens 
            # should remain generic [OP:-] and not be folded. The parser will handle unary logic.
            formatted.append(f"[OP:{t}]")
            
        # HANDLE PARENTHESES    
        elif t == '(':
            formatted.append("[LPAREN:(]")
        elif t == ')':
            formatted.append("[RPAREN:)]")
        else:
            # Catch things like @ or letters
            raise ValueError("Invalid character found")
            
    formatted.append("[END]")
    return formatted

# Roman: parser logic (Recursive Descent)

def parse_factor(tokens, pos):
    # Handles numbers, parens, and unary operators
    if pos[0] >= len(tokens):
        raise ValueError("Unexpected end of expression")
        
    tok = tokens[pos[0]]
    
    if tok == "[OP:-]":
        pos[0] += 1 
        tree, val = parse_factor(tokens, pos)
        return f"(neg {tree})", -val
        
    elif tok == "[OP:+]":
        # Rubric strictly requires unary + to produce an ERROR
        raise ValueError("Unary plus is strictly not allowed")
        
    elif tok == "[LPAREN:(]":
        pos[0] += 1
        tree, val = parse_expression(tokens, pos)
        if tokens[pos[0]] != "[RPAREN:)]":
            raise ValueError("Missing closing parenthesis")
        pos[0] += 1
        return tree, val
        
    elif tok.startswith("[NUM:"):
        pos[0] += 1
        # Extract the actual number string from the token
        num_str = tok[5:-1]
        return num_str, float(num_str)
        
    else:
        raise ValueError("Unexpected token for a factor")


def parse_term(tokens, pos):
    # Handles * and / and implicit multiplication
    left_tree, left_val = parse_factor(tokens, pos)
    
    while pos[0] < len(tokens):
        tok = tokens[pos[0]]
        
        if tok == "[OP:*]" or tok == "[OP:/]":
            op = tok[4:-1]
            pos[0] += 1
            right_tree, right_val = parse_factor(tokens, pos)
            
            if op == '/':
                if right_val == 0:
                    raise ValueError("Division by zero")
                left_val = left_val / right_val
            else:
                left_val = left_val * right_val
                
            left_tree = f"({op} {left_tree} {right_tree})"
            
        # Check for implicit multiplication (if next token is a number or open paren)
        elif tok == "[LPAREN:(]" or tok.startswith("[NUM:"):
            right_tree, right_val = parse_factor(tokens, pos)
            left_val = left_val * right_val
            left_tree = f"(* {left_tree} {right_tree})"
            
        else:
            break
            
    return left_tree, left_val


def parse_expression(tokens, pos):
    # Handles + and - (lowest mathematical precedence)
    left_tree, left_val = parse_term(tokens, pos)
    
    while pos[0] < len(tokens):
        tok = tokens[pos[0]]
        
        if tok == "[OP:+]" or tok == "[OP:-]":
            op = tok[4:-1]
            pos[0] += 1
            right_tree, right_val = parse_term(tokens, pos)
            
            if op == '+':
                left_val = left_val + right_val
            else:
                left_val = left_val - right_val
                
            left_tree = f"({op} {left_tree} {right_tree})"
        else:
            break
            
    return left_tree, left_val


# Formatter & evaluator: Kelly

def format_number(val):
    					# Whole numbers shouldn't show decimal points (e.g. 8.0 -> 8)
    if val == int(val):
        return str(int(val))
    else:
        return f"{round(val, 4)}"

def evaluate_file(input_path: str) -> list[dict]:
    					# Write output to the same directory as input
    output_dir = os.path.dirname(input_path)
    output_path = os.path.join(output_dir, 'output.txt')
    
    results = []
    
    with open(input_path, 'r') as f:
        lines = f.readlines()
        
    out_file = open(output_path, "w")
    
    for i, line in enumerate(lines):
        expr = line.strip()
        if not expr:
            continue
            
        				# Set default error states to catch any issues during execution
        tree_str = "ERROR"
        tokens_str = "ERROR"
        final_res = "ERROR"
        
        try:
            tokens = tokenize_to_format(expr)
            tokens_str = ' '.join(tokens)
            
            				# Using a list [0] to pass index by reference through recursive functions
            pos = [0] 
            tree_str, val = parse_expression(tokens, pos)
            
            if tokens[pos[0]] != "[END]":
                raise ValueError("Extra tokens left over at the end")
                
            final_res = format_number(val)
            
        except Exception:
           	 			# If ANY error happens (div by 0, unary +, bad char), it hits this block
            tree_str = "ERROR"
            tokens_str = "ERROR"
            final_res = "ERROR"
            
        				# Build required dictionary
        entry = {
            "input": expr,
            "tree": tree_str,
            "tokens": tokens_str,
            "result": final_res
        }
        results.append(entry)
        
        				# Physical formatting for output.txt
        out_file.write(f"Input: {expr}\n")
        out_file.write(f"Tree: {tree_str}\n")
        out_file.write(f"Tokens: {tokens_str}\n")
        out_file.write(f"Result: {final_res}\n")
        
        				# Keep spacing identical to sample_output.txt
        if i < len(lines) - 1:
            out_file.write("\n")
            
    out_file.close()
    return results

if __name__ == '__main__':
    # Test execution 
    evaluate_file("sample_input.txt")
