import time

import pdfkit
from os.path import join, dirname, realpath

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, make_response, Response, \
    send_file, send_from_directory
from flask_login import login_required, current_user
from .models import DienosAtaskaita, Darbuotojas, User, Ikainis
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
    elif current_user.role == "darbuotojas":
        ataskaitos = DienosAtaskaita.query.filter_by(darbuotojo_id=current_user.id).all()
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
    elif current_user.role == "administratorius":
        vartotojai = User.query.all()
        darbuotojai = Darbuotojas.query.all()
        ikainiai = Ikainis.query.all()
        return render_template("home.html", user=current_user, vartotojai=vartotojai,
                               darbuotojai=darbuotojai, ikainiai=ikainiai)
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
        if current_user.role != "darbuotojas":
            flash('Ataskaitas gali pildyti tik darbuotojas!', category='error')
        else:
            darbuotojas = Darbuotojas.query.get(current_user.id)
            new_dienos_ataiskata = DienosAtaskaita(data=data, perkeltos_dezes=perkeltos_dezes,
                                                   atidirbtos_valandos=atidirbtos_valandos,
                                                   darbuotojo_id=darbuotojas.id)
            db.session.add(new_dienos_ataiskata)
            naujausias_ataskaitos_ikainis = None
            darbuotojo_ikainiai = darbuotojas.ikainiai

            darbuotojo_ikainiai.sort(key=lambda x: x.data, reverse=False)
            print(darbuotojo_ikainiai)

            for ikainis in darbuotojo_ikainiai:
                if ikainis.data <= data:
                    naujausias_ataskaitos_ikainis = ikainis

            if naujausias_ataskaitos_ikainis:
                new_dienos_ataiskata.atlygis = (
                        float(new_dienos_ataiskata.atidirbtos_valandos) * naujausias_ataskaitos_ikainis.valandinis
                        + float(
                    new_dienos_ataiskata.perkeltos_dezes) * naujausias_ataskaitos_ikainis.atlygis_uz_deze)

            db.session.commit()
            flash('Dienos ataskaita prideta!', category='success')
            return redirect(url_for('views.home'))

    return render_template("dienos_ataskaita.html", user=current_user)


@views.route('/patvirtintiAtaskaita', methods=['POST'])
def patvirtinti_ataskaita():
    atsiustiDuomenys = json.loads(request.data)  # this function expects a JSON from the INDEX.js file
    ataskaitosId = atsiustiDuomenys['ataskaitosId']
    ataskaita = DienosAtaskaita.query.get(ataskaitosId)
    if ataskaita:
        ataskaita.patvirtinta = True
        db.session.commit()

    return jsonify({})


@views.route('/patvirtintiVartotoja', methods=['POST'])
def patvirtinti_vartotoja():
    atsiustiDuomenys = json.loads(request.data)  # this function expects a JSON from the INDEX.js file
    vartotojoId = atsiustiDuomenys['vartotojoId']
    vartotojas = User.query.get(vartotojoId)
    if vartotojas:
        vartotojas.patvirtinta = True
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


@views.route('/parsisiusti-pdf/<menuo>/<darbuotojoId>', methods=['GET', 'POST'])
def parsisiusti_pdf(menuo, darbuotojoId):
    path = join(dirname(realpath(__file__)), 'download_folder/pdf_ataskaita_' + str(menuo) + "_"
                + str(darbuotojoId) + '.pdf')
    if request.method == 'POST':
        if darbuotojoId is None:
            ataskaitos = DienosAtaskaita.query.all()
            darbuotojo_vardas = ""
        else:
            ataskaitos = DienosAtaskaita.query.filter_by(darbuotojo_id=darbuotojoId).all()
            darbuotojo_vardas = Darbuotojas.query.get(darbuotojoId).first_name

        atidirbtos_valandos = 0
        ismoketas_atlygis = 0
        deziu_kiekis = 0
        for ataskaita in ataskaitos:
            if ataskaita.patvirtinta and ataskaita.data[:-3] == str(menuo):
                atidirbtos_valandos += ataskaita.atidirbtos_valandos
                ismoketas_atlygis += ataskaita.atlygis
                deziu_kiekis += ataskaita.perkeltos_dezes

        html_content = render_template('pdf_ataskaita.html', user=current_user, menuo=menuo,
                                       atidirbtos_valandos=atidirbtos_valandos, ismoketas_atlygis=ismoketas_atlygis,
                                       deziu_kiekis=deziu_kiekis, ataskaitos=ataskaitos,
                                       darbuotojo_vardas=darbuotojo_vardas)

        pdfkit.from_string(html_content, path)
        return jsonify({})
    else:
        return send_file(path, as_attachment=True)


@views.route('/ikainis', methods=['GET', 'POST'])
@login_required
def ikainis():
    if request.method == 'POST':
        data = request.form.get('data')
        atlygis_uz_deze = request.form.get('atlygis_uz_deze')
        valandinis = request.form.get('valandinis')
        new_ikainis = Ikainis(data=data, valandinis=valandinis, atlygis_uz_deze=atlygis_uz_deze)
        db.session.add(new_ikainis)
        db.session.commit()

        darbuotojai = request.form.getlist('pasirinkti_darbuotojus')
        for darbuotojo_id in darbuotojai:
            darbuotojas = Darbuotojas.query.get(darbuotojo_id)
            darbuotojas.ikainiai.append(new_ikainis)
            atnaujinti_atlygi(darbuotojas)

        flash('Ikainis pridetas!', category='success')
        return redirect(url_for('views.home'))

    darbuotojai = Darbuotojas.query.all()

    if current_user.role == "administratorius":
        return render_template("ikainis.html", user=current_user, darbuotojai=darbuotojai)
    else:
        flash('Neturite teisiu perziureti si puslapi!', category='error')
        return redirect(url_for('views.home'))


def atnaujinti_atlygi(darbuotojas):
    for ataskaita in darbuotojas.ataskaitos:
        if not ataskaita.patvirtinta:
            # Suranda naujausia ikaini
            naujausias_ataskaitos_ikainis = None
            for ikainis in darbuotojas.ikainiai:
                if ikainis.data <= ataskaita.data:
                    naujausias_ataskaitos_ikainis = ikainis

            if naujausias_ataskaitos_ikainis:
                ataskaita.atlygis = (ataskaita.atidirbtos_valandos * naujausias_ataskaitos_ikainis.valandinis
                                     + ataskaita.perkeltos_dezes * naujausias_ataskaitos_ikainis.atlygis_uz_deze)
    db.session.commit()
