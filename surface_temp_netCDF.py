from netCDF4 import Dataset,MFDataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from scipy import stats

TS_fire=MFDataset('fwproject\\TS_fire_online_*nc','r')
TS_nofire=MFDataset('fwproject\\TS_nofire_online_*nc','r')


lons_fire = TS_fire.variables['lon'][:]
lats_fire = TS_fire.variables['lat'][:]
ts_fire = TS_fire.variables['TS'][:]
ts_units_fire = TS_fire.variables['TS'].units

lons_nofire = TS_nofire.variables['lon'][:]
lats_nofire = TS_nofire.variables['lat'][:]
ts_nofire = TS_nofire.variables['TS'][:]
ts_units_nofire = TS_nofire.variables['TS'].units

# perform t-test of two independent samples

# Compute the descriptive statistics of a and b.
ts_fire_bar = ts_fire.mean()
ts_fire_var = ts_fire.var(ddof=1)
n_ts_fire = ts_fire.size
ts_fire_dof = n_ts_fire - 1

ts_nofire_bar = ts_nofire.mean()
ts_nofire_var = ts_nofire.var(ddof=1)
n_ts_nofire = ts_nofire.size
ts_nofire_dof = n_ts_nofire - 1

t_value, p_value = stats.ttest_ind_from_stats(ts_fire_bar, np.sqrt(ts_fire_var), n_ts_fire,
                              ts_nofire_bar, np.sqrt(ts_nofire_var), n_ts_nofire,
                              equal_var=False)

print("ttest_independent_samples_from_stats: t = %g  p = %g" % (t_value, p_value))

def map_genetator(dataset_nc,lons,lats,ts_units,name_of_plot):
	# fucntion to generate a map
	sample2_np=np.zeros((1,53, 89))
	for i in range(dataset_nc.shape[0]):
	    sample_np=np.array(dataset_nc[i])
	    sample1_np=sample_np.reshape((1,53, 89))
	    sample2_np=sample2_np+sample1_np
	    
	sample3_np=sample2_np/dataset_nc.shape[0]
	#print(sample3_np.shape,lons_fire.shape,lats_fire.shape,dataset_nc.shape)

	lons_0 = lons.mean()
	lats_0 = lats.mean()
	ts_0_fire = dataset_nc.mean()

	print("Generating the map....")
	m = Basemap(width=10000000,height=9500000,
	            resolution='l',projection='stere',\
	            lat_ts=40,lat_0=lats_0,lon_0=lons_0)
	lon, lat = np.meshgrid(lons, lats)
	xi, yi = m(lon, lat)
	# Plot Data
	cs = m.pcolor(xi,yi,np.squeeze(sample3_np))
	# Add Grid Lines
	m.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
	m.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)
	# Add Coastlines, States, and Country Boundaries
	m.drawcoastlines()
	m.drawstates()
	m.drawcountries()
	# Add Colorbar
	cbar = m.colorbar(cs, location='bottom', pad="10%")
	cbar.set_label(ts_units)
	# Add Title
	plt.title('Plot of Avg Surface Temperatures: '+ name_of_plot)
	plt.show()

print("Generating map for fire dataset....")
#map_genetator(ts_fire,lons_fire,lats_fire,ts_units_fire,"Fire dataset")
print("Generating map for nofire data set....")
#map_genetator(ts_nofire,lons_nofire,lats_nofire,ts_units_nofire,"Nofire dataset")

print("Mean surface temperature for Fire data set: "+str(ts_fire.mean()))
print("Mean surface temperature for Nofire data set: "+str(ts_nofire.mean()))