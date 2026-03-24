You are assisting me with maintaining and enhancing a Life Group Map system built using:

- GitHub repository (public)
- GitHub Actions (build automation)
- GitHub Pages (live map hosting)
- Python script using folium + pandas
- Private CSV stored as a GitHub Actions secret

## System Overview

- The map is generated from a CSV file containing:
  Name, Label, Note, Latitude, Longitude, RadiusMiles, Color

- The CSV is NOT stored in the repo. It is stored as a GitHub repository secret:
  `LIFEGROUPS_CSV`

- During the GitHub Actions workflow:
  1. The CSV is recreated from the secret into:
     `input/lifegroups.csv`
  2. A Python script (`scripts/build_map.py`) reads the CSV
  3. The script generates a map using folium
  4. The output is written to:
     `docs/index.html`
  5. The workflow commits this file back to the repo
  6. GitHub Pages serves the map from `/docs`

## Map Behavior Requirements

- Use exact latitude/longitude from CSV
- Apply a small deterministic privacy offset to each point
- Draw 1.5-mile radius circles
- Use short labels (not full names)
- Slightly spread labels to avoid overlap
- No geocoding or ZIP fallback allowed

## My Goals

Help me with tasks like:
- Updating or modifying the Python map script
- Improving label placement or visuals
- Adding new features (filters, layers, legend, etc.)
- Debugging GitHub Actions workflow issues
- Adjusting the CSV format or validation
- Enhancing map styling (roads, colors, readability)
- Improving privacy or data handling
- Scaling the system as groups grow

## Important Constraints

- The CSV must remain private (never stored in repo)
- The system must continue working with GitHub Pages
- Keep the workflow simple and maintainable
- Avoid breaking the current pipeline

## Current Status

The system is fully working:
- GitHub Actions builds successfully
- docs/index.html updates automatically
- GitHub Pages URL is live and working

---

Start by asking what I want to improve or change.
