

import pandas as pd

import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import geoplot
import geoplot.crs as gcrs


# In[ ]:

#Stage Changes
stage_change = pd.DataFrame()

#Pull flood data from web
table = 'https://waterwatch.usgs.gov/webservices/flowchange?&format=csv'
stage_change = pd.read_csv(table)




stage_change['USGSstationID'] = stage_change['site_no'].astype(float)
sites = pd.read_csv('ahps_usgs.csv')
sites = sites[sites['usgs id'].notna()]
sites['USGSstationID'] = sites['usgs id'].astype(float)
ice_jam = pd.merge(stage_change,  
                      sites,  
                      on ='USGSstationID',  
                      how ='inner') 


ice_jam = ice_jam[ice_jam['stage_chg_percent'].notna()]
ice_jam = ice_jam.sort_values(by=['river/water-body name', 'site_no'])
ice_jam['site_no'] = ice_jam['site_no'].astype(float)
ice_jam['site_no_shift'] = ice_jam['site_no'].shift(-1)
ice_jam['stage_chg_percent'] = ice_jam['stage_chg_percent'].astype(float)
ice_jam['stage_chg_percent_shift'] = ice_jam['stage_chg_percent'].shift(-1)
ice_jam['river/water-body name_shift'] = ice_jam['river/water-body name'].shift(-1)






ice_jam.to_csv('delete.csv')



def f(ice_jam):
    if (ice_jam['site_no'] < ice_jam['site_no_shift']) and (ice_jam['stage_chg_percent'] > 0) and (ice_jam['stage_chg_percent_shift'] < 0) and (ice_jam['river/water-body name'] == ice_jam['river/water-body name_shift']):
        val = 'jam'
    else:
        val = 'clear'
    return val

ice_jam['jam_status'] = ice_jam.apply(f, axis=1)


ice_jam = ice_jam.loc[ice_jam['jam_status'] == 'jam']
ice_jam.to_csv('delete1.csv')

# In[ ]:

    






# In[ ]:





# In[ ]:


gdf = gpd.GeoDataFrame(
    ice_jam, geometry=gpd.points_from_xy(ice_jam.dec_long_va, ice_jam.dec_lat_va))


contiguous_usa = gpd.read_file(geoplot.datasets.get_path('contiguous_usa'),projection=gcrs.AlbersEqualArea())


ax = contiguous_usa.plot(
    color='lightgray', edgecolor='black')


gdf.plot(ax=ax, categorical=True, markersize=15, edgecolors='black', linewidths=0.2,legend=True, legend_kwds={'loc': 'lower right'})

ax.set_title('Ice Jam Stage Analysis', fontsize=10)
leg = ax.get_legend()

ax.set_axis_off()

#plt.show()
plt.savefig('ice_jam.png', dpi=1000, figsize=(60,50))


# In[ ]:





# In[ ]:




