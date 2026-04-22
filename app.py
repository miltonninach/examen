from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)