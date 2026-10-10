with open('academy.html', 'r', encoding='utf-8') as f:
    text = f.read()

fn_pos = 5806412
idx = text.find("let bodyHTML = '';", fn_pos)
print("bodyHTML starts at:", idx)
idx_exam = text.find("exam", idx)
print("exam in bodyHTML at:", idx_exam)
if idx_exam != -1 and idx_exam < fn_pos + 17000:
    print(text[idx_exam-50:idx_exam+300])
else:
    print("exam not found in bodyHTML, let's see how bodyHTML ends:")
    print(text[fn_pos + 15000:fn_pos + 16900])
