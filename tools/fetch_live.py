"""Fetch live profile data from GitHub (and optionally YouTube).

Writes:
  data/live.json               numbers the README cards are built from
  breakout/contributions.json  the contribution calendar the game plays on

Env:
  GITHUB_TOKEN        required (Actions provides it). A personal token with
                      read:user also counts private contributions.
  YOUTUBE_API_KEY     optional, with YOUTUBE_CHANNEL_ID, for the live
  YOUTUBE_CHANNEL_ID  subscriber count.

Run:  python3 tools/fetch_live.py
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROFILE = json.loads((ROOT / "data" / "profile.json").read_text(encoding="utf-8"))
USER = PROFILE["github_user"]

LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}

QUERY = """
query($login: String!, $cursor: String) {
  user(login: $login) {
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC, first: 100, after: $cursor,
                 orderBy: {field: PUSHED_AT, direction: DESC}) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes { name stargazerCount pushedAt isFork }
    }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel } }
      }
    }
  }
}
"""


def http_json(url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.loads(res.read().decode("utf-8"))


def graphql(token, variables):
    body = json.dumps({"query": QUERY, "variables": variables}).encode("utf-8")
    out = http_json(
        "https://api.github.com/graphql",
        data=body,
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": USER},
    )
    if out.get("errors"):
        raise RuntimeError(out["errors"])
    return out["data"]["user"]


def streaks(days):
    """Current and longest run of days with at least one contribution."""
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] > 0 else 0
        longest = max(longest, run)
    current = 0
    # today may not have a contribution yet; don't break the streak for it
    tail = days[:-1] if days and days[-1]["count"] == 0 else days
    for d in reversed(tail):
        if d["count"] == 0:
            break
        current += 1
    return current, longest


def fetch_github(token):
    user = graphql(token, {"login": USER, "cursor": None})
    repos = list(user["repositories"]["nodes"])
    page = user["repositories"]["pageInfo"]
    while page["hasNextPage"]:
        more = graphql(token, {"login": USER, "cursor": page["endCursor"]})
        repos += more["repositories"]["nodes"]
        page = more["repositories"]["pageInfo"]

    cal = user["contributionsCollection"]["contributionCalendar"]
    days = [
        {"date": d["date"], "count": d["contributionCount"], "level": LEVELS.get(d["contributionLevel"], 0)}
        for w in cal["weeks"] for d in w["contributionDays"]
    ]
    current, longest = streaks(days)
    own = [r for r in repos if not r["isFork"]]
    by_name = {r["name"].lower(): r for r in repos}
    projects = {}
    for key, repo in PROFILE.get("project_repos", {}).items():
        r = by_name.get(repo.lower())
        if r:
            projects[key] = {"repo": r["name"], "stars": r["stargazerCount"], "pushed": r["pushedAt"]}
    last = own[0] if own else None
    return {
        "followers": user["followers"]["totalCount"],
        "public_repos": user["repositories"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in own),
        "contributions_year": cal["totalContributions"],
        "current_streak": current,
        "longest_streak": longest,
        "last_push": {"repo": last["name"], "at": last["pushedAt"]} if last else None,
        "projects": projects,
    }, days


def fetch_youtube():
    key, channel = os.environ.get("YOUTUBE_API_KEY"), os.environ.get("YOUTUBE_CHANNEL_ID")
    if not key or not channel:
        return None
    q = urllib.parse.urlencode({"part": "statistics", "id": channel, "key": key})
    try:
        out = http_json(f"https://www.googleapis.com/youtube/v3/channels?{q}")
        stats = out["items"][0]["statistics"]
        if stats.get("hiddenSubscriberCount"):
            return None
        return int(stats["subscriberCount"])
    except Exception as e:  # keep the rest of the update going
        print("youtube fetch failed:", e, file=sys.stderr)
        return None


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("GITHUB_TOKEN is not set")
    live, days = fetch_github(token)
    live["youtube_subscribers"] = fetch_youtube()
    live["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")

    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "live.json").write_text(json.dumps(live, indent=2) + "\n", encoding="utf-8")
    cal = {
        "user": USER,
        "updated": date.today().isoformat(),
        "total": live["contributions_year"],
        "days": [{"date": d["date"], "level": d["level"]} for d in days],
    }
    (ROOT / "breakout" / "contributions.json").write_text(json.dumps(cal, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in live.items() if k != "projects"}, indent=2))


if __name__ == "__main__":
    main()
