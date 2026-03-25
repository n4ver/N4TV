# N4TV Dashboard

A Flask-based web dashboard for displaying Team Fortress 2 (TF2) match statistics in a stream-friendly format. Perfect for streamers who want to showcase competitive match data during broadcasts.

**Live Demo:** [https://nfourtv.vercel.app/](https://n4-tv.vercel.app/)

## Features

- **Match Statistics Display** - View comprehensive player and team stats from TF2 logs
- **Shareable Links** - Generate shareable URLs to display specific matches
- **Stream Integration** - Designed for easy browser capture during live streams
- **Form Validation** - Client-side validation for log URL inputs

## Requirements

- Python 3.5 or higher
- pip (Python package manager)

## Installation

1. **Clone or download this repository**
   ```bash
   git clone https://github.com/n4ver/N4TV
   cd N4TV
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the application**
   ```bash
   python wsgi.py
   ```

2. **Open in browser**
   Navigate to `http://localhost` (or `http://127.0.0.1`)

3. **Submit a TF2 log URL**
   - Paste a logs.tf URL in the form (e.g., `https://logs.tf/1234567`)
   - Click submit to view formatted match statistics

4. **Share your broadcast**
   - Use Windows/browser capture to record the results page
   - Or share the generated link with others to view the same match data

## Project Structure

```
N4TV/
├── dashboard/
│   ├── __init__.py           # Flask app factory
│   ├── routes.py              # API endpoints for log processing
│   ├── common.py              # Utility functions
│   ├── Templates/
│   │   ├── base.html          # Base template
│   │   ├── index.html         # Home page with form
│   │   └── match.html         # Match statistics display
│   └── static/
│       ├── css/
│       │   └── style.css      # Styling for dashboard
│       └── js/
│           └── validate_form.js # Client-side validation
├── wsgi.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── real_aliases.json          # Player name aliases mapping
└── README.md                  # This file
```

## API Integration

The dashboard fetches match data from the **logs.tf API**:
- Endpoint: `https://logs.tf/api/v1/log/{LOG_ID}`
- Handles rate limiting (429 responses) with automatic retry logic
- Processes player statistics and team information

## Configuration

The application runs on `localhost:80` by default. To modify the host or port, edit the `wsgi.py` file:

```python
app.run(host="127.0.0.1", port=80)
```

## Player Aliases

The `real_aliases.json` file stores mappings of player IDs to their display names for better readability in the statistics display.

## Browser Capture for Streaming

For best streaming results:
1. **Windows Capture** - Capture the entire results page window
2. **Browser Source** - Use the shareable link in OBS/Streamlabs as a browser source

## Troubleshooting

- **Port 80 already in use** - Change the port in `wsgi.py` to an available port (e.g., 5000)
- **Log not found** - Ensure the logs.tf URL is valid and the match data is publicly available
- **Rate limited** - The app automatically retries after 5 seconds when rate limited by logs.tf

## Technologies Used

- **Backend**: Flask 2.0.2
- **Frontend**: HTML5, CSS3, JavaScript
- **API Integration**: requests library
- **Data Processing**: Python 3.5+

## License

No license specified. Please add a LICENSE file if you plan to distribute this project.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

---
