# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerutinIV.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject,QRect, Qt)
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon
import requests
import json
import api_key

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 172)
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(170, 130, 75, 23))
        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(100, 60, 221, 20))
        self.comboBox = QComboBox(Dialog)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(70, 10, 271, 22))
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 100, 361, 20))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Banking Check Info", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Check", None))
        self.pushButton.clicked.connect(self.get_bank_name)
        self.label.setText(QCoreApplication.translate("Dialog", u"", None))
    # retranslateUi

    def __init__(self):
        self.banks_list = requests.get("https://api.vietqr.io/v2/banks")

    def print_banks_info(banks_data):
        for bank in banks_data['data']:
            print(f"ID: {bank['id']}")
            print(f"Name: {bank['name']}")
            print(f"Code: {bank['code']}")
            print(f"BIN: {bank['bin']}")
            print(f"Short Name: {bank['shortName']}")
            print(f"Logo: {bank['logo']}")
            print(f"Transfer Supported: {bank['transferSupported']}")
            print(f"Lookup Supported: {bank['lookupSupported']}")
            print("\n")
    def get_bank_account_name(self,bank_bin, bank_code):
        api_key_demo = api_key.api_key
        client_id_demo = api_key.client_id
        url = "https://api.vietqr.io/v2/lookup"
        headers = {
            'x-client-id': client_id_demo,
            'x-api-key': api_key_demo,
            'Content-Type': 'application/json',
        }
        data = {
            "bin": bank_bin,
            "accountNumber": bank_code,
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_data = response.json()
            if response_data is not None and 'data' in response_data:
                return response_data['data']['accountName']
            else:
                print("Invalid response data:", response_data)
                return None
        else:
            print("Failed to get account name, status code:", response.status_code)
            return None
    def get_bank_bin(self,bank_name):
        bank_name = bank_name.lower()
        for bank in self.banks_list.json()['data']:
            if bank_name in bank['name'].lower():
                return bank['bin']
            # else:
            #     print(f"{bank_name} not found in {bank['name'].lower()}")
        return None
    def get_bank_name(self):
        selected_bank = self.comboBox.currentText()
        account_number = self.lineEdit.text()
        for bank in self.banks_list.json()['data']:
            if bank['name'] == selected_bank:
                bank_bin = self.get_bank_bin(selected_bank)
                if bank_bin is not None:
                    account_name = self.get_bank_account_name(bank_bin, account_number)
                    self.label.setText(f"Tên tài khoản: {account_name}")
                    self.label.setAlignment(Qt.AlignCenter)
                else:
                    print(f"{selected_bank} not found")
                    return None

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)

    # Set the window icon
    app.setWindowIcon(QIcon('logo.ico'))

    bank_names = [bank['name'] for bank in ui.banks_list.json()['data']]
    ui.comboBox.addItems(bank_names)
    Dialog.show()
    sys.exit(app.exec_())