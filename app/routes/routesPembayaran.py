from flask import Blueprint, render_template, redirect, url_for, request, flash
from connect import create_connection

# Create a blueprint for modular routing
routesPembayaran = Blueprint('routesPembayaran', __name__)

@routesPembayaran.route('/')
def index():
    return render_template('home.html')

@routesPembayaran.route('/tablePembayaran')
def tablePembayaran():
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
            SELECT * FROM pembayaran
            ORDER BY id_pembayaran  -- or any other column for sorting
            OFFSET ? ROWS
            FETCH NEXT ? ROWS ONLY
        ''', (offset, per_page))

        # cursor.execute('SELECT * FROM TableA')
        
        # Fetch the results
        table = cursor.fetchall()
        
        # Get the total count of rows to calculate the number of pages
        cursor.execute('SELECT COUNT(*) FROM pembayaran')
        total_count = cursor.fetchone()[0]
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        
        # Calculate total number of pages
        total_pages = (total_count + per_page - 1) // per_page
        
        # Pass the results, total pages, and current page to the template
        return render_template('tablePembayaran.html', table=table, total_pages=total_pages, current_page=page)
    else:
        return render_template('tablePembayaran.html', table=None)
    
@routesPembayaran.route('/Create/createPembayaran', methods=['GET', 'POST'])
def create_Pembayaran():
    # Handle the form submission when the method is POST
    if request.method == 'POST':
        # properti input digunakan disini
        pembayaran_id_pembayaran        = request.form['id_pembayaran_Pembayaran']
        pembayaran_id_siswa             = request.form['id_siswa_Pembayaran']
        pembayaran_total_tagihan        = request.form['total_tagihan_Pembayaran']
        pembayaran_status               = request.form['status_Pembayaran']
        pembayaran_tanggal_transaksi    = request.form['tanggal_transaksi_Pembayaran']
        if not pembayaran_tanggal_transaksi:  # Jika kosong, set None
            pembayaran_tanggal_transaksi = None

        # Get a connection to the database
        conn = create_connection()
        
        # Check if the connection was successful
        if conn:
            cursor = conn.cursor()
            try:
                # Insert the new tableA into the database
                cursor.execute('INSERT INTO Pembayaran (id_pembayaran, id_siswa, total_tagihan, status, tanggal_transaksi) VALUES (?, ?, ?, ?, ?)', 
                                (pembayaran_id_pembayaran, pembayaran_id_siswa, pembayaran_total_tagihan, pembayaran_status, pembayaran_tanggal_transaksi))
                conn.commit()  # Commit the transaction
                
                # Redirect to the tableA list with a success message
                flash('Table Pembayaran added successfully!', 'success')
                return redirect(url_for('routesPembayaran.tablePembayaran'))
            except Exception as e:
                flash(f'Error: {str(e)}', 'danger')  # Flash error message
            finally:
                cursor.close()
                conn.close()
        
        flash('Failed to connect to the database', 'danger')  # Error if connection failed

    # Render the form for GET request
    return render_template('Create/createPembayaran.html')

# Delete Data
@routesPembayaran.route('/tablePembayaran/delete/<id_pembayaran>', methods=['POST'])
def delete_continent(id_pembayaran):
    # Get a connection to the database
    conn = create_connection()
    
    # Check if the connection was successful
    if conn:
        cursor = conn.cursor()
        try:
            # Delete the tableA from the database
            cursor.execute('DELETE FROM Pembayaran WHERE id_pembayaran = ?', (id_pembayaran,))
            conn.commit()  # Commit the transaction
            
            # Redirect to the tableA list with a success message
            flash(f'{id_pembayaran} deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()  # Ensure the connection is closed
    else:
        flash('Error: Unable to connect to the database.', 'danger')
    
    return redirect(url_for('routesPembayaran.tablePembayaran'))