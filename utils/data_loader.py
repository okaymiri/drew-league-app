"""
data_loader.py — Central data loading utility.
Loads all CSV files and provides clean DataFrames to every page.
"""
import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def _load(filename):
    path = os.path.join(DATA_DIR, filename)
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        return pd.DataFrame()


def load_teams():
    return _load("teams.csv")


def load_players():
    return _load("players.csv")


def load_games():
    df = _load("games.csv")
    if not df.empty:
        df["game_date"] = pd.to_datetime(df["game_date"])
    return df


def load_highlights():
    return _load("highlights.csv")


def load_podcasts():
    df = _load("podcasts.csv")
    if not df.empty:
        df["release_date"] = pd.to_datetime(df["release_date"])
    return df


def load_merch():
    return _load("merch.csv")


def load_sponsors():
    return _load("sponsors.csv")


def load_memberships():
    return _load("memberships.csv")


def load_tickets():
    return _load("tickets.csv")


def get_team_name(teams_df, team_id):
    """Return team name given team_id."""
    row = teams_df[teams_df["team_id"] == team_id]
    if not row.empty:
        return row.iloc[0]["name"]
    return "TBD"


def get_player_name(players_df, player_id):
    """Return player name given player_id."""
    row = players_df[players_df["player_id"] == player_id]
    if not row.empty:
        return row.iloc[0]["name"]
    return "Unknown"


def get_standings(teams_df):
    """Return teams sorted by win percentage."""
    df = teams_df.copy()
    df["win_pct"] = df["wins"] / (df["wins"] + df["losses"])
    return df.sort_values("win_pct", ascending=False).reset_index(drop=True)


def get_stat_leaders(players_df, stat="points_per_game", top_n=5):
    """Return top N players in a given stat."""
    return players_df.nlargest(top_n, stat)[["name", "team_id", "position", stat]].reset_index(drop=True)
