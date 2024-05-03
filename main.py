import requests
import json
import tkinter as tk
from tkinter import ttk
banks_list = requests.get("https://api.vietqr.io/v2/banks")
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

print_banks_info(banks_list.json())
def get_user_input():
    bank_name = input("Tên ngân hàng: ")
    bank_code = input("Số tài khoản: ")
    return bank_name, bank_code

def get_bank_account_name(bank_bin, bank_code):
    api_key_demo = "demo-2a02822e-ede3-4970-999b-18853d8e0ced"
    client_id_demo = "demo-a34a5775-ae15-4a05-8422-1023eccbda3f"
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
        return response.json()['data']['accountName']
    else:
        return None
def get_bank_bin(bank_name):
    bank_name = bank_name.lower()
    for bank in banks_list.json()['data']:
        if bank_name in bank['name'].lower():
            return bank['bin']
        else:
            print(f"{bank_name} not found in {bank['name'].lower()}")
    return None

def get_bank_name():
    selected_bank = combo.get()
    account_number = account_entry.get()
    for bank in banks_list.json()['data']:
        if bank['name'] == selected_bank:
            bank_bin = get_bank_bin(selected_bank)
            if bank_bin is not None:
                account_name = get_bank_account_name(bank_bin, account_number)
                account_label.config(text=f"Tên tài khoản: {account_name}")
            else:
                account_label.config(text="Không tìm thấy ngân hàng")

root = tk.Tk()

# Lấy danh sách tên ngân hàng
bank_names = [bank['name'] for bank in banks_list.json()['data']]

# Tạo combo box
combo = ttk.Combobox(root, values=bank_names)
combo.pack()

# Tạo trường nhập liệu cho số tài khoản
account_entry = tk.Entry(root)
account_entry.pack()

# Tạo nhãn để hiển thị tên tài khoản
account_label = tk.Label(root, text="")
account_label.pack()

# Tạo nút để lấy tên tài khoản
submit_button = tk.Button(root, text="Lấy tên tài khoản", command=get_bank_name)
submit_button.pack()

root.mainloop()