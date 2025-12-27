def check_brackets(expression):
    stack = []
    bracket_pairs = {')': '(', ']': '[', '}': '{'}

    for char in expression:
        if char in '([{':  # 左括号入栈
            stack.append(char)
        elif char in ')]}':  # 右括号检查
            if not stack:  # 栈为空，右括号多于左括号
                return -2
            if stack[-1] == bracket_pairs[char]:  # 匹配成功
                stack.pop()
            else:  # 配对次序不正确
                return -1

    # 遍历完成后检查栈的状态
    if not stack:
        return 0  # 完全匹配
    else:
        return -3  # 左括号多于右括号


def main():
    expression = input().strip()
    result = check_brackets(expression)
    print(result)


if __name__ == '__main__':
    for i in range(4):
        main()