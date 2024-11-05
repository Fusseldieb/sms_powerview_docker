# SMS PowerView [Docker]

Quick and dirty solution to run the "SMS PowerView" Java app inside a docker container.
Given your system exposes `/dev/ttyUSB0` when plugging in a compatible UPS, it should straight up work. Just start the container, that's all.

![smspowerview](https://github.com/Fusseldieb/sms_powerview_docker/blob/main/smspowerview.png)


### How do I run it?
Simply download this repo or clone it, and then execute: `docker compose up --build -d`. In a few moments, it should come up at `localhost:8080`.
By default, it listens on port `8080` and `/dev/ttyUSB0`. Feel free to re-route it via the `docker-compose.yml` file though.

### Which devices are compatible?
I'm not sure, but most likely most of their lineup should. I'm using a "SMS Power Sinus II".

### Why don't you use `nut` instead?
I've tried, but unfortunately, no driver is compatible with my particular model. It could be reverse-engineered from PowerView, but I hadn't time for that. 

### 'X' doesn't work! What gives?
This project wasn't actually tested on other machines. I just needed a quick way to spin this up without making my host system messy with Java and other dependencies, so I 'made it work' and shared it, so it could be useful for more people.
Therefore, if you have any suggestions, please make a PR!
I know, the code isn't the prettiest you've seen in your life, and it lacks stuff, but it works. The service, for example, is kept open by tailing /dev/null! ;)

#### Other remarks
The .tar.gz from their tool is from an older version of PowerView. There is no particular reason, though.

Special thanks to 'Sampayu': https://ubuntuforum-br.org/index.php?topic=114513.0

---

This 'project' is in no way, shape of form associated with Legrand or SMS. Use it at your own risk.
