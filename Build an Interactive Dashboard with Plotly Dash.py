from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# 1. تحميل البيانات
# تأكد أن ملف البيانات موجود في نفس المجلد
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# 2. إعداد التطبيق
app = Dash(__name__)

# 3. واجهة المستخدم (Layout)
app.layout = html.Div(children=[
    html.H1("SpaceX Launch Records Dashboard", style={'textAlign': 'center'}),
    
    # القائمة المنسدلة
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),
    
    # الرسم البياني الدائري
    dcc.Graph(id='success-pie-chart'),
    html.Br(),
    
    # الـ Slider لاختيار الوزن
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
        value=[0, 10000]
    ),
    
    # الرسم البياني المبعثر
    dcc.Graph(id='success-payload-scatter-chart')
])

# 4. الـ Callback الأول (للـ Pie Chart)
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches by Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', title=f'Total Success Launches for site {entered_site}')
        return fig

# 5. الـ Callback الثاني (للـ Scatter Plot)
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    df_filtered = spacex_df[mask]

    if entered_site == 'ALL':
        fig = px.scatter(df_filtered, x='Payload Mass (kg)', y='class', 
                         color="Booster Version Category",
                         title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        df_site = df_filtered[df_filtered['Launch Site'] == entered_site]
        fig = px.scatter(df_site, x='Payload Mass (kg)', y='class', 
                         color="Booster Version Category",
                         title=f'Correlation between Payload and Success for site {entered_site}')
        return fig

# 6. التشغيل
if __name__ == '__main__':
    app.run(debug=True, port=8050)