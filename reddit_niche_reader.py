import os
import sys
import logging
from typing import List
from dotenv import load_dotenv
import praw
from praw.exceptions import RedditAPIException
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

# Initialize Rich console and logging
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='arc_reader.log'
)

class ArcNicheFeedReader:
    """
    A read-only CLI tool for personal browsing of niche subreddits.
    Provides keyword filtering of new posts for efficient information retrieval.
    NO data is stored, archived, or exported.
    """
    def __init__(self):
        load_dotenv()
        
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        # Best practice User-Agent for API compliance
        self.user_agent = os.getenv("REDDIT_USER_AGENT", "windows:arc-niche-feed-reader:v1.0.0 (by /u/your_username)")
        
        if not self.client_id or not self.client_secret:
            console.print("[bold red]Error:[/] Missing API credentials in .env file.")
            sys.exit(1)

        try:
            # Initialize PRAW using only 'read' capabilities
            self.reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent
            )
            if not self.reddit.read_only:
                logging.warning("Script is not operating in strict read-only mode.")
        except Exception as e:
            console.print(f"[bold red]Initialization Error:[/] {e}")
            logging.error(f"Failed to initialize PRAW: {e}")
            sys.exit(1)

    def display_posts(self, posts: List, category: str, subreddit: str):
        """Renders fetched metadata for immediate on-screen display and discards it."""
        if not posts:
            console.print(f"[yellow]No posts found matching criteria in r/{subreddit}.[/]")
            return

        table = Table(
            title=f"[bold cyan]{category} Posts in r/{subreddit}[/]", 
            show_header=True, 
            header_style="bold magenta"
        )
        table.add_column("Title", style="white", overflow="fold")
        table.add_column("Author", style="green", justify="center")
        table.add_column("Score", style="yellow", justify="right")

        for post in posts:
            author = post.author.name if post.author else "[deleted]"
            title_link = f"[link=https://www.reddit.com{post.permalink}]{post.title}[/link]"
            table.add_row(title_link, f"u/{author}", str(post.score))

        console.print(table)
        console.print("\n")

    def fetch_subreddit_data(self, subreddit_name: str, keyword: str = ""):
        """Fetches latest post titles and metadata for efficient browsing (low intensity)."""
        try:
            with console.status(f"[bold green]Fetching data from r/{subreddit_name}...[/]"):
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Fetch recent new posts (limit to 15 to keep request volume low)
                new_posts = list(subreddit.new(limit=15))
                
                if keyword:
                    # Keyword-based filtering of new posts
                    filtered_posts = [
                        p for p in new_posts 
                        if keyword.lower() in p.title.lower() or 
                        (hasattr(p, 'selftext') and keyword.lower() in p.selftext.lower())
                    ]
                    # Discard excess, display up to 5 immediate results
                    posts_to_display = filtered_posts[:5]
                    category_label = f"NEW (Filtered by '{keyword}')"
                else:
                    posts_to_display = new_posts[:5]
                    category_label = "NEW"

            self.display_posts(posts_to_display, category_label, subreddit_name)
            logging.info(f"Fetched and displayed posts from r/{subreddit_name}. Keyword filter: '{keyword}'")

        except RedditAPIException as api_err:
            console.print(f"[bold red]Reddit API Error:[/] {api_err}")
            logging.error(f"API Error fetching r/{subreddit_name}: {api_err}")
        except Exception as e:
            console.print(f"[bold red]Error fetching r/{subreddit_name}[/]")
            logging.error(f"Error fetching r/{subreddit_name}: {e}")

    def run(self):
        """Main CLI loop for standalone private desktop workflow."""
        console.print(Panel.fit(
            "[bold cyan]arc-niche-feed-reader[/]\n"
            "Target communities: r/crm, r/SaaS, r/softwaredevelopment, r/cadcam\n"
            "Type 'q' or 'quit' to exit.",
            border_style="cyan"
        ))
        
        while True:
            sub = Prompt.ask("[bold yellow]Enter subreddit[/] (e.g., crm, SaaS)")
            if sub.lower() in ['q', 'quit', 'exit']:
                console.print("[dim]Exiting application...[/]")
                break
            
            sub = sub.replace("r/", "").strip()
            if not sub:
                continue
                
            keyword = Prompt.ask("[bold yellow]Enter keyword to filter by[/] (or press Enter to skip)")
            self.fetch_subreddit_data(sub, keyword.strip())


if __name__ == "__main__":
    app = ArcNicheFeedReader()
    app.run()
