from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def task_printer(list_of_tasks):
    if len(list_of_tasks) < 1:
        print("Nothing to do!")
    else:
        for i, t in enumerate(list_of_tasks):
            print(f"{i + 1}. {t}")


def task_printer_long(list_of_tasks):
    for i, t in enumerate(list_of_tasks):
        print(f"{i + 1}. {t}. {t.deadline.strftime('%d %b')}")
    print("")


while True:
    all_tasks = session.query(Table)
    today = datetime.today().date()
    print("1) Today's tasks", "2) Week's tasks", "3) All tasks",
          "4) Missed tasks", "5) Add task", "6) Delete task", "0) Exit", sep="\n")
    usr_ch = input()
    if usr_ch == "0":
        print("Bye!")
        break
    elif usr_ch == "1":
        today_tasks = all_tasks.filter(Table.deadline == today).all()
        print(f"Today {today.strftime('%d %b')}")
        task_printer(today_tasks)
    elif usr_ch == "2":
        for day in [today + timedelta(days=n) for n in range(0, 7)]:
            day_tasks = all_tasks.filter(Table.deadline == day).all()
            print(day.strftime("%A %d %b") + ":")
            task_printer(day_tasks)
            print("")
    elif usr_ch == "3":
        all_tasks_sorted = all_tasks.order_by(Table.deadline).all()
        print("All tasks:")
        task_printer_long(all_tasks_sorted)
    elif usr_ch == "4":
        missed_tasks = all_tasks.filter(Table.deadline < today).order_by(Table.deadline).all()
        print("Missed tasks:")
        task_printer_long(missed_tasks)
    elif usr_ch == "5":
        new_task = input("Enter task: ")
        new_task_date = datetime.strptime(input("Enter deadline: "), "%Y-%m-%d")
        new_row = Table(task=new_task, deadline=new_task_date)
        session.add(new_row)
        session.commit()
        print("The task has been added!")
    elif usr_ch == "6":
        all_tasks_sorted = all_tasks.order_by(Table.deadline).all()
        print("Choose the number of the task you want to delete:")
        task_printer_long(all_tasks_sorted)
        dlt_choice = int(input())
        session.delete(all_tasks_sorted[dlt_choice - 1])
        session.commit()
        print("The task has been deleted!")
