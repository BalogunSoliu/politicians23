import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import tweepy as tw
from textblob import TextBlob
import time

politicians = pd.read_csv('Politicians.csv')
politicians.drop('Unnamed: 0', axis=1, inplace=True)

#Twitter API credentials
API_Key='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
API_Secret_Key='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
Bearer_Token='AAAAAAAAAAAAAAAAAAAAADmyOgEAAAAAjbx0fOB3LfbKc0Ek3lHUeoEn1EE%3DD5tyg35YAEG97yYd8T2idrWaTAEXMdc5WDU4OE10Abg2M3tRYp'

Access_token='1700242764-qyTxjf3v4lexNdTSifGBgikeD4WU94VUxmgGgbx'
Access_token_secret='BvOX8keF7Nv9NHpc4a9lJArZ7ARWQQdBrcPNRzkcqREea'

#Authentication for api
auth=tw.OAuthHandler(API_Key,API_Secret_Key)
auth.set_access_token(Access_token, Access_token_secret)
api=tw.API(auth,wait_on_rate_limit=True)
politicians_options = [{'label': i, 'value': i} for i in politicians.Politicians.unique()]
plots = pd.DataFrame({'Plots': ['bar', 'Line', 'Scatter', 'Histogram', 'Violin Plot', 'Box Plot']})
plots_options = [{'label': i, 'value': i} for i in plots.Plots.unique()]

sentence = 'This product i ordered is fairly okay'
TextBlob(sentence).sentiment.polarity


def getSentiment(name, samples):
    # define the search tag
    searchtag = name

    Tweets = tw.Cursor(api.search_tweets, q=searchtag,
                       lang='en').items(samples)

    # extract the tweet
    sentiments = []
    for tweet in Tweets:
        # extracting the text from the tweets
        t = tweet.text.encode('utf-8')
        # print(t)

        sentence = t.decode('utf8')

        sentiment = TextBlob(sentence).sentiment.polarity

        sentiments.append(sentiment)
    if len(sentiments) != 0:
        return sum(sentiments) / len(sentiments)

politicians_options = [{'label': i, 'value':i} for i in politicians.Politicians.unique()]
plots = pd.DataFrame({'Plots':['Line','Pie','Scatter','Histogram']})
plots_options = [{'label': i, 'value':i} for i in plots.Plots.unique()]

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div(style={'backgroundColor': '#eee', 'display': 'inline-block', 'width': '100%'}, children=[
    html.H1(
        'Nigerian Politicians Sentimental Analysis Dashboard Based On Tweets'
        , style={'color': 'purple', 'font-weight': 'bold', 'font-family': 'sansserif', 'text-align': 'center',
                 'text-shadow': '2px 2px black'},

    ),

    html.Div([
html.Div([
        dcc.Input(id='search',value='Bola Tinubu'),
        html.Button(id='submit',n_clicks=0,children='Add Politician'),
        dcc.Loading(id='load',children=[html.Div(id='loading-output')],type='default'),
        ],style={'margin-bottom':'2em'}),
        dcc.Checklist(id='politician'),
        html.Div([
            dcc.Graph(id='graph',
                      style={'font-weight': 'bold', 'text-shadow': '1px 1px black', 'font-family': 'sansserif',
                             'width': '90%',
                             'float': 'left'}),
            dcc.Dropdown(plots_options, value='Line', id='plot', style={'width': '10%', 'float': 'left'})
        ], style={'width': '100%'})
    ], style={'background-color': '#eee', 'color': 'black', 'width': '100%'})
])


@app.callback(

    Output('politician', 'options'),
    Output('politician', 'value'),
    Output('loading-output', 'children'),
    Input('submit', 'n_clicks'),
    State('search', 'value')

)
def add_politician(dd_politician, new_politician):
    if new_politician:
        ss = getSentiment(new_politician, 100)
        newArt = {'Politicians': new_politician, 'sent_score': ss}
        global politicians
        politicians = politicians.append(newArt, ignore_index=True, verify_integrity=True)
        politicians_options = politicians.Politicians.unique()
    time.sleep(2)
    return politicians_options, politicians_options[16:19], new_politician


@app.callback(
    Output('graph', 'figure'),
    Input('plot', 'value'),
    Input('politician', 'value')

)
def OutputGraph(selected_plot, selected_politician):
    if selected_plot == 'Line':
        graph = px.line(politicians[politicians.Politicians.isin(selected_politician)]
                        , x='Politicians', y='sent_score')
    elif selected_plot == 'Histogram':
        graph = px.histogram(politicians[politicians.Politicians.isin(selected_politician)]
                             , x='Politicians', y='sent_score')
    elif selected_plot == 'Pie':
        graph = px.pie(politicians[politicians.Politicians.isin(selected_politician)]
                       , values='sent_score', names='Politicians', title='Politicians Sentimental Scores',
                       color='Politicians')

    else:
        graph = px.scatter(politicians[politicians.Politicians.isin(selected_politician)]
                           , x='Politicians', y='sent_score')
    return graph
    return plt.show


if __name__ == '__main__':
    app.run_server(debug=True)
