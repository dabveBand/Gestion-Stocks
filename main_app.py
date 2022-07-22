#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File      : magasin_qt.py
# Author    : Ibrahim Addadi, bdabve@gmail.com
# Created   : 07-October-2020
# Version   : 0.1.0
# Req      : PyQT5, Colorama
# Desc     : Gestion des stock
# --------------------------------------------------------

import sys
import os
from datetime import date
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5 import QtCore

from config_files import settings
from config_files.sqlite_functions import SqliteFunc

from headers.h_logIn import Ui_LogIn
from headers.h_main_window import Ui_MainWindow

from call_new_article import NewArticle
from call_article_details import ArticleDetails
from entree_sortie_modify_delete import TotalArticles, Movement


APP_DIR = os.getcwd()


class LogIn(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LogIn()
        self.ui.setupUi(self)

        # database handler
        db_name = APP_DIR + '/config_files/db.sqlite3'
        self.db_handler = SqliteFunc(db_name)

        self.ui.pushButtonLogin.clicked.connect(self.log_in)

    def log_in(self):
        """
        id           => 1
        password     => pbkdf2_sha256$100000$8R7d74p6q2oT$BLcPYA+HCmatLsSMeyfWYtgGDr0Ni7UfDHWaALKHkvM=
        last_login   => 2020-10-22 17:07:38.707788
        is_superuser => 1
        username     => admin
        first_name   => Ibrahim
        email        => dabve@gmail.com
        is_staff     => 1
        is_active    => 1
        date_joined  => 2020-08-28 13:21:24
        last_name    => Addadi
        """
        # database handler
        db_name = APP_DIR + '/config_files/db.sqlite3'
        self.db_handler = SqliteFunc(db_name)

        log_username = self.ui.lineEditUserName.text()
        log_pwd = self.ui.lineEditPwd.text()

        query = 'SELECT id, username, password FROM auth_user WHERE username = ?'
        params = [log_username]
        desc, rows = self.db_handler.make_query(query, params)
        if len(rows) == 0:
            self.ui.labelErrorMsg.setText('Wrong Username')
        else:
            user_id, username, pwd = rows[0]
            if pwd != log_pwd:
                self.ui.labelErrorMsg.setText('Wrong Password')
                main_app = MainApp(user_id)
                main_app.showMaximized()
                self.close()
            else:
                main_app = MainApp(user_id)
                main_app.showMaximized()
                self.close()


class MainApp(QMainWindow):
    def __init__(self, user_id, superuser=False):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.user_id = user_id          # handle movement and history by user_id
        # TODO: create a menu for log_in and log_out
        self.ui.toolButtonUser.setText(str(self.user_id))

        # aliases
        self.table_widget = self.ui.tableWidget
        self.label_title = self.ui.labelTitle

        if superuser is False:
            settings.disable_btns(self)
        else:
            # article details on item.doubleClicked; itemSelectionChanged enable toolbar_actions
            self.table_widget.doubleClicked.connect(self.article_details)
            self.table_widget.itemSelectionChanged.connect(self.enable_toolbarActions)

        # database handler
        db_name = APP_DIR + '/config_files/db.sqlite3'
        self.db_handler = SqliteFunc(db_name)
        self.fields = ['art_id', 'code', 'designation', 'ref', 'emp', 'umesure', 'qte', 'prix', 'valeur']

        # Set the window icon
        icon = QIcon()
        icon.addPixmap(QPixmap(APP_DIR + '/icons/box-share.png'), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        # icon callback for toolbar, menu actions and size for main table's columns
        # from config_files/settings.py
        settings.toolbar_icon_callback(self, APP_DIR)
        settings.menu_icon_callback(self, APP_DIR)
        settings.table_column_size(self)

        # main display
        self.ui.comboBoxCategory.currentIndexChanged.connect(self.articles_by_category)
        self.display_category()
        self.display_date()
        self.display_all_records()

        # search for article
        self.ui.lineEditSearch.returnPressed.connect(self.search_article)    # bind <ENTER> to search article callback
        # ('/icons/magnifier.png', self.ui.pushButtonSearch, self.search_article),
        self.ui.pushButtonSearch.clicked.connect(self.search_article)

    def display_date(self):
        # display date
        from ummalqura.hijri_date import HijriDate
        tday = date.today()
        hijri = HijriDate(tday.year, tday.month, tday.day, gr=True)
        hijri = '{}: {} {} {}'.format(hijri.day_name, hijri.day, hijri.month_name, hijri.year)
        tday = date.today().strftime('%A %d %b %Y')

        self.ui.labelDate.setText(str(tday))
        self.ui.labelHijri.setText(str(hijri))

    def display_records(self, query, params, title):
        """
        usage: display_records(query, query_params)
        """
        desc, articles = self.db_handler.make_query(query, params)
        self.table_widget.clear()
        self.table_widget.setRowCount(len(articles))    # required set row count for the tableWidget
        table_row = 0                                   # table_widget Row
        red_rows = []                                   # a list of int
        for article in articles:
            # we are inside a tuple of records
            for column, art in enumerate(article):
                # index, item_text
                item = QTableWidgetItem(str(art))                   # required; item must be QTableWidgetItem
                if column == 6 and art == 0:                        # index == 6 and qte == 0
                    red_rows.append(table_row)                      # row number where qte = 0
                self.table_widget.setItem(table_row, column, item)  # add item table_widget
                if column in (6, 7, 8):
                    item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)   # align (qte && prix) to the left
            table_row += 1

        # set backgroundColor red, and color white for article with qte = 0
        for red_row in red_rows:
            for column in range(9):          # we have 9 column
                self.table_widget.item(red_row, column).setBackground(QColor('#fab1a0'))
                # self.table_widget.item(red_row, c).setForeground(QColor('white'))     # foreground color

        # set the label title
        title = '{} = {} Article(s).'.format(title, len(articles))
        self.label_title.setText(title)

        # horizontal headers labels
        # i dont no why you must set the horizontalHeaderLabels after displaying records
        self.table_widget.setHorizontalHeaderLabels(['ID', 'Code', 'Designation', 'Reference', 'EMP', 'UM', 'Qte', 'Prix', 'Valeur'])
        self.enable_toolbarActions(False)       # disable toolBarButtons after dump records

    def display_category(self):
        # display category in comboBoxCategory
        query = 'SELECT cat_id, name FROM magasin_category ORDER BY cat_id'
        desc, categories = self.db_handler.make_query(query)
        self.ui.comboBoxCategory.insertItem(0, 'Tous')
        for category in categories:
            cat_id, cat = category
            self.ui.comboBoxCategory.insertItem(cat_id, str(cat))

    def articles_by_category(self):
        if self.ui.comboBoxCategory.currentIndex() == 0:
            # if category == 0; display all articles
            query = 'SELECT {} FROM magasin_article ORDER BY code'.format(', '.join(self.fields))
            params = []
            self.display_records(query, params, 'Tous Les Article')
        else:
            # Display article by category
            query = 'SELECT {} FROM magasin_article WHERE category_id = ? ORDER BY code'.format(', '.join(self.fields))
            params = [self.ui.comboBoxCategory.currentIndex()]
            title = '{} Article'.format(self.ui.comboBoxCategory.currentText())
            self.display_records(query, params, title)

    def display_all_records(self):
        # this function dump all records; send result to display_records method
        query = 'SELECT {} FROM magasin_article ORDER BY code ASC'.format(', '.join(self.fields))
        params = []
        self.display_records(query, params, 'Tous Les Article')

    def search_article(self):
        # search for article; send result to display_records method
        search_word = self.ui.lineEditSearch.text()
        if self.ui.radioButtonCode.isChecked():
            search_by = 'code'
        elif self.ui.radioButtonDesig.isChecked():
            search_by = 'designation'
        elif self.ui.radioButtonRef.isChecked():
            search_by = 'ref'

        query = 'SELECT {} FROM magasin_article WHERE {} LIKE ?'.format(', '.join(self.fields), search_by)
        params = ['%' + search_word + '%']
        title = 'Recherche Par {}: {}'.format(search_by, search_word)
        self.display_records(query, params, title)

    def enable_toolbarActions(self, enable=True):
        # if enable is True; then enable toolbarButtons; else disable toolbarButtons
        toolbar_btns = (self.ui.actionNewEntry, self.ui.actionNewSortie, self.ui.actionModify, self.ui.actionDel)
        if not enable:
            # disable toolbarButtons.
            for btn in toolbar_btns:
                btn.setEnabled(False)
        else:
            for btn in toolbar_btns:
                btn.setEnabled(True)
            # enable toolbarActionArtMovement
            row = self.table_widget.currentRow()
            art_id = str(self.table_widget.item(row, 0).text())   # column 0 = art_id; this will return QTableWidgetItem.text()
            if self.db_handler.product_exists('art_id_id', 'magasin_movement', 'art_id_id', art_id):
                self.ui.actionArtMov.setEnabled(True)
                # FIXME: problem with this button when triggered
                self.ui.actionArtMov.triggered.connect(lambda: self.movement_by_article(art_id))
            else:
                self.ui.actionArtMov.setEnabled(False)

    def movement_by_article(self, art_id):
        self.w_movement_by_art = Movement(art_id)
        self.w_movement_by_art.show()

    def movement(self):
        self.w_movement = Movement()
        self.w_movement.show()

    def add_article(self):
        # this method handled in call_new_article file.
        w_new_article = NewArticle(self.user_id)
        w_new_article.exec_()
        self.display_all_records()

    def get_article_id(self):
        # this function will return ArticleDetails window
        row = self.table_widget.currentRow()
        art_id = str(self.table_widget.item(row, 0).text())   # column 0 = art_id; this will return QTableWidgetItem.text()
        w_article_detail = ArticleDetails(art_id, self.user_id)
        return w_article_detail

    def article_details(self, item):
        w_article_detail = self.get_article_id()
        w_article_detail.exec_()
        self.display_all_records()

    def new_entry(self):
        w_article_detail = self.get_article_id()
        w_article_detail.new_entree()
        self.display_all_records()

    def new_sortie(self):
        w_article_detail = self.get_article_id()
        w_article_detail.new_sortie()
        self.display_all_records()

    def modify_article(self):
        w_article_detail = self.get_article_id()
        w_article_detail.modify_article()
        self.display_all_records()

    def del_article(self):
        w_article_detail = self.get_article_id()
        w_article_detail.delete_article()
        self.display_all_records()

    def stock_alarm(self):
        # stock alarm: qte = 0
        query = 'SELECT {} FROM magasin_article WHERE qte = ?'.format(', '.join(self.fields))
        params = [0]
        title = 'Quantité egale a 0'
        self.display_records(query, params, title)

    def article_sans_prix(self):
        query = 'SELECT {} FROM magasin_article WHERE prix = ?'.format(', '.join(self.fields))
        params = [0]
        title = 'Article Sans Prix'
        self.display_records(query, params, title)

    def article_sans_emp(self):
        query = 'SELECT {} FROM magasin_article WHERE emp = ?'.format(', '.join(self.fields))
        params = ['...']
        title = 'Article Sans Emplacement'
        self.display_records(query, params, title)

    def total_article(self):
        query = 'SELECT COUNT(art_id), SUM(valeur), SUM(qte) FROM magasin_article'
        params = []
        desc, rows = self.db_handler.make_query(query, params)
        for row in rows:
            total_article, valeur, total_qte = row
        w_total_article = TotalArticles()
        w_total_article.ui.labelArticle.setText(': ' + str(total_article))
        w_total_article.ui.labelValeur.setText(': ' + str(valeur) + ' DA')
        w_total_article.ui.labelTotalQte.setText(': ' + str(total_qte))
        w_total_article.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # TODO: add login to our app
    # log_in_window = LogIn()
    # log_in_window.show()
    w = MainApp(user_id=1, superuser=True)
    w.showMaximized()
    sys.exit(app.exec_())
