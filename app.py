from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)


def get_db_connection():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='employee',
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn  
    except pymysql.MySQLError as e:
        print(f"Database connection failed: {e}")
        return None



@app.route('/')
def index():
    conn = get_db_connection()
    if conn is None:
        return "Database connection failed", 500
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employeee")
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html",employees=employees)


@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            department = request.form['department']
            salary = request.form['salary']

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO employeee (name, email, department, salary) VALUES (%s, %s, %s, %s)",
                (name, email, department, salary)
            )
            conn.commit()
            cursor.close()
            conn.close()

            print("✅ INSERT SUCCESS")
            return redirect(url_for('index'))

        except Exception as e:
            print("❌ DB ERROR:", e)
            return "Database error — check terminal"

    return render_template("add.html")



@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        department = request.form.get('department')
        salary = request.form.get('salary')

        cursor.execute(
            "UPDATE employee SET name=%s, email=%s, department=%s, salary=%s WHERE id=%s",
            (name, email, department, salary, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM employee WHERE id=%s", (id,))
    employee = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("edit.html", employee=employee)

@app.route('/delete/<int:id>')
def delete_employee(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employeee WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
