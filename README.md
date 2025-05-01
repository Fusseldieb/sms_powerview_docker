# SMS PowerView [Docker]

Quick and dirty solution to run the "SMS PowerView" Java app inside a docker container.
Given your system exposes `/dev/ttyUSB0` when plugging in a compatible UPS, it should straight up work. Just start the container, that's all.

![smspowerview](https://github.com/Fusseldieb/sms_powerview_docker/blob/main/smspowerview.png)

---

### Features

- Provides the official SMS PowerView dashboard
- Provides a JSON endpoint to the system monitor - great for use in third-party software, such as Home Assistant, etc.
- Latest known version of SMS PowerView
- Internal known-working database
- Keeps the host system free of dependencies thanks to Docker

### How do I run it?
- Simply download this repo or clone it
- Copy `.env.example` to `.env` and put in your Serial port. If on Linux, it's likely `/dev/ttyUSB0`, on Windows `COMx` (**x** being a number). Leave blank for no connection.
- Execute: `docker compose up --build -d`. In a few moments it should then come up at `localhost:8080
`.
By default, SMS PowerView listens on port `8080` and the JSON Endpoint on port `5000`. Feel free to re-route it via the `.env` file though. Use the `.env.example` as a reference.

Stopping the container is as easy as using `docker compose down`.

### JSON Endpoint

`http://<server>:5000/monitor`

```
{
  "info": {
    "alert": "Off",
    "battery": "Off",
    "high_power": "Off",
    "mobile_gateway": "Off",
    "power_grid": "Off",
    "self_test": "Off",
    "time_for_shutdown": "00:00:00",
    "ups": "Off"
  },
  "status": {
    "battery_charge": {
      "current": "0",
      "max": "0",
      "min": "0"
    },
    "input_voltage": {
      "current": "0",
      "max": "0",
      "min": "0"
    },
    "output_frequency": {
      "current": "0",
      "max": "0",
      "min": "0"
    },
    "output_voltage": {
      "current": "0",
      "max": "0",
      "min": "0"
    },
    "temperature": {
      "current": "0",
      "max": "0",
      "min": "0"
    },
    "ups_load": {
      "current": "0",
      "max": "0",
      "min": "0"
    }
  }
}
```

### Protecting using a password
If you want to protect the SMS PowerView interface with a password, you can do that. For that you'll need to also set the password in `.env` using the `WEB_PASSWORD` variable in order for JSON requests to authenticate correctly. 

### Starting over
As you might know, this application has a database, and with sufficiently wrong configurations you could get locked out. Therefore, to reset the state, just delete the `db` folder and restart the container, which will re-initialize the database to a known-good state.

### Developing
If you're changing files in the project structure, you may need to rebuild the image. If that's the case, run:
```
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Which devices are compatible?
Most likely most of their (older) lineup should. I'm using a "SMS Power Sinus II".

Further compatible devices, as per documentation: 
- New Station Expert
- Net 4+ Expert
- Power Vision NG
- Manager III Senoidal NG
- Power Sinus NG
- Atrium
- Atrium Rack
- Mirage
- Daker
- Sinus Triad NG
- Keor BR

Please open an Issue if there's any incorrect information.

### Why don't you use `nut` instead?
I've tried, but unfortunately, no driver is compatible with my particular model. It could be reverse-engineered from PowerView, but I hadn't time for that. 

### 'X' doesn't work! What gives?
This project wasn't actually tested on other machines. I just needed a quick way to spin this up without making my host system messy with Java and other dependencies, so I 'made it work' and shared it, so it could be useful for more people.
Therefore, if you have any suggestions, please make a PR!
I know, the code isn't the prettiest you've seen in your life, and it lacks stuff, but it works.

### Other remarks
Special thanks to 'Sampayu': https://ubuntuforum-br.org/index.php?topic=114513.0

---

This 'project' is in no way, shape of form associated with Legrand or SMS. Use it at your own risk.
