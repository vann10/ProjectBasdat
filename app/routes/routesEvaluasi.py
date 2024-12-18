from flask import Blueprint, render_template, redirect, url_for, request, flash
from connect import create_connection

# Create a blueprint for modular routing
routesEvaluasi = Blueprint('routesEvaluasi', __name__)

@routesEvaluasi.route('/')
def index():
    return render_template('home.html')

@routesEvaluasi.route('/tableEvaluasi')
def tableEvaluasi():
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
            SELECT * FROM evaluasi
            ORDER BY id_evaluasi  -- or any other column for sorting
            OFFSET ? ROWS
            FETCH NEXT ? ROWS ONLY
        ''', (offset, per_page))

        # cursor.execute('SELECT * FROM TableA')
        
        # Fetch the results
        table = cursor.fetchall()
        
        # Get the total count of rows to calculate the number of pages
        cursor.execute('SELECT COUNT(*) FROM evaluasi')
        total_count = cursor.fetchone()[0]
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        # Calculate total number of pages
        total_pages = (total_count + per_page - 1) // per_page
        
        # Pass the results, total pages, and current page to the template
        return render_template('tableEvaluasi.html', table=table, total_pages=total_pages, current_page=page)
    else:
        return render_template('tableEvaluasi.html', table=None)

# Create Data
@routesEvaluasi.route('/Create/createEvaluasi', methods=['GET', 'POST'])
def create_Evaluasi():
    # Handle the form submission when the method is POST
    if request.method == 'POST':
        # properti input digunakan disini
        evaluasi_id_evaluasi = request.form['id_evaluasi_Evaluasi']
        evaluasi_id_siswa = request.form['id_siswa_Evaluasi']
        evaluasi_status = request.form['status_Evaluasi']
        evaluasi_rerata_kehadiran = request.form['rerata_kehadiran_Evaluasi']
        evaluasi_rerata_nilai = request.form['rerata_nilai_Evaluasi']

        # Get a connection to the database
        conn = create_connection()
        
        # Check if the connection was successful
        if conn:
            cursor = conn.cursor()
            try:
                # Insert the new tableA into the database
                cursor.execute('INSERT INTO Evaluasi (id_evaluasi, id_siswa, status, rerata_kehadiran, rerata_nilai) VALUES (?, ?, ?, ?, ?)', 
                               (evaluasi_id_evaluasi,evaluasi_id_siswa, evaluasi_status, evaluasi_rerata_kehadiran, evaluasi_rerata_nilai))
                conn.commit()  # Commit the transaction
                
                # Redirect to the tableA list with a success message
                flash('TableA added successfully!', 'success')
                return redirect(url_for('routesEvaluasi.tableEvaluasi'))
            except Exception as e:
                flash(f'Error: {str(e)}', 'danger')  # Flash error message
            finally:
                cursor.close()
                conn.close()
        
        flash('Failed to connect to the database', 'danger')  # Error if connection failed

    # Render the form for GET request
    return render_template('Create/createEvaluasi.html')

# Delete Data
@routesEvaluasi.route('/tableEvaluasi/delete/<id_evaluasi>', methods=['POST'])
def delete_continent(id_evaluasi):
    # Get a connection to the database
    conn = create_connection()
    
    # Check if the connection was successful
    if conn:
        cursor = conn.cursor()
        try:
            # Delete the tableA from the database
            cursor.execute('DELETE FROM Evaluasi WHERE id_evaluasi = ?', (id_evaluasi,))
            conn.commit()  # Commit the transaction
            
            # Redirect to the tableA list with a success message
            flash(f'{id_evaluasi} deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()  # Ensure the connection is closed
    else:
        flash('Error: Unable to connect to the database.', 'danger')
    
    return redirect(url_for('routesEvaluasi.tableEvaluasi'))