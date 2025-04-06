 1. Initial Thought Process & Breakdown
When I read the problem, I saw it as a geospatial proximity search problem with the following core tasks:

Interpret a free-text location (e.g., "Agra" or "Connaught Place")

Convert that to latitude/longitude

Compare it to a fixed list of known property locations

Return all properties within a 50 km radius

I broke the task into smaller parts:

Input handling: Accept user input as a natural-language query.

Geocoding: Convert this query to coordinates using a geolocation service.

Data source: Store or mock property data with known coordinates.

Distance calculation: Calculate distances to all properties using geospatial formulas.

Filtering & response: Filter for <= 50 km, format the results cleanly.

2. Tools, Libraries & Resources Used
Libraries:
FastAPI: Chosen for its performance, simplicity, and support for async I/O. It’s lightweight, perfect for internal APIs like this.

geopy: Used for both geocoding (via Nominatim) and calculating distances using the Haversine formula under the hood.

Nominatim (OpenStreetMap): A free, public geocoding service. Chosen over Google Maps to avoid API keys and usage costs for a prototype.

Pydantic: FastAPI uses it internally for input validation and output schema — very useful for API robustness.

Why these over others?
I preferred Nominatim over Google Maps API for ease and zero-cost during initial development.

geopy over manual Haversine because it’s more readable, tested, and provides fallback methods.

FastAPI over Flask for speed and ease of API building with built-in OpenAPI docs.

3. Key Challenge & Solution
Challenge: Accurately geocoding any vague or varied user input (like “near Taj Mahal” or “Connaught Place”) to reliable coordinates.

Solution:

Initially relied on Nominatim which works for many named places, but can fail on very ambiguous or non-standard names.

Planned a fallback using LLMs (like GPT or Groq) to parse vague queries and turn them into structured prompts or location names for the geocoder — e.g., "near Taj Mahal" → "Agra".

This hybrid approach (LLM + geocoder) ensures both coverage and accuracy.

4. If I Had More Time — Improvements/Alternatives
Here’s what I’d explore further:

a. LLM-Based Location Resolution
Integrate OpenAI or Groq to handle fuzzy user queries and ambiguous place names.

Ex: “close to India Gate” → get accurate geolocation with GPT function calling.

b. Vector Search + Spatial Indexing
Use PostGIS or H3 spatial indexing for efficient querying when dataset grows.

Better performance for real-time queries at scale.

c. External Property DB or Admin Panel
Move from hardcoded properties to a live database (MongoDB, PostgreSQL with PostGIS) with an admin panel for the sales team to update/add new properties.

d. Caching and Rate Limiting
Add caching (Redis) to avoid repeated geocoding of the same query.

Implement rate-limiting to stay within usage limits for free services like Nominatim.
