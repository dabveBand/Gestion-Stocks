#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file   : call_article_details.py
# caller : magasin_qt.py
# desc   : call the article details window.
# NOTE   : this file handle the {entree, sortie, modify, delete} article
# -----------------------------------------------------------------------

from PyQt5.QtWidgets import QDialog, QMenu, QMessageBox      # , QAction
from PyQt5.QtGui import QFont, QIcon, QPixmap

from config_files.sqlite_functions import SqliteFunc
from headers.h_article_details import Ui_ArticleDetails

from entree_sortie_modify_delete import ArticleEntree, ArticleSortie, ModifyArticle, message_box_result, Movement


class ArticleDetails(QDialog):
    def __init__(self, art_id, user_id):
        super().__init__()
        self.art_id = art_id
        self.user_id = user_id
        self.ui = Ui_ArticleDetails()
        self.ui.setupUi(self)

        # Database handler
        db_name = './config_files/db.sqlite3'
        self.db_handler = SqliteFunc(db_name)

        # window configuration
        window_icon = QIcon()
        window_icon.addPixmap(QPixmap('./icons/clipboard--pencil.png'), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(window_icon)

        # Font for menu
        self.menu_font = QFont()
        self.menu_font.setFamily("Monaco")
        self.menu_font.setPointSize(11)

        # initial display
        self.article_details()

        # Movement Menu
        self.moveMenu = QMenu(self.ui.toolButtonMovement)
        self.ui.toolButtonMovement.setMenu(self.moveMenu)
        self.moveMenu.aboutToShow.connect(self.movement_menu)

        # Action Menu
        self.actionMenu = QMenu(self.ui.toolButtonAction)
        self.ui.toolButtonAction.setMenu(self.actionMenu)
        self.actionMenu.aboutToShow.connect(self.action_menu)

    def article_details(self):
        query = 'SELECT * FROM magasin_article WHERE art_id = ?'
        params = [self.art_id]
        desc, rows = self.db_handler.make_query(query, params)
        for row in rows:
            art_id, slug, desig, self.code, ref, um, emp, qte, prix, valeur, cat_id, obs = row
            self.ui.labelArticlId.setText('Fiche de Stock N° ' + str(art_id))
            self.ui.labelCat.setText(': ' + str(cat_id))
            self.ui.labelCode.setText(': ' + self.code)
            self.ui.labelDesig.setText(': ' + desig)
            self.ui.labelRef.setText(': ' + ref)
            self.ui.labelUM.setText(': ' + um)
            self.ui.labelEmp.setText(': ' + emp)
            self.ui.labelQte.setText(': ' + str(qte))
            self.ui.labelPrix.setText(': ' + str(prix))
            self.ui.labelValeur.setText(': ' + str(valeur))
            if not obs:
                obs = 'RAS'
            self.ui.labelNote.setText(': ' + obs)

    def action_menu(self):
        self.actionMenu.clear()
        actions = [('Modifier', self.modify_article, QIcon('./icons/application--pencil.png')),
                   ('Supprimer', self.delete_article, QIcon('./icons/scissors--minus.png'))]

        for action, callback, icon in actions:
            menu_label = self.actionMenu.addAction(action)
            menu_label.setFont(self.menu_font)
            menu_label.setIcon(icon)
            menu_label.triggered.connect(callback)

    def movement_menu(self):
        self.moveMenu.clear()
        actions = [('Entree', self.new_entree, QIcon('./icons/box--plus.png')),
                   ('Sortie', self.new_sortie, QIcon('./icons/box--minus.png')),
                   ]
        for action, callback, icon in actions:
            menu_label = self.moveMenu.addAction(action)
            menu_label.setFont(self.menu_font)
            menu_label.setIcon(icon)
            menu_label.triggered.connect(callback)

        # movement history for one article
        action_move_history = self.moveMenu.addAction('Mov History')
        action_move_history.setFont(self.menu_font)
        action_move_history.setIcon(QIcon('./icons/clock-history.png'))
        # check if article has movement history
        # FIXME: product_exists in sqlite_functions
        product_exist = self.db_handler.product_exists('art_id_id', 'magasin_movement', 'art_id_id', self.art_id)
        # print(product_exist)
        if product_exist:
            action_move_history.setEnabled(True)
            action_move_history.triggered.connect(self.movement_history)
        else:
            action_move_history.setEnabled(False)

    def new_entree(self):
        w_entree = ArticleEntree(self.art_id, self.user_id)
        w_entree.exec_()
        self.article_details()

    def new_sortie(self):
        w_sortie = ArticleSortie(self.art_id, self.user_id)
        w_sortie.exec_()
        self.article_details()

    def movement_history(self):
        self.w_movement = Movement(self.art_id)
        self.w_movement.show()

    def modify_article(self):
        w_modify_article = ModifyArticle(self.art_id, self.user_id)
        w_modify_article.exec_()
        self.article_details()

    def delete_article(self):
        msg_title = 'Supprimer Article'
        msg = 'Are you sure to delete article with CODE: <b>{}</b>'.format(self.code)
        msg_box = message_box_result(self, msg_title, msg, 'question')
        if msg_box == QMessageBox.Yes:
            query = 'DELETE FROM magasin_article WHERE art_id = ?'
            params = [self.art_id]
            result = int(self.db_handler.make_query(query, params))

            if result > 0:
                msg = '{} Article Supprimer Avec Succes'.format(result)
                message_box_result(self, msg_title, msg, 'info')
                self.close()
            else:
                msg = '<b>Error</b>: {}'.format(result)
                QMessageBox.warning(self, msg_title, msg, QMessageBox.Close)
                message_box_result(self, msg_title, msg, 'warning')
