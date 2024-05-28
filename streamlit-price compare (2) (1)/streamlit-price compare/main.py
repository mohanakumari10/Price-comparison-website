import amazon_scrapper
import flipkart_scrapper
import pandas as pd
import streamlit as st
import review
# import review_sentiment_analyzer as rsa
import time
import plotly
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="price comparison")


def run(name):
    search_query = name.replace(' ', '+')
    base_url = 'https://www.amazon.com/s?k={0}'.format(search_query)
    items = amazon_scrapper.amazon(base_url)
    # amazon scrapping
    amazon_scrapper.amozon_csv(items, name)
    # flipkart scrapping
    flipkart_scrapper.flipkart(name)


st.title('Price comparison website')
st.markdown('#### Created by  ** MOHANA **')

name = st.text_input(
    'Product Name', placeholder='Enter the product name:')


if name:
    g = st.empty()
    my_bar = st.progress(0)
    run(name)
    ama = pd.read_csv('csv_files/{0}_amazon.csv'.format(name))
    ########################################################
    # ama = pd.read_csv('csv_files/name_amazon.csv')
    ########################################################
    flip = pd.read_csv('csv_files/{0}_flipkart.csv'.format(name))
    ama_sort = ama.sort_values('price')
    flip_sort = flip.sort_values('Price')

    for percent_complete in range(100):
        g.text('processing...')
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1)

    # st.write(ama)
    # st.write(flip)
    # st.write(ama_sort)
    g.text('')
    # my_bar.progress(0)
    x = ama_sort.head(1)
    y = flip_sort.head(1)
    # li = x._get_value(0, 'product url')
    li = ama_sort._get_value(1, 3, takeable=True)
    review.review_scrapper(li, name)
    amaze_review = pd.read_csv('review_csv/{0}_amazon.csv'.format(name))
    # st.write(ama_sort)
    # st.write(flip_sort)
    # st.write(amaze_review)
    # tot_num, pos_num, neg_num, neu_num = rsa.review_analyzer(name)
    amo = ama_sort._get_value(1, 2, takeable=True)
    flipo = flip_sort._get_value(1, 1, takeable=True)
    # st.write(tot_num, pos_num, neg_num, neu_num)
    if amo > flipo:
        emo = flipo
    else:
        emo = amo
    fis = int(amo-flipo)

    # if pos_num > neg_num:
    #     ama_pos = pos_num
    # else:
    #     ama_pos = '-{0}'.format(neg_num)
    # col1, col2, col3 = st.columns(3)
    # col1.metric("Amazon", amo, ama_pos)
    # col2.metric("Flipkart", flipo, "-100")
    # col3.metric("Lowest product", emo, fis)
    fig = px.bar(ama_sort, x='price', y='rating',
                 hover_data=['price', 'rating'], color='price',
                 labels={'rating': 'no. of rating'}, height=400)
    st.plotly_chart(fig, use_container_width=True)
    # labels = ['Total reviews', 'positive reviews',
    #           'Negative reviews', 'Neutral reviews']
    # values = [tot_num, pos_num, neg_num, neu_num]
    # fig1 = go.Figure(
    #     data=[go.Pie(labels=labels, values=values, pull=[0.1, 0.1, 0.2, 0.1])])
    # st.plotly_chart(fig1, use_container_width=True)

    st.write(ama_sort)
    st.write(flip_sort)
