"""
Analytics layer for MindTrack.

Uses Pandas to turn raw daily entries into trend data the dashboard
can render: rolling averages, streaks, and simple rule-based insights.
Kept separate from routes so the logic is unit-testable in isolation.
"""
import pandas as pd


def entries_to_dataframe(rows):
    """Convert sqlite3.Row objects into a tidy Pandas DataFrame."""
    df = pd.DataFrame([dict(r) for r in rows])
    if df.empty:
        return df
    df["entry_date"] = pd.to_datetime(df["entry_date"])
    df = df.sort_values("entry_date").reset_index(drop=True)
    return df


def compute_trends(df, window=7):
    """Compute rolling averages for mood and sleep."""
    if df.empty:
        return df
    df = df.copy()
    df["mood_rolling"] = df["mood"].rolling(window, min_periods=1).mean().round(2)
    df["sleep_rolling"] = df["sleep_hours"].rolling(window, min_periods=1).mean().round(2)
    return df


def compute_streak(df):
    """Count the current consecutive-day logging streak, most recent first."""
    if df.empty:
        return 0
    dates = pd.to_datetime(df["entry_date"]).dt.date.tolist()
    dates = sorted(set(dates), reverse=True)

    streak = 1
    for i in range(1, len(dates)):
        if (dates[i - 1] - dates[i]).days == 1:
            streak += 1
        else:
            break
    return streak


def compute_summary(df):
    """Produce headline stats and a simple rule-based insight message."""
    if df.empty:
        return {
            "avg_mood": None,
            "avg_sleep": None,
            "exercise_rate": None,
            "streak": 0,
            "insight": "Log your first entry to start seeing trends.",
        }

    avg_mood = round(df["mood"].mean(), 2)
    avg_sleep = round(df["sleep_hours"].mean(), 2)
    exercise_rate = round(df["exercised"].mean() * 100, 1)
    streak = compute_streak(df)

    insight = _generate_insight(df, avg_mood, avg_sleep, exercise_rate)

    return {
        "avg_mood": avg_mood,
        "avg_sleep": avg_sleep,
        "exercise_rate": exercise_rate,
        "streak": streak,
        "insight": insight,
    }


def _generate_insight(df, avg_mood, avg_sleep, exercise_rate):
    """Lightweight rule-based observation, not a diagnosis."""
    if len(df) < 3:
        return "Keep logging daily to unlock personalized trend insights."

    exercised_mood = df.loc[df["exercised"] == 1, "mood"].mean()
    rest_mood = df.loc[df["exercised"] == 0, "mood"].mean()

    if pd.notna(exercised_mood) and pd.notna(rest_mood) and exercised_mood - rest_mood >= 0.5:
        return "Your mood tends to be higher on days you exercise."
    if avg_sleep < 6:
        return "Your average sleep is under 6 hours — sleep is strongly linked to mood."
    if exercise_rate < 30:
        return "You've exercised on fewer than a third of logged days."
    return "Your mood and habits look fairly stable this period."
