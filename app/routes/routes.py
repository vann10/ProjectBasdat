from flask import Blueprint, render_template, redirect, url_for, request, flash
from connect import create_connection

# Create a blueprint for modular routing
routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template('home.html')

@routes.route('/tableA/create', methods=['GET', 'POST'])
def create_tableA():
    # Handle the form submission when the method is POST
    if request.method == 'POST':
        # properti input digunakan disini
        tableA_name = request.form['nameTableA']
        
        # Get a connection to the database
        conn = create_connection()
        
        # Check if the connection was successful
        if conn:
            cursor = conn.cursor()
            try:
                # Insert the new tableA into the database
                cursor.execute('INSERT INTO TableA (Name) VALUES (?)', (tableA_name))
                conn.commit()  # Commit the transaction
                
                # Redirect to the tableA list with a success message
                flash('TableA added successfully!', 'success')
                return redirect(url_for('routes.tableA'))
            except Exception as e:
                flash(f'Error: {str(e)}', 'danger')  # Flash error message
            finally:
                cursor.close()
                conn.close()
        
        flash('Failed to connect to the database', 'danger')  # Error if connection failed

    # Render the form for GET request
    return render_template('createTableA.html')


@routes.route('/tableA/update/<id>', methods=['GET', 'POST'])
def update_tableA(id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            if request.method == 'POST':
                # Get updated data from the form
                new_name = request.form['nameTableA']

                # Update the tableA in the database
                cursor.execute('UPDATE tableA SET name = ? WHERE id = ?', (new_name, id))
                conn.commit()

                flash('Table A updated successfully!', 'success')
                return redirect(url_for('routes.tableA'))

            # For GET request, fetch current data to pre-fill the form
            cursor.execute('SELECT name FROM tableA WHERE id = ?', (id))
            table = cursor.fetchone()
            if not table:
                flash('Table not found!', 'danger')
                return redirect(url_for('routes.tableA'))

            # Pass the current data to the form
            return render_template('editTableA.html', table={'name': table[0]})
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
    else:
        flash('Error: Unable to connect to the database.', 'danger')
        return redirect(url_for('routes.continents'))

@routes.route('/tableA/delete/<id>', methods=['POST'])
def delete_continent(id):
    # Get a connection to the database
    conn = create_connection()
    
    # Check if the connection was successful
    if conn:
        cursor = conn.cursor()
        try:
            # Delete the tableA from the database
            cursor.execute('DELETE FROM TableA WHERE id = ?', (id))
            conn.commit()  # Commit the transaction
            
            # Redirect to the tableA list with a success message
            flash('Table A deleted successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()  # Ensure the connection is closed
    else:
        flash('Error: Unable to connect to the database.', 'danger')
    
    return redirect(url_for('routes.tableA'))