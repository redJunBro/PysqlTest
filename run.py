from flask import Flask
from flask import request
from flask import redirect
from datetime import timedelta
from flask import url_for
from flask import render_template
from flask import flash
from flask import session
import pymysql
import time
import math



app = Flask(__name__)
app.config["SECRET_KEY"] = "ascd"
app.config["PERMANT_SESSION_LOFETIME"] = timedelta(minutes=30)

def insert_board_func(name, title, contents):
        try:
                conn = pymysql.connect(host="localhost", user="root", password="111111", db="toto", charset="utf8")
                curs = conn.cursor()
                sql = """insert into board(name, title, contents)
                        values (%s, %s, %s)"""      
                data = (name, title, contents)

                curs.execute(sql, data)
                board_id = curs.lastrowid
                conn.commit()
                conn.close()

                print('보드 인설트 완료 :'+ str(board_id))
                return board_id
        except pymysql.err as e:
                print('보드 인설트 오류'+ e)
        


def insert_memvers_func(name, email, password, phone_number):
        try:
                conn = pymysql.connect(host="localhost", user="root", password="111111", db="toto", charset="utf8")
                curs = conn.cursor()
                sql = """insert into memvers(name, email, password, phone_number)
                        values (%s, %s, %s, %s)"""      
                data = (name, email, password, phone_number)

                curs.execute(sql, data)
                conn.commit()
                conn.close()

                print('멤버 인설트 완료')
        except Exception as e:
                print('멤버 인설트 오류')
                ValueError(e)

def memvers_select(email):
        try:
                conn = pymysql.connect(host="localhost", user="root", password="111111", db="toto", charset="utf8")
                curs = conn.cursor()
                sql = "select * from memvers where email=%s"      
                data= (email,)
                curs.execute(sql,data)
                row = curs.fetchone()
                
                if row is not None:
                        x = 1
                else:
                        x = 2
                
                conn.close()

                print('멤버 셀럭트 완료')
                return x
        except Exception as e:
                print('멤버셀렉트 오류')
                print(e)
                return 2

def board_select(board_id):
        try:
                conn = pymysql.connect(host="localhost", user="root", password="111111", db="toto", charset="utf8")
                curs = conn.cursor()
                sql = "select id,name,title,contents from board where id='%s'" 
                data = int(board_id,)     
                curs.execute(sql, data)
                row = curs.fetchone()
                conn.close()

                print('보드 셀럭트 완료 :')
                return row
        except Exception as e:
                print('보드 셀렉트 오류'+e)


def all_board_select(limite,now_page):
        try:
                conn = pymysql.connect(host="localhost", user="root", password="111111", db="toto", charset="utf8")
                #curs = conn.cursor()
                curs = conn.cursor(pymysql.cursors.DictCursor)
                # sql = '''select * from board'''
                sql = '''select * from board LIMIT %s OFFSET %s;'''
                data = (limite, now_page)
                curs.execute(sql,data)
                rows = curs.fetchall()
                print(rows)
                print('올 보드 셀럭트 완료 : ')
                return rows
        except Exception as e:
                print('보드 셀렉트 오류'+e)

def title_board_select(keyword,limite,now_page):
        try:
                conn = pymysql.connect(host="localhost", user="root", password="111111", db="toto", charset="utf8")
                #curs = conn.cursor()
                curs = conn.cursor(pymysql.cursors.DictCursor)
                # sql = '''select * from board'''
                sql = '''select * from board where title=%sLIMIT %s OFFSET %s;'''
                
                data = (keyword, limite, now_page)
                curs.execute(sql,data)
                rows = curs.fetchall()
                print(rows)
                print('타이틀 보드 셀럭트 완료 : ')
                return rows
        except Exception as e:
                print('보드 셀렉트 오류'+e)

def name_board_select(name,limite,now_page):
        try:
                conn = pymysql.connect(host="localhost", user="root", password="111111", db="toto", charset="utf8")
                #curs = conn.cursor()
                curs = conn.cursor(pymysql.cursors.DictCursor)
                # sql = '''select * from board'''
                sql = '''select * from board WHERE name=%sLIMIT %s OFFSET %s;'''
                data = (name,limite, now_page)
                curs.execute(sql,data)
                rows = curs.fetchall()
                print(rows)
                print('올 보드 셀럭트 완료 : ')
                return rows
        except Exception as e:
                print('보드 셀렉트 오류'+e)

def contents_board_select(contents,limite,now_page):
        try:
                conn = pymysql.connect(host="localhost", user="root", password="111111", db="toto", charset="utf8")
                #curs = conn.cursor()
                curs = conn.cursor(pymysql.cursors.DictCursor)
                # sql = '''select * from board'''
                sql = '''select * from board WHERE contents=%s LIMIT %s OFFSET %s;'''
                data = (contents, limite, now_page)
                curs.execute(sql,data)
                rows = curs.fetchall()
                print(rows)
                print('올 보드 셀럭트 완료 : ')
                return rows
        except Exception as e:
                print('보드 셀렉트 오류'+e)

# def list_board():
#         try:
#                 conn = pymysql.connect(host="localhost", user="root", password="111111", db="toto", charset="utf8")
#                 # curs = conn.cursor()
#                 curs = conn.cursor(pymysql.cursors.DictCursor)
#                 sql = '''select * from board'''
#                 curs.execute(sql)
#                 for x in w:
#                         rows = curs.fetchone()


#                 print('리스트 보드 셀럭트 완료 :')
#                 return rows
#         except Exception as e:
#                 print('리스트 보드 오류'+e)

def board_count():
        try:
                conn = pymysql.connect(host="localhost", user="root", password="111111", db="toto", charset="utf8")
                curs = conn.cursor()
                sql = '''select count(*) from board'''
                curs.execute(sql)
                row = curs.fetchone()
                count = row[0]

                return count
        except Exception as e:
                print('보드 카운트 오류'+e)

def password_memvers_select(email,password):
        try:
                conn = pymysql.connect(host="localhost", user="root", password="111111", db="toto", charset="utf8")
                curs = conn.cursor()
                sql = "select * from memvers where email=%s and password=%s"      
                data= (email,password)
                curs.execute(sql,data)
                row = curs.fetchone()
                print(row)
                
                if row is not None:
                        x = 1
                else:
                        x = 2
                
                conn.close()

                print('패스워드 멤버 셀럭트 완료')
                return x
        except Exception as e:
                print('멤버셀렉트 오류')
                print(e)
                return 2


        



@app.route("/write", methods=["GET","POST"])
def board_write():
        if request.method == "POST":
                name = request.form.get("name")
                title = request.form.get("title")
                contents = request.form.get("contents")

                board_id = insert_board_func(name,title,contents)
                return redirect(url_for("board_view",idx=board_id))

        else :
                return render_template("write.html")

@app.route("/view/<idx>", methods=["GET"])
def board_view(idx):
        if idx is not None and idx:
                page = request.args.get("page")
                search = request.args.get("search")
                keyword = request.args.get("keyword")
                data = board_select(idx)
                if data is not None:
                        result = {
                                "name": data[1],
                                "title": data[2],
                                "contents":data[3]
                        }
                else: 
                        pass

        return render_template("view.html",result=result,page=page,search=search,keyword=keyword)

@app.route("/list")
def lists():
        search = request.args.get("search", -1, type=int)
        keyword = request.args.get("keyword", "", type = str)
        page = request.args.get("page", 1, type=int)
        limite = request.args.get("limite", 5,type=int)
        

        

        # 페이지가 1이면 1 페이지가 2 면 6 페이지가 3이면 11
        now_page = (page * limite) - 4
        print (now_page)
        tot_count = board_count()
        last_page_num = math.ceil(tot_count / limite)
        block_size = 5
        block_num = int((page - 1) / block_size)
        block_start = int((block_size * block_num) + 1)
        block_last = math.ceil(block_start + (block_size - 1))
        # datas = all_board_select(limite,now_page)
        
        if search == -1:
                print(keyword)
                datas = all_board_select(limite,now_page)
        elif search == 0:
                print(keyword)
                datas = title_board_select(keyword,limite,now_page)
        elif search == 1:#내용
                datas = contents_board_select(keyword,limite,now_page)
        # elif search == 2:#제목 내용
        #         datas = title_board_select(keyword,limite,now_page) + contents_board_select(keyword,limite,now_page)
                
        elif search == 3:#작성자
              datas = name_board_select(keyword,limite,now_page)


        return render_template(
                "list.html",
                datas=datas,
                page=page,
                limite=limite,
                last_page_num=last_page_num,
                block_start=block_start,
                block_last=block_last,
                search = search,
                keyword = keyword
                )

@app.route("/join", methods=["GET", "POST"])
def member_join():
    if request.method == "POST":
        print('전송완료')
        name = request.form.get("name", type=str)
        email = request.form.get("email", type=str)
        pass1 = request.form.get("pass1", type=str)
        pass2 = request.form.get("pass2", type=str)
        phone = request.form.get("phone", type=str)

        if name == "" or email == "" or pass1 == "" or pass2 == "":
            flash("입력되지 않은 값이 있습니다.")
            return render_template("join.html")
        if pass1 != pass2:
            flash("비밀번호가 일치하지 않습니다.")
            return render_template("join.html")

        print(email)
        i = memvers_select(email)
        if i == 1:
            flash("중복된 이메일 입니다.")
            return render_template("join.html")
        else:
                print("login")
                insert_memvers_func(name,email,pass1,phone)
                flash("회원가입 완료.")
                return redirect(url_for("lists"))

    else:
        return render_template("join.html")


@app.route("/login", methods=["GET", "POST"])
def member_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pass1")
        data = memvers_select(email)

        if data is None:
            flash("회원정보가 없습니다")
            return redirect(url_for("member_login"))
        else:
                x = password_memvers_select(email,password)
                if  x == 1:
                        session["email"] = email
                        session.permanent = True
                
                        return redirect(url_for("lists"))

                else:
                        flash("비밀번호가 일치하지않습니다.")
                        return redirect(url_for("member_login"))
        
    else:
        
        return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True, port=9000)