import os
import re
from re import T
from atexit import register
# from tkinter.tix import Select
from unittest import result
import time
import random
import sqlite3


# 데이터 베이스 연결
conn = sqlite3.connect("lib_project", isolation_level=None)
cur = conn.cursor()
#cur.execute("SELECT * FROM booklist")
regist_id = []
bucket = []
userid = ''
uid = ''
pwd = ''
name = ''
num = ''


def bucket_book():  # 장바구니
    global bookt1
    global bucket
    select = ""

    conn = sqlite3.connect("lib_project")
    cur = conn.cursor()

    if not bucket == []:
        print(f"내 장바구니 목록 ₍ ᐢ. ̫ .ᐢ ₎ . . {bucket}\n")
    print('')

    select = input('장바구니에 담을 책 이름을 입력하세요 (q를 누를시 담기를 종료합니다)\n')
    find = cur.execute('SELECT bookname from rentlist where bookname=?', (select,))
    find = find.fetchone()

    if find is None:
        print('대여가능')
        select = '%' + select + '%'
        cur.execute('SELECT bookname,booknum from booklist where bookname like ?', (select,))
        result = cur.fetchall()
        print('')
        print(*result, sep='\n') 

        bookselect = input('대여할 책의 번호를 입력해주세요')
        # 입력한 책이 책 리스트에 있는지 검사
        find = cur.execute('SELECT booknum,bookname from booklist where booknum=?', (bookselect,))
        find = find.fetchone()

        if find is None:
            print('그런책없음')
        else:
            # 대여리스트에 있는지 검사
            find2 = cur.execute('SELECT booknum,bookname from rentlist where booknum=?', (bookselect,))
            find2 = find2.fetchone()
            # 대여 리스트에 없으면
            if find2 is None:
                bucket.append(find)
                print('=====================₍ ᐢ. ̫ .ᐢ ₎==================')
                print(f"장바구니 리스트 {bucket}\n")
                print('===============================================')
            else:
                os.system("clear")
                print('error 이미 대여중인 책입니다')
                time.sleep(2)

    else:
        print('이미 대여중인 책입니다')

    if select == 'q' or select == 'Q':
        os.system("clear")
        print("종료합니다")
        time.sleep(1)
        os.system("clear")
    conn.close()
    rent_book()


def rent_book():  # 대여
    global book
    global bucket
    select2 = ''
    rent = ''

    time.sleep(1)
    os.system("clear")

    while (1):
        if not bucket == []:
            print(f"내 장바구니 목록 ₍ ᐢ. ̫ .ᐢ ₎ . . {bucket}\n")

        print('=' * 55)
        print('1.장바구니담기 2.대여 3.메인으로 4.반납\n')
        select2 = input()

        if select2 == '1':
            print('장바구니 화면으로 돌아갑니다')
            time.sleep(1)
            os.system('clear')
            bucket_book()

        if select2 == '2':  # 대여

            conn = sqlite3.connect("lib_project")
            cur = conn.cursor()

            print('')
            print('=====================₍ ᐢ. ̫ .ᐢ ₎==================')
            print(f"장바구니 리스트 {bucket}", sep='\n')
            print('===============================================')

            bookselect = input('대여할 책의 번호를 입력해주세요: ')
            rentBool = True
            for i in bucket:
                if bookselect == str(i[0]):
                    find = cur.execute('SELECT booknum,bookname,writer from booklist where booknum=?', (bookselect,))
                    find = find.fetchone()

                    if find is None:
                        print('입력 정보를 다시 확인 해주세요')
                    else:
                        cur.execute("SELECT rentcount FROM userlist WHERE id=?", (userid,))  # 입력한 아이디의 행 수를 count
                        count = cur.fetchone()
                        if count[0] >= 3:
                            print('최대 대여 권수를 초과했습니다')
                            rentBool = False
                            time.sleep(1)
                        else:
                            rentBool = False
                            print('')
                            print(' 대여 완료 ^ㅅ^)b ')
                            cur.execute("INSERT INTO rentlist VALUES(?,?,?,?,date('now'),date('now','7 days'))",
                                        (find[0], find[1], find[2], userid))
                            cur.execute("UPDATE userlist SET rentcount=rentcount+1 WHERE id=?", (userid,))
                            conn.commit()
                            conn.close()

                            for i in bucket:
                                if str(i[0]) == bookselect:
                                    num = bucket.index(i)
                                    del bucket[num]
                                    
            if (rentBool):
                print('error 1004 입력 정보를 확인해주세요 ')
               
        if select2 == '3':
            main()
        if select2 == '4':
            return_book()


def return_book():
    global book
    turnback = ''
    turnname = ''
    turnnum = ''
    conn = sqlite3.connect("lib_project")
    cur = conn.cursor()

    print('    반납 방법을 선택해주세요')
    print('1.도서명으로 반납  2.도서 번호로 반납')
    turnback = input('\n')

    if turnback == '1':
        turnname = input('반납할 책 이름을 입력해주세요: ')
        cur.execute('SELECT booknum,bookname,userid,date from rentlist where bookname=?', (turnname,))
        find = (cur.fetchone())

        if find is None:
            print('error 입력 정보를 확인해주세요')

        else:

            cur.execute('DELETE from rentlist where bookname=?', (turnname,))
            conn.commit()
            cur.execute("INSERT INTO returnlist VALUES(?,?,?,?,date('now'))", (find[0], find[1], find[2], find[3]))
            cur.execute("UPDATE userlist SET rentcount=rentcount-1 WHERE id=?", (userid,))
            conn.commit()
            conn.close()
            os.system("clear")
            time.sleep(1)
            print(f'{find[0], find[1]} 반납 되었습니다 ᴖ-ᴖ')

    if turnback == '2':
        turnnum = input('반납할 책 번호를 입력해주세요')
        cur.execute('SELECT booknum,bookname,userid,date from rentlist where booknum=?', (turnnum,))
        find = (cur.fetchone())

        if find is None:
            print('error 입력 정보를 확인해주세요')

        else:

            cur.execute('DELETE from rentlist where booknum=?', (turnnum,))
            conn.commit()
            cur.execute("INSERT INTO returnlist VALUES(?,?,?,?,date('now'))", (find[0], find[1], find[2], find[3]))
            cur.execute("UPDATE userlist SET rentcount=rentcount-1 WHERE id=?", (userid,))
            conn.commit()
            conn.close()
            os.system("clear")
            time.sleep(1)
            print(f'{find[0], find[1]} 반납 되었습니다 ᴖ-ᴖ')


def SearchBar():  # 조회
    while 1:
        find = input('-' * 10 + '도서 검색' + '-' * 10 + '\n''(연번/도서명/저자)(종료:나가기): ')
        cur.execute(
            f"SELECT * FROM booklist WHERE bookname LIKE '%{find}%' OR booknum LIKE '{find}' OR writer LIKE '{find}%'")
        result = cur.fetchall()

        for i in range(len(result)):
            if find == '나가기':
                return
            else:
                if 0 != len(result):  # 0권이 아니면 모두 출력
                    print(f'연  번: {result[i][0]}''\n'f'도서명: {result[i][1]}''\n'f'저  자: {result[i][2]}''\n')


def Recommend():
    cur.execute("SELECT bookname FROM booklist ORDER by RANDOM() LIMIT 3")
    print('=' * 20 + '추천 도서' + '=' * 20)
    print(*cur.fetchall(), sep='\n')
    print('=' * 49)


def Donation():
    cur.execute("SELECT * FROM booklist")
    allBook = cur.fetchall()
    booklen = len(allBook)  # 총 길이 값
    donate = input("'기증' 하시겠습니까?(Y/n)")
    if donate == 'Y' or donate == 'y':
        bookname = input('도서 명: ')
        writer = input('저자: ')
        cur.execute('INSERT INTO booklist values(?, ?, ?)', (booklen, bookname, writer))
    elif donate == 'N' or donate == 'n':
        print('기증을 취소합니다')
        return
    else:
        print('다시 입력하세요')
        return Donation()

    cur.execute(f'SELECT * FROM booklist LIMIT {booklen}, {booklen}')  # 마지막 줄 확인
    print(cur.fetchall(), 'booklist에 추가 되었습니다')  # 추가 확인 확인
    conn.commit()


def make_id(regist_user):  # 아이디생성 함수

    while 1:
        global uid
        uid = str(input('아이디를 입력하세요: '))
        if uid in regist_user:  # 아이디 중복 확인
            print('중복됨 ㅇㅇ')
            ex = input('메인 화면으로 이동? ㅋㅋ (y/n): ')
            if ex == 'y' or ex == 'Y':
                return 0
            else:
                continue
        else:  # 아이디 중복 아닐 시
            regist_id.append(uid)  # append로 리스트에 추가
            break

    while 1:
        global pwd
        pwd = str(input('비밀번호를 입력하세요: '))
        regist_id.append(pwd)  # 조건 만족 시 추가 (생성)
        break

    while 1:
        global name
        name = str(input('이름을 입력하세요: '))
        regist_id.append(name)  # 조건 만족 시 추가 (생성)
        break

    while 1:
        global num
        num = str(input('번호를 입력하세요: '))
        regist_id.append(num)  # 조건 만족 시 추가 (생성)
        break
    cur.execute('INSERT INTO userlist VALUES (?,?,?,?,?)', (uid, pwd, name, num, 0))
    return regist_id


def change_password(pwd):  # 비밀번호 바꾸기
    global userid
    while 1:
        pw = str(input('새로운 비번 입력:'))
        if pw == pwd:  # 바꿀 비번이 기본과 똑같을때
            print(f'기존의 비밀번호 입니다.!')
            continue
        else:
            n_pwd = pw
            break
    cur.execute("update userlist set pwd = ? where id = ?", (n_pwd, userid))
    print('수정완료')
    time.sleep(1)
    os.system('clear')
    return n_pwd


def change_name(name):
    global userid
    while 1:
        new_name = str(input('변경할 이름입력:'))
        if new_name == name:
            print(f'기존과 동일한 이름 입니다.!')
            continue
        else:
            n_name = new_name
            break
    cur.execute("update userlist set name = ? where id = ?", (n_name, userid))
    print('수정완료')
    time.sleep(1)
    os.system('clear')
    return n_name


def change_num(num):
    global userid
    while 1:
        new_num = str(input('변경할 번호입력:'))
        if new_num == num:
            print(f'기존과 동일한 번호 입니다.!')
            continue
        else:
            n_num = new_num
            break
    cur.execute("update userlist set num = ? where id = ?", (n_num, userid))
    print('수정완료')
    time.sleep(1)
    os.system('clear')
    return n_num


def main():
    global returninfo
    menu_select = ''
    slt = ''
    # conn = sqlite3.connect("lib_project")
    # cur = conn.cursor()

    os.system("clear")
    while (1):
        time.sleep(1)
        os.system("clear")

        Recommend()  # 추천 도서 함수

        print('1.조회 2.대여 3.반납 4.기증 5.나의정보')
        menu_select = input()

        if (menu_select == '1'):
            SearchBar()  # 도서 검색 함수
        if (menu_select == '2'):
            bucket_book()  # 대여/장바구니 함수
        if (menu_select == '3'):
            return_book()  # 반납 함수
        if (menu_select == '4'):
            Donation()  # 기증 함수
        if (menu_select == '5'):
            while (1):
                os.system("clear")
                time.sleep(1)
                print('---------ଘʕ੭·ㅅ·ʔ੭ 내 정보 ଘʕ੭·ㅅ·ʔ੭---------')

                print('▶ 대여중인 도서 리스트')
                cur.execute('SELECT * FROM rentlist WHERE userid=?', (userid,))
                find = cur.fetchall()
                print(find)

                print('=' * 30)
                print('▶ 대여후 반납한 도서 리스트')
                cur.execute('SELECT * FROM returnlist WHERE userid=?', (userid,))
                find = cur.fetchall()
                print(find)

                print('▶ 미납중인 도서 리스트')

                cur.execute('SELECT * FROM rentlist WHERE userid=?', (userid,))
                find = cur.fetchall()
                print(find)

                print('=' * 30)

                print('1.내 정보 변경')
                print('2.연체 정보 조회하기')
                print('-----------------------------------------')
                slt = input()
                if slt == '1':  # 내 정보 변경
                    regist_user = {}  # regist_user 딕셔너리 (만든 아이디 저장)
                    sw = 1
                    while sw:
                        cur.execute("SELECT id,pwd FROM userlist")  # 로그인할때 필요한 id,pwd읽기
                        db_user = cur.fetchall()  # 동일함
                        print('1)비밀번호 변경 2)이름 변경 3)번호 변경 4)나가기')
                        choice = int(input('선택해주세요:'))
                        if (choice == 1):
                            uid = str(input('아이디를 입력해주세요:'))
                            cur.execute("SELECT id FROM userlist")
                            db_id = cur.fetchall()
                            for search in db_id:
                                if uid in search:
                                    new_pwd = change_password(pwd)
                                    print('비밀번호 변경 완료\n')
                                else:
                                    continue

                        elif (choice == 2):
                            uid = str(input('아이디를 입력해주세요:'))
                            cur.execute("SELECT id FROM userlist")
                            db_id = cur.fetchall()
                            for search in db_id:
                                if uid in search:
                                    new_name = change_name(name)
                                    print('이름 변경 완료\n')
                                else:
                                    continue
                        elif (choice == 3):
                            uid = str(input('아이디를 입력해주세요:'))
                            cur.execute("SELECT id FROM userlist")
                            db_id = cur.fetchall()
                            for search in db_id:
                                if uid in search:
                                    new_num = change_num(num)
                                    print('번호 변경 완료\n')
                                else:
                                    continue
                        elif (choice == 4):
                            break
                    else:
                        print('1~4 중에 골라주세요')
                        continue
                if slt == '2':
                    print('연체 정보 없음')
                    print('연체 정보 없음')
                    cur.execute("SELECT bookname,writer,returndate FROM rentlist WHERE userid=?", (userid,))
                    find = cur.fetchall()
                    for i in find:
                        print(f'{i[0]},{i[1]}, 반납일은 {i[2]}까지 입니다.')
                        time.sleep(2)

                if slt == 'q' or 'ㅂ':
                    break


def main2():
    global userid
    regist_user = {}  # regist_user 딕셔너리 (만든 아이디 저장)
    sw = 1  # while문 1 or 0 조건을 위해 선언
    while sw:
        cur.execute("SELECT id,pwd FROM userlist")  # 로그인할때 필요한 id,pwd읽기
        db_user = cur.fetchall()  # 동일함
        print('-' * 30)
        print('1. 아이디 생성')
        print('2. 아이디 & 비밀번호 찾기')
        print('3. 아이디 목록 ')
        print('4. 로그인 ')
        print('5. 종료')
        print('-' * 30)
        select_no = int(input('번호 선택(1~5): '))

        if select_no == 1:  # 아이디생성
            id_result = make_id(regist_user)
            if id_result:
                regist_user[id_result[0]] = id_result[1]
                print('ID 생성 완료!')
                time.sleep(1)
                os.system('clear')

        elif select_no == 2:  # ID/PW 찾기
            global name
            name = input('회원가입한 ID를 입력하세요: ')
            for search in db_user:
                if name in search:
                    print(search)
                    time.sleep(2)
                    break
                else:
                    # print('등록된 ID가 아닙니다.\n')
                    time.sleep(1)
                    continue

        elif select_no == 3:  # 아이디 목록 확인
            for i in db_user:
                print(i)
            time.sleep(2)
            os.system('clear')

        elif select_no == 4:  # 로그인
            id_input = input('ID 입력:')
            pw_input = input('PW 입력:')
            for search in db_user:
                if id_input == search[0] and pw_input == search[1]:
                    print('로그인 성공')
                    global userid
                    userid = id_input
                    time.sleep(2)
                    main()
            else:
                print('로그인 실패')
                continue
        elif select_no == 5:  # 종료
            sw = 0
        else:  # 예외처리
            print('잘못입력하셨습니다. 1~5 중에 골라주세요')
            time.sleep(1)
            os.system('clear')
            continue


main2()
cur.close()