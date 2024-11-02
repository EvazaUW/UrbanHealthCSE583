# you need to install shiny, shinywidgets and ipyleaflet to be able to run this
from shiny import App, ui, reactive, render
from ipyleaflet import Map, GeoJSON
from shinywidgets import output_widget, render_widget


# data needed to flow into the app
ten_metro = ['Seattle', 'New York', 'Boston', 'Chicago', "Washington DC", "Los Angeles", "San Francisco", "Phoenix", "Houston", "Jacksonville"]

coordinates = {
    'Seattle': (47.608013, -122.335167),
    'New York': (40.712776, -74.005974), 
    'Boston': (42.360081, -71.058884), 
    'Chicago': (41.878113, -87.629799), 
    "Washington DC": (38.907192, -77.036873),
    "Los Angeles": (34.073520, -118.253879), 
    "San Francisco": (0,0),
    "Phoenix": (0,0), 
    "Houston": (0,0), 
    "Jacksonville": (0,0)
    }

# input dataframes needed here

# It looks like pyshiny has two sets of syntax - express and core (https://shiny.posit.co/py/docs/express-vs-core.html)
# I used core because it has more functionality

# html interface - all components nested within page.fluid()
app_ui = ui.page_fluid(
    
    # this is the drop-down menu. The selected choice will be stored in input.metro_area()
    ui.input_select(  
        id = "metro_area",  
        label = "Select an option below:",  
        choices = ten_metro
    ),  
    
    ui.input_select(
        id = "census_tract",
        label = "Select a region:",
        choices = ['census tract 1', 'census tract 2']
    ),

    # this creates a container to display some text that will be defined in the server function
    ui.output_text(
        id = "selected_metro"
    ),

    output_widget("map")
)

def server(input, output, session):
    
    @render.text
    def selected_metro():
        message = f"You selected {input.metro_area()}, the life expectancy is ##"
        return  message

    @render_widget  
    def map():
        return Map(center= coordinates[input.metro_area()], zoom=10)  

app = App(app_ui, server)
