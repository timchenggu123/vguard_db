CREATE TABLE IF NOT EXISTS gps_data (
    boothid TEXT,
    timestamp TEXT,
    latitude TEXT,
    longitude TEXT,
    elevation TEXT,
    accuracy TEXT,
    bearing TEXT,
    speed_meters_per_second TEXT,
    satellites TEXT,
    provider TEXT,
    hdop TEXT,
    vdop TEXT,
    pdop TEXT,
    geoidheight TEXT,
    ageofdgpsdata TEXT,
    dgpsid TEXT,
    activity TEXT,
    battery TEXT,
    annotation TEXT,
    distance_meters TEXT,
    elapsed_time_seconds TEXT
);

/*CREATE TABLE IF NOT EXISTS backup_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    foo TEXT NOT NULL,
    bar TEXT NOT NULL
);*/
