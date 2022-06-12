###################################################################################################
#                                                                                                 #
# Visualización de datos                                                                          #
# A9: Creación de la visualización y entrega del proyecto (Práctica II)                           #
#                                                                                                 #
# Titulo: Fit or Fat? (Europe's Edition)                                                          #
# Autor: Rubén Moya Vázquez <rmoyav@uoc.edu>                                                      #
# Fecha: 13/06/2021                                                                               #
# Versión: 1.0.0                                                                                  #
#                                                                                                 #
###################################################################################################

import json
import os
import pathlib

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from pycountry_convert import country_name_to_country_alpha3

###################################################################################################
#                                                                                                 #
#                                            CONSTANTS                                            #
#                                                                                                 #
###################################################################################################

app = Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
app.title = "Fit or Fat? (Europe's Edition)"

server = app.server

# Dictionary to parse countries
COUNTRY_TRANSLATION = {
    'BE': 'Belgium',
    'BG': 'Bulgaria',
    'CZ': 'Czechia',
    'DK': 'Denmark',
    'DE': 'Germany',
    'EE': 'Estonia',
    'IE': 'Ireland',
    'EL': 'Greece',
    'ES': 'Spain',
    'FR': 'France',
    'HR': 'Croatia',
    'IT': 'Italy',
    'CY': 'Cyprus',
    'LV': 'Latvia',
    'LT': 'Lithuania',
    'LU': 'Luxembourg',
    'HU': 'Hungary',
    'MT': 'Malta',
    'NL': 'Netherlands',
    'AT': 'Austria',
    'PL': 'Poland',
    'PT': 'Portugal',
    'RO': 'Romania',
    'SI': 'Slovenia',
    'SK': 'Slovakia',
    'FI': 'Finland',
    'SE': 'Sweden',
    'IS': 'Iceland',
    'NO': 'Norway',
    'UK': 'United Kingdom',
    'RS': 'Serbia',
    'TR': 'Turkey'
}

# Dictionary to parse gender
GENDER_TRANSLATION = {
    'F': 'Female',
    'M': 'Male',
    'T': 'Total'
}

# Dictionary to parse BMI levels
BMI_TRANSLATION = {
    'BMI_LT18P5': 'Underweight',
    'BMI18P5-24': 'Normal',
    'BMI_GE25': 'Overweight',
    'BMI25-29': 'Pre-obese',
    'BMI_GE30': 'Obese'
}

EDUCATION_TRANSLATION = {
    'ED0-2': 'Primary',
    'ED3_4': 'Secondary',
    'ED5-8': 'Tertiary',
    'TOTAL': 'Total'
}

AGE_TRANSLATION = {
    'Y15-24': '15-24',
    'Y25-34': '25-34',
    'Y35-44': '35-44',
    'Y45-54': '45-54',
    'Y55-64': '55-64',
    'Y65-74': '65-74',
    'Y_GE75': '75+',
    'TOTAL': 'Total'
}

###################################################################################################
#                                                                                                 #
#                                            FUNCTIONS                                            #
#                                                                                                 #
###################################################################################################

def translate_value(code:str, translator:dict) -> str:
    """This function is meant to translate the value found
    within the original dataset to a human readable one.

    Args:
        code (str): Value to be translated
        translator (dict): Dictionary to use for the translation

    Raises:
        ValueError: Raised if the code is not found within the translator dictionary

    Returns:
        str: Transalted value.
    """
    if code in translator.keys():
        translated = translator[code]
    else:
        raise ValueError("The code '{:s}' could not be found within the translation dictionary!!".format(code))
    return translated

def format_data(data:pd.DataFrame) -> pd.DataFrame:
    """This function will format the original data to be easy
    to read and analyse.

    Args:
        data (pd.DataFrame): Our data before parsing.

    Returns:
        pd.DataFrame: Our data ready to be used.
    """

    # Drop the NA values
    data = data.dropna(subset=['OBS_VALUE'])

    # Drop the agregated values
    data = data[data.geo != 'EU27_2020']
    data = data[data.geo != 'EU28']

    # Drop non standard age groups
    data = data[data.age != 'Y_GE65']
    data = data[data.age != 'Y15-19']
    data = data[data.age != 'Y15-29']
    data = data[data.age != 'Y25-29']
    data = data[data.age != 'Y25-64']
    data = data[data.age != 'Y15-64']
    data = data[data.age != 'Y18-24']
    data = data[data.age != 'Y18-29']
    data = data[data.age != 'Y18-44']
    data = data[data.age != 'Y18-64']
    data = data[data.age != 'Y_GE18']
    data = data[data.age != 'Y20-24']
    data = data[data.age != 'Y45-64']

    # Value Parsing
    data['sex'] = data.sex.apply(lambda x: translate_value(x, GENDER_TRANSLATION))
    data['bmi'] = data.bmi.apply(lambda x: translate_value(x, BMI_TRANSLATION))
    data['isced11'] = data.isced11.apply(lambda x: translate_value(x, EDUCATION_TRANSLATION))
    data['age'] = data.age.apply(lambda x: translate_value(x, AGE_TRANSLATION))
    data['country'] = data.geo.apply(lambda x: translate_value(x, COUNTRY_TRANSLATION))
    data['alpha3'] = data.country.apply(lambda x: country_name_to_country_alpha3(x))
    data = data.drop(['geo'], axis=1)
    return data


def read_data(data_file:str="hlth_ehis_bm1e_linear.csv") -> pd.DataFrame:
    """This function is meant to used to read the data file and prepare it to be used
    within our dashboard

    Args:
        file (str, optional): The path to our data source file. Defaults to "hlth_ehis_bm1e_linear.csv".

    Returns:
        pd.DataFrame: The data ready to be used.
    """
    if os.path.isfile(data_file):
        my_data = pd.read_csv(data_file)
        my_data = my_data.drop(['DATAFLOW', 'LAST UPDATE', 'OBS_FLAG', 'freq', 'unit'], axis=1)
        my_data = format_data(my_data)
    else:
        raise FileNotFoundError("The path given as parameter is not a file!!")

    return my_data

###################################################################################################
#                                                                                                 #
#                                            DATA LOAD                                            #
#                                                                                                 #
###################################################################################################

APP_PATH = str(pathlib.Path(__file__).parent.resolve())

full_data = read_data(os.path.join(APP_PATH, "hlth_ehis_bm1e_linear.csv"))

YEARS = full_data.TIME_PERIOD.unique()

BMI_VALUES = full_data.bmi.unique()

DEFAULT_COLORSCALE = [
    "#69e7c0",
    "#59dab2",
    "#45d0a5",
    "#31c194",
    "#2bb489",
    "#25a27b",
    "#1e906d",
    "#188463",
    "#157658",
    "#11684d",
    "#10523e",
]

DEFAULT_OPACITY = 0.8

###################################################################################################
#                                                                                                 #
#                                           APP LAYOUT                                            #
#                                                                                                 #
###################################################################################################

app.layout = html.Div(
    id="root",
    children=[
        # HEADER
        html.Div(
            id="header",
            children=[
                html.H2(children="Fit or Fat? (Europe's Edition)"),
                html.P(
                    id="description",
                    children="This simple dashboard will allow the \
                        user to answer several questions related to \
                        the health condition of the European population \
                        such as 'Which country has a greater problem \
                        with overweight?' or 'Are young germans healthier \
                        than their elders?'",
                ),
            ],
        ),
        # BODY
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="slider-container",
                            children=[
                                html.P(
                                    id="year-text",
                                    children="Select the year:"
                                    ),
                                dcc.RadioItems(
                                    id='years-radio',
                                    options=YEARS,
                                    value=min(YEARS),
                                    inline=True
                                    ),
                                html.P(
                                    id="bmi-text",
                                    children="Select the BMI:"
                                ),
                                dcc.RadioItems(
                                    id='bmi-radio',
                                    options=BMI_VALUES,
                                    value=min(BMI_VALUES),
                                    inline=True
                                    ),
                            ],
                        ),
                        html.Div(
                            id="map-container",
                            children=[
                                html.H3(
                                    id="map-title",
                                    children="This heatmap shows the percentage of '{0}' people for each country for the year {1}".format(min(BMI_VALUES).lower(), min(YEARS))
                                ),
                                dcc.Graph(id="map"),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    id="graph-container",
                    children=[
                        html.P(id="chart-selector", children="Select chart:"),
                        dcc.Dropdown(
                            options=[
                                {
                                    "label": "Percentage of people with selected BMI by sex",
                                    "value": 1,
                                },
                                {
                                    "label": "Percentage of people with selected BMI by age",
                                    "value": 2,
                                },
                                {
                                    "label": "Percentage of people with selected BMI by education level",
                                    "value": 3,
                                },
                                {
                                    "label": "Evolution of the percentage of people with selected BMI",
                                    "value": 4,
                                },
                                {
                                    "label": "Wind Rose Chart",
                                    "value": 5,
                                },
                            ],
                            value=1,
                            id="chart-dropdown",
                        ),
                        dcc.Graph(
                            id="selected-data",
                            figure=dict(
                                data=[dict(x=0, y=0)],
                                layout=dict(
                                    paper_bgcolor="#F4F4F8",
                                    plot_bgcolor="#F4F4F8",
                                    autofill=True,
                                    margin=dict(t=75, r=50, b=100, l=50),
                                ),
                            ),
                        ),
                    ],
                ),
            ],
        ),
    # FOOTER
    html.Div(
            id="footer",
            children=[
                html.A(
                    html.Button("Data Source", className="button"),
                    href="https://ec.europa.eu/eurostat/databrowser/view/HLTH_EHIS_BM1E/default/table?lang=en",
                ),
                html.A(
                    html.Button("Map Source", className="link-button"),
                    href="https://geojson-maps.ash.ms/",
                ),
                html.A(
                    html.Button("Organization", className="link-button"),
                    href="https://www.uoc.edu/portal/es/index.html",
                ),
                html.A(
                    html.Button("Source Code", className="link-button"),
                    href="https://github.com/rmoyav/PRA2_visualizacion",
                ),
            ],
        ),],
)

###################################################################################################
#                                                                                                 #
#                                         APP CALLBACKS                                           #
#                                                                                                 #
###################################################################################################

@app.callback(
    Output("map", "figure"),
    [Input("bmi-radio", "value"), Input("years-radio", "value")]
)
def display_map(bmi, year):
    # Reading geojson
    with open(os.path.join(APP_PATH, "europe.geo.json"), 'r') as euro:
        countries = json.load(euro)
    
    totals = full_data[(full_data.age == 'Total') & (full_data.sex == 'Total') & (full_data.isced11 == 'Total') & (full_data.bmi == bmi) & (full_data.TIME_PERIOD == year)]

    # Creating map
    fig = px.choropleth(totals, geojson=countries, color="OBS_VALUE", locations="alpha3",
    featureidkey="properties.iso_a3", range_color=[totals.OBS_VALUE.min(), totals.OBS_VALUE.max()])
    
    fig.update_geos(fitbounds="locations", visible=True)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=630, paper_bgcolor="#F4F4F8", dragmode="select")
    return fig

@app.callback(Output("map-title", "children"), [Input("bmi-radio", "value"), Input("years-radio", "value")])
def update_map_title(bmi, year):
    return "This heatmap shows the percentage of '{0}' people for each country for the year {1}".format(bmi.lower(), year)


@app.callback(
    Output("selected-data", "figure"),
    [
        Input("map", "selectedData"),
        Input("chart-dropdown", "value"),
        Input("years-radio", "value"),
        Input("bmi-radio", "value"),
    ],
)
def display_selected_data(selectedData, chart_dropdown, year, bmi):
    if selectedData is None:
        response =  dict(
            data=[dict(x=0, y=0)],
            layout=dict(
                title="Drag over the map to select countries",
                paper_bgcolor="#1f2630",
                plot_bgcolor="#1f2630",
                font=dict(color="#05C3DD"),
                margin=dict(t=75, r=50, b=100, l=75),
            ),
        )
    else:
        
        filtered = full_data[full_data.bmi == bmi]
        
        sel_countries = []
        for point in selectedData["points"]:
            sel_countries.append(point["location"])

        for country in filtered.alpha3.unique():
            if not country in sel_countries:
                filtered  = filtered[filtered.alpha3 != country]
                
        if chart_dropdown == 1:
            filtered = filtered[(full_data.TIME_PERIOD == year) & (filtered.isced11 == 'Total') & (filtered.age == 'Total') & (filtered.sex != 'Total')]
            fig = px.histogram(filtered, x="OBS_VALUE", y="country", color="sex")
            title = "Percentage of people with '<b>{0}</b>' BMI by sex (<b>{1}</b>)".format(bmi, year)
        elif chart_dropdown == 2:
            filtered = filtered[(full_data.TIME_PERIOD == year) & (filtered.sex == 'Total') & (filtered.isced11 == 'Total') & (filtered.age != 'Total')]
            fig = px.histogram(filtered, x="OBS_VALUE", y="country", color="age")
            title = "Percentage of people with '<b>{0}</b>' BMI by age (<b>{1}</b>)".format(bmi, year)
        elif chart_dropdown == 3:
            filtered = filtered[(full_data.TIME_PERIOD == year) & (filtered.sex == 'Total') & (filtered.age == 'Total') & (filtered.isced11 != 'Total')]
            fig = px.histogram(filtered, x="OBS_VALUE", y="country", color="isced11")
            title = "Percentage of people with '<b>{0}</b>' BMI by education (<b>{1}</b>)".format(bmi, year)
        elif chart_dropdown == 4:
            filtered = filtered[(filtered.age == 'Total') & (filtered.sex == 'Total') & (filtered.isced11 == 'Total')]
            fig = px.area(filtered, y="OBS_VALUE", x="TIME_PERIOD", color="country")
            title = "Trend for people with '<b>{0}</b>' BMI (2014-2019)".format(bmi)
        elif chart_dropdown == 5:
            filtered = full_data[(full_data.TIME_PERIOD == year) & (full_data.sex == 'Total') & (full_data.age == 'Total') & (full_data.isced11 == 'Total')]
            for country in filtered.alpha3.unique():
                if not country in sel_countries:
                    filtered  = filtered[filtered.alpha3 != country]
            title = "Wind rose of all BMIs for year <b>{0}</b>".format(year)
            fig = px.bar_polar(filtered, r="OBS_VALUE", theta="country", color="bmi", color_discrete_sequence= px.colors.sequential.Plasma_r, title=title)
            
        else:
            response =  dict(
                data=[dict(x=0, y=0)],
                layout=dict(
                    title="Ups! Something's gone wrong... :S",
                    paper_bgcolor="#1f2630",
                    plot_bgcolor="#1f2630",
                    font=dict(color="#05C3DD"),
                    margin=dict(t=75, r=50, b=100, l=75),
                ),
        )

        if fig is not None:
            fig_layout = fig["layout"]
            fig_layout["yaxis"]["title"] = title
            fig_layout["xaxis"]["title"] = ""
            fig_layout["title"] = "<b>{0}</b> countries selected".format(len(filtered.country.unique()))
            fig_layout["yaxis"]["fixedrange"] = True
            fig_layout["xaxis"]["fixedrange"] = False
            fig_layout["paper_bgcolor"] = "#1f2630"
            fig_layout["font"]["color"] = "#05C3DD"
            fig_layout["xaxis"]["tickfont"]["color"] = "#05C3DD"
            fig_layout["yaxis"]["tickfont"]["color"] = "#05C3DD"
            fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
            fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"
            fig_layout["font"]["color"] = "#05C3DD"
            fig_layout["title"]["font"]["color"] = "#05C3DD"
            fig_layout["hovermode"] = "closest"
            fig_layout["legend"] = dict(orientation="v")
            fig_layout["autosize"] = True
            fig_layout["margin"]["t"] = 75
            fig_layout["margin"]["r"] = 50
            fig_layout["margin"]["b"] = 100
            fig_layout["margin"]["l"] = 50

            if chart_dropdown < 4:
                fig_data = fig["data"]
                fig_data[0]["marker"]["color"] = "#05C3DD"
                fig_data[0]["marker"]["opacity"] = 1
                fig_data[0]["marker"]["line"]["width"] = 0
                fig_data[0]["textposition"] = "outside"
            
            
            
            
            response = fig
        elif (fig is not None) and (chart_dropdown == 4):
            # See plot.ly/python/reference

            
            
            
            response = fig

    return response

###################################################################################################
#                                                                                                 #
#                                              MAIN                                               #
#                                                                                                 #
###################################################################################################

if __name__ == '__main__':
    app.run_server(debug=False)
