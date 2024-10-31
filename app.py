# you need to install shiny, shinywidgets and ipyleaflet to be able to run this
from shiny import App, ui, reactive, render
from ipyleaflet import Map
from shinywidgets import output_widget, render_widget


# data needed to flow into the app
ten_metro = ['Seattle', 'New York', 'Boston', 'Chicago', "Washington DC", "Los Angeles", "San Francisco", "Phoenix", "Houston", "Jacksonville"]

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
        return Map(center=(50.6252978589571, 0.34580993652344), zoom=3)  

app = App(app_ui, server)
