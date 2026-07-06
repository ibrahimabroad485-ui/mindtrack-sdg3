"""
Chart rendering for MindTrack.

Generates a base64-encoded PNG chart of mood/sleep trends so the
dashboard can embed it directly without needing a static file route.
"""
import base64
import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def render_trend_chart(df):
    """Return a base64 PNG string plotting mood and rolling mood average."""
    if df.empty:
        return None

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["entry_date"], df["mood"], marker="o", label="Daily mood", alpha=0.5)
    ax.plot(df["entry_date"], df["mood_rolling"], linewidth=2, label="7-day rolling avg")
    ax.set_ylim(0, 10)
    ax.set_ylabel("Mood (1–10)")
    ax.set_title("Mood Trend Over Time")
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")
