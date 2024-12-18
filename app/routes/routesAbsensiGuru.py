from flask import Blueprint, render_template, redirect, url_for, request, flash
from connect import create_connection

# Create a blueprint for modular routing
routesAbsensiGuru = Blueprint('routesAbsensiGuru', __name__)

@routesAbsensiGuru.route('/')
def index():
    return render_template('home.html')

# Show All Data
@routesAbsensiGuru.route('/tableAbsensiGuru')
def tableAbsensiGuru():
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
            SELECT * FROM absensiguru
            ORDER BY id_absensiguru  -- or any other column for sorting
            OFFSET ? ROWS
            FETCH NEXT ? ROWS ONLY
        ''', (offset, per_page))

        # cursor.execute('SELECT * FROM TableA')
        
        # Fetch the results
        table = cursor.fetchall()
        
        # Get the total count of rows to calculate the number of pages
        cursor.execute('SELECT COUNT(*) FROM absensiguru')
        total_count = cursor.fetchone()[0]
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        # Calculate total number of pages
        total_pages = (total_count + per_page - 1) // per_page
        
        # Pass the results, total pages, and current page to the template
        return render_template('tableAbsensiGuru.html', table=table, total_pages=total_pages, current_page=page)
    else:
        return render_template('tableAbsensiGuru.html', table=None)

# Create Data
@routesAbsensiGuru.route('/Create/createAbsGuru', methods=['GET', 'POST'])
def create_AbsensiGuru():
    # Handle the form submission when the method is POST
    if request.method == 'POST':
        # properti input digunakan disini
        absensiGuru_id_absensiguru = request.form['id_absensiguru_AbsensiGuru']
        absensiGuru_id_guru = request.form['id_guru_AbsensiGuru']
        absensiGuru_tanggal = request.form['tanggal_AbsensiGuru']
        absensiGuru_status = request.form['status_AbsensiGuru']
        
        # Get a connection to the database
        conn = create_connection()
        
        # Check if the connection was successful
        if conn:
            cursor = conn.cursor()
            try:
                # Insert the new tableA into the database
                cursor.execute('INSERT INTO AbsensiGuru (id_absensiguru, id_guru, tanggal, status) VALUES (?, ?, ?, ?)', 
                               (absensiGuru_id_absensiguru, absensiGuru_id_guru, absensiGuru_tanggal, absensiGuru_status))
                conn.commit()  # Commit the transaction
                
                # Redirect to the tableA list with a success message
                flash(f'{absensiGuru_id_absensiguru} added successfully!', 'success')
                return redirect(url_for('routesAbsensiGuru.tableAbsensiGuru'))
            except Exception as e:
                flash(f'Error: {str(e)}', 'danger')  # Flash error message
            finally:
                cursor.close()
                conn.close()
        
        flash('Failed to connect to the database', 'danger')  # Error if connection failed

    # Render the form for GET request
    return render_template('Create/createAbsGuru.html')

#Update Data
@routesAbsensiGuru.route('/tableAbsensiGuru/update/<id_absensiguru>', methods=['GET', 'POST'])
def update_AbsensiGuru(id_absensiguru):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            if request.method == 'POST':
                # Get updated data from the form
                new_id_guru = request.form['id_guru_AbsensiGuru']
                new_tanggal = request.form['tanggal_AbsensiGuru']
                new_status = request.form['status_AbsensiGuru']
                
                # Update the tableA in the database
                cursor.execute('''UPDATE AbsensiGuru 
                               SET  id_guru = ?, tanggal = ?, status = ?
                                WHERE id_absensiguru = ?''', (new_id_guru, new_tanggal, new_status, id_absensiguru))
                conn.commit()

                flash(f'{id_absensiguru} updated successfully!', 'success')
                return redirect(url_for('routesAbsensiGuru.tableAbsensiGuru'))

            # For GET request, fetch current data to pre-fill the form
            cursor.execute('SELECT id_guru, tanggal, status FROM AbsensiGuru WHERE id_absensiguru = ?', (id_absensiguru,))
            table = cursor.fetchone()
            if not table:
                flash('Table not found!', 'danger')
                return redirect(url_for('routesAbsensiGuru.tableAbsensiGuru'))

            # Pass the current data to the form
            return render_template('/Update/updateAbsGuru.html', AbsensiGuru={
                'id_guru': table[0],
                'tanggal': table[1],
                'status': table[2]
                })
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('routesAbsensiGuru.tableAbsensiGuru'))
        finally:
            cursor.close()
            conn.close()
    else:
        flash('Error: Unable to connect to the database.', 'danger')
        return redirect(url_for('routesAbsensiGuru.continents'))
    
    flash('Unexpected error occurred.', 'danger')
    return redirect(url_for('routesAbsensiGuru.AbsensiGuru'))

# Delete Data
@routesAbsensiGuru.route('/tableAbsensiGuru/delete/<id_absensiguru>', methods=['POST'])
def delete_continent(id_absensiguru):
    # Get a connection to the database
    conn = create_connection()
    
    # Check if the connection was successful
    if conn:
        cursor = conn.cursor()
        try:
            # Delete the tableA from the database
            cursor.execute('DELETE FROM AbsensiGuru WHERE id_absensiguru = ?', (id_absensiguru,))
            conn.commit()  # Commit the transaction
            
            # Redirect to the tableA list with a success message
            flash(f'{id_absensiguru} deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()  # Ensure the connection is closed
    else:
        flash('Error: Unable to connect to the database.', 'danger')
    
    return redirect(url_for('routesAbsensiGuru.tableAbsensiGuru'))