from flask import Blueprint, render_template, redirect, url_for, request, flash
from connect import create_connection

# Create a blueprint for modular routing
routesMataPelajaran = Blueprint('routesMataPelajaran', __name__)

@routesMataPelajaran.route('/')
def index():
    return render_template('home.html')
    d
@routesMataPelajaran.route('/tableMataPelajaran')
def tableMataPelajaran():
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
            SELECT * FROM matapelajaran
            ORDER BY id_mapel  -- or any other column for sorting
            OFFSET ? ROWS
            FETCH NEXT ? ROWS ONLY
        ''', (offset, per_page))

        # cursor.execute('SELECT * FROM TableA')
        
        # Fetch the results
        table = cursor.fetchall()
        
        # Get the total count of rows to calculate the number of pages
        cursor.execute('SELECT COUNT(*) FROM matapelajaran')
        total_count = cursor.fetchone()[0]
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        # Calculate total number of pages
        total_pages = (total_count + per_page - 1) // per_page
        
        # Pass the results, total pages, and current page to the template
        return render_template('tableMataPelajaran.html', table=table, total_pages=total_pages, current_page=page)
    else:
        return render_template('tableMataPelajaran.html', table=None)

@routesMataPelajaran.route('/Create/createMataPelajaran', methods=['GET', 'POST'])
def create_MataPelajaran():
    # Handle the form submission when the method is POST
    if request.method == 'POST':
        # properti input digunakan disini
        mataPelajaran_id_mapel         = request.form['id_mapel_MataPelajaran']
        mataPelajaran_mata_pelajaran   = request.form['mata_pelajaran_MataPelajaran']
        mataPelajaran_kelas            = request.form['kelas_MataPelajaran']
        mataPelajaran_id_guru          = request.form['id_guru_MataPelajaran']


        # Get a connection to the database
        conn = create_connection()
        
        # Check if the connection was successful
        if conn:
            cursor = conn.cursor()
            try:
                # Insert the new tableA into the database
                cursor.execute('INSERT INTO Kelas (id_mapel, mata_pelajaran, kelas, id_guru) VALUES (?, ?, ?, ?)', 
                                (mataPelajaran_id_mapel, mataPelajaran_mata_pelajaran, mataPelajaran_kelas, mataPelajaran_id_guru))
                conn.commit()  # Commit the transaction
                
                # Redirect to the tableA list with a success message
                flash('Table Mata Pelajaran added successfully!', 'success')
                return redirect(url_for('routesMataPelajaran.tableMataPelajaran'))
            except Exception as e:
                flash(f'Error: {str(e)}', 'danger')  # Flash error message
            finally:
                cursor.close()
                conn.close()
        
        flash('Failed to connect to the database', 'danger')  # Error if connection failed

    # Render the form for GET request
    return render_template('Create/createMataPelajaran.html')