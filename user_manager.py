import sqlite3
import streamlit as st

DB_NAME = 'users.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    address TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()


def add_user(first_name, last_name, address):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO users (first_name, last_name, address) VALUES (?, ?, ?)",
              (first_name, last_name, address))
    conn.commit()
    conn.close()


def list_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    rows = c.execute('SELECT id, first_name, last_name, address FROM users').fetchall()
    conn.close()
    return rows


def delete_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE id=?', (user_id,))
    conn.commit()
    conn.close()


def main():
    st.title('User Manager')
    init_db()

    st.header('Add User')
    with st.form('add_form'):
        fn = st.text_input('First Name')
        ln = st.text_input('Last Name')
        address = st.text_input('Address (include ZIP and Country)')
        submit = st.form_submit_button('Add')

    if submit:
        if fn and ln and address:
            add_user(fn, ln, address)
            st.success('User added')
            st.experimental_rerun()
        else:
            st.error('Please fill in all fields')

    st.header('Current Users')
    users = list_users()
    if users:
        for row in users:
            st.write(f"ID: {row[0]} | FN: {row[1]} | LN: {row[2]} | Address: {row[3]}")
    else:
        st.write('No users found.')

    st.header('Delete User')
    user_ids = [row[0] for row in users]
    if user_ids:
        selected = st.selectbox('User ID', user_ids)
        if st.button('Delete'):
            delete_user(selected)
            st.success(f'User {selected} deleted')
            st.experimental_rerun()
    else:
        st.write('No users to delete.')


if __name__ == '__main__':
    main()
