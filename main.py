import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium

# Set a style for seaborn
sns.set(style="whitegrid")

# Ensure that you have the correct path to the CSV file.
file_path = 'C:/Users/prajj/Documents/HTI STUDY/HTI 550/201306-citibike-tripdata/201306-citibike-tripdata.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Convert 'starttime' and 'stoptime' to datetime
df['starttime'] = pd.to_datetime(df['starttime'])
df['stoptime'] = pd.to_datetime(df['stoptime'])



# Number of trips over time
daily_trips = df.resample('D', on='starttime').size()
plt.figure(figsize=(12, 6))
daily_trips.plot(kind='line', color="coral", marker="o")
plt.title('Number of Trips Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Trips')
plt.show()

#  Scatter plot of start and end stations 
sample_df = df.sample(n=1000, random_state=1)  # Sampling to avoid overplotting
plt.figure(figsize=(12, 8))
sns.scatterplot(data=sample_df, x='start station longitude', y='start station latitude', hue='end station id', legend=False)
plt.title('Flow of Bikes from Start to End Stations')
plt.xlabel('Start Station Longitude')
plt.ylabel('Start Station Latitude')
plt.show()

# Bar chart showing the count of trips by user type
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='usertype', palette="pastel")
plt.title('Count of Trips by User Type')
plt.xlabel('User Type')
plt.ylabel('Number of Trips')
plt.show()



# Popular Start Stations
start_station_counts = df['start station name'].value_counts().head(10)
plt.figure(figsize=(12, 6))
sns.barplot(y=start_station_counts.index, x=start_station_counts.values, palette='coolwarm')
plt.title('Top 10 Popular Start Stations')
plt.xlabel('Number of Trips Started')
plt.ylabel('Start Station Name')
plt.show()

# Popular End Stations
end_station_counts = df['end station name'].value_counts().head(10)
plt.figure(figsize=(12, 6))
sns.barplot(y=end_station_counts.index, x=end_station_counts.values, palette='coolwarm')
plt.title('Top 10 Popular End Stations')
plt.xlabel('Number of Trips Ended')
plt.ylabel('End Station Name')
plt.show()

# Heatmap of Popular Routes (Top 20)
#top_routes = df.groupby(['start station name', 'end station name']).size().reset_index(name='count').sort_values(by='count', ascending=False).head(20)
top_routes = df.groupby(['start station name', 'end station name']).size().reset_index(name='count').sort_values(by='count', ascending=False).head(20)
pivot_table_routes = top_routes.pivot_table(index='start station name', columns='end station name', values='count', fill_value=0)
plt.figure(figsize=(10, 8))
sns.heatmap(pivot_table_routes, annot=True, fmt=".0f", cmap='YlGnBu')  # Ensure fmt is set to ".0f" for floating point data
plt.title('Top 20 Popular Routes')
plt.xlabel('End Station Name')
plt.ylabel('Start Station Name')
plt.show()

# Geographical Map of Start Stations

# Calculate usage for each station
start_station_usage = df['start station id'].value_counts()
end_station_usage = df['end station id'].value_counts()

# Create a map centered around an average location
mean_lat = df['start station latitude'].mean()
mean_lon = df['start station longitude'].mean()
m = folium.Map(location=[mean_lat, mean_lon], zoom_start=13)

# Loops each station to add it to the map
for idx, row in df.drop_duplicates('start station id').iterrows():
    station_id = row['start station id']
    start_usage = start_station_usage.get(station_id, 0)
    end_usage = end_station_usage.get(station_id, 0)
    total_usage = start_usage + end_usage

    # Generate a popup message for each station
    popup_message = folium.Popup(f"{row['start station name']}<br>Starts: {start_usage}<br>Ends: {end_usage}", parse_html=True)

    # Color-code the marker based on total usage
    if total_usage > 1000:  
        color = 'red'
    elif total_usage > 500:  
        color = 'orange'
    else:
        color = 'green'

    # Add the marker to the map
    folium.CircleMarker([row['start station latitude'], row['start station longitude']],
                        radius=5,
                        popup=popup_message,
                        color=color,
                        fill=True,
                        fill_color=color,
                        fill_opacity=0.7).add_to(m)

# Save the map
map_file_path = 'C:\\Users\\prajj\\Documents\\HTI STUDY\\HTI 550\\201306-citibike-tripdata\\enhanced_citibike_map.html'
m.save(map_file_path)
print(f"Enhanced map saved! Open {map_file_path} to view it.")
