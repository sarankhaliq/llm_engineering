""""
class student:

    def __init__(self, name, marks1, marks2, marks3):
        self.name=name
        self.marks1=marks1
        self.marks2=marks2
        self.marks3=marks3
        self.average=0

    def average_marks(self):
        self.average=(self.marks1+self.marks2+self.marks3)/3      
        print("Average marks for student ", self.name, " = ", self.average)
"""


# class for student exam marks and average
class student:

    def __init__ (self, name, marks):
        self.name=name
        self.marks= marks
        self.average=0

    def average_marks(self):
        self.average=(self.marks[0]+self.marks[1]+self.marks[2])/3
        print("average marks = ", self.average)


s1=student("Ali", [55, 74, 76])
s1.average_marks()
print(s1.marks)


class bank:
    def __init__(self, account_num, balance):
        self.account_num=account_num
        self.balance=balance;

    def credit(self, credit_amount):
        self.balance=self.balance+credit_amount

    def debit(self, debit_amount):
        self.balance=self.balance-debit_amount
    
    def show_balance(self):
        print("Your current balance against account number ", self.account_num, "is Rs", self.balance)


b1=bank("03200104930180", 100000)
b1.show_balance()
b1.debit(50000)
b1.show_balance()
b1.credit(25000)
b1.show_balance()