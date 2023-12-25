from flask import Flask, render_template, request, session
import razorpay
import configparser
from db import MongoDB
import datetime

mydb = MongoDB("Payment", "Data")

config = configparser.ConfigParser()

# Read the configuration file
config.read('key_config.ini')

# Access values from the configuration file
api = config.get('DEFAULT', 'API_KEY')
secret = config.get('DEFAULT', 'KEY_SECRET')
client = razorpay.Client(auth=(api, secret))
print(client)

app = Flask(__name__)
app.secret_key = config.get('SESSION',"KEY")  # Set a secret key for session handling
# Render the HTML page
@app.route('/')
def index():
    return render_template('pay.html')

# Handle form submission
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    data = request.get_json(force=True)
    DATA = {
        "amount": data["amount"]+"00",
        "currency": data["currency"],
        "receipt": "receipt#1",
        "notes": {
            "name": data["name"],
            "email": data["email"]
        }
    }
    order = client.order.create(data=DATA)
    return order


@app.route("/handle_payment", methods=['POST'])
def handle_payment():
    # Receive payment data from the client
    payment_data = request.get_json(force=True)
    
    if client.utility.verify_payment_signature({
        'razorpay_order_id': payment_data['razorpay_order_id'],
        'razorpay_payment_id': payment_data['razorpay_payment_id'],
        'razorpay_signature': payment_data['razorpay_signature']
    }):
        # Insert payment details into the database
        dict = {
            "order_id": payment_data['razorpay_order_id'],
            "payment_id": payment_data['razorpay_payment_id'],
            "name": payment_data["name"],
            "email": payment_data["email"],
            "amount": int(str(payment_data["amount"])[:-2])
        }
        mydb.insert(dict)

        # Generate a receipt
        receipt_data = {
            "order_id": payment_data['razorpay_order_id'],
            "payment_id": payment_data['razorpay_payment_id'],
            "name": payment_data["name"],
            "email": payment_data["email"],
            "amount": payment_data["amount"],
            "status": "Payment successful",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # Store relevant data in session
        session['order_id'] = receipt_data['order_id']
        session['payment_id']=receipt_data["payment_id"]
        session['name'] = receipt_data['name']
        session['email'] = receipt_data['email']
        session['amount'] = str(receipt_data['amount'])[:-2]
        return receipt_data
        

    else:
        print('Payment not received')


@app.route('/show_receipt')
def show_receipt():
    # Retrieve receipt data from URL parameters
    receipt_data = {
        "order_id": session.get('order_id'),
        "payment_id":session.get("payment_id"),
        "name": session.get('name'),
        "email": session.get('email'),
        "amount": session.get('amount'),
        "status": "Payment successful",
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     }

    
    
    # Render the receipt page
    return render_template('receipt.html', receipt=receipt_data)


if __name__ == '__main__':
    app.run(debug=True)
