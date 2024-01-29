from time import time
import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
taxi_zone_lookup_df = pd.read_csv('taxi+_zone_lookup.csv')

# Find the LocationID of the zone named Astoria
astoria_location_id = taxi_zone_lookup_df.loc[taxi_zone_lookup_df['Zone'] == 'Astoria', 'LocationID'].values[0]

print("LocationID of Astoria:", astoria_location_id)

with engine.connect() as connection, connection.begin():
    #truncate_query = text('TRUNCATE TABLE green_taxi_data')
    
    #connection.execute(truncate_query)

    #df_iter = pd.read_csv('yellow_tripdata_2021-07.csv', iterator=True, chunksize=100000)
    df_iter = pd.read_csv('green_tripdata_2019-09.csv')
    #print(df_iter.info())
    #df_first_chunk = next(df_iter)
    df_iter['lpep_pickup_datetime'] = pd.to_datetime(df_iter['lpep_pickup_datetime'])
    df_iter['lpep_dropoff_datetime'] = pd.to_datetime(df_iter['lpep_dropoff_datetime'])

    print(df_iter.info())

    sept_18_trips = df_iter[df_iter['lpep_pickup_datetime'].dt.date == pd.to_datetime('2019-09-18').date()]

    number_of_trips = len(sept_18_trips)

    print(f'The number of taxi trips made on September 18th, 2019 is: {number_of_trips}')

    df_iter['pickup_day'] = df_iter['lpep_pickup_datetime'].dt.date

    # daily_trip_distances = df_iter.groupby('pickup_day')['trip_distance'].sum()

    # day_with_largest_distance = daily_trip_distances.idxmax()
    # largest_distance = daily_trip_distances.max()

    # print(f'The pickup day with the largest total trip distance is {day_with_largest_distance} with a total distance of {largest_distance} miles.')

    #df_first_chunk['pickup_day'] = df_first_chunk['lpep_pickup_datetime'].dt.date

    # Question5: Top three pickup borough on Sep-18-2019 whose total_amount is greater than 50000.
    # df_merged = df_iter.merge(taxi_zone_lookup_df, left_on='PULocationID', right_on='LocationID', how='left')

    # filtered_data = df_merged[(df_merged['pickup_day'] == pd.to_datetime('2019-09-18').date()) & 
    #                           (df_merged['Borough'] != 'Unknown')]
    
    # borough_total_amount = filtered_data.groupby('Borough')['total_amount'].sum()
    
    # top_boroughs = borough_total_amount[borough_total_amount > 50000].nlargest(3)
    
    # print("Top 3 pickup boroughs with a sum of total_amount > 50000:")
    # print(top_boroughs)

    # Question6: Find drop off zone name who had largest tip amount for Astoria pickup zone in September 2019.
    september_trips = df_iter[pd.to_datetime(df_iter['lpep_pickup_datetime']).dt.month == 9]

    astoria_trips = september_trips[september_trips['PULocationID'] == astoria_location_id]

    print("Number of trips picked up in Astoria in September 2019:", len(astoria_trips))

    largest_tip_trip = astoria_trips.loc[astoria_trips['tip_amount'].idxmax()]

    dropoff_location_id = largest_tip_trip['DOLocationID']

    dropoff_zone_name = taxi_zone_lookup_df.loc[taxi_zone_lookup_df['LocationID'] == dropoff_location_id, 'Zone'].values[0]

    print("Zone name corresponding to the drop-off location ID:", dropoff_zone_name)
 
    # df_first_chunk.head(0).to_sql(name='green_taxi_data', con=connection, if_exists='replace', index=False)

    # for i, df_chunk in enumerate(df_iter, start=1):
    #     start_time = time()
    #     df_chunk['lpep_pickup_datetime'] = pd.to_datetime(df_chunk['lpep_pickup_datetime'])
    #     df_chunk['lpep_dropoff_datetime'] = pd.to_datetime(df_chunk['lpep_dropoff_datetime'])
        
    #     df_chunk.to_sql(name='green_taxi_data', con=connection, if_exists='append', index=False, method='multi')

    #     end_time = time()
    #     print(f"Inserted chunk {i}, took {end_time - start_time:.3f} seconds")
