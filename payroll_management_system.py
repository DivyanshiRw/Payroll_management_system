import mysql.connector
import datetime
from tabulate import tabulate

db=input('Enter Database name :')

mydb=mysql.connector.connect(host='localhost',user='root',passwd='[password]')    
mycursor=mydb.cursor()

sql='CREATE DATABASE if not exists %s'%(db,)
mycursor.execute(sql)
print('Database Created Successfully')
mycursor=mydb.cursor()
mycursor.execute('Use '+db)
TableName=input('Name of the table to be created :')
query='Create table if not exists '+TableName+' \
(empno int primary key,\
name varchar(15) not null,\
job varchar(15),\
BasicSalary int,\
DA float,\
HRA float,\
GrossSalary float,\
Tax float,\
NetSalary float)'
print('Table '+TableName+' Created Successfully..')
mycursor.execute(query)

while True:
    print('\n\n\n')
    print('#'*50)
    print('\t\t\t\t\t MAIN MENU')
    print('#'*50)
    print('\t\t\t\t\t 1. Adding Employee Records')
    print('\t\t\t\t\t 2. TO Display Record of all the Employees')
    print('\t\t\t\t\t 3. To Display Record of a Particular Employee')
    print('\t\t\t\t\t 4. To Delete Record of all the Employees')
    print('\t\t\t\t\t 5. To Delete Record of a Particular Employee')
    print('\t\t\t\t\t 6. To Modify a Record')
    print('\t\t\t\t\t 7. To Display Payroll')
    print('\t\t\t\t\t 8. To Display Salary Slip of all the Employees')
    print('\t\t\t\t\t 9. To Display Salary Slip of a particular Employee')
    print('\t\t\t\t\t 10. To Exit')
    print('Enter Your Choice : ',end='')
    choice=int(input())
    if choice==1:
        try:
            print('Enter Employee Information....')
            mempno=int(input('Enter Employee no. :'))
            mname=input('Enter Employee Name :')
            mjob=input('Enter Employee Job :')
            mbasic=float(input('Enter Basic Salary :'))
            if mjob.upper()=='PRESIDENT':
                mda=mbasic*0.50
                mhra=mbasic*0.35
                mtax=mbasic*0.2
            elif mjob.upper()=='MANAGER':
                mda=mbasic*0.45
                mhra=mbasic*0.30
                mtax=mbasic*0.15
            else:
                mda=mbasic*0.40
                mhra=mbasic*0.25
                mtax=mbasic*0.1
            mgross=mbasic+mda+mhra
            mnet=mgross-mtax
            rec=(mempno,mname,mjob,mbasic,mda,mhra,mgross,mtax,mnet)
            query='insert into '+TableName+' values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,rec)

            mydb.commit()
            print('Record added successfully !!')
        except:
            print('Something went wrong :( .....')

    elif choice==2:
        try:
            query='select * from '+TableName
            mycursor.execute(query)
            print(tabulate(mycursor, headers=['EmpNo','Name','Job','Basic Salary','DA','HRA','Gross Salary','Tax','Net Salary'], tablefmt='psql'))
            '''myrecords=mycursor.fetchall()
            for rec in myrecords:
                print(rec)'''
        except:
            print('Something went wrong :( .....')

    elif choice==3:
        try:
            en=input('Enter Employee No. of the Record to be displayed... :')
            query='select * from '+TableName+' where empno='+en
            mycursor.execute(query)
            myrecord=mycursor.fetchone()
            print('\n\n Record of Employee No. :'+en)
            print(myrecord)
            c=mycursor.rowcount
            if c==-1:
                print('Nothing to Display !')
        except:
            print('Something went wrong :( .....')

    elif choice==4:
        try:
            ch=input('Do you want to delete all the records ? (y/n)')
            if ch.upper()=='Y':
                mycursor.execute('delete from '+TableName)
                mydb.commit()
                print('All the records are successfully deleted...')
        except:
            print('No Record has been deleted !')

    elif choice==5:
        try:
            en=input('Enter employee no. of the record to be deleted...')
            query='delete from '+TableName+' where empno='+en
            mycursor.execute(query)
            mydb.commit()
            c=mycursor.rowcount
            if c>0:
                print('deletion done')
            else:
                print('Employee no ' ,en, ' not found')
        except:
            print('something went wrong :(......')



    elif choice==6:
        try:
            en=input('Enter employee no. of the record to be modified...')
            query='select * from '+TableName+' where empno='+en
            mycursor.execute(query)
            myrecord=mycursor.fetchone()
            c=mycursor.rowcount
            if c==-1:
                print('Empno '+en+' does not exist')
            else:
                mname=myrecord[1]
                mjob=myrecord[2]
                mbasic=myrecord[3]
                print('empno  :',myrecord[0])
                print('name   :',myrecord[1])
                print('job    :',myrecord[2])
                print('basic  :',myrecord[3])
                print('da     :',myrecord[4])
                print('hra    :',myrecord[5])
                print('gross  :',myrecord[6])
                print('tax    :',myrecord[7])
                print('net    :',myrecord[8])
                print('---------------------')
                print('Type value to modify below or press Enter for no change')
                x=input('Enter name ')
                if len(x)>0:
                    mname=x
                x=input('Enter job ')
                if len(x)>0:
                    mjob=x
                x=input('Enter basic salary ')
                if len(x)>0:
                    mbasic=float(x)
                query='update '+TableName+' set name='+"'"+mname+"'"+','+'job='+"'"+mjob+"'"+','+'basicsalary='\
                       +str(mbasic)+' where empno='+en
                print(query)
                mycursor.execute(query)
                mydb.commit()
                print('record modified')

        except:
            print('something went wrong :(......')
    elif choice==7:
        try:
            query='select * from '+TableName
            mycursor.execute(query)
            myrecords=mycursor.fetchall()
            print('\n\n\n')
            print(95*'*')
            print('Employee Payroll'.center(90))
            print(95*'*')
            now = datetime.datetime.now()
            print('current Date and Time:',end= ' ')
            print(now.strftime('%Y-%m-%d %H:%M:%S'))
            print()
            print(95*'-')
            print('%-5s %-15s %-10s %-8s %-8s %-8s %-9s %-8s %-9s'\
                  %('Empno','Name', 'Job' , 'Basic' , 'DA' , 'HRA' , 'Gross' , 'Tax' , 'Net'))
            print(95*'-')
            for rec in myrecords:
                print('%4d %-15s %-10s %-8.2f %-8.2f %-8.2f %-9.2f %-8.2f %-9.2f'%rec)
            print(95*'-')
        except:
            print('something went wrong :( .....')

    elif choice==8:
        try:
            query='select * from '+TableName
            mycursor.execute(query)
            now = datetime.datetime.now()
            print('\n\n\n')
            print('-'*95)
            print('\t\t\t\tSalary Slip')
            print('-'*95)
            print('current Date and Time:',end= ' ')
            print(now.strftime('%Y-%n-%d %H:%M:%S'))
            myrecords=mycursor.fetchall()
            for rec in myrecords:
                print('%4d %-15s %-10s %-8.2f %-8.2f %-8.2f %-9.2f %-8.2f %-9.2f'%rec)
        except:
            print('something went wrong :( ......')

    elif choice==9:
        try:
            en=input('enter employee number whose pay slip you want to retrive:')
            query='select * from '+TableName+' where empno='+en
            mycursor.execute(query)
            now = datetime.datetime.now()
            print('\n\n\n\t\t\t\tSALARY SLIP')
            print('current Date and Time:',end= ' ')
            print(now.strftime('%Y-%n-%d %H:%M:%S'))
            print(tabulate(mycursor, headers=['Empno','Name', 'Job' , 'Basic Salary' , 'DA' , 'HRA' , 'Gross' , 'Tax' , 'Net']))

        except Exception as e:
            print('something went wrong :( .....',e)

    elif choice==10:

        break
    else:
        print('Wrong Choice...')