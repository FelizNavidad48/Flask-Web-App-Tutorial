import time

import pdfkit
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, make_response, Response, \
    send_file, send_from_directory
from flask_login import login_required, current_user
from .models import Note, DienosAtaskaita, Darbuotojas
from . import db
import json

from pdfkit import from_file

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if current_user.role == "vadybininkas":
        darbuotojai = Darbuotojas.query.all()
        print(darbuotojai)
        return render_template("home.html", user=current_user,
                               darbuotojai=darbuotojai)
    if current_user.role == "darbuotojas":
        darbuotojo_id = Darbuotojas.query.filter_by(user_id=current_user.id).first().id
        ataskaitos = DienosAtaskaita.query.filter_by(darbuotojo_id=darbuotojo_id).all()
        ataskaitu_skaicius = len(ataskaitos)
        valandos = 0
        dezes = 0
        atlygis = 0
        for ataskaita in ataskaitos:
            if ataskaita.patvirtinta:
                valandos += ataskaita.atidirbtos_valandos
                dezes += ataskaita.perkeltos_dezes
                atlygis += ataskaita.atlygis

        return render_template("home.html", user=current_user, ataskaitos=ataskaitu_skaicius,
                               dezes=dezes, valandos=valandos, atlygis=atlygis)
    return render_template("home.html", user=current_user)


@views.route('/dienos_ataskaita', methods=['GET', 'POST'])
@login_required
def dienos_ataiskaita():
    if request.method == 'POST':
        data = request.form.get('data')
        perkeltos_dezes = request.form.get('deziu_kiekis')
        atidirbtos_valandos = request.form.get('darbo_valandos')
        if int(perkeltos_dezes) < 0:
            flash('Deziu kiekis negali buti maziau nei 0!', category='error')
        if int(atidirbtos_valandos) < 0:
            flash('Darbo valandu negali buti maziau nei 0!', category='error')
        else:
            new_dienos_ataiskata = DienosAtaskaita(data=data, perkeltos_dezes=perkeltos_dezes,
                                                   atidirbtos_valandos=atidirbtos_valandos,
                                                   darbuotojo_id=Darbuotojas.query
                                                   .filter_by(user_id=current_user.id).first().id)
            db.session.add(new_dienos_ataiskata)
            db.session.commit()
            flash('Dienos ataskaita prideta!', category='success')
            return redirect(url_for('views.home'))

    return render_template("dienos_ataskaita.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)  # this function expects a JSON from the INDEX.js file
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/patvirtinti', methods=['POST'])
def patvirtinti_ataskaita():
    atsiustiDuomenys = json.loads(request.data)  # this function expects a JSON from the INDEX.js file
    ataskaitosId = atsiustiDuomenys['ataskaitosId']
    ataskaita = DienosAtaskaita.query.get(ataskaitosId)
    if ataskaita:
        ataskaita.patvirtinta = True
        db.session.commit()

    return jsonify({})


@views.route('/redaguoti', methods=['POST'])
def redaguoti():
    atsiustiDuomenys = json.loads(request.data)  # this function expects a JSON from the INDEX.js file

    ataskaitosId = atsiustiDuomenys['ataskaitosId']
    darbuotojoId = atsiustiDuomenys['darbuotojoId']
    data = atsiustiDuomenys['data']
    dezes = atsiustiDuomenys['dezes']
    valandos = atsiustiDuomenys['valandos']
    atlygis = atsiustiDuomenys['atlygis']

    print("dezes:" + dezes)

    ataskaita = DienosAtaskaita.query.get(ataskaitosId)
    if ataskaita:
        ataskaita.data = data
        ataskaita.perkeltos_dezes = dezes
        ataskaita.atidirbtos_valandos = valandos
        ataskaita.atlygis = atlygis
        ataskaita.darbuotojo_id = darbuotojoId
        db.session.commit()

    return jsonify({})


@views.route('/parsisiusti-pdf', methods=['GET', 'POST'])
def parsisiusti_pdf():
    atsiustiDuomenys = json.loads(request.data)  # this function expects a JSON from the INDEX.js file
    ataskaitosId = atsiustiDuomenys['ataskaitosId']
    ataskaita = DienosAtaskaita.query.get(ataskaitosId)
    html_content = render_template('pdf_ataskaita.html', user=current_user, ataskaita=ataskaita)

    pdf = pdfkit.from_string(html_content, "download_folder/pdf_ataskaita_" + str(ataskaita.id) + ".pdf")
    return send_from_directory("download_folder", "pdf_ataskaita_" + str(ataskaita.id) + ".pdf", as_attachment=True)
