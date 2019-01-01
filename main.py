import requests
import json
from tkinter import *
from tkinter import messagebox


def change_frame(f):
    f.tkraise()


root = Tk()

root.title("محاسبه زمان اجراي کد")

root.geometry('800x500')

frame1 = Frame(root)
frame2 = Frame(root)
frame3 = Frame(root)

for frame in (frame1, frame2, frame3):
    frame.grid(row=0, column=0, sticky='news')


def hframe3():
    root.geometry('800x500')
    change_frame(frame3)

def calc_handle():
    user_input = frame2entry.get("1.0", "end-1c")
    complexity = equation(user_input)
    messagebox.showwarning("", f"{complexity} \n")

Button(frame1, text=' محاسبه مرتبه زمانی یک کد مستقل ' , bg="yellow", fg="black", command=lambda: change_frame(frame2)).place(x=350, y=150)


Button(frame1, text='مقایسه مرتبه زمانی دو کد', bg="yellow", fg="black", command=lambda: change_frame(frame3)).place(x=372,y=200)

Button(frame2, text='بازگشت به صفحه اول', bg="black", fg="white", command=lambda: change_frame(frame1)).place(x=525,y=300)

btn = Button(frame2, text="محاسبه کن", bg="green", fg="white", command=calc_handle).place(x=550, y=200)



frame2entry = Text(frame2, bg="yellow", fg="red", height=30, width=60)
frame2entry.place(x=10, y=10)
frame2entry.insert(END, """// Enter your code here: 
int main()
{	

	
return 0;
}""")


def compiler(inpt):
    url = "https://api.jdoodle.com/v1/execute"
    headers = {'Content-type': 'application/json'}
    payload = {"clientId": "fdd703fe8c319389ca26ed052413ae87",
               "clientSecret": "51133fcab2c301dc71e99ee905643c23bb5a6ff7cdb2b85a4849c1083e362360",
               "script": """{}""".format(inpt),
               "language": "c",
               "versionIndex": "0",
               }
    response = requests.post(url=url, data=json.dumps(payload), headers=headers)
    response_parsed = response.json()
    return response_parsed['output']


def lagrange_api(points):
    url = "https://www.dcode.fr/api/"
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    payload = {"tool": "lagrange-interpolating-polynomial",
               "points": f"{points}"
               }

    response = requests.post(url=url, data=payload, headers=headers)
    output = response.json()
    return output


def point(source, N):
    final_source = "\n#include<stdio.h>" + "\n" + "#define n {}\n".format(N) + source
    output = compiler(final_source)
    tup = (N, len(output))
    return tup


def equation(usr_src):
    points = ""
    for n in range(0, 5, 1):
        points += str(point(usr_src, n))

    print("final points are: {}".format(points))
    dcode_response = lagrange_api(points)
    equation = dcode_response['results']
    print(f"Equation: {equation.strip('$$')}")
    final_equation = equation.strip('$$')
    return final_equation






Label(frame3).place(x=0, y=0, relwidth=1, relheight=1)
frame3entry = Text(frame3, bg="yellow", fg="black", height=25, width=35)
frame3entry.insert(END, "//Your first code here:")
frame3entry.grid(column=1, row=1)

lbl = Label(frame3, bg="black", fg="white", text="vs.")
lbl.grid(column=2, row=1)

frame3entry2 = Text(frame3, bg="red", fg="black", height=25, width=35)
frame3entry2.insert(END, "//Your second code here:")
frame3entry2.grid(column=3, row=1)


def compare_handle():
    c1 = equation(frame3entry.get("1.0", "end-1c"))
    c2 = equation(frame3entry2.get("1.0", "end-1c"))
    if c1 > c2:
        messagebox.showinfo("", f"left={c1} and has not a better performance")
    elif c1 < c2:
        messagebox.showinfo("", f"right={c2} and has not a better performance")
    else:
        messagebox.showinfo("", f"The order of both codes : {c1}")


compare_btn = Button(frame3,
                     text="مقایسه کن",
                     bg="green", fg="white", command=compare_handle)
compare_btn.grid(row=1, column=5)


change_frame(frame1)
root.mainloop()
