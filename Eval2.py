import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import streamlit_authenticator as stauth

nltk.download('vader_lexicon')
sent = SentimentIntensityAnalyzer()

import streamlit as st

names = ['John Doe']
usernames = ['jdoe']
passwords = ['123']

hashed_passwords = stauth.hasher(passwords).generate()

authenticator = stauth.authenticate(names,usernames,hashed_passwords,
    'some_cookie_name','some_signature_key',cookie_expiry_days=30)

name, authentication_status = authenticator.login('Login \n(Username = jdoe & Password = 123)','main')

if authentication_status:
    st.write('Welcome *%s*' % (name))
    st.title("Evaluation")

    uploaded_file = st.file_uploader("Choose a file")
    # global df
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.subheader("MAIN FILE")
        st.write(df)

        score_pos = []

        for i in range(0, df.shape[0]):
            score = sent.polarity_scores(str(df.iloc[i][2]))
            score1 = score['pos']
            score_pos.append(score1)

        df['positive'] = score_pos

        g_df = df.loc[df['positive'] > 0.6]
        r_df = g_df.loc[g_df['Star'] < 3]

        pd.set_option('max_columns', None)
        pd.set_option("max_rows", None)
    
        st.subheader("Positive reviews with negative ratings")

        st.table(r_df[['Text', 'Star']])
        
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
