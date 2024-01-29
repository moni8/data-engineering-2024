services:
  pgdatabase:
    image: postgres:13
    environment:
      - POSTGRES_USER=root
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=ny_taxi
    volumes:
      - "./ny_taxi_postgres_data:/var/lib/postgresql/data:rw"
    ports:
      - "5432:5432"
  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    ports:
      - "8080:80"
    

    winpty docker run -it \
      -e POSTGRES_USER="root" \
      -e POSTGRES_PASSWORD="root" \
      -e POSTGRES_DB="ny_taxi" \
      -v //d/data_engineer_course/week_1/2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
      -p 5432:5432 \
     postgres:13

    docker run -it -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" 
      -e PGADMIN_DEFAULT_PASSWORD="root" 
      -p 8080:80 
      dpage/pgadmin4

## cmd to download ny taxi csv file
Invoke-WebRequest -Uri https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz -OutFile D:\data_engineer_course\week_1\2_docker_sql\green_tripdata_2019-09.csv.gz
