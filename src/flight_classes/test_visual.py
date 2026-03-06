import folium
from datetime import datetime
from .Flight import Flight  # adjust import if running outside the package

# 1️⃣ Center map roughly on the continental USA
m = folium.Map(location=[39.0, -98.0], zoom_start=4)

# 2️⃣ Generate a random flight
f = Flight.new_random_flight(datetime.now(), "UAL1")

# 3️⃣ Extract points (lat, lon)
points = [(event.location.latitude, event.location.longitude) for event in f.flight_events]

# 4️⃣ Draw the flight path
folium.PolyLine(points, color="blue", weight=2.5, opacity=0.8).add_to(m)

# 5️⃣ Add markers for the origin and destination
folium.Marker(points[0], popup="Origin", icon=folium.Icon(color='green')).add_to(m)
folium.Marker(points[-1], popup="Destination", icon=folium.Icon(color='red')).add_to(m)

# 6️⃣ Optional: add markers for intermediate points (if you want)
for lat, lon in points[1:-1]:
    folium.CircleMarker(location=[lat, lon], radius=3, color='blue', fill=True).add_to(m)

# 7️⃣ Save the map to HTML (open in browser)
m.save("map.html")

# If running in Jupyter, display inline
# from IPython.display import display
# display(m)