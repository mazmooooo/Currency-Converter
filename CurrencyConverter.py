import requests
import tkinter as tk
from tkinter import ttk, messagebox
from config import API_KEY #The API key is stored separately for security and confidentiality purposes.

#This is the main class used for everything, from fetching data, processing data, and displaying data, everything is within this section of the program.
class CurrencyConverter:

#Loads up the essential information and code needed to be able to use the API for the Currency Converter.
    def __init__(self):
        self.base_url = "https://api.freecurrencyapi.com/v1/latest"
        self.api_key = API_KEY
        self.exchangeRates = {}
        self.loadExchangeRates()
    
    def loadExchangeRates(self):
        url = f"{self.base_url}?apikey={self.api_key}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            if "data" not in data:
                raise ValueError("Invalid response format")

            self.exchangeRates = data
            print("data retrieved")

#This is the error handling section just in case there are other issues that the program might face during the loading of exchange rates from the API
        except requests.exceptions.Timeout: #Notifies the user that they timed out after 10 seconds of no response
            messagebox.showerror("Error", "The request timed out. Please check your internet connection.")

        except requests.exceptions.ConnectionError: #Notifies the user that the program couldn’t connect to the currency service.
            messagebox.showerror("Error", "Unable to connect to the currency service.")

        except requests.exceptions.HTTPError as e: #Notifies the user of an API error with the specific HTTP issue.
            messagebox.showerror("Error", f"API Error: {e}")

        except ValueError: #Notifies the user that the data received from the API was invalid.
            messagebox.showerror("Error", "Received invalid data from the API.")

        except Exception as e:#Catches any other unexpected errors and shows the error message to the user.
            messagebox.showerror("Error", f"Unexpected error: {e}")

#This is the main conversion process section. This converts by getting the usd equivalent of the initial currency to be able to convert into the desired currency. once the entire conversion process finishes, it returns back to the user the total converted amount, as well as the symbol that the currency uses.
    def convert(self, amount, previousCurrency, afterCurrency):
        usd = amount / self.exchangeRates['data'][previousCurrency]
        converted_amount = usd * self.exchangeRates['data'][afterCurrency]
        symbol = currencySymbol["symbol"][afterCurrency]
        return f"{symbol} {converted_amount:.2f}"
    
    def swapCurrencies(self):
        #Get current selections
        from_currency = currencyBefore.get()
        to_currency = currencyAfter.get()
        
        #Swaps them with each other
        currencyBefore.set(to_currency)
        currencyAfter.set(from_currency)

#This is the conversion output section. This section is the final step in the Currency Converter application, it goes through a series of error handling which first checks if the amount is actually a number, and if so, it must be a positive numeric value. After that, the currency chosen initially, and the currency chosen to convert to, must be within the currency_choices list which has the list of the valid currencies for the user to choose from. This ensures that the user chooses a currency to convert from and to. Finally, once all the conditions are met, it will display the total amount that the money got converted to, as well as its currency symbol.
    def conversionOutput(self):
        try:
            amount = float(amountEntry.get())

            if amount <= 0:
                messagebox.showerror("Invalid Value", "Please enter an amount that you would like to convert.")
                return

            if currencyBefore.get() not in currency_choices or currencyAfter.get() not in currency_choices:
                messagebox.showerror("Invalid Selection", "Please select a valid option from the list")
                return

            final = self.convert(amount,currencyBefore.get(),currencyAfter.get())

            output.config(text=final)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a numeric value.")

#This is the Exchange Rate Window section. This section is responsible for popping up a new window which shows all the available currencies along with with their respective conversion rates. This window can be used as a guide for the user on to what they might be interested on exchanging to.
    def showExchangeRatesWindow(self):
        if not self.exchangeRates or "data" not in self.exchangeRates:
            messagebox.showerror("Error", "Exchange rates not loaded.")
            return

        rates_window = tk.Toplevel()
        rates_window.title("Exchange Rates")
        rates_window.geometry("450x500")
        rates_window.config(background="#F5F0EA")
        rates_window.resizable(False, False)

        title = tk.Label(
            rates_window,
            text="Base Rate: USD",
            font=('sans-serif', 22, 'bold'),
            bg="#F5F0EA",
            fg="#22333B")
        title.pack(pady=10)

        columns = ("Currency", "Rate")

        tree = ttk.Treeview(
            rates_window,
            columns=columns,
            show="headings",
            height=18)

        tree.heading("Currency", text="Currency")
        tree.heading("Rate", text="Rate")
        tree.column("Currency", anchor=tk.CENTER, width=120)
        tree.column("Rate", anchor=tk.CENTER, width=250)

        for currency, rate in sorted(self.exchangeRates["data"].items()):
            tree.insert("", tk.END, values=(currency, f"{rate:.6f}"))
        tree.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)
        tree.bind(
            "<<TreeviewSelect>>",
            lambda e: tree.selection_remove(tree.selection()))

currency = CurrencyConverter() 

#This list is used to provide options to choose from in the combobox in the GUI and also a reference to check if proper currencies were chosen.
currency_choices = ['AUD','BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EUR', 'GBP', 'HKD', 'HRK', 'HUF', 'IDR', 'ILS', 'INR', 'ISK', 'JPY', 'KRW', 'MXN', 'MYR', 'NOK', 'NZD','PHP', 'PLN', 'RON', 'RUB', 'SEK', 'SGD', 'THB', 'TRY', 'USD', 'ZAR' ]

#This dictionary is used to provide the respective currency symbols for each currency chosen to convert to.
currencySymbol = {'symbol' : {
    "AUD": "AUD$","BGN": "лв", "BRL": "R$", "CAD": "CAD$", "CHF": "CHF", "CNY": "CN¥", "CZK": "Kč", "DKK": "DKK kr", "EUR": "€", "GBP": "£", "HKD": "HK$", "HRK": "kn", "HUF": "Ft", "IDR": "Rp", "ILS": "₪", "INR": "₹", "ISK": "ISK kr", "JPY": "JP¥", "KRW": "₩", "MXN": "MX$", "MYR": "RM", "NOK": "NOK kr", "NZD": "NZ$", "PHP": "₱","PLN": "zł", "RON": "lei", "RUB": "₽","SEK": "SEK kr","SGD": "S$","THB": "฿","TRY": "₺","USD": "US$","ZAR": "R"} }

#GUI
window = tk.Tk()
window.geometry('800x600')
window.title("Currency Converter")
window.resizable(width=False, 
                 height=False)
window.config(background="#F5F0EA")
icon = tk.PhotoImage(file="CurrencyConverter.png")
window.iconphoto(True, icon)

#Title
title = tk.Label(window, text="Currency Converter", 
              font=('sans-serif',45,'bold'), 
              background='#F5F0EA', 
              fg='#22333B')
title.pack(pady=5, padx=0)

#Window for showing the exchange rates
showExchangeRates = tk.Button(window,
                           text="SHOW EXCHANGE RATES",
                           font=('sans-serif', 15),
                           width=41,
                           background='white',
                           command=currency.showExchangeRatesWindow
                           )
showExchangeRates.place(x=100, y=150)

#The section where the user can enter however much they would like in numeric form, or click the up or down arrow depending on what amount they would be satisfied with.
amountEntry = tk.Spinbox(window,
                         from_=0, 
                         to_=99999999999,
                         width=15,
                         font=('sans-serif',25),
                         border=1,
                         fg='#2E2E2E')
amountEntry.place(x=347, y=250)

#The drop down / combobox that will display all of the currencies available on which they would convert from.
currencyBefore = ttk.Combobox(window,
                               values=currency_choices,
                               height=20,
                               width=10,
                               font=('sans-serif',24),
                               state='readonly')
currencyBefore.place(x=100, y=250)

#This button is the conversion button that allows the program to process and convert the amount that the user had entered and display it on the screen.
convertButton = tk.Button(window,
                           text="CONVERT",
                           font=('sans-serif', 15),
                           width=25,
                           height=1,
                           command=currency.conversionOutput,
                           bg='white')
convertButton.place(x=325, y=325)

#This button is the swap button that allows the user to swap the currencies that they have chosen
swapButton = tk.Button(window,
                       text="Swap ⇅", 
                       font=('sans-serif', 18, 'bold'),
                       width=13,
                       bg='white',
                       border=1,
                       command=currency.swapCurrencies)
swapButton.place(x=100, y=400) 

##The drop down / combobox that will display all of the currencies available on which they would like to convert to.
currencyAfter = ttk.Combobox(window,
                               values=currency_choices,
                               height=20,
                               width=10,
                               font=('sans-serif',23),
                               state='readonly')
currencyAfter.place(x=100, y=325)

#Empty space to replace later on to show the final converted amount
output = tk.Label(window, text="",
               font=('sans-serif', 20, 'underline'), 
               background="#F5F0EA")
output.place(x=430, y=412)

window.mainloop()