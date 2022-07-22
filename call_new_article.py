#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file          : call_new_article.py
# caller        : magasin_qt.py
# author        : Ibrahim Addadi, dabve@gmail.com
# -----------------------------------------------------

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon, QPixmap
# from decimal import Decimal

from headers.h_new_article import Ui_newArticle

from config_files import sqlite_functions
from entree_sortie_modify_delete import message_box_result


class NewArticle(QDialog):
    def __init__(self, user_id):
        super().__init__()
        self.ui = Ui_newArticle()
        self.user_id = user_id
        self.ui.setupUi(self)

        # Database handler
        db_name = './config_files/db.sqlite3'
        self.db_handler = sqlite_functions.SqliteFunc(db_name)

        # window icon
        icon = QIcon()
        icon.addPixmap(QPixmap('./icons/baggage-cart-box-label.png'), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        # combobox add category
        self.display_category()

        # Filter lineEdit input
        # TODO: Use the QValidator to validate CODE, DESIG, REF
        self.ui.lineEditCode.editingFinished.connect(self.validate_code)
        # self.ui.lineEditDesig.editingFinished.connect(self.filter_desig)

        # pushButtons callback functions
        self.ui.pushButtonAdd.setEnabled(False)
        self.ui.pushButtonAdd.clicked.connect(self.add_article)

    def display_category(self):
        query = 'SELECT cat_id, name FROM magasin_category ORDER BY cat_id'
        desc, categories = self.db_handler.make_query(query)
        self.category_list = [cat[1] for cat in categories]
        for category in categories:
            cat_id, cat = category
            self.ui.comboBoxCategory.insertItem(cat_id, str(cat))

    def validate_code(self):
        code = self.ui.lineEditCode.text().upper()
        index = code.find('-')
        codeStr = code[:index]
        if codeStr not in self.category_list:
            self.ui.labelError.setText('No Category for This Code.')
            self.ui.pushButtonAdd.setEnabled(False)
        elif self.db_handler.product_exists('art_id', 'magasin_article', 'code', code):
            # check if code exists
            self.ui.labelError.setText('Article With This Code Exist')
            self.ui.pushButtonAdd.setEnabled(False)
        else:
            self.ui.labelError.setText('')
            self.ui.pushButtonAdd.setEnabled(True)

    # def filter_desig(self):
        # if len(self.ui.lineEditDesig.text()) < 5:
            # self.ui.labelError.setText('Designation Must Be Greater Than 5 Chars')
        # else:
            # self.ui.labelError.setText('')

    def add_article(self):
        cat_id = self.ui.comboBoxCategory.currentIndex() + 1
        code = self.ui.lineEditCode.text().upper()
        slug = code.lower()

        desig = self.ui.lineEditDesig.text().title()
        ref = self.ui.lineEditRef.text().upper()
        um = self.ui.lineEditUM.text()
        emp = self.ui.lineEditEmp.text().upper()
        obs = self.ui.lineEditObs.text()
        if len(emp) < 1:
            emp = '...'

        qte = self.ui.spinBoxQte.value()
        prix = self.ui.doubleSpinBoxPrix.value()
        valeur = qte * prix

        fields = ['category_id', 'code', 'slug', 'designation', 'ref', 'umesure', 'emp', 'qte', 'prix', 'valeur', 'observation']
        query = 'INSERT INTO magasin_article({}) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'.format(', '.join(fields))
        params = [cat_id, code, slug, desig, ref, um, emp, qte, prix, valeur, obs]
        result = self.db_handler.make_query(query, params)

        msg_title = 'Nouveaux Article'
        if type(result) == int:
            msg = 'Article Ajouter avec Successe'
            message_box_result(self, msg_title, msg, 'info')
            art_id = self.db_handler.get_article_id(code)
            # insert new article in history log
            sqlite_functions.MagasinHistory(art_id, self.user_id).new_article()
            self.close()
        else:
            message_box_result(self, msg_title, result, 'warning')
