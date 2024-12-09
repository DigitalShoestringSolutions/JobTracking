# Job Tracking Starter Solution

Scan barcodes to associate them with a scanner/location.  
Presents a table listing which codes were most recently scanned by each scanner.

## Download
- Clone this repo: `git clone https://github.com/DigitalShoestringSolutions/JobTracking`
- Open the downloaded folder `cd JobTracking`

## Configure
- Run the `./setup_keys.sh` script

## Build & Run
- Build using docker: `docker compose build`
- Run using the `./start.sh` script.

## Usage
- Configure locations at `localhost:8001/admin`
- View Grafana dashboards in a web browser: `localhost`
