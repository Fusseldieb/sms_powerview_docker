# SMS PowerView [Docker]

Quick and dirty solution to run the "SMS PowerView" Java app inside a docker container.

### How do I run it?

Simply download this repo or clone it, and then execute: `docker compose up --build -d`. In a few moments, it should come up at `localhost:8080`.
By default, it listens on port `8080` and `/dev/ttyUSB0`. Feel free to re-route it via the `docker-compose.yml` file though.

### 'X' doesn't work! What gives?
This project wasn't actually tested on other machines. I just needed a quick way to spin this up without making my host system messy with Java and other dependencies, so I 'made it work' and shared it, so it could be useful for more people.
Therefore, if you have any suggestions, please make a PR!
I know, the code isn't the prettiest you've seen in your life, and it lacks stuff, but it works. The service, for example, is kept open by tailing /dev/null! Feel free to adapt it to your needs.

---

This 'project' is in no way, shape of form associated with Legrand or SMS. Use it at your own risk.
