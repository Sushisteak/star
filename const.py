DOMAIN = "STAR"

CONF_API_KEY = "api_key"
CONF_UPDATE_INTERVAL = "update_interval"
DEFAULT_UPDATE_INTERVAL = 60  # secondes
CONF_BUS_NUMBER = "bus_number"
CONF_STOP = "stop"
CONF_DIRECTION = "direction"

LINE_API_URL = "https://data.explore.star.fr/api/explore/v2.1/catalog/datasets/tco-bus-topologie-lignes-td/records?select=nomcourt%2Cnomlong&where=nomfamillecommerciale%3D%27CHRONOSTAR%27%20OR%20%27Urbaine%27%20OR%20%27Inter-quartiers%27%20OR%20%27M%C3%A9tropolitaine%27&order_by=nomcourt&limit=100&offset=0&timezone=Europe%2FParis&include_links=false&include_app_metas=false"
DIRECTIONS_API_URL = "https://data.explore.star.fr/api/explore/v2.1/catalog/datasets/tco-bus-topologie-parcours-td/records?select=nomcourtligne%2C%20id%2C%20nomarretarrivee%2C%20libellelong%2C%20type&where=nomcourtligne%3D%27{ligne}%27&limit=100&offset=0&timezone=UTC&include_links=false&include_app_metas=false"
ARRETS_API_URL = "https://data.explore.star.fr/api/explore/v2.1/catalog/datasets/tco-bus-topologie-dessertes-td/records?select=nomcourtligne%2C%20nomarret%2C%20idparcours&where=idparcours%3D%27{parcours}%27&order_by=ordre&limit=100&offset=0&timezone=UTC&include_links=false&include_app_metas=false"
HORAIRE_API_URL = "https://data.explore.star.fr/api/explore/v2.1/catalog/datasets/tco-bus-circulation-passages-tr/records?select=depart%2Cidbus&where=nomcourtligne%3D%27{bus_number}%27%20AND%20nomarret%3D%27{stop}%27%20AND%20precision%3D%27Temps%20r%C3%A9el%27%20AND%20destination%3D%27{direction}%27&order_by=depart&limit=2&offset=0&timezone=Europe%2FParis&include_links=false&include_app_metas=false&apikey={api_key}"
COORDINATES_BUS_API_URL = "https://data.explore.star.fr/api/explore/v2.1/catalog/datasets/tco-bus-vehicules-position-tr/records?select=coordonnees&where=idbus%3D%27{idbus}%27&limit=10&offset=0&timezone=UTC&include_links=false&include_app_metas=false&apikey={api_key}"