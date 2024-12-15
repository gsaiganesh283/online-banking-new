import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to fetch data from the database
def fetch_data():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Daddy22@",
            database="internetbanking"
        )
        cursor = conn.cursor()

        # Fetch total number of iBank clients
        cursor.execute("SELECT count(*) FROM iB_clients")
        iBClients = cursor.fetchone()[0]

        # Fetch total number of iBank staffs
        cursor.execute("SELECT count(*) FROM iB_staff")
        iBStaffs = cursor.fetchone()[0]

        # Fetch total number of iBank account types
        cursor.execute("SELECT count(*) FROM iB_Acc_types")
        iB_AccsType = cursor.fetchone()[0]

        # Fetch total number of iBank accounts
        cursor.execute("SELECT count(*) FROM iB_bankAccounts")
        iB_Accs = cursor.fetchone()[0]

        # Fetch total deposits
        cursor.execute("SELECT SUM(transaction_amt) FROM iB_Transactions WHERE tr_type = 'Deposit'")
        iB_deposits = cursor.fetchone()[0] or 0

        # Fetch total withdrawals
        cursor.execute("SELECT SUM(transaction_amt) FROM iB_Transactions WHERE tr_type = 'Withdrawal'")
        iB_withdrawal = cursor.fetchone()[0] or 0

        # Fetch total transfers
        cursor.execute("SELECT SUM(transaction_amt) FROM iB_Transactions WHERE tr_type = 'Transfer'")
        iB_Transfers = cursor.fetchone()[0] or 0

        # Calculate total balance in account
        TotalBalInAccount = iB_deposits - (iB_withdrawal + iB_Transfers)

        # Close the connection
        cursor.close()
        conn.close()

        return {
            "iBClients": iBClients,
            "iBStaffs": iBStaffs,
            "iB_AccsType": iB_AccsType,
            "iB_Accs": iB_Accs,
            "iB_deposits": iB_deposits,
            "iB_withdrawal": iB_withdrawal,
            "iB_Transfers": iB_Transfers,
            "TotalBalInAccount": TotalBalInAccount
        }
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# Function to update the UI with fetched data
def update_ui(data):
    if data:
        clients_label.config(text=f"Clients: {data['iBClients']}")
        staffs_label.config(text=f"Staffs: {data['iBStaffs']}")
        acc_types_label.config(text=f"Account Types: {data['iB_AccsType']}")
        accounts_label.config(text=f"Accounts: {data['iB_Accs']}")
        deposits_label.config(text=f"Deposits: ${data['iB_deposits']}")
        withdrawals_label.config(text=f"Withdrawals: ${data['iB_withdrawal']}")
        transfers_label.config(text=f"Transfers: ${data['iB_Transfers']}")
        balance_label.config(text=f"Wallet Balance: ${data['TotalBalInAccount']}")

# Function to plot graphs
def plot_graphs(data):
    if data:
        fig, axs = plt.subplots(2, 2, figsize=(10, 8))

        # Bar graph for transaction amounts by type
        labels = ['Deposits', 'Withdrawals', 'Transfers']
        values = [data['iB_deposits'], data['iB_withdrawal'], data['iB_Transfers']]
        axs[0, 0].bar(labels, values, color=['green', 'red', 'blue'])
        axs[0, 0].set_title('Transaction Amounts by Type')
        axs[0, 0].set_xlabel('Transaction Types')
        axs[0, 0].set_ylabel('Amount')

        # Pie chart for account types
        labels_pie = ['Clients', 'Staffs', 'Account Types', 'Accounts']
        sizes_pie = [data['iBClients'], data['iBStaffs'], data['iB_AccsType'], data['iB_Accs']]
        axs[0, 1].pie(sizes_pie, labels=labels_pie, autopct='%1.1f%%', startangle=140)
        axs[0, 1].set_title('Distribution of Account Types')

        # Line graph for deposits, withdrawals, and transfers
        labels_line = ['Deposits', 'Withdrawals', 'Transfers']
        values_line = [data['iB_deposits'], data['iB_withdrawal'], data['iB_Transfers']]
        axs[1, 0].plot(labels_line, values_line, marker='o')
        axs[1, 0].set_title('Transaction Trends')
        axs[1, 0].set_xlabel('Transaction Types')
        axs[1, 0].set_ylabel('Amount')

        # Horizontal bar graph for total balance
        axs[1, 1].barh(['Total Balance'], [data['TotalBalInAccount']], color='purple')
        axs[1, 1].set_title('Total Balance in Account')
        axs[1, 1].set_xlabel('Amount')

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Initialize the main tkinter window
root = tk.Tk()
root.title("Admin Dashboard")
root.geometry("1000x800")

# Create a frame for the dashboard
frame = ttk.Frame(root, padding="20")
frame.pack(fill="both", expand=True)

# Add labels to display the data
clients_label = ttk.Label(frame, text="Clients: ", font=("Helvetica", 12))
clients_label.grid(row=0, column=0, pady=10, padx=5, sticky=tk.W)

staffs_label = ttk.Label(frame, text="Staffs: ", font=("Helvetica", 12))
staffs_label.grid(row=1, column=0, pady=10, padx=5, sticky=tk.W)

acc_types_label = ttk.Label(frame, text="Account Types: ", font=("Helvetica", 12))
acc_types_label.grid(row=2, column=0, pady=10, padx=5, sticky=tk.W)

accounts_label = ttk.Label(frame, text="Accounts: ", font=("Helvetica", 12))
accounts_label.grid(row=3, column=0, pady=10, padx=5, sticky=tk.W)

deposits_label = ttk.Label(frame, text="Deposits: $", font=("Helvetica", 12))
deposits_label.grid(row=4, column=0, pady=10, padx=5, sticky=tk.W)

withdrawals_label = ttk.Label(frame, text="Withdrawals: $", font=("Helvetica", 12))
withdrawals_label.grid(row=5, column=0, pady=10, padx=5, sticky=tk.W)

transfers_label = ttk.Label(frame, text="Transfers: $", font=("Helvetica", 12))
transfers_label.grid(row=6, column=0, pady=10, padx=5, sticky=tk.W)

balance_label = ttk.Label(frame, text="Wallet Balance: $", font=("Helvetica", 12))
balance_label.grid(row=7, column=0, pady=10, padx=5, sticky=tk.W)

# Fetch and display the data
data = fetch_data()
update_ui(data)
plot_graphs(data)

# Run the tkinter loop
root.mainloop()