import mysql.connector as mc
import random
import datetime
from datetime import datetime, timedelta

mydb=mc.connect(host="localhost",user="root",password="Jeet@123",database="ATM")    #it is connect function, it is used for connecting the mysql to python
cr=mydb.cursor()                                                                    #it is cursor function, it is used for perform any operation of mysql
# cr.execute("create database ATM")                                                 #Execute function,it is used for executing the mysql command


a=mydb.cursor()
s=("create table user_data("
   "id int auto_increment primary key,"
   "Name varchar(20) not null,"
   "Email varchar(255) not null,"
   "Account_No varchar(20) not null,"
   "PIN char(4) not null,"
   "Phone_NO varchar(10) not null"
   ",Balance decimal(10,2) default 0")      #command for creating user_data table
# cr.execute(s)
# mydb.commit()


transactin_table = """                                 #for creating  transactions table 
CREATE TABLE IF NOT EXISTS transactions (
    txn_id INT AUTO_INCREMENT PRIMARY KEY,
    account_no VARCHAR(20),
    txn_type VARCHAR(10),
    amount DECIMAL(10,2),
    balance_after DECIMAL(10,2),
    txn_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

# cr.execute(transactin_table)
# mydb.commit()

print("1 If Your Account Already Exist")
print("2 Open Your Account")
enter_choice=input("Enter your choice:-")

if enter_choice=="1":
    print("1 Enter PIN")
    print("2 Forgot PIN")
    enter_Pin_choice=input("Enter your choice:-")


    if enter_Pin_choice=="1":
        enter_pin = input("Enter the Pin:-")
        s = "SELECT PIN FROM user_data WHERE PIN = %s"
        cr.execute(s, (enter_pin,))
        result = cr.fetchone()


        if result and enter_pin == result[0]:

                    while True:

                        print("1 Check Balance")
                        print("2 Deposite Money")
                        print("3 Withdraw Money")
                        print("4 Exit")

                        choice = input("Enter Choice:-")

                        query = "SELECT PIN, Balance FROM user_data WHERE PIN = %s"
                        cr.execute(query, (enter_pin,))
                        result = cr.fetchone()
                        if result:
                            db_pin = result[0]
                            balance = result[1]

                            if enter_pin == db_pin:

                                if choice=="1":
                                    print("Balance:-",balance)

                                elif choice == "2":

                                    add_amount = float(input("Enter Amount:-"))
                                    new_balance = float(balance) + add_amount

                                    # Update balance in user_data
                                    cr.execute(

                                        "UPDATE user_data SET Balance = %s WHERE PIN = %s",
                                        (new_balance, enter_pin)

                                    )

                                    # Insert into transactions table

                                    cr.execute(

                                        """INSERT INTO transactions
                                        (account_no, txn_type, amount, balance_after)
                                        VALUES (
                                            (SELECT Account_No FROM user_data WHERE PIN = %s),
                                            %s, %s, %s)""",
                                        (enter_pin, "DEPOSIT", add_amount, new_balance)

                                    )
                                    mydb.commit()
                                    print("✅ Deposit Successful")



                                elif choice == "3":

                                    withdraw = float(input("Enter Amount:-"))
                                    if withdraw <= balance:
                                        new_balance = float(balance) - withdraw

                                        # Update balance

                                        cr.execute(

                                            "UPDATE user_data SET Balance = %s WHERE PIN = %s",
                                            (new_balance, enter_pin)

                                        )

                                        # Insert transaction
                                        cr.execute(

                                            """INSERT INTO transactions
                                            (account_no, txn_type, amount, balance_after)
                                            VALUES (
                                                (SELECT Account_No FROM user_data WHERE PIN = %s),
                                                %s, %s, %s)""",
                                            (enter_pin, "WITHDRAW", withdraw, new_balance)

                                        )
                                        mydb.commit()
                                        print("✅ Withdraw Successful")

                                    else:
                                        print("Insufficient Balance")


                                elif choice == "4":
                                    print("Thankyou for using ATM")
                                    break
                                else:

                                   print("Invaid choice")


        else:
          print("Invalid Pin")

    else:
        user_email=input("Enter your Email:-")
        query = "SELECT Email FROM user_data WHERE Email = %s"
        cr.execute(query, (user_email,))
        result1 = cr.fetchone()                                 #mysql return data into tuple
        if result1 and user_email == result1[0]:                #for tuple indexing
            random_otp=random.randrange(1000,9999)
            expiry_time = datetime.now() + timedelta(seconds=10)
            print("OTP:-",random_otp)
            user_otp=int(input("Enter OTP:-"))


            if datetime.now() <= expiry_time:                  #for comparing the current time
                if user_otp == random_otp:
                    print("OTP Verified ✅")
                    new_pin = input("Enter Your New  Pin:-")
                    query = "UPDATE user_data SET Pin = %s WHERE Email = %s"
                    cr.execute(query, (new_pin, user_email))
                    mydb.commit()

                    print("✅ PIN Updated Successfully")

                else:
                     print("Wrong OTP ❌")
            else:
                 print("OTP Expired ⏰")


        else:
            print("Invalid Email")

else:
        #insert data into table
        def user_information():
            s="insert into user_data(Name,Email,Account_no,PIN,Phone_No,Balance) values(%s,%s,%s,%s,%s,%s)"
            Name=input("Enter your Name:-")
            Email=input("Enter your Email:-")
            Account_No = input("Enter your Account number:-")
            Pin=input("Enter your PIN:-")
            Phone_No=input("Enter your Phone Number:-91 ")
            Balance=input("Deposite Your Amount:-")
            data1=(Name,Email,Account_No,Pin,Phone_No,Balance)
            cr.execute(s,data1)
            mydb.commit()
            return data1
        data=user_information()
