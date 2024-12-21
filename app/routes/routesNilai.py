from flask import Blueprint, render_template, redirect, url_for, request, flash
from connect import create_connection

# Create a blueprint for modular routing
routesNilai = Blueprint('routesNilai', __name__)

@routesNilai.route('/')
def index():
    return render_template('home.html')

@routesNilai.route('/tableNilai')
def tableNilai():
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
            SELECT * FROM nilai
            ORDER BY id_nilai  -- or any other column for sorting
            OFFSET ? ROWS
            FETCH NEXT ? ROWS ONLY
        ''', (offset, per_page))

        # cursor.execute('SELECT * FROM TableA')
        
        # Fetch the results
        table = cursor.fetchall()
        
        # Get the total count of rows to calculate the number of pages
        cursor.execute('SELECT COUNT(*) FROM nilai')
        total_count = cursor.fetchone()[0]
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        # Calculate total number of pages
        total_pages = (total_count + per_page - 1) // per_page
        
        # Pass the results, total pages, and current page to the template
        return render_template('tableNilai.html', table=table, total_pages=total_pages, current_page=page)
    else:
        return render_template('tableNilai.html', table=None)
    
#Create Data
@routesNilai.route('/Create/createNilai', methods=['GET', 'POST'])
def create_Nilai():
    # Handle the form submission when the method is POST
    if request.method == 'POST':
        # properti input digunakan disini
        Nilai_id_nilai       = request.form['id_nilai_Nilai']
        Nilai_id_mapel       = request.form['id_mapel_Nilai']
        Nilai_id_siswa       = request.form['id_siswa_Nilai']
        Nilai_nilai_akhir    = request.form['nilai_akhir_Nilai']
        

        # Get a connection to the database
        conn = create_connection()
        
        # Check if the connection was successful
        if conn:
            cursor = conn.cursor()
            try:
                # Insert the new tableA into the database
                cursor.execute('INSERT INTO Nilai (id_nilai, id_mapel, id_siswa, nilai_akhir) VALUES (?, ?, ?, ?)', 
                                (Nilai_id_nilai, Nilai_id_mapel, Nilai_id_siswa, Nilai_nilai_akhir))
                conn.commit()  # Commit the transaction
                
                # Redirect to the tableA list with a success message
                flash(f'{Nilai_id_nilai} added successfully!', 'success')
                return redirect(url_for('routesNilai.tableNilai'))
            except Exception as e:
                flash(f'Error: {str(e)}', 'danger')  # Flash error message
            finally:
                cursor.close()
                conn.close()
        
        flash('Failed to connect to the database', 'danger')  # Error if connection failed

    # Render the form for GET request
    return render_template('Create/createNilai.html')

#Update Data
@routesNilai.route('/tableNilai/update/<id_nilai>', methods=['GET', 'POST'])
def update_Nilai(id_nilai):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            if request.method == 'POST':
                # Get updated data from the form

                new_id_mapel = request.form['id_mapel_Nilai']
                new_id_siswa = request.form['id_siswa_Nilai']
                new_nilai_akhir  = request.form['nilai_akhir_Nilai']
                
                # Update the tableA in the database
                cursor.execute('''UPDATE Nilai
                               SET  id_mapel = ?, id_siswa = ?, nilai_akhir = ?
                               WHERE id_nilai = ?''', (new_id_mapel, new_id_siswa, new_nilai_akhir, id_nilai))
                conn.commit()

                flash(f'{id_nilai} updated successfully!', 'success')
                return redirect(url_for('routesNilai.tableNilai'))

            # For GET request, fetch current data to pre-fill the form
            cursor.execute('SELECT id_mapel, id_siswa, nilai_akhir FROM Nilai WHERE id_nilai = ?', (id_nilai,))
            table = cursor.fetchone()
            if not table:
                flash('Table not found!', 'danger')
                return redirect(url_for('routesNilai.tableNilai'))

            # Pass the current data to the form
            return render_template('/Update/updateNilai.html', Nilai={
                'id_mapel': table[0],
                'id_siswa': table[1],
                'nilai_akhir': table[2]
                })
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('routesNilai.tableNilai'))
        finally:
            cursor.close()
            conn.close()
    else:
        flash('Error: Unable to connect to the database.', 'danger')
        return redirect(url_for('routesNilai.continents'))

# Delete Data
@routesNilai.route('/tableNilai/delete/<id_nilai>', methods=['POST'])
def delete_continent(id_nilai):
    # Get a connection to the database
    conn = create_connection()
    
    # Check if the connection was successful
    if conn:
        cursor = conn.cursor()
        try:
            # Delete the tableA from the database
            cursor.execute('DELETE FROM Nilai WHERE id_nilai = ?', (id_nilai,))
            conn.commit()  # Commit the transaction
            
            # Redirect to the tableA list with a success message
            flash(f'{id_nilai} deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()  # Ensure the connection is closed
    else:
        flash('Error: Unable to connect to the database.', 'danger')
    
    return redirect(url_for('routesNilai.tableNilai'))