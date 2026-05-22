from flask import Flask, request
import boto3
import uuid
import re
import json
import requests

app = Flask(__name__)

# =========================
# AWS
# =========================
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('Orders')

sns = boto3.client('sns', region_name='ap-south-1')

# =========================
# TOPICS (STANDARD)
# =========================
INTERNAL_TOPIC_ARN = "arn:aws:sns:ap-south-1:859384798216:OPC"
CUSTOMER_TOPIC_ARN = "arn:aws:sns:ap-south-1:859384798216:Customers_"


# =========================
# SNS CONFIRMATION HANDLER
# =========================
def confirm_subscription(data):
    if data.get("Type") == "SubscriptionConfirmation":
        url = data.get("SubscribeURL")
        requests.get(url)
        print("✅ SNS Subscription Confirmed")


# =========================
# HOME
# =========================
@app.route('/')
def home():
    return '''
    <h2>🍔 Food Order System</h2>

    <form action="/order" method="post">
        Customer ID: <input name="customer_id" required><br>
        Phone (+91XXXXXXXXXX): <input name="phone" required><br>
        Food: <input name="order_name" required><br>
        <button type="submit">Place Order</button>
    </form>

    <br>

    <form action="/track" method="post">
        Order ID: <input name="order_id" required><br>
        <button type="submit">Track</button>
    </form>

    <br>
    <a href="/restaurant">Restaurant</a><br>
    <a href="/delivery">Delivery</a>
    '''


# =========================
# ORDER CREATE
# =========================
@app.route('/order', methods=['POST'])
def order():
    customer_id = request.form['customer_id']
    phone = request.form['phone']
    order_name = request.form['order_name']

    if not re.match(r'^\+91\d{10}$', phone):
        return "❌ Invalid phone format"

    order_id = str(uuid.uuid4())

    table.put_item(Item={
        "order_id": order_id,
        "customer_id": customer_id,
        "phone": phone,
        "order_name": order_name,
        "status": "PLACED",
        "history": ["PLACED"]
    })

    # 🔵 INTERNAL PIPELINE (STANDARD → no FIFO params)
    try:
        sns.publish(
            TopicArn=INTERNAL_TOPIC_ARN,
            Message=f"PLACED|RESTAURANT|{order_id}"
        )
    except Exception as e:
        print("SNS INTERNAL ERROR:", e)

    # 🟢 CUSTOMER NOTIFICATION
    try:
        sns.publish(
            TopicArn=CUSTOMER_TOPIC_ARN,
            Message=f"🍔 Order placed: {order_id}"
        )
    except Exception as e:
        print("SNS CUSTOMER ERROR:", e)

    return f"✅ Order Created: {order_id}"


# =========================
# TRACK
# =========================
@app.route('/track', methods=['POST'])
def track():
    order_id = request.form['order_id']

    item = table.get_item(Key={'order_id': order_id}).get('Item')

    if not item:
        return "❌ Order not found"

    status = item.get("status", "UNKNOWN")
    history = item.get("history", [])

    # remove duplicates while keeping order
    clean_history = []
    for h in history:
        if len(clean_history) == 0 or clean_history[-1] != h:
            clean_history.append(h)

    history_text = " → ".join(clean_history)

    return f"""
    📦 ORDER TRACKING

    Status: {status}
    Timeline: {history_text}
    """


# =========================
# RESTAURANT UI
# =========================
@app.route('/restaurant')
def restaurant():
    return '''
    <h2>👨‍🍳 Restaurant</h2>
    <form action="/update" method="post">
        Order ID: <input name="order_id"><br>
        <button name="status" value="READY">Mark READY</button>
    </form>
    '''


# =========================
# DELIVERY UI
# =========================
@app.route('/delivery')
def delivery():
    return '''
    <h2>🚚 Delivery</h2>
    <form action="/update" method="post">
        Order ID: <input name="order_id"><br>
        <button name="status" value="DELIVERED">Mark DELIVERED</button>
    </form>
    '''


# =========================
# UPDATE FLOW
# =========================
@app.route('/update', methods=['POST'])
def update():
    order_id = request.form['order_id']
    status = request.form['status']

    item = table.get_item(Key={'order_id': order_id}).get('Item')

    if not item:
        return "❌ Order not found"

    table.update_item(
        Key={'order_id': order_id},
        UpdateExpression="SET #s = :s, history = list_append(history, :h)",
        ExpressionAttributeNames={'#s': 'status'},
        ExpressionAttributeValues={
            ':s': status,
            ':h': [status]
        }
    )

    # 🔵 INTERNAL PIPELINE
    try:
        sns.publish(
            TopicArn=INTERNAL_TOPIC_ARN,
            Message=f"{status}|{order_id}"
        )
    except Exception as e:
        print("SNS INTERNAL ERROR:", e)

    # 🟢 CUSTOMER UPDATE
    try:
        sns.publish(
            TopicArn=CUSTOMER_TOPIC_ARN,
            Message=f"📦 Update: {status} | {order_id}"
        )
    except Exception as e:
        print("SNS CUSTOMER ERROR:", e)

    return f"✅ Updated → {status}"


# =========================
# SNS ENDPOINTS
# =========================
@app.route('/restaurant_notify', methods=['POST'])
def restaurant_notify():
    data = json.loads(request.data.decode())

    confirm_subscription(data)

    print("🍽 RESTAURANT EVENT:", data)

    return "OK", 200


@app.route('/delivery_notify', methods=['POST'])
def delivery_notify():
    data = json.loads(request.data.decode())

    confirm_subscription(data)

    print("🚚 DELIVERY EVENT:", data)

    return "OK", 200


# =========================
# RUN
# =========================
if __name__ == '__main__':
    app.run(debug=True)