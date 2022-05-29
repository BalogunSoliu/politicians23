import dash
from dash import dcc
from dash import html
import pandas as pd
import matplotlib.pyplot as plt
from dash.dependencies import Input, Output, State
import plotly.express as px
import tweepy as tw

from textblob import TextBlob

app = dash.Dash()
server=app.server

musicians = pd.read_csv('musicians.csv')
musicians.drop('Unnamed: 0',axis=1,inplace=True)
musicians.rename(columns={'Sentiment':'sent_score'},inplace=True)

musicians_options = [{'label': i, 'value':i} for i in musicians.Musicians.unique()]
plots = pd.DataFrame({'Plots':['bar','Line','Scatter','Histogram','Violin Plot','Box Plot']})
plots_options = [{'label': i, 'value':i} for i in plots.Plots.unique()]

app.layout = html.Div(style={'backgroundColor': '#eee','display':'inline-block', 'width':'100%'}, children=[
    html.H1(
        'Nigerian Musicians Sentimental Analysis Dashboard Based On Tweets'
    ,style={'color':'purple','font-weight':'bold','font-family':'sansserif','text-align':'center', 'text-shadow':'2px 2px black'},
        
    ), 
    
    html.Div([
           
        dcc.Checklist(id='artist', options=musicians_options, value=['CDQ','Wizkid']),
        html.Div([
        dcc.Graph(id='graph',style={'font-weight':'bold','text-shadow':'1px 1px black','font-family':'sansserif','width':'90%',
                                   'float':'left'}),
        dcc.Dropdown(plots_options,value='Line',id='plot',style={'width':'10%','float':'left'})
        ],style={'width':'100%'})
    ],style={'background-color':'#eee','color':'black','width':'100%'})
])

@app.callback(
    Output('graph','figure'),
    Input('plot','value'),
    Input('artist','value')
    
)
def OutputGraph(selected_plot,selected_artist):
    if selected_plot == 'Line':
        graph= px.line(musicians[musicians.Musicians.isin(selected_artist)]
                  ,x='Musicians',y='sent_score',title=f'Sentiments ratings for {selected_artist}')
    elif selected_plot == 'bar':
        graph= px.bar(musicians[musicians.Musicians.isin(selected_artist)]
                  ,x='Musicians',y='sent_score',title=f'Sentiments ratings for {selected_artist}')
    elif selected_plot == 'Histogram':
        graph= px.histogram(musicians[musicians.Musicians.isin(selected_artist)]
                  ,x='Musicians',y='sent_score',title=f'Sentiments ratings for {selected_artist}')
    elif selected_plot == 'Box Plot':
        graph= px.box(musicians[musicians.Musicians.isin(selected_artist)]
                  ,x='Musicians',y='sent_score',title=f'Sentiments ratings for {selected_artist}')
    elif selected_plot == 'Violin Plot':
        graph= px.violin(musicians[musicians.Musicians.isin(selected_artist)]
                  ,x='Musicians',y='sent_score',color='Musicians',title=f'Sentiments ratings for {selected_artist}')
        
    else:
        graph= px.scatter(musicians[musicians.Musicians.isin(selected_artist)]
                  ,x='Musicians',y='sent_score',title=f'Sentiments ratings for {selected_artist}')
    return graph
    return plt.show
if __name__ == '__main__':
    app.run_server(debug=True)
