from django.core.management.base import BaseCommand
from sbapi.scripts.match_scraper import MatchScraper

class Command(BaseCommand):
    help = 'Get match data and stores it in the database'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='WS match URL to scrape')

    def handle(self, *args, **options):
        url = options['url']
        
        self.stdout.write(self.style.SUCCESS('Starting match scraping...'))
        
        try:
            scraper = MatchScraper()
            match_data = scraper.scrape_match(url)
            processed_data = scraper.process_match_data(match_data)
            
            self.stdout.write(self.style.SUCCESS(
                f'Successfully scraped and processed match data. \n'
                f'Events: {len(processed_data["events"])} rows\n'
                f'Match info stored in database.'
            ))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error scraping match: {str(e)}'))