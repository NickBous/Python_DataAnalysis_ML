# Κάνουμε τα απαράιτητα imports
import streamlit as st
from openai import OpenAI
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import timedelta

# Αντικαταθιστούμε το "your_api_key_here" με το πραγματικό μας OpenAI API key (αποκρύπτεται για λόγους ιδιωτικότητας)
client = OpenAI(api_key="your_api_key_here")

# Τίτλος της εφαρμογής
st.title('Διαδραστικό Εργαλείο Συγκριτικής Ανάλυσης Χρηματιστηριακών Αγορών')

# Συνάρτηση για να φέρει δεδομένα χρηματιστηρίου ανάμεσα σε δύο δοσμένες ημερομηνίες
def get_stock_data(ticker, start_date='2024-01-01', end_date='2024-02-01'):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Παράθυρο για τις εισροές του χρήστη
st.sidebar.header('Επιλογές Εισροών Χρήστη')
selected_stock = st.sidebar.text_input('Εισάγετε Τicker Χρηματιστηρίου 1', 'AAPL').upper()
selected_stock2 = st.sidebar.text_input('Εισάγετε Τicker Χρηματιστηρίου 2', 'GOOGL').upper()

# Επιλογή ημερομηνιών από τον χρήστη
start_date = st.sidebar.date_input('Ημερομηνία Έναρξης', pd.to_datetime('2024-01-01'))
end_date = st.sidebar.date_input('Ημερομηνία Λήξης', pd.to_datetime('2024-02-01'))

# Φέρνουμε τα δεδομένα χρηματιστηρίου
stock_data = get_stock_data(selected_stock, start_date=start_date, end_date=end_date)
stock_data2 = get_stock_data(selected_stock2, start_date=start_date, end_date=end_date)

# Στήλες για την εμφάνιση δεδομένων
col1, col2 = st.columns(2)

# Εμφάνιση δεδομένων για το πρώτο stock
with col1:
    st.subheader(f"Εμφάνιση δεδομένων για: {selected_stock}")
    st.write(stock_data)
    chart_type = st.sidebar.selectbox(f'Επιλέξτε Τύπο Γραφήματος για {selected_stock}', ['Linear', 'Bar'])
    if chart_type == 'Linear':
        st.line_chart(stock_data['Close'])
    elif chart_type == 'Bar':
        st.bar_chart(stock_data['Close'])

# Εμφάνιση δεδομένων για το δεύτερο stock
with col2:
    st.subheader(f"Εμφάνιση δεδομένων για: {selected_stock2}")
    st.write(stock_data2)
    chart_type2 = st.sidebar.selectbox(f'Επιλέξτε Τύπο Γραφήματος για {selected_stock2}', ['Linear', 'Bar'])
    if chart_type2 == 'Linear':
        st.line_chart(stock_data2['Close'])
    elif chart_type2 == 'Bar':
        st.bar_chart(stock_data2['Close'])

# Εμφάνιση χρηματοοικονομικών μετρικών
def financial_metrics(data):
    # Υπολογισμός χρηματοοικονομικών μετρικών (μέση τιμή,τυπική απόκλιση, μέγιστη-ελάχιστη τιμή)
    mean_price = data['Close'].mean()
    volatility = data['Close'].std()
    max_price = data['Close'].max()
    min_price = data['Close'].min()
    
    return mean_price, volatility, max_price, min_price

# Παρουσίαση μετρικών για τα δύο stocks
mean_stock1, volatility_stock1, max_stock1, min_stock1 = financial_metrics(stock_data)
mean_stock2, volatility_stock2, max_stock2, min_stock2 = financial_metrics(stock_data2)

st.subheader(f"Χρηματοοικονομικά Μετρικά για {selected_stock}")
st.write(f"Μέση Τιμή: {mean_stock1:.2f}")
st.write(f"Τυπική Απόκλιση: {volatility_stock1:.2f}")
st.write(f"Μέγιστη Τιμή: {max_stock1:.2f}")
st.write(f"Ελάχιστη Τιμή: {min_stock1:.2f}")

st.subheader(f"Χρηματοοικονομικά Μετρικά για {selected_stock2}")
st.write(f"Μέση Τιμή: {mean_stock2:.2f}")
st.write(f"Τυπική Απόκλιση: {volatility_stock2:.2f}")
st.write(f"Μέγιστη Τιμή: {max_stock2:.2f}")
st.write(f"Ελάχιστη Τιμή: {min_stock2:.2f}")

# Κουμπί για συγκριτική ανάλυση
if st.button('Συγκριτική Απόδοση'):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Είσαι ένας χρηματοοικονομικός βοηθός που θα αναλύσει δύο σύνολα δεδομένων χρηματιστηριακής αγοράς και θα συνοψίσει την συγκριτική απόδοση σε πλήρη λεπτομέρεια με τα βασικά σημεία για κάθε μετοχή και με ένα συμπέρασμα."},
            {"role": "user", "content": f"Αυτά είναι τα δεδομένα για τη μετοχή {selected_stock}: {stock_data.to_string()}, και αυτά για τη μετοχή {selected_stock2}: {stock_data2.to_string()}"}
        ]
    )
    st.write(response['choices'][0]['message']['content'])

# Υπολογισμός ποσοστιαίας απόδοσης των stocks και δημιουργία DataFrame και Line Chart
stock_perf = (stock_data['Close'] / stock_data['Close'].iloc[0]) * 100
stock_perf2 = (stock_data2['Close'] / stock_data2['Close'].iloc[0]) * 100

st.subheader("📈 Συγκριτική Απόδοση (%)")
perf_df = pd.DataFrame({
    f'{selected_stock} (%)': stock_perf,
    f'{selected_stock2} (%)': stock_perf2
})
st.line_chart(perf_df)

# Συνάρτηση πρόβλεψης τιμής με μοντέλο Γραμμικής Παλινδρόμησης 

def predict_stock_prices(data, days=5):
    data = data.reset_index()
    data['Date_Ordinal'] = pd.to_datetime(data['Date']).map(pd.Timestamp.toordinal)
    
    X = data[['Date_Ordinal']]
    y = data['Close']
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Δημιουργία μελλοντικών ημερομηνιών
    last_date = data['Date'].iloc[-1]
    future_dates = [last_date + timedelta(days=i) for i in range(1, days+1)]
    future_ordinals = np.array([pd.Timestamp(d).toordinal() for d in future_dates]).reshape(-1, 1)
    
    predictions = model.predict(future_ordinals)
    
    future_df = pd.DataFrame({'Ημερομηνία': future_dates, 'Προβλεπόμενη Τιμή': predictions})
    return future_df

# Πρόβλεψη μελλοντικών τιμών των δύο μετοχών για τις επόμενες 5 μέρες

st.subheader(f"🔮 Πρόβλεψη Τιμής για τις επόμενες 5 ημέρες: {selected_stock}")
forecast1 = predict_stock_prices(stock_data)
st.write(forecast1)

st.subheader(f"🔮 Πρόβλεψη Τιμής για τις επόμενες 5 ημέρες: {selected_stock2}")
forecast2 = predict_stock_prices(stock_data2)
st.write(forecast2)
