from flask import Blueprint, render_template, redirect, url_for, request, flash
from connect import create_connection

# Create a blueprint for modular routing
routesKelas = Blueprint('routesKelas', __name__)

@routesKelas.route('/')
def index():
    return render_template('home.html')

@routesKelas.route('/tableKelas')
def tableKelas():
    # Get the current page number from the query string (default to page 1)
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Number of items per page
    
    # Calculate the starting row for the query (offset)
    offset = (page - 1) * per_page
    
    # Get a connection to the database
    conn = create_connection()
    
    if conn:
        # Create a cursor from the connection
        cursor = conn.cursor()
        
        # Execute a query with pagination using OFFSET and FETCH NEXT
        cursor.execute('''
            SELECT * FROM kelas
            ORDER BY id_kelas  -- or any other column for sorting
            OFFSET ? ROWS
            FETCH NEXT ? ROWS ONLY
        ''', (offset, per_page))

        # cursor.execute('SELECT * FROM TableA')
        
        # Fetch the results
        table = cursor.fetchall()
        
        # Get the total count of rows to calculate the number of pages
        cursor.execute('SELECT COUNT(*) FROM kelas')
        total_count = cursor.fetchone()[0]
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        # Calculate total number of pages
        total_pages = (total_count + per_page - 1) // per_page
        
        # Pass the results, total pages, and current page to the template
        return render_template('tableKelas.html', table=table, total_pages=total_pages, current_page=page)
    else:
        return render_template('tableKelas.html', table=None)

@routesKelas.route('/Create/createKelas', methods=['GET', 'POST'])
def create_Kelas():
    # Handle the form submission when the method is POST
    if request.method == 'POST':
        # properti input digunakan disini
        kelas_id_kelas  = request.form['id_kelas_Kelas']
        kelas_id_guru   = request.form['id_guru_Kelas']
        kelas_kelas     = request.form['kelas_Kelas']

        # Get a connection to the database
        conn = create_connection()
        
        # Check if the connection was successful
        if conn:
            cursor = conn.cursor()
            try:
                # Insert the new tableA into the database
                cursor.execute('INSERT INTO Kelas (id_kelas, id_guru, kelas) VALUES (?, ?, ?)', 
                                (kelas_id_kelas, kelas_id_guru, kelas_kelas))
                conn.commit()  # Commit the transaction
                
                # Redirect to the tableA list with a success message
                flash('Table Kelas added successfully!', 'success')
                return redirect(url_for('routesKelas.tableKelas'))
            except Exception as e:
                flash(f'Error: {str(e)}', 'danger')  # Flash error message
            finally:
                cursor.close()
                conn.close()
        
        flash('Failed to connect to the database', 'danger')  # Error if connection failed

    # Render the form for GET request
    return render_template('Create/createKelas.html')

# Delete Data
@routesKelas.route('/tableKelas/delete/<id_kelas>', methods=['POST'])
def delete_continent(id_kelas):
    # Get a connection to the database
    conn = create_connection()
    
    # Check if the connection was successful
    if conn:
        cursor = conn.cursor()
        try:
            # Delete the tableA from the database
            cursor.execute('DELETE FROM Kelas WHERE id_kelas = ?', (id_kelas,))
            conn.commit()  # Commit the transaction
            
            # Redirect to the tableA list with a success message
            flash(f'{id_kelas} deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()  # Ensure the connection is closed
    else:
        flash('Error: Unable to connect to the database.', 'danger')
    
    return redirect(url_for('routesKelas.tableKelas'))