import requests
from bs4 import BeautifulSoup
import re
import simplejson as json

f = open("test.txt","w",encoding='utf-8')
for quzi in range(1,10586):
   
    r = requests.post("http://q.fran.kr/문제/"+str(quzi))
    if(r.text.find("올바르지 않은 문제번호") != -1):
        pass
    else:
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        soup_title_text = soup.find("h5",class_="subject")
        soup_title_text_str = str(soup_title_text.text)
        r_text_id = soup.find('span',id='examSelect')
        rsid = str(r_text_id.text)
        print("\n"+rsid.strip()+"\n\n")
        f.write(soup_title_text_str+"\n")
        print(soup_title_text.text)
        if(soup.find("pre")):
            f.write('\n')
            print()
            f.write("ㅡㅡㅡㅡㅡ 보기 ㅡㅡㅡㅡㅡ\n")
            print("ㅡㅡㅡㅡㅡ 보기 ㅡㅡㅡㅡㅡ")
            for i in soup.find_all("pre"):
                i_text = str(i.text)
                f.write(i_text+"\n")
                print(i.text)
            f.write("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n")
            print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
        else:
            pass
            print('')
            f.write("\n")
        soup_checkanswer = soup.find("ul",class_="example")
        expl = soup_checkanswer.find_all("li")
        
        for solve_value in expl:
            test_solve = str(solve_value.text)
            f.write(test_solve+"\n")
            print(solve_value.text,end='\n\n')
        solve_answer = soup.find("div",class_="answer")
        if solve_answer:
            solve_answer = str(solve_answer.text).replace("클릭하면 정답이 보입니다.", "")
            test = " ".join(solve_answer.split())
            print(test)
        else:
            solve_board = soup.find("div",class_ = "border")
            if(solve_board):
                print("정답이 없는 서술형 문제입니다 설명하시오")
            else:
                for i in range(1,20):
                    data ={
                        'question':quzi,
                        'answer':i
                    }
                    req = requests.post("http://q.fran.kr/checkAnswer.php",data=data)
                    d = json.loads(req.text)
                    if d.get("msg"):
                        ok_msg = 10
                    if i >= 19:
                        if ok_msg == 10:
                            print("해당 페이지의 오류로인해 정답이 없는거같습니다.")

                    if d.get("data"):
                        a = i
                        reques = requests.post("http://q.fran.kr/server/showAnswer.php",data=data)
                        q = json.loads(reques.text)
                        da_ta_value = 1
                        ok = 2
                        for da_ta in q['data']:
                            if da_ta_value == a:
                                ok = 1
                                ok_msg = 5
                                f.write("\n************************************\n")
                                print("************************************")

                                f.write("정답"+str(i)+" 번:"+da_ta['contents']+"\n")
                                print("정답 "+str(i)+" 번 :"+da_ta['contents']+"\n")

                                f.write("************************************\n\n")
                                print("************************************\n")
                                break
                            else:
                                pass
                            da_ta_value+=1
                        break
                    else:
                        pass
f.close()