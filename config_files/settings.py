#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# FILE     :
# AUTHOR   : daBve, dabve@gmail.com
# CREATED  :
# UPDATED  :
# -----------------------------------------------------
# REQ      :
# DESC     :
# -----------------------------------------------------

from PyQt5.QtGui import QIcon, QPixmap        # QColor
import os

APP_DIR = os.getcwd()


def table_column_size(root):
    root.table_widget.setColumnWidth(0, 60)       # ID Column
    root.table_widget.setColumnWidth(1, 100)      # Code Column
    root.table_widget.setColumnWidth(2, 250)      # Designation Column
    root.table_widget.setColumnWidth(3, 230)      # Ref Column
    root.table_widget.setColumnWidth(4, 80)       # Emp Column
    root.table_widget.setColumnWidth(5, 60)       # UM Column
    root.table_widget.setColumnWidth(6, 70)      # Qte Column
    root.table_widget.setColumnWidth(7, 100)      # Prix Column
    root.table_widget.setColumnWidth(8, 133)      # Valeur Column


def toolbar_icon_callback(root, app_dir):

    toolbar_items = [('/icons/baggage-cart-box-label.png', root.ui.actionAddArticle, root.add_article),
                     ('/icons/box--plus.png', root.ui.actionNewEntry, root.new_entry),
                     ('/icons/box--minus.png', root.ui.actionNewSortie, root.new_sortie),
                     ('/icons/box--pencil.png', root.ui.actionModify, root.modify_article),
                     ('/icons/cross-button.png', root.ui.actionDel, root.del_article)
                     ]
    for btn_icon, btn, callback in toolbar_items:
        icon = QIcon()
        icon.addPixmap(QPixmap(app_dir + btn_icon), QIcon.Normal, QIcon.Off)
        btn.setIcon(icon)
        btn.triggered.connect(callback)

    actionArtMovIcon = QIcon()
    actionArtMovIcon.addPixmap(QPixmap(app_dir + '/icons/arrow-retweet'), QIcon.Normal, QIcon.Off)
    root.ui.actionArtMov.setIcon(actionArtMovIcon)


def menu_icon_callback(root, app_dir):
    menu_items = [('/icons/box--exclamation.png', root.ui.actionStockAlarm, root.stock_alarm),
                  ('/icons/report.png', root.ui.actionArticleSansPrix, root.article_sans_prix),
                  ('/icons/report.png', root.ui.actionArticleSansEmp, root.article_sans_emp),
                  ('/icons/chart.png', root.ui.actionTotalDesArticle, root.total_article),
                  ('/icons/clock-history.png', root.ui.actionHistoryMovement, root.movement),
                  ('/icons/document-excel-table.png', root.ui.actionSaveAsExcel, root.total_article),
                  ]
    for btn_icon, btn, callback in menu_items:
        icon = QIcon()
        icon.addPixmap(QPixmap(app_dir + btn_icon), QIcon.Normal, QIcon.Off)
        btn.setIcon(icon)
        btn.triggered.connect(callback)


def disable_btns(root):
    toolbar_items = [root.ui.actionAddArticle,
                     root.ui.actionNewEntry,
                     root.ui.actionNewSortie,
                     root.ui.actionModify,
                     root.ui.actionDel
                     ]

    for btn in toolbar_items:
        btn.setEnabled(False)
