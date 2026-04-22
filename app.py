from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
def init_db():
    conn = sqlite3.connect('citas.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mascota TEXT NOT NULL,
            propietario TEXT NOT NULL,
            especie TEXT,
            fecha TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('citas.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pacientes")
    citas = cursor.fetchall()

    conn.close()
    return render_template('index.html', citas=citas)


@app.route('/create')
def create():
    return render_template('create.html')


@app.route('/save', methods=['POST'])
def save():
    mascota = request.form['mascota']
    propietario = request.form['propietario']
    especie = request.form['especie']
    fecha = request.form['fecha']

    conn = sqlite3.connect('citas.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pacientes (mascota, propietario, especie, fecha)
        VALUES (?, ?, ?, ?)
    """, (mascota, propietario, especie, fecha))

    conn.commit()
    conn.close()

    return redirect('/')
@app.route('/edit/<int:id>')
def edit(id):
    conn = sqlite3.connect('citas.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pacientes WHERE id=?", (id,))
    cita = cursor.fetchone()

    conn.close()
    return render_template('edit.html', cita=cita)

@app.route('/update', methods=['POST'])
def update():
    id = request.form['id']
    mascota = request.form['mascota']
    propietario = request.form['propietario']
    especie = request.form['especie']
    fecha = request.form['fecha']

    conn = sqlite3.connect('citas.db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE pacientes 
        SET mascota=?, propietario=?, especie=?, fecha=? 
        WHERE id=?
    """, (mascota, propietario, especie, fecha, id))

    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('citas.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM pacientes WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)