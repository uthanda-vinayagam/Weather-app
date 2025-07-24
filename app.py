from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "b89667a75c56a97b95aa22bd6ef45139"  
@app.route("/", methods=["GET", "POST"])
def index():
    city = "Tirunelveli"  
    weather_data = None

    if request.method == "POST":
        city = request.form.get("city")

    
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    geo_response = requests.get(geo_url)
    geo_json = geo_response.json()

    if not geo_json:
        return render_template("error.html", message="City not found.")

    lat = geo_json[0]["lat"]
    lon = geo_json[0]["lon"]

    
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(forecast_url)
    forecast_json = response.json()

    if "list" not in forecast_json:
        return render_template("error.html", message="Weather data not available.")

    weather_data = {
        "city": geo_json[0]["name"],
        "country": geo_json[0]["country"],
        "forecast": forecast_json["list"][:5], 
        "current": forecast_json["list"][0]
    }

    return render_template("index.html", weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
