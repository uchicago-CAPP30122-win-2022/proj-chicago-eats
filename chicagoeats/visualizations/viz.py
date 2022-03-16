import folium
import geopandas as gpd
import pandas as pd
import mapclassify
import panel as pn
import param
pn.extension()


acs = gpd.read_parquet('data/acs.parquet')
food = pd.read_csv('data/food_source_final.csv')

food_geo = gpd.GeoDataFrame(
    food, geometry=gpd.points_from_xy(food.longitude, food.latitude))
food_geo.dropna(inplace=True)

acs = acs[['GEOID', 'geometry', 'year', 'tract', 'total_pop', 'n_white', 'n_black', 'n_asian', 'n_hispanic', 'n_poverty',
           'median_household_income', 'median_home_value', 'p_poverty', 'p_black','p_white', 'p_hispanic', 'p_asian' ]]
columns = list(acs.columns[-7:])

# create a classfier from all of the data so that
# we can compare across the years
bins = {}
for col in columns:
    bins[col] = mapclassify.Quantiles(acs[col].dropna().values, k=6).bins


def base_map():
    """
    Creates base map fo other functions to build off of.
    Inputs:
        None
    Ouputs:
        Folium map of Chicago
    """
    return folium.Map(location=[41.87494504366721, -87.62871556344562], zoom_level=5)

def attr_map(m_obj, attr, year):
    """
    Creates a map from the selected ACS data.
    Inputs:
        m_obj: Folium.Map object to add this map to
        attr: attribute of the dataframe to map
        year: year of the data to select
    Ouputs:
        A folium.GeoJSON map object
    """
    return acs[acs.year == year].explore(m = m_obj, name='Attributes', column= attr,
                                         cmap='plasma', scheme="user_defined", legend=True,
                                         tooltip=attr, legend_kwds=dict(colorbar=False),
                                         classification_kwds={'bins': bins[attr]})

def food_map(m_obj, cat):
    """
    Creates a map of the food data with desired filter.
    Inputs:
        m_obj: Folium.Map object to add the map to
        cat: Category of food source to graph
    Ouputs:
        A Folium.GeoJSON map object
    """
    return food_geo[food_geo.category == cat].explore(m=m_obj, name='Food Sources', 
                                                  tooltip=['dba_name', 'facility_type'])


def build_map(attr, year, cat):
    """
    A function that utilizes base_map(), attr_map(), and food_map()
    to create a new map. Is called in our Panel instance to build a new map
    when an update is required.
    Inputs:
        attr: attribute from acs data to plot
        year: year of food and CAs data to plot
        cat: caegory of food sources to plot
    Ouputs:
        A Folium.Map object with the ACS and food data plotted
    """
    chi = food_map(attr_map(base_map(), attr, year), cat)
    folium.LayerControl().add_to(chi)
    return chi



class FoliumPanel(param.Parameterized):
    """
    A class that creates a Folium pane object with
    the necessary selectors using the param library.
    """
    attribute = param.Selector(default ='median_household_income', objects=columns)
    year = param.Selector(default=2019, objects=list(acs.year.unique()))
    food = param.Selector(default='Grocery Store', objects=list(food_geo.category.unique()))

    def __init__(self, **params):
        super().__init__(**params)
        self.folium_pane = pn.pane.plot.Folium(sizing_mode="stretch_both", min_height=800, margin=0)    
        self.view = pn.Row(
            pn.Column(pn.pane.Markdown('#Chicago Eats'), self.folium_pane, sizing_mode='stretch_both'),
            pn.Column(self.param.attribute, self.param.year, self.param.food,
            pn.pane.Markdown('These maps contain a lot of data, \
            and can take a moment to update when selecting new attributes.'),
            height=300, width=400)
            ).servable()
        self.map = build_map(self.attribute, self.year, self.food)
        self._update_map()

    @param.depends('attribute', 'year', 'food', watch=True)
    def _update_map(self):
        """
        Calls build_map() to rebuild the map whenever there is a change
        selected options.
        """
        self.map = build_map(self.attribute, self.year, self.food)
        self.folium_pane.object = self.map
