#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file      : sqlite_functions.py
# created   : 09-Apr-2019 (older by one month than marwa)
# author    : Ibrahim Addadi, dabve@gmail.fr
#
# desc      : sqlite operations to help work with sqlite databases
# req       : sys, csv, collections(namedtuple, OrderedDict), sqlite3, terminaltables, xlsxwriter, colorama


import csv
from collections import namedtuple, OrderedDict
import sqlite3
from sqlite3 import Error


class SqliteFunc:
    def __init__(self, db_name):
        self.db_name = db_name

    def login(self):
        """
        Connect to a specific database; if database does not exist sqlite will create it
        """
        try:
            conn = sqlite3.connect(self.db_name)
        except Error as err:
            return 'Error: {}'.format(err)
        else:
            curs = conn.cursor()
            return conn, curs

    def get_article_id(self, art_code):
        query = 'SELECT art_id FROM magasin_article WHERE code = ?'
        params = [art_code]
        _, rows = self.make_query(query, params)
        return rows[0][0]

    def make_query(self, query, params=(), desc=False):
        """
        Usage   : make_query('SELECT * FROM table WHERE id = ?', [1])
          query   : CRUD Query
          params  : parameter for the query (list)
          return tuple (desc, rows) | rowcount for update and delete operations
        """
        conn, curs = self.login()
        try:
            curs.execute(query, params)
        except Error as err:
            return err
        else:
            stmt = query.split()[0].upper()
            if stmt == 'SELECT':
                desc = [desc[0] for desc in curs.description]
                rows = curs.fetchall()
                return (desc, rows)
            else:
                conn.commit()
                return curs.rowcount
        finally:
            if conn: conn.close()

    def product_exists(self, select, table, column, value):
        """
        Check if product exists
            - Usage   : product_exists('magasin_pdr', 'code', 'BHS-0005')
            - table   : table name
            - column  : column to search with like id, name, firstname
            - value   : value to search for
        Return True or False
        """
        conn, curs = self.login()
        try:
            curs.execute('SELECT ' + select + ' FROM ' + table + ' WHERE ' + column + ' = ?', [value])
        except Error as err:
            return 'Error: {}'.format(err)
        else:
            if curs.fetchone(): return True
            else: return False
        finally:
            if conn: conn.close()

    def display(self, display, desc, rows):
        """
        Display result as:
            - ordereddict : return OrderedDict object.
            - dic         : return a dict object.
            - namedtuple  : return a named tuple.
        Note: desc, rows required
        """
        if display == 'ordereddict':
            # convert desc, rows to an OrderedDictt object
            rowdicts = [OrderedDict(zip(desc, row)) for row in rows]
            return rowdicts
        elif display == 'dict':
            rowdicts = [dict(zip(desc, row)) for row in rows]
            return rowdicts
        elif display == 'namedtuple':
            return self.__as_namedtuple(desc, rows)

    def __as_namedtuple(self, desc, rows):
        for ind, value in enumerate(desc):
            # namedtuple take this form: Parts = namedtuple('Parts', 'id_num desc cost amount')
            # find white space on description and change it to '_' chars
            index = value.find(' ')     # index of white space inside value; find return the index
            if index > 0:
                desc[ind] = value.replace(' ', '_')
        Row = namedtuple('Row', desc)               # getting the key from description
        rows = [Row(*r) for r in rows]              # getting values
        return rows

    def write_to_csv(self, csv_out, query, params=()):
        """
        Write a query to a csv file
            Usage   : write_to_csv('outfile.csv', 'SELECT * FROM table WHERE id = ?', [10])
            csv_out : Out file to write into
            query   : SQL Query
            params  : parameters for the query
        """
        conn, curs = self.login()
        desc, rows = self.make_query(query, params)
        with open(csv_out, 'w', encoding='utf-8') as f:
            csv_writer = csv.writer(f, delimiter=';')
            csv_writer.writerow(desc)
            for row in rows:
                csv_writer.writerow(row)
        return 'Done \nResult in :{}'.format(f.name)

    def load_from_csv(self, table_name, csv_file):
        '''
        Load data from csv file to table_name
        Note:
            - Add headers to your file.
            - Values separated with ';'
        '''
        conn, curs = self.login()
        with open(csv_file, encoding='latin-1') as input_file:
            csv_reader = csv.reader(input_file, delimiter=';')
            headers = ', '.join(next(csv_reader))               # string that containt headers to add to the query
            rows = [tuple(row) for row in csv_reader]
            bind = ('?, ' * len(rows[0]))[:-2]                  # bind will contain '?, ?' * headers number

        query = 'INSERT INTO ' + table_name + '(' + headers + ') VALUES(' + bind + ')'
        try:
            curs.executemany(query, rows)
        except Error as err:
            print('Error: {}'.format(err))
        else:
            conn.commit()
            return '[{}] affected rows'.format(curs.rowcount)
        finally:
            if conn:
                conn.close()

    def write_to_excel(self, desc, rows, date_):
        import os
        from datetime import date
        import xlsxwriter
        '''
        Write SQL Query to xlsx file
        desc : colnames
        rows : data
        date_ : to name the file.
        '''
        if not os.path.exists('Etats'):
            os.mkdir('Etats')

        fname = './Etats/etat_' + date_ + '.xlsx'
        if os.path.exists(fname):
            # remove old file with the same name
            os.remove(fname)

        # formate rows and description and headers
        wbook = xlsxwriter.Workbook(fname, {'remove_timezone': True})
        desc_format = wbook.add_format({'font_name': 'Times New Roman',
                                        'bold': True,
                                        'font_size': 16,
                                        'border': 1,
                                        'align': 'center',
                                        'valign': 'center'})

        rows_format = wbook.add_format({'font_name': 'Times New Roman', 'font_size': 14, 'border': 1})
        date_format = wbook.add_format({'font_name': 'Times New Roman', 'font_size': 14, 'border': 1, 'num_format': 'dd mmmm yyyy'})
        money_format = wbook.add_format({'font_name': 'Times New Roman', 'font_size': 14, 'border': 1, 'num_format': '# ##0,00 €'})

        wsheet = wbook.add_worksheet(date_)
        wsheet.set_row(3, 25)               # set height for row 0
        wsheet.set_column('A:A', 25)        # set length for (movement_date)
        wsheet.set_column('B:B', 18)        # set length for (code)
        wsheet.set_column('C:C', 32)        # set length for (designation)
        wsheet.set_column('D:D', 18)        # set length for (movement)
        wsheet.set_column('E:E', 12)        # set length for (qte)
        wsheet.set_column('F:F', 18)        # set length for (prix)
        wsheet.set_column('G:G', 18)        # set length for (valeur)

        # write title and date
        title_format = wbook.add_format({'font_name': 'Times New Roman',
                                         'font_size': 20,
                                         'bold': True,
                                         'italic': True,
                                         'valign': 'center'})
        wsheet.merge_range('A1:C1', 'Etats Du ' + date_, title_format)

        # date
        tday = date.today().strftime('%d/%m/%Y')
        tday_format = wbook.add_format({'font_name': 'Times New Roman', 'font_size': 14, 'valign': 'right'})
        wsheet.merge_range('F1:G1', 'Bou Ismail Le: ' + tday, tday_format)

        # write description
        excel_row = 3
        excel_col = 0
        for des in desc:
            wsheet.write(excel_row, excel_col, des.title(), desc_format)
            excel_col += 1

        # write rows
        excel_row = 4
        for row in rows:
            excel_col = 0
            for i, r in enumerate(row):
                if i == 0:
                    wsheet.write(excel_row, excel_col, r, date_format)
                elif i == 5 or i == 6:        # prix, valeur index
                    wsheet.write(excel_row, excel_col, r, money_format)
                else:
                    rows_format.set_num_format('0')
                    wsheet.write(excel_row, excel_col, r, rows_format)
                excel_col += 1
            excel_row += 1

        wbook.close()
        return fname

    def __repr__(self):
        return '<{!r} connected to {!r} >'.format(self.__class__.__name__, self.db_name)


class MovementTable:
    def __init__(self, art_id, user_id):
        self.art_id = int(art_id)
        self.user_id = user_id

        db_name = './config_files/db.sqlite3'
        self.db_handler = SqliteFunc(db_name)

    def new_entree(self, ent_date, qte, prix):
        query = '''INSERT INTO magasin_movement(art_id_id, movement_date, user_id_id, movement, qte, prix, valeur)
                   VALUES(?, ?, ?, ?, ?, ?, ?)'''
        valeur = qte * prix
        params = [self.art_id, ent_date, self.user_id, 'Entree', qte, prix, valeur]
        result = self.db_handler.make_query(query, params)
        print(result)

    def new_sortie(self, ent_date, qte, prix):
        query = '''INSERT INTO magasin_movement(art_id_id, movement_date, user_id_id, movement, qte, prix, valeur)
                   VALUES(?, ?, ?, ?, ?, ?, ?)'''
        valeur = qte * prix
        params = [self.art_id, ent_date, self.user_id, 'Sortie', qte, prix, valeur]
        result = self.db_handler.make_query(query, params)
        print(result)


class MagasinHistory:
    def __init__(self, art_id, user_id):
        self.art_id = art_id
        self.user_id = user_id

        # history db handler
        db_name = './config_files/db.sqlite3'
        self.db_handler = SqliteFunc(db_name)

    def new_article(self):
        query = '''INSERT INTO magasin_history(hist_date, user_id, art_id, operation, old_values, new_values)
                   VALUES(date('now'), ?, ?, ?, ?, ?)'''
        params = [self.user_id, self.art_id, 'Nouveaux Article', '', '']
        self.db_handler.make_query(query, params)

    def modify_article(self, old_values, new_values):
        query = '''INSERT INTO magasin_history(hist_date, user_id, art_id, operation, old_values, new_values)
                   VALUES(date('now'), ?, ?, ?, ?, ?)'''
        params = [self.user_id, self.art_id, 'Modification', old_values, new_values]
        print(self.db_handler.make_query(query, params))


if __name__ == '__main__':
    db_name = 'db.sqlite3'
    dbase = SqliteFunc(db_name)

    query = 'UPDATE magasin_article SET valeur = qte * prix'
    params = []
    result = dbase.make_query(query, params)
    print(result)
