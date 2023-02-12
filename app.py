import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

from app_main import app
if __name__ == '__main__':
    app.run(debug = False, port = 8000)