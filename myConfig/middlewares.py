from scrapy import signals

from itemadapter import is_item, ItemAdapter

class RobotsTxtMiddleware:
    def __init__(self):
        self.forbidden_domains = set()

    def process_request(self, request, spider):
        # Check if the domain is in the forbidden list
        if any(domain in request.url for domain in self.forbidden_domains):
            spider.logger.info(f'Ignoring request to {request.url} due to forbidden robots.txt')
            raise IgnoreRequest(f'Forbidden by robots.txt at {request.url}')

    def process_response(self, request, response, spider):
        # Check if the response is for robots.txt
        if 'robots.txt' in request.url and response.status == 403:
            # Extract domain and add to forbidden list
            domain = request.url.split('/robots.txt')[0]
            self.forbidden_domains.add(domain)
            spider.logger.warning(f'Forbidden response for {request.url}, added {domain} to forbidden list')
            # Ignore the request for the robots.txt
            raise IgnoreRequest(f'Forbidden robots.txt at {request.url}')
        
        # Return the response if it's not a robots.txt or if it's allowed
        return response

    def process_exception(self, request, exception, spider):
        # Handle any exceptions that occur during processing
        pass        
