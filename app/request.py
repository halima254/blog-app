import requests



def random_quote():
    
    
    get_quote = requests.get('http://quotes.stormconsultancy.co.uk/random.json').json()
    
    return get_quote