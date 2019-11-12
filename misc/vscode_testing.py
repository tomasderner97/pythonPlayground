#%%
from bokeh.io import output_notebook, show
from bokeh.models.widgets import Dropdown

output_notebook()

menu = [("Item 1", "item_1"), ("Item 2", "item_2"), None, ("Item 3", "item_3")]
dropdown = Dropdown(label="Dropdown button", button_type="warning", menu=menu)

show(dropdown)

