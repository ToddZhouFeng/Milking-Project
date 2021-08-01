from flask import Flask, render_template, request, jsonify
import database.database as database
import milk.milk as milk
from threading import Thread

app = Flask(__name__)

@app.route("/milk", methods=["GET", "POST"])
def milk_index():
    if request.method == "POST":
        if "get_num" in request.form:
            try:
                get_num = request.form["get_num"]
            except KeyError:
                return jsonify({})
            return jsonify({"scan_num": milk.scan_num})
        elif "input" in request.form:
            try:
                keyWord = request.form["input"]
                page = int(request.form["page"])
            except KeyError:
                print("KeyError")
                return jsonify({})
            if keyWord == "":
                where = ""
            else:
                where = ""
            page_num = 20
            db = database.MilkDatabase()
            result = db.select(start = (page-1)*page_num, num = page_num, sort = "scanDate", order = 'DESC', where = "instr(fileName, '%s') > 0"%keyWord)
            db.close()

            json = {
                "length":len(result),
                "result":[
                    {
                        "tempCode": i[0],
                        "fileName": i[1],
                        "totalSizeByte": milk.StrOfSize(i[2]),
                        "uniqueUrl": i[3],
                        "uploadDate": i[4],
                        "expireAt": i[5],
                        "scanDate": i[6]
                    } for i in result
                ]
            }
            return jsonify(json)
    else:
        return render_template("milk_index.html")

def print_scan():
    current_scan_num = -1
    while(True):
        if current_scan_num != milk.scan_num:
            print("scan num",milk.scan_num)
            current_scan_num = milk.scan_num
        else:
            continue

if __name__ == '__main__':
    
    scan_thread = Thread(target=milk.scan)
    # print_thread = Thread(target=print_scan)
    scan_thread.start()
    # print_thread.start()
    app.run(host='0.0.0.0', port=5000, debug = False)
    print("Main program end.")
    
    
    


#参考
#如何写get方法：https://gist.github.com/KentaYamada/2eed4af1f6b2adac5cc7c9063acf8720