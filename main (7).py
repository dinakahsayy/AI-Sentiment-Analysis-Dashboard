import streamlit as st
from textblob import TextBlob
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Setting page title and layout
st.set_page_config(page_title="AI Sentiment Analysis Dashboard", layout="wide")

# Adding header
st.title("🤖 AI Sentiment Analysis Dashboard")
st.markdown("---")

# Creating two columns for different input methods
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Analyze Single Text")
    user_input = st.text_area("Enter text to analyze:")

    if st.button("Analyze Text"):
        if user_input:
            # Getting sentiment
            sentiment = TextBlob(user_input).sentiment

            # Creating a bar chart for polarity
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = sentiment.polarity,
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [-1, 1]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [-1, -0.3], 'color': "red"},
                        {'range': [-0.3, 0.3], 'color': "yellow"},
                        {'range': [0.3, 1], 'color': "green"}
                    ]
                }
            ))

            # Showing results
            st.plotly_chart(fig)

            # Showing interpretation
            if sentiment.polarity > 0:
                st.success(f"Positive Sentiment (Score: {sentiment.polarity:.2f}) 😊")
            elif sentiment.polarity < 0:
                st.error(f"Negative Sentiment (Score: {sentiment.polarity:.2f}) 😞")
            else:
                st.warning(f"Neutral Sentiment (Score: {sentiment.polarity:.2f}) 😐")

with col2:
    st.subheader("📊 Analyze CSV File")
    uploaded_file = st.file_uploader("Upload CSV file with a 'text' column", type=['csv'])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if 'text' in df.columns:
            # Analyzing each text in the file
            df['polarity'] = df['text'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
            df['sentiment'] = df['polarity'].apply(lambda x: 
                'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))

            # Creating pie chart
            fig_pie = px.pie(df, names='sentiment', title='Sentiment Distribution')
            st.plotly_chart(fig_pie)

            # Showing average sentiment
            avg_sentiment = df['polarity'].mean()
            st.metric("Average Sentiment Score", f"{avg_sentiment:.2f}")

            # Showing the analyzed data
            st.dataframe(df[['text', 'sentiment', 'polarity']])
        else:
            st.error("CSV file must contain a 'text' column")

# Adding footer
st.markdown("---")
st.markdown("Built in like 2 days pray i get an A lol")