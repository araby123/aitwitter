import base64
import io
import pandas as pd
import streamlit as st
import joblib
import altair as alt
import tweepy


consumer_key="rFUGAhVrfB6IWYRLTBLFPNuz7"
consumer_secret="3SZDYpvbCCnRYAmZn3p2pKcrE6zksKzcsv2Sb1dSVkAFWeWA0x"
access_token="887772648876498945-dC9hqXTQ4pE3BpkDEIRTbdQBvhM3myu"
access_token_secret="K13c2K1wAItqroOnE8FlguhlEdZ2hmMTqhXtSjK4L0wW1"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
pipe_lr = joblib.load(open("ٍsauditwitter_classifier_pipe_lr_16_june_2021.pkl","rb"))

def predict_emotions(docx):
	results = pipe_lr.predict([docx])
	return results[0]

def get_prediction_proba(docx):
	results = pipe_lr.predict_proba([docx])
	return results
st.title("                   Artificial Intelligence Model (NLP) ")
st.write("""### Twitter Customers Behavior Analysis in Mentions of Companies Twitter Account""")
st.write("""###                 Developed by Marwan Zamkah""")
st.write("""###             """)
st.write("""###             """)
st.video('https://www.youtube.com/watch?v=-waNOxpboZQ')
st.write("""###             """)
value = st.text_input("Enter The Twitter Account @")
st.write("""###             """)
if value:
 Search_Company =value
 screen=[]
 text = []
 pred= []
 account = []
 time=[]
#tweets = tweepy.Cursor(api.search, q=Search_Company).items(100)
 r = st.slider('Select Numbers Of Tweets shown in  your Mentions (Max 100) ', min_value=1, max_value=100)
 st.write("""###             """)
 for tweet in tweepy.Cursor(api.search, q=Search_Company,lang='ar').items(r):

    prediction =predict_emotions(tweet.text)
    screen.append("@"+tweet.user.screen_name)
    time.append(tweet.created_at)
    account.append(tweet.user.name)
    text.append(tweet.text)
    pred.append(prediction)
 emotions_emoji_dict = { "Request": "😨😱", "Appreciate": "🤗", "Joke & unrelated": "😂", "Imfo": "😐",
                        "Complain": "😔",   "Promotion": "😮"}
 df2 = pd.DataFrame({'tweet': text,'status':pred,"time":time,"user_id":account,"Twitter Account":screen})
 df2.to_excel('data.xlsx')
 g=df2['status'].value_counts()

 df = pd.read_excel("data.xlsx",index_col=None)

 st.write("""###             """)
 st.header(""" EDA """)
 #st.dataframe(df)
 st.write(emotions_emoji_dict)
 st.table(df)
 st.write("""###             """)
 st.write("""Summary""")
 st.table(g)
 st.write("""###             """)
 prediction_count = df['status'].value_counts().rename_axis('Prediction').reset_index(name='Counts')
 pc = alt.Chart(prediction_count).mark_bar().encode(x='Prediction',y='Counts',color='Prediction')
 st.altair_chart(pc,use_container_width=True)

 download2 = st.button('Download Analysis file')
 if download2:
     'Download Started!'

     g_download = pd.DataFrame(df2)

     towrite = io.BytesIO()
     downloaded_file = g_download.to_excel(towrite, encoding='utf-8', index=False, header=True)
     towrite.seek(0)
     b64 = base64.b64encode(towrite.read()).decode()
     linko = f'<a href="data:file/xls;base64,{b64}" download="download.xls">Download Excel file</a>'
     st.markdown(linko, unsafe_allow_html=True)
