import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


df = pd.read_csv("data/df_eda.csv")

cat_cols = df.select_dtypes('object').columns.tolist()
tier_cols = ['Progress Tier', 'Achievement Tier', 'Climate Tier']

colors = {
    'text': '#3f5378',
    'retention': '#B0C4DE',
    'turnover':'#FFA500'
}
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets) 

markdown_text = '''
For more information and to see how these features were used in 
binary classification models to predict teacher turnover, 
please visit this [github repository](https://github.com/mross715/Predicting_Teacher_Turnover).'''


app.layout = html.Div(children=[
    html.H1(children='Exploring Teacher Turnover',
            style={
            'textAlign': 'center',
            'color': colors['text'], 
            'marginTop':40,
            'marginBottom':40, 
            'font-family': "Gill Sans",
            'font-weight': 'bold'
        }
    ),

html.Div(children= ''' 
The School District of Philadelphia has teacher turnover rates above the national average. Research on teacher turnover has shown that occupational 
factors and student demographic factors influence turnover. The dataset used for these visualizations results from merging occupational 
factors with student demographic factors and contains approximately 8,000 records representing public school teachers in the School District 
of Philadelphia from the 2017-2018 school year.  Those teachers were identified as either returning to their current placement or 
having turned over using employee information from the following school year.'''
,
             style={'textAlign': 'center',
             'font-family': "Gill Sans",
             'fontSize': 18,
             'marginLeft': 50, 
             'marginRight': 50,
             'color': colors['text']
    }),
        html.Br(),
html.Div([
    dcc.Markdown(children=markdown_text)],
             style={'textAlign': 'center',
             'font-family': "Gill Sans",
             'fontSize': 18,
             'marginLeft': 50, 
             'marginRight': 50,
             'color': colors['text']
    }),
        html.Br(),
html.Div(children= '''
Select a feature below to show the overall distribution of the feature in the entire dataset as well as the relationship 
the variable has with teacher turnover.'''
,
             style={'textAlign': 'center',
             'font-family': "Gill Sans",
             'fontSize': 18,
             'marginLeft': 50, 
             'marginRight': 50,
             'font-weight': 'bold',
             'color': colors['text']
    }),
        html.Br(),
        dcc.Dropdown( id = 'dropdown',
        options = [
            {'label': 'Teacher Gender', 'value':'Gender' },
            {'label': 'Teaching Experience', 'value':'Teaching Experience'},
            {'label': 'Teacher Title Description', 'value':'Title Description'},
            {'label': 'Teacher Salary', 'value':'Salary'},
            {'label': 'Climate Tier', 'value':'Climate Tier'},
            {'label': 'Achievement Tier', 'value':'Achievement Tier'},
            {'label': 'Progress Tier', 'value':'Progress Tier'},
            {'label': 'School Level', 'value':'School Level'},
            {'label': 'Enrollment', 'value':'Enrollment'},
            {'label': 'Admissions Type', 'value':'Admissions Type'},
            {'label': 'Turnaround Model', 'value':'Turnaround Model'},
            {'label': 'Percentage of English Language Learners', 'value':'Percent ELL'},
            {'label': 'Percentage of Special Education Students', 'value':'Percent IEP'},
            {'label': 'Percentage of Black/African American Students', 'value':'Percent Black/African American'},
            {'label': 'Percantage of White Students', 'value':'Percent White'},
            {'label': 'Percantage of Economically Disadvantaged Students', 'value':'Economically Disadvantaged Rate'},
            ],
        value = 'Gender',
        clearable=False,
        style=dict(
                    width='50%',
                    horizontalAlign="center"
                )),
   
        html.Div([
            html.H3(''),
            dcc.Graph(id = 'graph_a')
        ], className="five columns"),

        html.Div([
            html.H3(''),
            dcc.Graph(id='graph_b')
        ], className="five columns"),
    ], className="row")



@app.callback(Output(component_id='graph_a', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value')])

def graph_update(dropdown_value):
    print(dropdown_value)
    if dropdown_value in cat_cols:
        fig_a = go.Figure()
        fig_a.add_trace(go.Histogram(x=df['{}'.format(dropdown_value)], histnorm='probability', opacity=0.8, marker_color= '#3f5378'))
        fig_a.update_layout(title = 'Overall Distribution of {}'.format(dropdown_value),template="plotly_white",
                      xaxis_title = '{}'.format(dropdown_value),
                      yaxis_title = 'Proportion'
                      )
        if dropdown_value in tier_cols:
            fig_a.update_layout(xaxis={'categoryorder':'array', 'categoryarray':['Insufficient Data','INTERVENE','WATCH','REINFORCE','MODEL']})
            return fig_a
        else:
            return fig_a
    else:
        fig1 = go.Figure()
        fig1.add_trace(go.Histogram(x=df['{}'.format(dropdown_value)], histfunc='count', nbinsx=10, opacity=0.8, marker_color= '#3f5378'))
        fig1.update_layout(title = 'Overall Distribution of {}'.format(dropdown_value),template="plotly_white",
                            xaxis_title = '{}'.format(dropdown_value)
                      )
        return fig1

@app.callback(Output(component_id='graph_b', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value')])
def graph_update(dropdown_value):
    print(dropdown_value)
    if dropdown_value in cat_cols:
        pv = pd.pivot_table(df, values="HOME_ORGANIZATION", index='{}'.format(dropdown_value), columns="TURNOVER", aggfunc='count')
        pv = pv.T.div(pv.T.sum()).T
        trace1 = go.Bar(x=pv.index, y=pv[0.0], name='Retention', marker_color= colors['retention'])
        trace2 = go.Bar(x=pv.index, y=pv[1.0], name='Turnover', marker_color= colors['turnover'])
        fig_b = go.Figure([trace1, trace2])
        fig_b.update_layout(title = '{} vs. Teacher Turnover'.format(dropdown_value),barmode='stack',template="plotly_white",
                      xaxis_title = '{}'.format(dropdown_value),
                      yaxis_title = 'Proportion'
                      )
        if dropdown_value in tier_cols:
            fig_b.update_layout(xaxis={'categoryorder':'array', 'categoryarray':['Insufficient Data','INTERVENE','WATCH','REINFORCE','MODEL']})
            return fig_b
        else:
            return fig_b
    else:
        x0 = df['{}'.format(dropdown_value)].loc[df['Status']=='Retention']
        x1 = df['{}'.format(dropdown_value)].loc[df['Status']=='Turnover']
        fig2 = go.Figure()
        fig2.add_trace(go.Box( x=x0, orientation ='h', name = 'Retention', marker_color =colors['retention']))
        fig2.add_trace(go.Box( x=x1, orientation ='h', name = 'Turnover', marker_color =colors['turnover']))
        fig2.update_layout(title = '{} vs. Teacher Turnover'.format(dropdown_value),template="plotly_white",
                            xaxis_title = '{}'.format(dropdown_value)
                      )
        return fig2

if __name__ == "__main__":
    app.run_server(debug=True)