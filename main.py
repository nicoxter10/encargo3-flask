from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

registros_ej1 = []
registros_ej2 = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/menu')
def menu():
    return redirect(url_for('index'))


@app.route('/ejercicio1', methods=['GET', 'POST'])
@app.route('/ejercicio1/<int:indice>', methods=['GET'])
def ejercicio1(indice=None):
    if indice is not None:
        if indice < 0 or indice >= len(registros_ej1):
            abort(404)
        reg = registros_ej1[indice]
        return render_template('ejercicio1.html', promedio=reg['promedio'],
                               estado=reg['estado'], historial=registros_ej1)

    if request.method == 'POST':
        try:
            nota1 = float(request.form['nota1'])
            nota2 = float(request.form['nota2'])
            nota3 = float(request.form['nota3'])
            asistencia = float(request.form['asistencia'])
        except (KeyError, ValueError):
            abort(400)

        if not (10 <= nota1 <= 70 and 10 <= nota2 <= 70 and
                10 <= nota3 <= 70 and 0 <= asistencia <= 100):
            abort(400)

        promedio = (nota1 + nota2 + nota3) / 3
        if promedio >= 40 and asistencia >= 75:
            estado = 'Aprobado'
        else:
            estado = 'Reprobado'
        promedio = round(promedio, 1)

        registros_ej1.append({'notas': [nota1, nota2, nota3],
                              'asistencia': asistencia,
                              'promedio': promedio, 'estado': estado})
        return render_template('ejercicio1.html', promedio=promedio,
                               estado=estado, historial=registros_ej1)

    return render_template('ejercicio1.html', promedio=None,
                           estado=None, historial=registros_ej1)


@app.route('/ejercicio2', methods=['GET', 'POST'])
@app.route('/ejercicio2/<int:indice>', methods=['GET'])
def ejercicio2(indice=None):
    if indice is not None:
        if indice < 0 or indice >= len(registros_ej2):
            abort(404)
        reg = registros_ej2[indice]
        return render_template('ejercicio2.html', nombre_largo=reg['nombre'],
                               cantidad=reg['cantidad'], historial=registros_ej2)

    if request.method == 'POST':
        nombre1 = request.form.get('nombre1', '').strip()
        nombre2 = request.form.get('nombre2', '').strip()
        nombre3 = request.form.get('nombre3', '').strip()

        if not nombre1 or not nombre2 or not nombre3:
            abort(400)
        if len({nombre1.lower(), nombre2.lower(), nombre3.lower()}) != 3:
            abort(400)

        nombres = [nombre1, nombre2, nombre3]
        nombre_largo = max(nombres, key=len)
        cantidad = len(nombre_largo)

        registros_ej2.append({'nombres': nombres,
                              'nombre': nombre_largo, 'cantidad': cantidad})
        return render_template('ejercicio2.html', nombre_largo=nombre_largo,
                               cantidad=cantidad, historial=registros_ej2)

    return render_template('ejercicio2.html', nombre_largo=None,
                           cantidad=None, historial=registros_ej2)


@app.errorhandler(400)
def error_400(e):
    return render_template('error.html', codigo=400,
                           mensaje='Datos ingresados inválidos.'), 400


@app.errorhandler(404)
def error_404(e):
    return render_template('error.html', codigo=404,
                           mensaje='Página o registro no encontrado.'), 404


if __name__ == '__main__':
    app.run(debug=True)