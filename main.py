import requests
from datetime import datetime
import smtplib

# Statement below is for debugging/testing purposes only, otherwise is_overhead will become true only during the
# specific times

# is_overhead = True

# Enter your own lat and long coordinates below
MY_LAT = 12.34567
MY_LONG = -89.01234

# Enter the email and password of the account the message will come from, can save as environment variables
my_email = "ENTER YOUR EMAIL"
password = "ENTER YOUR PASSWORD"


# This function sends a get request to the ISS API, which constantly provides lat/long data for where the ISS is.
def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    check_position = True

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Checks to see if your position is within +/- 5 degrees of the ISS position.
    while check_position:
        lat_overhead = abs(iss_latitude - MY_LAT)
        lng_overhead = abs(iss_longitude - MY_LONG)

        if lat_overhead <= 5 and lng_overhead <= 5:
            is_overhead = True
            check_position = False
    return is_overhead


# Sunrise-sunset API parameters
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

# Get request to the sunrise-sunset API to grab the times for that day.
sun_response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
sun_response.raise_for_status()
sun_data = sun_response.json()
sunrise = int(sun_data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(sun_data["results"]["sunset"].split("T")[1].split(":")[0])

# current time (hour)
time_now = datetime.now()
current_hour = time_now.hour


# If the ISS is close to your current position AND it is currently dark then send an email to tell you to look up.

def is_night():
    if current_hour >= sunset or current_hour <= sunrise:
        return True


# If it's dark enough and the ISS is overhead, an email will be sent to the "to_addrs" email, update for personal use.
# NOTICE: This code won't run until the the proper to and from email addresses are put in, they've been removed for public use.
if is_night and is_iss_overhead:
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs='email_address_to_notify@email.com',
                            msg=f"Subject:Look Up!!\n\nThe ISS is overhead, go look outside!")
