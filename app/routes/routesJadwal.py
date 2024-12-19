from flask import Blueprint, render_template, redirect, url_for, request, flash
from connect import create_connection

# Create a blueprint for modular routing
routesJadwal = Blueprint('routesJadwal', __name__)

@routesJadwal.route('/')
def index():
    return render_template('home.html')

@routesJadwal.route('/tableJadwal')
def tableJadwal():
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
            SELECT 
                id_jadwal,
                id_kelas,
                id_mapel,
                id_guru, 
                hari,                       
                CONVERT(VARCHAR(5), jam_mulai, 108) AS jam_mulai,
                CONVERT(VARCHAR(5), jam_selesai, 108) AS jam_selesai
            FROM 
                jadwal
            WHERE 
                jam_mulai IS NOT NULL
            ORDER BY 
                id_jadwal
            OFFSET ? ROWS
            FETCH NEXT ? ROWS ONLY
        ''', (offset, per_page))
        
        # Fetch the results
        table = cursor.fetchall()
        
        # Get the total count of rows to calculate the number of pages
        cursor.execute('SELECT COUNT(*) FROM jadwal')
        total_count = cursor.fetchone()[0]
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        # Calculate total number of pages
        total_pages = (total_count + per_page - 1) // per_page
        
        # Pass the results, total pages, and current page to the template
        return render_template('tableJadwal.html', table=table, total_pages=total_pages, current_page=page)
    else:
        return render_template('tableJadwal.html', table=None)

# Create Data
@routesJadwal.route('/Create/createJadwal', methods=['GET', 'POST'])
def create_Jadwal():
    # Handle the form submission when the method is POST
    if request.method == 'POST':
        # properti input digunakan disini
        jadwal_id_jadwal  = request.form['id_jadwal_Jadwal']
        jadwal_id_kelas  = request.form['id_kelas_Jadwal']
        jadwal_id_mapel  = request.form['id_mapel_Jadwal']
        jadwal_id_guru  = request.form['id_guru_Jadwal']
        jadwal_hari  = request.form['hari_Jadwal']
        jadwal_jam_mulai  = request.form['jam_mulai_Jadwal']
        jadwal_jam_selesai  = request.form['jam_selesai_Jadwal']

        # Get a connection to the database
        conn = create_connection()
        
        # Check if the connection was successful
        if conn:
            cursor = conn.cursor()
            try:
                # Insert the new tableA into the database
                cursor.execute('INSERT INTO Jadwal (id_jadwal, id_kelas, id_mapel,  id_guru, hari, jam_mulai, jam_selesai) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                                (jadwal_id_jadwal, jadwal_id_kelas, jadwal_id_mapel, jadwal_id_guru, jadwal_hari, jadwal_jam_mulai, jadwal_jam_selesai))
                conn.commit()  # Commit the transaction
                
                # Redirect to the tableA list with a success message
                flash('Table Kelas added successfully!', 'success')
                return redirect(url_for('routesJadwal.tableJadwal'))
            except Exception as e:
                flash(f'Error: {str(e)}', 'danger')  # Flash error message
            finally:
                cursor.close()
                conn.close()
        
        flash('Failed to connect to the database', 'danger')  # Error if connection failed

    # Render the form for GET request
    return render_template('Create/createJadwal.html')

# Delete Data
@routesJadwal.route('/tableJadwal/delete/<id_jadwal>', methods=['POST'])
def delete_continent(id_jadwal):
    # Get a connection to the database
    conn = create_connection()
    
    # Check if the connection was successful
    if conn:
        cursor = conn.cursor()
        try:
            # Delete the tableA from the database
            cursor.execute('DELETE FROM Jadwal WHERE id_jadwal = ?', (id_jadwal,))
            conn.commit()  # Commit the transaction
            
            # Redirect to the tableA list with a success message
            flash(f'{id_jadwal} deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()  # Ensure the connection is closed
    else:
        flash('Error: Unable to connect to the database.', 'danger')
    
    return redirect(url_for('routesJadwal.tableJadwal'))