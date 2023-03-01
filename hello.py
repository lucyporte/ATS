#print("Hello World")
num1 = float(input("Please enter the first number"))
num2 = float(input("Please enter the second number"))
print("You entered ", num1, "and",num2)
sum = num1 + num2
print("The sum of the two numbers entered is", sum)
product = num1 * num2
print(num1, "x", num2, "=", product)
if num2 != 0:
	quotient = num1 / num2
	print(num1, "/", num2, "=", quotient)
	remainder = num1%num2
	print(num1, "mod", num2, "=", remainder	)
