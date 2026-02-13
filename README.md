## Mall Foot Traffic Design

The primary focus was on maintaining a structured and maintainable architecture design with basic functionality. The following reflects on key design decisions I made during the implementation process including limitations and potential improvements. 

## Backend Design

FastAPI:

* Recommended to use from Wednesdays meeting.
* Allows me to use Uvicorn as a development ASGI server.
* I separated foot traffic and store data requests into distinct endpoints to follow REST principles (api/stores & api/traffic). One endpoint is for aggregation (stores traffic) and the other is for timestamp filtering, which makes the API more explicit and maintainable.

API routes:

API routes were separated into logical domains under the "routers/" directory
* upload.py
* stores.py
* traffic.py

This keeps API logic separated based on responsibility and ensures the app is maintainable for future development. This also keeps business logic separate from main.py which is focused on application configuration.

Additionally, I chose to implement both total and store specific traffic into one /api/traffic/timeseries route instead of splitting them into two separate endpoints. This is because they perform the same timestamp foot traffic aggregation and the combined implementation was simpler given the time frame. However, separating these endpoints could improve scalability for the project. For example, if future permission control is implemented that restricts some users from accessing total mall foot traffic, having two separate endpoints improves clarity given the more complex system.

## Frontend Design

React states:

The main App.tsx file maintains all core application state:
* stores (available store list)
* selectedStores (user interaction state)
* timeSeries (aggregated API response)
* selectedTimestamp (chart interaction state)
* breakdown (drilldown API response)

For example, whenever selectedStores changes, a useEffect hook triggers a data fetch. The updated state automatically refreshes the line chart. This ensures that the UI is consistent with the applications state and avoids manual DOM manipulation.

A trade-off I intentionally made with this design was that every filter change triggers a full API request. This introduces potential issues like race conditions if a user selects a filter quickly and increases load times given that there is no caching.

Because the dataset is small, this approach is acceptable for now. A future improvement could be to introduce React Query or caching mechanisms which would improve scalability if the dataset became more complex.

## Data Storage (SQLite)

Schema Design:

A single foot_traffic table stores (seen in models.py):
* timestamp (DateTime)
* store_id (String)
* store_name (String)
* people_count (Integer)

I chose to include both store_name and store_id within the foot_traffic table as it was the simplest design as it removed the need for table joins. The tradeoff of this decision is that only one dataset can exist at a time due to denormalisation. For this reason, the application will overwrite the database if a new CSV file is uploaded to prevent conflicts.

For future scalability, switching to PostgreSQL via Docker Compose (as mentioned in the bonus criteria) with separate stores and datasets tables with foreign key relationships would allow:
* Multiple datasets
* More complex features to be included (i.e. historical comparisons)
* Improved performance for larger datasets

## Other Tradeoffs

* CORS policy currently allows all origins (*) which poses a security risk.
* No input sanitation (apart from type validation).
* Only supports a single user as there is no session management.
* No authentication or authorisation.
* Only supports a single dataset.
* Very basic UI design that prioritise functionality over visuals.

## If I Had 8 More Hours

* Add backend test coverage using FastAPI's TestClient. I would test the CSV ingestion, aggregation correctness, and breakdown sorting functionality specifically.
* Include more validation checks on CSV files such as preventing duplicate (timestamp, store_id) rows or handling missing entries. Currently, the app only checks file extension, required columns exist and ensure people_count >= 0.
* Improve loading states when making API fetch requests. At times, the application freezes and the UI becomes temporarily stale.
* Improve error messaging in the UI. For example, failed uploads or invalid CSVs. 
* Fix denormalisation issue with SQLite by separating store_name and store_id into a seperate table to allow for multiple datasets to be uploaded (no overwriting).
* Seperate /api/traffic/timeseries endpoint into two seperate endpoints for all traffic and store specific traffic.

## If I had 1 week

* Migrate to PostgreSQL via Docker Compose.
* Add dataset versioning to allow user(s) to compare foot traffic across different days.
* Potentially add authorisation and session management to support multiple users.
* Restrict CORS policy to include only necessary origins (not *)
* Introduce caching for aggregation API requests, specifically for total mall foot traffic timeseries.
* Add time range filtering (i.e. hourly, daily) for the graph.
* Add CI/CD pipeline with automated tests and linting.
* Containerise the entire application, including database, backend, and frontend.