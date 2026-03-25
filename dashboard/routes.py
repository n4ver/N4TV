"""Routes for TF2 log display and API interactions."""
import logging
import time
from typing import Dict, List, Tuple

import requests
from flask import render_template, request
from flask import current_app as app

from .common import extract_log_no, special_sort, load_json

logger = logging.getLogger(__name__)

# Configuration constants
LOGS_TF_API_BASE = "https://logs.tf/api/v1/log"
RATE_LIMIT_STATUS = 429
RATE_LIMIT_WAIT_SECONDS = 5
ALIASES_FILE = "real_aliases.json"


@app.route('/')
def index():
    """Render the home page with log input form."""
    return render_template('index.html')


@app.route('/log', methods=['GET', 'POST'])
def log() -> str:
    """Process TF2 log requests and display match statistics.
    
    Accepts log URL via POST form or GET parameter.
    
    Returns:
        Rendered match.html template with game statistics.
    """
    # Extract log URL from POST or GET request
    if request.method == 'POST':
        log_url = request.form.get('logsurl', '')
    else:
        log_url = request.args.get('l', '')
    
    # Extract and validate log number
    log_no = extract_log_no(log_url)
    if log_no == -1:
        logger.warning(f"Invalid log URL provided: {log_url}")
        return render_template('index.html', error="Invalid log URL"), 400 # type: ignore
    
    # Fetch log data from API with retry logic
    try:
        log_data = _fetch_log_data(log_no)
    except requests.RequestException as e:
        logger.error(f"Failed to fetch log data: {e}")
        return render_template('index.html', error="Failed to fetch log data"), 500 # type: ignore
    
    # Load player aliases and process data
    player_aliases = load_json(ALIASES_FILE)
    game_data, map_played, score = _process_log_data(player_aliases, log_data)
    
    sharelink = f"{request.base_url}?l={log_url}"
    return render_template('match.html', data=game_data, sharelink=sharelink,
                          map_played=map_played, score=score)


def _fetch_log_data(log_id: int) -> Dict:
    """Fetch log data from logs.tf API with rate limit handling.
    
    Args:
        log_id: The logs.tf log ID number
    
    Returns:
        JSON response data from logs.tf API
    
    Raises:
        requests.RequestException: If API request fails
    """
    api_url = f"{LOGS_TF_API_BASE}/{log_id}"
    response = requests.get(api_url, timeout=10)
    
    # Handle rate limiting with exponential backoff
    while response.status_code == RATE_LIMIT_STATUS:
        logger.info(f"Rate limited by logs.tf API, waiting {RATE_LIMIT_WAIT_SECONDS}s")
        time.sleep(RATE_LIMIT_WAIT_SECONDS)
        response = requests.get(api_url, timeout=10)
    
    response.raise_for_status()
    return response.json()


def _process_log_data(player_aliases: Dict[str, str], log_response: Dict) -> Tuple[List, str, List]:
    """Process raw log data into formatted game statistics.
    
    Args:
        player_aliases: Mapping of player IDs to display names
        log_response: Raw JSON response from logs.tf API
    
    Returns:
        Tuple of (formatted_data, map_name, [blue_score, red_score])
    """
    # Extract core data from response
    player_names = log_response.get("names", {})
    player_data = log_response.get("players", {})
    map_name = log_response.get("info", {}).get("map", "Unknown")
    scores = [
        log_response.get("teams", {}).get("Blue", {}).get("score", 0),
        log_response.get("teams", {}).get("Red", {}).get("score", 0)
    ]
    
    # Class order for TF2
    class_order_list = ['scout', 'soldier', 'pyro', 'demoman', 'heavyweapons',
                        'engineer', 'medic', 'sniper', 'spy']
    class_order_map = {class_name: idx for idx, class_name in enumerate(class_order_list)}
    
    # Organize players by team
    red_team_list = []
    blu_team_list = []
    
    for player_id in player_names:
        # Update aliases
        if player_id not in player_aliases:
            player_aliases[player_id] = player_names[player_id]
        
        player_class = player_data[player_id]["class_stats"][0]["type"]
        class_index = class_order_map.get(player_class, 0)
        
        if player_data[player_id]["team"] == "Blue":
            blu_team_list.append([player_id, class_index])
        elif player_data[player_id]["team"] == "Red":
            red_team_list.append([player_id, class_index])
    
    # Sort teams by class order
    red_team_list = special_sort(red_team_list)
    blu_team_list = special_sort(blu_team_list)
    
    # Initialize data and totals
    game_data = [[], [], [], []]  # [blu_players, red_players, blu_totals, red_totals]
    red_totals = [0, 0, 0, 0]
    blu_totals = [0, 0, 0, 0]
    
    # Process Red team players
    for player_id, _ in red_team_list:
        player_stats = [
            player_data[player_id]["kills"],
            player_data[player_id]["deaths"],
            player_data[player_id]["dapm"],
            player_data[player_id]["hr"],
            player_aliases[player_id],
            player_data[player_id]["class_stats"][0]["type"]
        ]
        game_data[1].append(player_stats)
        
        # Update totals
        red_totals[0] += player_stats[0]  # kills
        red_totals[1] += player_stats[1]  # deaths
        red_totals[2] += player_data[player_id]['dmg']  # damage
        red_totals[3] += player_stats[3]  # healing rate
    
    # Process Blue team players
    for player_id, _ in blu_team_list:
        player_stats = [
            player_data[player_id]["class_stats"][0]["type"],
            player_aliases[player_id],
            player_data[player_id]["kills"],
            player_data[player_id]["deaths"],
            player_data[player_id]["dapm"],
            player_data[player_id]["hr"]
        ]
        game_data[0].append(player_stats)
        
        # Update totals
        blu_totals[0] += player_stats[2]  # kills
        blu_totals[1] += player_stats[3]  # deaths
        blu_totals[2] += player_data[player_id]['dmg']  # damage
        blu_totals[3] += player_stats[5]  # healing rate
    
    game_data[2] = blu_totals
    game_data[3] = red_totals
    
    return game_data, map_name, scores
