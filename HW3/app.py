from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# 初始化 task.xlsx
TASK_FILE = "task.xlsx"
try:
    df = pd.read_excel(TASK_FILE)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Date", "Task", "Location", "Priority", "Subtask 1", "Subtask 2", "Subtask 3"])
    df.to_excel(TASK_FILE, index=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/task", methods=["GET", "POST"])
def task():
    if request.method == "POST":
        date = request.form["date"]
        task = request.form["task"]
        location = request.form["location"]
        priority = request.form["priorty"]
        detail_1 = request.form["detail_1"]
        detail_2 = request.form["detail_2"]
        detail_3 = request.form["detail_3"]

        # 新增事件到 DataFrame
        new_event = pd.DataFrame([{
            "Date": date,
            "Task": task,
            "Location": location,
            "Priority": priority,
            "Subtask 1": detail_1,
            "Subtask 2": detail_2,
            "Subtask 3": detail_3,
        }])

        # 使用 pd.concat 合併新事件
        df = pd.read_excel(TASK_FILE)
        updated_df = pd.concat([df, new_event], ignore_index=True)
        updated_df.to_excel(TASK_FILE, index=False)

        return redirect(url_for("index"))
    return render_template("task.html")


@app.route("/date/<date>")
def date_view(date):
    df = pd.read_excel(TASK_FILE)
    # 篩選選中的日期的任務
    filtered_tasks = df[df["Date"] == date]
    tasks = filtered_tasks[["Task"]].to_dict(orient="records")
    return render_template("date.html", date=date, tasks=tasks)


if __name__ == "__main__":
    app.run(debug=True)
