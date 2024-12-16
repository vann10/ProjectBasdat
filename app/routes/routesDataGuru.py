from flask import Blueprint, render_template, redirect, url_for, request, flash
from connect import create_connection

# Create a blueprint for modular routing
routesDataGuru = Blueprint('routesDataGuru', __name__)

@routesDataGuru.route('/')
def index():
    return render_template('home.html')

@routesDataGuru.route('/tableDataGuru')
def tableDataGuru():
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
            SELECT * FROM dataguru
            ORDER BY id_guru  -- or any other column for sorting
            OFFSET ? ROWS
            FETCH NEXT ? ROWS ONLY
        ''', (offset, per_page))

        # cursor.execute('SELECT * FROM TableA')
        
        # Fetch the results
        table = cursor.fetchall()
        
        # Get the total count of rows to calculate the number of pages
        cursor.execute('SELECT COUNT(*) FROM dataguru')
        total_count = cursor.fetchone()[0]
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        # Calculate total number of pages
        total_pages = (total_count + per_page - 1) // per_page
        
        # Pass the results, total pages, and current page to the template
        return render_template('tableDataGuru.html', table=table, total_pages=total_pages, current_page=page)
    else:
        return render_template('tableDataGuru.html', table=None)

# Create Data
@routesDataGuru.route('/Create/createDataGuru', methods=['GET', 'POST'])
def create_DataGuru():
    # Handle the form submission when the method is POST
    if request.method == 'POST':
        # properti input digunakan disini
        dataGuru_id_guru        = request.form['id_guru_DataGuru']
        dataGuru_nuptk          = request.form['nuptk_DataGuru']
        dataGuru_nama_guru      = request.form['nama_guru_DataGuru']
        dataGuru_jenis_kelamin  = request.form['jenis_kelamin_DataGuru']
        dataGuru_tanggal_lahir  = request.form['tanggal_lahir_DataGuru']
        dataGuru_alamat         = request.form['alamat_DataGuru']
        
        # Get a connection to the database
        conn = create_connection()
        
        # Check if the connection was successful
        if conn:
            cursor = conn.cursor()
            try:
                # Insert the new tableA into the database
                cursor.execute('INSERT INTO DataGuru (id_guru, nuptk, nama_guru, jenis_kelamin, tanggal_lahir, alamat) VALUES (?, ?, ?, ?, ?, ?)', 
                               (dataGuru_id_guru, dataGuru_nuptk, dataGuru_nama_guru, dataGuru_jenis_kelamin, dataGuru_tanggal_lahir, dataGuru_alamat))
                conn.commit()  # Commit the transaction
                
                # Redirect to the tableA list with a success message
                flash('TableA added successfully!', 'success')
                return redirect(url_for('routesDataGuru.tableDataGuru'))
            except Exception as e:
                flash(f'Error: {str(e)}', 'danger')  # Flash error message
            finally:
                cursor.close()
                conn.close()
        
        flash('Failed to connect to the database', 'danger')  # Error if connection failed

    # Render the form for GET request
    return render_template('Create/createDataGuru.html')

