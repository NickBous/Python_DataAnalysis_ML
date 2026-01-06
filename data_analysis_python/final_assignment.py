# Κάνουμε τα απαραίτητα imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Φορτώνουμε το dataset
url = 'https://storage.googleapis.com/courses_data/Assignment%20CSV/finance_liquor_sales.csv'
df = pd.read_csv(url)

#Δείχνουμε τις βασικές πληροφορίες του dataset
print(df.info())
print(df.head())

# Διαχειριζόμαστε τις στήλες με μηδενικές τιμές και τις αφαιρούμε(dropna), τροποποιώντας το ίδιο το DataFrame(inplace=True)
df.dropna(inplace=True)

# Μετατρέπουμε την στήλη ημερομηνίας σε datetime format
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Αφαιρούμε τυχόν άκυρα data entries στη συγκεριμένη στήλη
df = df.dropna(subset=['date'])

# Ένας τελικός έλεγχος
print(df.info())
print(df.head())

# Στατιστικά σύνοψης για αριθμητικά δεδομένα
print(df.describe())  

# Έλεγχος για μηδενικές τιμές
missing_values = df.isnull().sum()
print("\nMissing values:\n", missing_values)

# Φιλτράρουμε τα δεδομένα για τις χρονιές 2016-2019
filtered_df = df[(df['date'].dt.year >= 2016) & (df['date'].dt.year <= 2019)]

# Ο σκοπός μας είναι να ταυτοποιήσουμε το πιο κυρίαρχο αντικείμενο ανά zipcode
# Κάνουμε λοιπόν group by zipcode και item, προσθέτωντας τις πωλήσεις (bottles_sold)
bottles_sold = filtered_df.groupby(["zip_code", "item_number"])["bottles_sold"].sum().reset_index()
bottles_sold["zip_code"] = bottles_sold["zip_code"].astype(int)

# Βρίσκουμε το πιο δημοφιλές αντικείμενο χρησιμοποιώντας την συνάρτηση idxmax
idx = bottles_sold.groupby("zip_code")["bottles_sold"].idxmax()
max_bottles = bottles_sold.loc[idx].reset_index()

# Κάνουμε sort τις τιμές με βάση τα bottles_sold σε descending order και προβάλλουμε τις πρώτες 20
sorted_values = max_bottles.sort_values(by="bottles_sold", ascending=False).head(20)

# Υπολογίζουμε την αναλογία πωλήσεων για κάθε κατάστημα τις χρονιές 2016–2019
# Συνολικές πωλήσεις ανά κατάστημα
total_sales = sum(filtered_df["sale_dollars"])

# Συνολικές πωλήσεις ανά κατάστημα
sales = filtered_df.groupby("store_name")["sale_dollars"].sum()

# Ποσοστό Πωλήσεων ανά κατάστημα
percentage_sales = (sales * 100 / total_sales).round(2)

# Κάνουμε πάλι sort τις τιμές με βάση τα bottles_sold σε descending order και προβάλλουμε τις πρώτες 20
percentage_sorted_sales = percentage_sales.sort_values(ascending=True).tail(15)

# Κομμάτι της οπτικοποίησης με Matplotlib Pyplot:

#(1) Bar Plot: Μεγαλύτερος Αριθμός Πωλήσεων Μπουκαλιών ανά zipcode 
plt.figure(figsize=(10,6))
plt.bar(sorted_values["zip_code"].astype(str), sorted_values["bottles_sold"], color="skyblue")
plt.xlabel("Zip Code")
plt.ylabel("Bottles Sold")
plt.title("Max bottles sold per zip code")
plt.xticks(rotation=45)
plt.show()

# (2) Bar Plot: Ποσοστό Πωλήσεων ανά κατάστημα
p = plt.barh(percentage_sorted_sales.index, percentage_sorted_sales.values, height=0.7)
plt.title("Percentage of Sales by store")
plt.xlabel("Percentage of Sales", fontsize=12)
plt.bar_label(p, fmt="%.2f")
plt.xlim([0,20])
plt.show()

# Κομμάτι της οπτικοποίησης με Seaborn:

# (1) Scatter Plot: Μεγαλύτερος Αριθμός Πωλήσεων Μπουκαλιών ανά zipcode 
plt.figure(figsize=(12, 6))
sns.scatterplot(data=max_bottles, x="zip_code", y="bottles_sold", size="bottles_sold", hue="bottles_sold", palette="viridis", sizes=(20, 200))
plt.title("Most Popular Item by Zipcode (2016–2019)")
plt.xlabel("Zipcode")
plt.ylabel("Bottles Sold")
plt.legend(title="Bottles Sold", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.show()


# (2) Scatter Plot: Ποσοστό Πωλήσεων Ανά Κατάστημα 
plt.figure(figsize=(12, 6))
sns.scatterplot(x=percentage_sales.index, y=percentage_sales.values, size=percentage_sales.values, hue=percentage_sales.values, palette="coolwarm", sizes=(20, 200))
plt.title("Percentage of Sales by Store (2016–2019)")
plt.xlabel("Store Name")
plt.ylabel("Percentage of Sales (%)")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Percentage of Sales", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.show()







