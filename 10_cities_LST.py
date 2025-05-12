import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
import easygems.healpix as egh
from shapely.geometry import mapping
from cartopy.feature import ShapelyFeature
import intake
from easygems import healpix as egh
import pandas as pd
import xarray as xr



cat = intake.open_catalog("https://digital-earths-global-hackathon.github.io/catalog/catalog.yaml")["online"]
list(cat)

ds = cat["um_glm_n2560_RAL3p3"](zoom = 1).to_dask()
ds = ds.pipe(egh.attach_coords)



# Create land mask: only retain points where orography is valid
# Assume NaNs or zeros in orog are ocean (you can customize the threshold if needed)
land_mask = ds['orog'] > 0  # or use `.notnull()` if orog has NaNs over ocean
ts_land = ds['ts'].isel(time=0).where(land_mask)

# Set up the map
fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([110, 160, -50, -10], crs=ccrs.PlateCarree())

# Add features
ax.add_feature(cf.COASTLINE, linewidth=0.8)
ax.add_feature(cf.BORDERS, linewidth=0.4)

# Plot only land values
egh.healpix_show(ts_land, ax=ax, cmap='jet')


# Top 10 cities
cities = {
    "Sydney": (-33.8688, 151.2093),
    "Melbourne": (-37.8136, 144.9631),
    "Brisbane": (-27.4698, 153.0251),
    "Perth": (-31.9505, 115.8605),
    "Adelaide": (-34.9285, 138.6007),
    "Hobart": (-42.8821, 147.3272),
    "Darwin": (-12.4634, 130.8456),
    "Canberra": (-35.2809, 149.1300),
    "Gold Coast": (-28.0167, 153.4000),
    "Newcastle": (-32.9283, 151.7817)
}

for city, (lat, lon) in cities.items():
    ax.plot(lon, lat, 'ro',markersize=4, transform=ccrs.PlateCarree())
    ax.text(lon + 1, lat + 1, city, fontsize=9, transform=ccrs.PlateCarree())

plt.title("Surface Temperature over Australia (Land Only via Orography)")
plt.show()

