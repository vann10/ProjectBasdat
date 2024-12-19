from flask import Blueprint, render_template, redirect, url_for, request, flash
from connect import create_connection

# Create a blueprint for modular routing
routesDataSiswa = Blueprint('routesDataSiswa', __name__)

@routesDataSiswa.route('/')
def index():
    return render_template('home.html')

#Show ALL 
@routesDataSiswa.route('/tableDataSiswa')
def tableDataSiswa():
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
            SELECT id_siswa, nisn, nama_siswa, 
                CASE 
                    WHEN jenis_kelamin = 'L' THEN 'Laki-laki' 
                    WHEN jenis_kelamin = 'P' THEN 'Perempuan'
                    ELSE 'Tidak Diketahui' 
                END AS jenis_kelamin,
                tanggal_lahir, alamat, id_kelas
            FROM datasiswa
            ORDER BY id_siswa  -- or any other column for sorting
            OFFSET ? ROWS
            FETCH NEXT ? ROWS ONLY
        ''', (offset, per_page))

        # cursor.execute('SELECT * FROM TableA')
        
        # Fetch the results
        table = cursor.fetchall()
        
        # Get the total count of rows to calculate the number of pages
        cursor.execute('SELECT COUNT(*) FROM datasiswa')
        total_count = cursor.fetchone()[0]
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        # Calculate total number of pages
        total_pages = (total_count + per_page - 1) // per_page
        
        # Pass the results, total pages, and current page to the template
        return render_template('tableDataSiswa.html', table=table, total_pages=total_pages, current_page=page)
    else:
        return render_template('tableDataSiswa.html', table=None)

# Create Data
@routesDataSiswa.route('/Create/createDataSiswa', methods=['GET', 'POST'])
def create_DataSiswa():
    # Handle the form submission when the method is POST
    if request.method == 'POST':
        # properti input digunakan disini
        dataSiswa_id_siswa = request.form['id_siswa_DataSiswa']
        dataSiswa_nisn = request.form['nisn_DataSiswa']
        dataSiswa_nama_siswa = request.form['nama_siswa_DataSiswa']
        dataSiswa_jenis_kelamin = request.form['jenis_kelamin_DataSiswa']
        dataSiswa_tanggal_lahir = request.form['tanggal_lahir_DataSiswa']
        dataSiswa_alamat = request.form['alamat_DataSiswa']
        dataSiswa_id_kelas = request.form['id_kelas_DataSiswa']
        
        # Get a connection to the database
        conn = create_connection()
        
        # Check if the connection was successful
        if conn:
            cursor = conn.cursor()
            try:
                # Insert the new tableA into the database
                cursor.execute('INSERT INTO DataSiswa (id_siswa, nisn, nama_siswa, jenis_kelamin, tanggal_lahir, alamat, id_kelas) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                               (dataSiswa_id_siswa, dataSiswa_nisn, dataSiswa_nama_siswa, dataSiswa_jenis_kelamin, dataSiswa_tanggal_lahir, dataSiswa_alamat, dataSiswa_id_kelas))
                conn.commit()  # Commit the transaction
                
                # Redirect to the tableA list with a success message
                flash('TableA added successfully!', 'success')
                return redirect(url_for('routesDataSiswa.tableDataSiswa'))
            except Exception as e:
                flash(f'Error: {str(e)}', 'danger')  # Flash error message
            finally:
                cursor.close()
                conn.close()
        
        flash('Failed to connect to the database', 'danger')  # Error if connection failed

    # Render the form for GET request
    return render_template('Create/createDataSiswa.html')

# Delete Data
@routesDataSiswa.route('/tableDataSiswa/delete/<id_siswa>', methods=['POST'])
def delete_continent(id_siswa):
    # Get a connection to the database
    conn = create_connection()
    
    # Check if the connection was successful
    if conn:
        cursor = conn.cursor()
        try:
            # Delete the tableA from the database
            cursor.execute('DELETE FROM DataSiswa WHERE id_siswa = ?', (id_siswa,))
            conn.commit()  # Commit the transaction
            
            # Redirect to the tableA list with a success message
            flash(f'{id_siswa} deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()  # Ensure the connection is closed
    else:
        flash('Error: Unable to connect to the database.', 'danger')
    
    return redirect(url_for('routesDataSiswa.tableDataSiswa'))

#Update Data
@routesDataSiswa.route('/tableDataSiswa/update/<id_siswa>', methods=['GET', 'POST'])
def update_DataSiswa(id_siswa):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            if request.method == 'POST':
                # Get updated data from the form

                new_nisn = request.form['nisn_DataSiswa']
                new_nama_siswa = request.form['nama_siswa_DataSiswa']
                new_jenis_kelamin = request.form['jenis_kelamin_DataSiswa']
                new_tanggal_lahir = request.form['tanggal_lahir_DataSiswa']
                new_alamat = request.form['alamat_DataSiswa']
                new_id_kelas = request.form['id_kelas_DataSiswa']
                
                # Update the tableA in the database
                cursor.execute('''UPDATE DataSiswa 
                               SET  nisn = ?, nama_siswa = ?, jenis_kelamin = ?, tanggal_lahir = ?, alamat = ?, id_kelas = ?
                                WHERE id_siswa = ?''', (new_nisn, new_nama_siswa, new_jenis_kelamin, new_tanggal_lahir, new_alamat, new_id_kelas, id_siswa))
                conn.commit()

                flash(f'{id_siswa} updated successfully!', 'success')
                return redirect(url_for('routesDataSiswa.tableDataSiswa'))

            # For GET request, fetch current data to pre-fill the form
            cursor.execute('SELECT nisn, nama_siswa, jenis_kelamin, tanggal_lahir, alamat, id_kelas FROM DataSiswa WHERE id_siswa = ?', (id_siswa,))
            table = cursor.fetchone()
            if not table:
                flash('Table not found!', 'danger')
                return redirect(url_for('routesDataSiswa.tableDataSiswa'))

            # Pass the current data to the form
            return render_template('/Update/updateDataSiswa.html', DataSiswa={
                'nisn': table[0],
                'nama_siswa': table[1],
                'jenis_kelamin': table[2],
                'tanggal_lahir': table[3],
                'alamat': table[4],
                'id_kelas': table[5]
                })
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('routesDataSiswa.tableDataSiswa'))
        finally:
            cursor.close()
            conn.close()
    else:
        flash('Error: Unable to connect to the database.', 'danger')
        return redirect(url_for('routesDataSiswa.continents'))
