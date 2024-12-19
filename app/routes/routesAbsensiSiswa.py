from flask import Blueprint, render_template, redirect, url_for, request, flash
from connect import create_connection

# Create a blueprint for modular routing
routesAbsensiSiswa = Blueprint('routesAbsensiSiswa', __name__)

@routesAbsensiSiswa.route('/')
def index():
    return render_template('home.html')

@routesAbsensiSiswa.route('/tableAbsensiSiswa')
def tableAbsensiSiswa():
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
            SELECT * FROM absensisiswa
            ORDER BY id_absensisiswa  -- or any other column for sorting
            OFFSET ? ROWS
            FETCH NEXT ? ROWS ONLY
        ''', (offset, per_page))

        # cursor.execute('SELECT * FROM TableA')
        
        # Fetch the results
        table = cursor.fetchall()
        
        # Get the total count of rows to calculate the number of pages
        cursor.execute('SELECT COUNT(*) FROM absensisiswa')
        total_count = cursor.fetchone()[0]
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        # Calculate total number of pages
        total_pages = (total_count + per_page - 1) // per_page
        
        # Pass the results, total pages, and current page to the template
        return render_template('tableAbsensiSiswa.html', table=table, total_pages=total_pages, current_page=page)
    else:
        return render_template('tableAbsensiSiswa.html', table=None)

# Create Data
@routesAbsensiSiswa.route('/Create/createAbsSiswa', methods=['GET', 'POST'])
def create_AbsensiSiswa():
    # Handle the form submission when the method is POST
    if request.method == 'POST':
        # properti input digunakan disini
        absensiSiswa_id_absensisiswa = request.form['id_absensisiswa_AbsensiSiswa']
        absensiSiswa_id_siswa = request.form['id_siswa_AbsensiSiswa']
        absensiSiswa_tanggal = request.form['tanggal_AbsensiSiswa']
        absensiSiswa_status = request.form['status_AbsensiSiswa']

        # Get a connection to the database
        conn = create_connection()
        
        # Check if the connection was successful
        if conn:
            cursor = conn.cursor()
            try:
                # Insert the new tableA into the database
                cursor.execute('INSERT INTO AbsensiSiswa (id_absensisiswa, id_siswa, tanggal, status) VALUES (?, ?, ?, ?)', 
                               (absensiSiswa_id_absensisiswa, absensiSiswa_id_siswa, absensiSiswa_tanggal, absensiSiswa_status))
                conn.commit()  # Commit the transaction
                
                # Redirect to the tableA list with a success message
                flash(f'{absensiSiswa_id_absensisiswa} added successfully!', 'success')
                return redirect(url_for('routesAbsensiSiswa.tableAbsensiSiswa'))
            except Exception as e:
                flash(f'Error: {str(e)}', 'danger')  # Flash error message
            finally:
                cursor.close()
                conn.close()
        
        flash('Failed to connect to the database', 'danger')  # Error if connection failed

    # Render the form for GET request
    return render_template('Create/createAbsSiswa.html')

# Delete Data
@routesAbsensiSiswa.route('/tableAbsensiSiswa/delete/<id_absensisiswa>', methods=['POST'])
def delete_continent(id_absensisiswa):
    # Get a connection to the database
    conn = create_connection()
    
    # Check if the connection was successful
    if conn:
        cursor = conn.cursor()
        try:
            # Delete the tableA from the database
            cursor.execute('DELETE FROM AbsensiSiswa WHERE id_absensisiswa = ?', (id_absensisiswa,))
            conn.commit()  # Commit the transaction
            
            # Redirect to the tableA list with a success message
            flash(f'{id_absensisiswa} deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()  # Ensure the connection is closed
    else:
        flash('Error: Unable to connect to the database.', 'danger')
    
    return redirect(url_for('routesAbsensiSiswa.tableAbsensiSiswa'))

#Update Data
@routesAbsensiSiswa.route('/tableAbsensiSiswa/update/<id_absensisiswa>', methods=['GET', 'POST'])
def update_AbsensiSiswa(id_absensisiswa):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            if request.method == 'POST':
                # Get updated data from the form
                new_id_siswa = request.form['id_siswa_AbsensiSiswa']
                new_tanggal = request.form['tanggal_AbsensiSiswa']
                new_status = request.form['status_AbsensiSiswa']
                
                # Update the tableA in the database
                cursor.execute('''UPDATE AbsensiSiswa 
                               SET  id_siswa = ?, tanggal = ?, status = ?
                                WHERE id_absensisiswa = ?''', (new_id_siswa, new_tanggal, new_status, id_absensisiswa))
                conn.commit()

                flash(f'{id_absensisiswa} updated successfully!', 'success')
                return redirect(url_for('routesAbsensiSiswa.tableAbsensiSiswa'))

            # For GET request, fetch current data to pre-fill the form
            cursor.execute('SELECT id_siswa, tanggal, status FROM AbsensiSiswa WHERE id_absensisiswa = ?', (id_absensisiswa,))
            table = cursor.fetchone()
            if not table:
                flash('Table not found!', 'danger')
                return redirect(url_for('routesAbsensiSiswa.tableAbsensiSiswa'))

            # Pass the current data to the form
            return render_template('/Update/updateAbsSiswa.html', AbsensiSiswa={
                'id_siswa': table[0],
                'tanggal': table[1],
                'status': table[2]
                })
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('routesAbsensiSiswa.tableAbsensiSiswa'))
        finally:
            cursor.close()
            conn.close()
    else:
        flash('Error: Unable to connect to the database.', 'danger')
        return redirect(url_for('routesAbsensiSiswa.continents'))
