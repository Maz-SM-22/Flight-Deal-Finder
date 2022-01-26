import datetime as dt 
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from user import User

data_controller = DataManager()
search_tool = FlightSearch()
alert_tool = NotificationManager()
user_manager = User(None, None, None)

def get_destination_codes(): 
    for city in cities: 
        iata_code = search_tool.get_iata_code(city)
        city_index = cities.index(city)
        data_controller.edit_rows(city_index, iata_code)

def get_user(): 
    name = input('What is your first name? ')
    surname = input('What is your surname? ')
    email_first_entry = input('Please enter your email: ')
    email_second_entry = input('Type your email again to confirm: ')
    if email_first_entry == email_second_entry: 
        name = name
        surname = surname 
        email = email_first_entry
        return user_manager.add_user(User(name, surname, email))
    else: 
        print('Email addresses do not match \nPlease try again')
        get_user()

data = data_controller.read_rows()
cities = [item['city'] for item in data]
price_lookup = {item['iataCode']: {item['city']: item['lowestPrice']} for item in data}
iata_codes = [item['iataCode'] for item in data] 

current_date = dt.datetime.now().strftime('%d/%m/%Y')
six_month_date = (dt.datetime.now() + dt.timedelta(minutes=262800)).strftime('%d/%m/%Y')

def get_flight_text_alerts(): 
    for value in iata_codes: 
        search_params = {
            'fly_from': 'BCN', 
            'fly_to': value, 
            'date_from': current_date, 
            'date_to': six_month_date, 
            'nights_in_dst_from': 7, 
            'nights_in_dst_to': 28, 
            'flight_type': 'round',
            'one_for_city': 1,
            'max_stopovers': 0, 
            'curr': 'EUR'
        }
        flight_data = search_tool.search_flights(search_params)

        try: 
            flight_price = price_lookup[flight_data['cityCodeTo']][flight_data['cityTo']]
        except: 
            continue

        if flight_data['price'] < flight_price: 
            outward_date = flight_data['route'][0]['local_departure'].split('T')[0]
            return_date = flight_data['route'][1]['local_arrival'].split('T')[0]
            alert = alert_tool.create_notification(
                price=flight_data['price'], 
                destination=flight_data['cityCodeTo'], 
                iata=flight_data['flyTo'], 
                from_date=outward_date, 
                to_date=return_date
            )
            alert_tool.send_alert(alert)

def email_deals_to_all_users(): 
    for value in iata_codes: 
        search_params = {
            'fly_from': 'BCN', 
            'fly_to': value, 
            'date_from': current_date, 
            'date_to': six_month_date, 
            'nights_in_dst_from': 7, 
            'nights_in_dst_to': 28, 
            'flight_type': 'round',
            'one_for_city': 1,
            'max_stopovers': 0, 
            'curr': 'EUR'
        }
        flight_data = search_tool.search_flights(search_params)
        
        try: 
            flight_price = price_lookup[flight_data['cityCodeTo']][flight_data['cityTo']]
        except: 
            continue

        if flight_data['price'] < flight_price: 
            outward_date = flight_data['route'][0]['local_departure'].split('T')[0]
            return_date = flight_data['route'][1]['local_arrival'].split('T')[0]
            alert = alert_tool.create_notification(
                price=flight_data['price'], 
                destination=flight_data['cityCodeTo'], 
                iata=flight_data['flyTo'], 
                from_date=outward_date, 
                to_date=return_date
            )
            for email in user_manager.get_user_emails(): 
                alert_tool.send_email(alert, email)