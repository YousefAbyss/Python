from collections import deque


def variables(**variable):
    for key, value in variable.items():
        assignments[key] = value


class ParenthesesError(Exception):

    def __str__(self):
        return 'Invalid expression'


class InfixToPostfix:

    def __init__(self, expression):
        self.expression = expression.replace(' ', '')
        n_minus = self.expression.count('-')
        if n_minus > 1:
            for i1 in range(n_minus, 1, -1):
                if i1 % 2 == 0:
                    self.expression = self.expression.replace(i1 * '-', '+')
                elif i1 % 2 == 1:
                    self.expression = self.expression.replace(i1 * '-', '-')
        n_plus = self.expression.count('+')
        if n_plus > 1:
            for i2 in range(n_plus, 1, -1):
                self.expression = self.expression.replace(i2 * '+', '+')

    def numbers_and_indexes(self):
        numbers_in_expression = self.expression.replace('+', ' ').replace('-', ' ').replace('*', ' ')\
            .replace('/', ' ').replace('^', ' ').replace(')', ' ').replace('(', ' ').split()
        for element in numbers_in_expression:
            if not element.isdigit():
                try:
                    numbers_in_expression[numbers_in_expression.index(element)] = assignments[element]
                    self.expression = self.expression.replace(element, assignments[element])
                except KeyError:
                    raise KeyError
        from_index = 0
        to_index = 1
        indexes_numbers = {}
        temp = numbers_in_expression.copy()
        for number in temp:
            while to_index != len(self.expression) + 1:
                if self.expression[from_index: to_index].isdigit():
                    if self.expression[from_index: to_index] != number:
                        to_index += 1
                    elif self.expression[from_index: to_index] == number:
                        indexes_numbers[(from_index, to_index)] = self.expression[from_index: to_index]
                        numbers_in_expression.remove(self.expression[from_index: to_index])
                        from_index = to_index
                        to_index += 1
                        break
                else:
                    from_index += 1
                    to_index += 1

        return indexes_numbers

    def elements_of_expression(self):
        dict_numbers_indexes = self.numbers_and_indexes()
        position = []
        numbers = []
        expression_as_list = []
        for key, value in dict_numbers_indexes.items():
            position.append(key)
            numbers.append(value)
        for i in range(len(position)):
            expression_as_list.append(int(numbers[i]))
            try:
                for char in self.expression[position[i][1]: position[i + 1][0]]:
                    expression_as_list.append(char)
            except IndexError:
                for char in self.expression[position[i][1]:]:
                    expression_as_list.append(char)
        return expression_as_list

    def postfix(self):
        my_deque = deque()
        postfix_result = deque()
        operators = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        elements = self.elements_of_expression()
        for element in elements:
            try:
                if type(element) == int:
                    postfix_result.append(element)
                elif element == '(':
                    my_deque.append(element)
                elif element == ')' and my_deque[-1] != '(':
                    while True:
                        if my_deque[-1] == '(':
                            my_deque.pop()
                            break
                        postfix_result.append(my_deque.pop())
                elif element == ')' and my_deque[-1] == '(':
                    my_deque.pop()
                elif not my_deque or my_deque[-1] == '(':
                    my_deque.append(element)
                elif operators[element] > operators[my_deque[-1]]:
                    my_deque.append(element)
                elif operators[element] <= operators[my_deque[-1]]:
                    while True:
                        if not my_deque or my_deque[-1] == '(' or operators[element] > operators[my_deque[-1]]:
                            my_deque.append(element)
                            break
                        postfix_result.append(my_deque.pop())
            except IndexError:
                raise IndexError
        for _ in range(len(my_deque)):
            postfix_result.append(my_deque.pop())
        return postfix_result


class PostfixCalculation(InfixToPostfix):

    def __init__(self, input_):
        expression = input_
        super().__init__(expression)
        self.postfix_form = self.postfix()

    def parentheses_error(self):
        if '(' in self.postfix_form or ')' in self.postfix_form:
            return False
        else:
            return True

    def calculation(self):
        expression_result = deque()
        if self.parentheses_error():
            try:
                for element in self.postfix_form:
                    if type(element) == int:
                        expression_result.append(element)
                    elif element == '+':
                        first = expression_result.pop()
                        second = expression_result.pop()
                        res = second + first
                        expression_result.append(res)
                    elif element == '-':
                        first = expression_result.pop()
                        second = expression_result.pop()
                        res = second - first
                        expression_result.append(res)
                    elif element == '*':
                        first = expression_result.pop()
                        second = expression_result.pop()
                        res = second * first
                        expression_result.append(res)
                    elif element == '/':
                        first = expression_result.pop()
                        second = expression_result.pop()
                        res = second / first
                        expression_result.append(res)
                    elif element == '^':
                        first = expression_result.pop()
                        second = expression_result.pop()
                        res = pow(second, first)
                        expression_result.append(res)
            except IndexError:
                raise IndexError
            return expression_result
        elif not self.parentheses_error():
            raise ParenthesesError


assignments = dict()


def main():
    while True:
        solve = input()
        try:
            if solve.startswith('/'):
                if solve != '/exit' and solve != '/help':
                    print('Unknown command')
                    continue
                elif solve == '/help':
                    print('this is a smart calculator')
                    continue
                elif solve == '/exit':
                    print('Bye!')
                    break
            elif solve.replace(' ', '') == '':
                continue
            elif '=' in solve:
                assignment = solve.replace(' ', '').split('=')
                if any(char.isdigit() for char in assignment[0]):
                    print('Invalid identifier')
                    continue
                elif assignment[1].isdigit():
                    variables(**{assignment[0]: assignment[1]})
                elif assignment[1] in assignments:
                    assignments[assignment[0]] = assignments[assignment[1]]
                elif any(char.isdigit() for char in assignment[1]):
                    print('Invalid assignment')
                    continue
                else:
                    print('Unknown variable')
            else:
                result = PostfixCalculation(solve).calculation()
                print(int(result[0]))
        except ParenthesesError:
            print('Invalid expression')
        except IndexError:
            print('Invalid expression')
        except KeyError:
            print('Unknown variable')


main()
