#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File      : entree_sortie_modify_delete.py
# Caller    : call_article_details.py
# author    : Ibrahim Addadi; dabve@gmail.com.
# ---------------------------------------------------------
# desc      : this file contain Entree, Sortie, Modify, Delete
# Thanks    :
# ---------------------------------------------------------

from PyQt5.QtWidgets import QDialog, QMessageBox, QMainWindow, QTableWidgetItem            # , QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
# from decimal import Decimal

from config_files import sqlite_functions

from headers.h_entree import Ui_Entree
from headers.h_sortie import Ui_Sortie
from headers.h_modify_article import Ui_ModifyArticle
from headers.h_total_des_article import Ui_TotalArticle
from headers.h_movement import Ui_MainWindowMovement
from headers.h_etats import Ui_Etats


def message_box_result(parent, msg_title, message, icon):
    msg = '<p style=font-family: "Monaco"; font-size: 14>{}</p>'.format(message)
    if icon == 'info':
        QMessageBox.information(parent, msg_title, msg, QMessageBox.Close)
    elif icon == 'warning':
        QMessageBox.warning(parent, msg_title, msg, QMessageBox.Close)
    elif icon == 'question':
        msg_box = QMessageBox.question(parent, msg_title, msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return msg_box


class ArticleEntree(QDialog):
    def __init__(self, art_id, user_id):
        super().__init__()
        self.ui = Ui_Entree()
        self.art_id = art_id
        self.user_id = user_id

        self.ui.setupUi(self)

        # Database handler
        db_name = './config_files/db.sqlite3'
        self.db_handler = sqlite_functions.SqliteFunc(db_name)

        # window configuration
        icon = QIcon()
        icon.addPixmap(QPixmap('./icons/box--plus.png'), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        # add the code to the lineEdit
        self.display_records()

        # handling pushButtons callback funstions
        self.ui.pushButtonAddEntree.clicked.connect(self.add_entree)

    def display_records(self):
        query = 'SELECT code, qte, prix, valeur FROM magasin_article WHERE art_id = ?'
        params = [self.art_id]
        desc, rows = self.db_handler.make_query(query, params)
        for row in rows:
            self.art_code, self.art_qte, self.art_prix, self.art_valeur = row
            self.ui.lineEditCode.setText(self.art_code)
            self.ui.spinBoxPrix.setValue(self.art_prix)

    def add_entree(self):
        ent_date = self.ui.dateEditDate.date().toPyDate()
        ent_qte = self.ui.spinBoxQte.value()
        ent_prix = self.ui.spinBoxPrix.value()

        new_qte = self.art_qte + ent_qte

        if ent_prix != self.art_prix:
            # Cout Moyene Penduré = Total des valeur / Total des quantité
            new_prix = ((ent_qte * ent_prix) + self.art_valeur) / (new_qte)
            query = 'UPDATE magasin_article SET qte = ?, prix = ? WHERE art_id = ?'
            params = [new_qte, new_prix, self.art_id]
        else:
            query = 'UPDATE magasin_article SET qte = ? WHERE art_id = ?'
            params = [new_qte, self.art_id]

        result = self.db_handler.make_query(query, params)
        msg_title = 'Nouvelle Entree'
        if type(result) == int:
            msg = 'Entree Ajouter Avec Success'
            message_box_result(self, msg_title, msg, 'info')

            # insert entree into movement table
            sqlite_functions.MovementTable(self.art_id, self.user_id).new_entree(ent_date, ent_qte, ent_prix)

            self.close()        # close window
        else:
            msg = 'Probleme'
            message_box_result(self, msg_title, msg, 'warning')


class ArticleSortie(QDialog):
    def __init__(self, art_id, user_id):
        super().__init__()
        self.ui = Ui_Sortie()
        self.ui.setupUi(self)
        self.art_id = art_id
        self.user_id = user_id

        # Database handler
        db_name = './config_files/db.sqlite3'
        self.db_handler = sqlite_functions.SqliteFunc(db_name)

        # window icon
        icon = QIcon()
        icon.addPixmap(QPixmap('./icons/box--minus.png'), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        # add the code to the lineEdit
        self.display_records()

        # handling pushButtons callback funstions
        self.ui.pushButtonAddSortie.clicked.connect(self.add_sortie)

    def display_records(self):
        query = 'SELECT code, qte, prix FROM magasin_article WHERE art_id = ?'
        params = [self.art_id]
        desc, rows = self.db_handler.make_query(query, params)
        for row in rows:
            self.art_code, self.art_qte, self.art_prix = row
            self.ui.lineEditCode.setText(self.art_code)
            self.ui.spinBoxPrix.setValue(self.art_prix)

    def add_sortie(self):
        ent_date = self.ui.dateEditSrtDate.date().toPyDate()
        ent_qte = self.ui.spinBoxQte.value()
        ent_prix = self.ui.spinBoxPrix.value()
        msg_title = 'Nouvelle Sortie'
        if ent_qte > self.art_qte:
            msg = 'Quantité insuffisant dans le stock'
            message_box_result(self, msg_title, msg, 'warning')
        else:
            new_qte = self.art_qte - ent_qte
            query = 'UPDATE magasin_article SET qte = ? WHERE art_id = ?'
            params = [new_qte, self.art_id]

            if self.db_handler.make_query(query, params):
                msg = 'Sortie Ajouter Avec Success'
                message_box_result(self, msg_title, msg, 'info')

                # FIXME: problem with binding paramter prix with Decimal type
                sqlite_functions.MovementTable(self.art_id, self.user_id).new_sortie(ent_date, ent_qte, ent_prix)
                self.close()
            else:
                msg = 'Error: Verifier vos données.'
                message_box_result(self, msg_title, msg, 'warning')


class ModifyArticle(QDialog):
    def __init__(self, art_id, user_id):
        super().__init__()
        self.ui = Ui_ModifyArticle()
        self.ui.setupUi(self)
        self.art_id = art_id
        self.user_id = user_id

        # Database handler
        db_name = './config_files/db.sqlite3'
        self.db_handler = sqlite_functions.SqliteFunc(db_name)

        # set window icon
        icon = QIcon()
        icon.addPixmap(QPixmap('./icons/clipboard--pencil.png'), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        # display value of article
        self.display_records()

        # handling pushButton callback funstion
        self.ui.pushButtonModify.clicked.connect(self.modify_article)

    def display_records(self):
        self.ui.labelTitle.setText('Modifier Article N° {}'.format(self.art_id))
        query = 'SELECT code, designation, ref, umesure, emp, observation FROM magasin_article WHERE art_id = ?'
        params = [self.art_id]
        desc, rows = self.db_handler.make_query(query, params)
        for row in rows:
            code, desig, ref, umesure, emp, obs = row
            self.ui.lineEditCode.setText(code)
            self.ui.lineEditDesig.setText(desig)
            self.ui.lineEditRef.setText(ref)
            self.ui.lineEditUM.setText(umesure)
            self.ui.lineEditEmp.setText(emp)
            self.ui.lineEditObs.setText(obs)

    def modify_article(self):
        query = 'SELECT code, designation, ref, umesure, emp, observation FROM magasin_article WHERE art_id = ?'
        _, rows = self.db_handler.make_query(query, [self.art_id])
        for row in rows:
            art_code, art_desig, art_ref, art_um, art_emp, art_obs = row

        ent_code = self.ui.lineEditCode.text()
        ent_desig = self.ui.lineEditDesig.text()
        ent_ref = self.ui.lineEditRef.text()
        ent_um = self.ui.lineEditUM.text()
        ent_emp = self.ui.lineEditEmp.text()
        ent_obs = self.ui.lineEditObs.text()

        # find defferences
        old_values = list()
        new_values = list()
        if art_code != ent_code:
            old_values.append(art_code)
            new_values.append(ent_code)
        if art_desig != ent_desig:
            old_values.append(art_desig)
            new_values.append(ent_desig)
        if art_ref != ent_ref:
            old_values.append(art_ref)
            new_values.append(ent_ref)
        if art_um != ent_um:
            old_values.append(art_um)
            new_values.append(ent_um)
        if art_emp != ent_emp:
            old_values.append(art_emp)
            new_values.append(ent_emp)
        if art_obs != ent_obs:
            old_values.append(art_obs)
            new_values.append(ent_obs)

        query = '''UPDATE magasin_article SET code = ?, designation = ?, ref = ?, umesure = ?, emp = ?, observation = ?
                   WHERE art_id = ?'''
        params = [ent_code, ent_desig, ent_ref, ent_um, ent_emp, ent_obs, self.art_id]
        result = self.db_handler.make_query(query, params)
        msg_title = "Modification D\'article"
        if type(result) == int:
            msg = 'Article Modifier Avec Succes'
            message_box_result(self, msg_title, msg, 'info')
            sqlite_functions.MagasinHistory(self.art_id, self.user_id).modify_article(';'.join(old_values), ';'.join(new_values))
            self.close()
        else:
            msg = 'Error: {}'.format(result)
            message_box_result(self, msg_title, msg, 'info')


class TotalArticles(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_TotalArticle()
        self.ui.setupUi(self)


class Movement(QMainWindow):
    def __init__(self, art_id=None):
        super().__init__()
        self.ui = Ui_MainWindowMovement()
        self.ui.setupUi(self)
        self.art_id = art_id

        # db_handler
        db_name = './config_files/db.sqlite3'
        self.db_handler = sqlite_functions.SqliteFunc(db_name)

        self.table_movement = self.ui.tableWidget
        # size of table column
        self.table_movement.setColumnWidth(0, 250)       # date
        self.table_movement.setColumnWidth(1, 100)      # user
        self.table_movement.setColumnWidth(2, 120)      # operation
        self.table_movement.setColumnWidth(3, 120)      # code Column
        self.table_movement.setColumnWidth(4, 270)       # desigantion Column
        self.table_movement.setColumnWidth(5, 150)       # qte Column

        if self.art_id:
            self.movement_by_article()
        else:
            self.display_all_records()

        self.ui.actionJournalier.triggered.connect(lambda: self.etats_('journalier'))
        self.ui.actionMensuel.triggered.connect(lambda: self.etats_('mensuel'))
        self.ui.actionTous.triggered.connect(lambda: self.etats_('tous'))

        self.ui.pushButtonSearchMov.clicked.connect(self.search_movement)
        self.ui.pushButtonMovRefresh.clicked.connect(self.display_all_records)

    def display_records(self, query, params):
        """
        usage: display_records(query, query_params)
        """
        # result is a tuple containing (desc, rows); else error
        result = self.db_handler.make_query(query, params)
        self.table_movement.clear()                       # clear table before inserting new row
        if result:
            self.table_movement.setRowCount(len(result[1]))    # required set row count for the tableWidget
            table_row = 0                                   # table_widget Row
            for article in result[1]:
                # article is a tuple that contain records
                for column, art in enumerate(article):
                    item = QTableWidgetItem(str(art))                   # required; item must be QTableWidgetItem
                    self.table_movement.setItem(table_row, column, item)  # add the item to the table_widget
                    if column == 5 or column == 6:
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)   # align (qte && prix) to the left
                table_row += 1

        # horizontal headers labels
        self.table_movement.setHorizontalHeaderLabels(['Date', 'User', 'Operation', 'Code', 'Designaton', 'Qte', 'Prix'])

    def display_all_records(self):
        query = '''SELECT DATE(mov.movement_date) AS mov_date, user.username, mov.movement, art.code, art.designation, mov.qte, mov.prix
                   FROM magasin_movement AS mov
                   INNER JOIN magasin_article AS art ON mov.art_id_id = art.art_id
                   INNER JOIN auth_user AS user ON user.id = mov.user_id_id
                   ORDER BY mov_date DESC'''
        params = []
        self.display_records(query, params)

    def search_movement(self):
        code = self.ui.lineEditSearchMov.text()
        operation = self.ui.comboBoxOperation.currentText().lower()
        date = self.ui.dateEditMov.date().toPyDate()
        if operation == 'tous':
            query = '''SELECT mov.movement_date, user.username, mov.movement, art.code, art.designation, mov.qte, mov.prix
                       FROM magasin_movement AS mov
                       INNER JOIN magasin_article AS art ON mov.art_id_id = art.art_id
                       INNER JOIN auth_user AS user ON user.id = mov.user_id_id
                       WHERE art.code LIKE ? AND mov.movement_date LIKE ?'''
            params = ['%' + code + '%', '%' + str(date) + '%']
        else:
            query = '''SELECT mov.movement_date, user.username, mov.movement, art.code, art.designation, mov.qte, mov.prix
                       FROM magasin_movement AS mov
                       INNER JOIN magasin_article AS art ON mov.art_id_id = art.art_id
                       INNER JOIN auth_user AS user ON user.id = mov.user_id_id
                       WHERE art.code LIKE ? AND mov.movement_date LIKE ? AND mov.movement LIKE ?'''
            params = ['%' + code + '%', '%' + str(date) + '%', '%' + operation + '%']

        self.display_records(query, params)

    def movement_by_article(self):
        query = '''SELECT DATE(mov.movement_date) AS mov_date, user.username, mov.movement, art.code, art.designation, mov.qte, mov.prix
                   FROM magasin_movement AS mov
                   INNER JOIN magasin_article AS art ON mov.art_id_id = art.art_id
                   INNER JOIN auth_user AS user ON user.id = mov.user_id_id
                   WHERE mov.art_id_id = ? ORDER BY mov_date DESC'''
        params = [self.art_id]
        self.display_records(query, params)

    def etats_(self, etats):
        w_etat = Etats(etats)
        w_etat.exec_()


class Etats(QDialog):
    def __init__(self, etats):
        super().__init__()
        self.ui = Ui_Etats()
        self.ui.setupUi(self)
        self.etats = etats

        # Database handler
        db_name = './config_files/db.sqlite3'
        self.db_handler = sqlite_functions.SqliteFunc(db_name)

        self.display_dates()
        self.ui.pushButtonSaveEtats.clicked.connect(self.save_etats)

    def display_dates(self):
        if self.etats == 'journalier':
            query = 'SELECT DISTINCT(strftime("%Y-%m-%d", movement_date)) FROM magasin_movement'
            params = ()
            _, rows = self.db_handler.make_query(query, params)
            for index, date in enumerate(rows):
                self.ui.comboBoxDate.insertItem(index, str(date[0]))
        elif self.etats == 'mensuel':
            query = 'SELECT DISTINCT(strftime("%Y-%m", movement_date)) FROM magasin_movement'
            params = ()
            _, rows = self.db_handler.make_query(query, params)
            for index, date in enumerate(rows):
                self.ui.comboBoxDate.insertItem(index, str(date[0]))
        else:
            self.ui.comboBoxDate.insertItem(0, 'Tous')

    def save_etats(self):
        if self.etats == 'tous':
            date_ = 'tousLesMovement'
            query = '''SELECT DATE(mov.movement_date) AS Date, art.code, art.designation, mov.movement, mov.qte, mov.prix,
                       mov.valeur
                       FROM magasin_movement AS mov
                       INNER JOIN magasin_article AS art ON mov.art_id_id = art.art_id'''
            params = ()
        else:
            date_ = self.ui.comboBoxDate.currentText()
            query = '''SELECT DATE(mov.movement_date) AS Date, art.code, art.designation, mov.movement, mov.qte, mov.prix,
                       mov.valeur
                       FROM magasin_movement AS mov
                       INNER JOIN magasin_article AS art ON mov.art_id_id = art.art_id
                       WHERE mov.movement_date LIKE ?'''
            params = ['%' + date_ + '%']

        desc, rows = self.db_handler.make_query(query, params)
        # FIXME in sqlite functions file
        fname = self.db_handler.write_to_excel(desc, rows, date_)
        msg_title = 'Etats'
        message = '{} Enregistrer avec success'.format(fname)
        message_box_result(self, msg_title, message, 'info')
        self.close()
