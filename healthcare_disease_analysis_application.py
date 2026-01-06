# Kάνουμε τα απαραίτητα imports
import streamlit as st
from openai import OpenAI
import json
import pandas as pd
import io
import base64

# Τοποθέτηση του OpenAI API key από τα μυστικά του Streamlit
client = OpenAI(api_key=st.secrets["OPEN_API_KEY"])

# Συνάρτηση για λήψη πληροφοριών σχετικά με μια ασθένεια μέσω του OpenAI
def get_disease_info(disease_name):
    # Μορφή JSON για τα φάρμακα
    medication_format = '''"name":"" 
    "side_effects":[ 
    0:"" 
    1:"" 
    ... 
    ] 
    "dosage":""'''
    
    # Κλήση στο OpenAI API με αίτημα δομημένης πληροφορίας για την ασθένεια
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Please provide information on the following aspects for {disease_name}: 1. Key Statistics, 2. Recovery Options, 3. Recommended Medications. Format the response in JSON with keys for 'name', 'statistics', 'total_cases' (this always has to be a number), 'recovery_rate' (this always has to be a percentage), 'mortality_rate' (this always has to be a percentage) 'recovery_options', (explain each recovery option in detail), and 'medication', (give some side effect examples and dosages) always use this json format for medication : {medication_format}."}
        ]
    )
    # Επιστροφή του περιεχομένου της απάντησης
    return response.choices[0].message.content

# Συνάρτηση για την εμφάνιση των πληροφοριών της ασθένειας με χρήση Streamlit
def display_disease_info(disease_info):
    try:
        # Ανάγνωση της απάντησης σε μορφή JSON
        info = json.loads(disease_info)

        # Μετατροπή των ποσοστών σε αριθμητική μορφή
        recovery_rate = float(info['statistics']["recovery_rate"].strip('%'))
        mortality_rate = float(info['statistics']["mortality_rate"].strip('%'))

        # Δημιουργία πίνακα για τα γραφήματα
        chart_data = pd.DataFrame(
            {
                "Recovery Rate": [recovery_rate],
                "Mortality Rate": [mortality_rate],
            },
            index = ["Rate"]  # Μοναδικό index για το γράφημα
        )

        # Εμφάνιση τίτλου και στατιστικών
        st.write(f"## Στατιστικά για την ασθένεια: {info['name']}")
        st.bar_chart(chart_data)

        # Εμφάνιση των επιλογών ανάρρωσης
        st.write("## Επιλογές Ανάρρωσης")
        recovery_options = info['recovery_options']
        for option, description in recovery_options.items():
            st.subheader(option)
            st.write(description)

        # Εμφάνιση φαρμακευτικής αγωγής
        st.write("## Φαρμακευτική Αγωγή")
        medication = info['medication']
        medication_count = 1
        for option, description in medication.items():
            st.subheader(f"{medication_count}. {option}")
            st.write(description)
            medication_count += 1
    except json.JSONDecodeError:
        # Εμφάνιση μηνύματος λάθους σε περίπτωση αποτυχίας ανάλυσης JSON
        st.error("Αποτυχία στην ανάλυση του JSON. Ελέγξτε τη μορφή της απάντησης από το OpenAI.")

# Τίτλος της εφαρμογής
st.title("Πίνακας Πληροφοριών Ασθενειών")

# Πεδίο εισαγωγής του ονόματος της ασθένειας από τον χρήστη
disease_name = st.text_input("Πληκτρολογήστε το όνομα της ασθένειας:")

# Αν έχει δοθεί όνομα, λήψη και εμφάνιση πληροφοριών
if disease_name:
    disease_info = get_disease_info(disease_name)
    display_disease_info(disease_info)

# Δημιουργία session state για ιστορικό αναζητήσεων ασθενειών
if "search_history" not in st.session_state:
    st.session_state.search_history = []

# Ενημέρωση ιστορικού με την τρέχουσα αναζήτηση
if disease_name and disease_name not in st.session_state.search_history:
    st.session_state.search_history.append(disease_name)

# Προβολή ιστορικού
if st.session_state.search_history:
    st.write("Πρόσφατες Αναζητήσεις:")
    for item in reversed(st.session_state.search_history[-5:]):
        if st.button(f"{item}"):
            disease_name = item

# Συνάρτηση σύγκρισης ασθενειών
def compare_diseases(disease_get_info):
    # Προβολή τίτλου για τη σύγκριση
    st.write("Σύγκριση Ασθενειών")

    # Επιλογή πολλαπλών ασθενειών από το ιστορικό
    comparison_selection = st.multiselect(
        "Επέλεξε ασθένειες για σύγκριση:",
        options=st.session_state.get("search_history", [])
    )

    # Προετοιμασία δομής δεδομένων για το γράφημα
    comparison_data = {
        "Ασθένεια": [],
        "Ανάρρωση %": [],
        "Θνησιμότητα %": []
    }

    # Ανάκτηση και προσθήκη δεδομένων για κάθε ασθένεια
    for disease in comparison_selection:
        try:
            info = json.loads(disease_get_info(disease))
            comparison_data["Ασθένεια"].append(info["name"])
            comparison_data["Ανάρρωση %"].append(float(info["statistics"]["recovery_rate"].strip('%')))
            comparison_data["Θνησιμότητα %"].append(float(info["statistics"]["mortality_rate"].strip('%')))
        except Exception as e:
            st.warning(f"Δεν ήταν δυνατή η ανάκτηση στοιχείων για: {disease}")

    # Αν υπάρχουν δεδομένα, εμφάνιση γραφήματος
    if comparison_data["Ασθένεια"]:
        df_compare = pd.DataFrame(comparison_data).set_index("Ασθένεια")
        st.bar_chart(df_compare)

# Συνάρτηση για εξαγωγή σε CSV
def download_csv(info):
    df = pd.DataFrame({
        "Όνομα Ασθένειας": [info["name"]],
        "Περιστατικά": [info["statistics"]["total_cases"]],
        "Ποσοστό Ανάρρωσης": [info["statistics"]["recovery_rate"]],
        "Θνησιμότητα": [info["statistics"]["mortality_rate"]],
    })
    return df.to_csv(index=False).encode('utf-8')

# Κουμπί για λήψη CSV
csv = download_csv(info)
st.download_button(
    label="📄 Λήψη CSV",
    data=csv,
    file_name=f'{info["name"]}_info.csv',
    mime='text/csv',
)
