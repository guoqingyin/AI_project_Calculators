# -----------------------------Reverse Polish Notion Caculator--------------------------------
class Stack():  
    def __init__(self,):
        self.stack = []

    def push(self, data):  
        self.stack.append(data)

    def pop(self):  
        return self.stack.pop()

    def is_empty(self):  
        return not len(self.stack)

    def top(self):  
        if self.is_empty():
            return None
        return self.stack[-1]


class InversPolishCalculator(object):  

    def deal(self, exspression): 
        list_expression = self.get_list_expression(exspression)
        stack = Stack()  
        for ele in list_expression:  
            if ele.replace('.', '').isdigit() or ele.replace('-', '').isdigit(): 
                stack.push(ele)
            else:  
                ret = self.operation(ele, float(
                    stack.pop()), float(stack.pop()))
                stack.push(ret)
        temp = stack.pop()
        if abs(temp-int(temp)) <= 0.01:
            return int(temp)
        else:
            return '%.2f' % temp

    def operation(self, sign, num2, num1):  
        if sign == '*':
            return num1 * num2
        if sign == '/':

            return num1/num2
        if sign == '+':
            return num1 + num2
        if sign == '-':
            return num1 - num2

    def deal_str(self, expression):  
        status = 0
        res = ''
        expression = expression.strip().replace(' ', '')
        for i, ele in enumerate(expression):
            if i == 0 and ele == '-':
                status = 1
                res = res + ele + ' '
            elif i > 0 and ele == '-' and expression[i - 1] == '(':
                status = 1
                res = res + ele + ' '
            elif ele.isdigit() or ele == '.':
                if status == 1:  # the previous one is digit or .
                    res = res.strip(' ')
                    res = res + ele + ' '
                else:  # the previous one is operator
                    status = 1
                    res = res + ele + ' '
            else:
                status = 0
                res = res + ele + ' '
        return res.strip().split(' ')

    def get_list_expression(self, exspression):
        lst = self.deal_str(exspression)
        s1 = Stack()
        s2 = Stack()  # Store the numbers
        for ele in lst:
            if ele.replace('.', '').isdigit() or ele.replace('-', '').isdigit():
                s2.push(ele)
            else:
                self.deal_symbol(ele, s1, s2)
        while not s1.is_empty():
            s2.push(s1.pop())
        res = []
        while not s2.is_empty():
            res.append(s2.pop())
        return res[::-1]

    def deal_symbol(self, ele, s1, s2):  
        if s1.is_empty() or s1.top() == '(' or ele == '(':
            s1.push(ele)
        elif ele == ')':
            while s1.top() != '(':
                s2.push(s1.pop())
            s1.pop()
        elif self.get_priority(ele) > self.get_priority(s1.top()):
            s1.push(ele)
        else:
            s2.push(s1.pop())
            self.deal_symbol(ele, s1, s2)

    def get_priority(self, sign):  
        if sign == '*' or sign == '/':
            return 2
        elif sign == '+' or sign == '-':
            return 1


if __name__ == '__main__':
    # exspression = input('请输入计算公式:')
    # Calculator = InversPolishCalculator()
    # ret = Calculator.deal(exspression)
    # print('计算结果:',ret)
    # input()

    Calculator = InversPolishCalculator()
    ret = Calculator.deal("1+2")
    print('计算结果:', ret)
