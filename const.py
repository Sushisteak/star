DOMAIN = "STAR"

CONF_API_KEY = "api_key"
CONF_UPDATE_INTERVAL = "update_interval"
DEFAULT_UPDATE_INTERVAL = 60  # secondes
CONF_BUS_NUMBER = "bus_number"
CONF_STOP = "stop"
CONF_DIRECTION = "direction"

LINE_API_URL = "https://data.explore.star.fr/api/explore/v2.1/catalog/datasets/tco-bus-topologie-li\
    gnes-td/records?select=nomcourt%2Cnomlong&where=nomfamillecommerciale%3D%27CHRONOSTAR%27%20OR%2\
        0%27Urbaine%27%20OR%20%27Inter-quartiers%27%20OR%20%27M%C3%A9tropolitaine%27&order_by=nomco\
            urt&limit=100&offset=0&timezone=Europe%2FParis&include_links=false&include_app_metas=fa\
                lse"
DIRECTIONS_API_URL = "https://data.explore.star.fr/api/explore/v2.1/catalog/datasets/tco-bus-topolo\
    gie-parcours-td/records?select=nomcourtligne%2C%20id%2C%20nomarretarrivee%2C%20libellelong%2C%2\
        0type&where=nomcourtligne%3D%27{ligne}%27&limit=100&offset=0&timezone=UTC&include_links=fal\
            se&include_app_metas=false"
ARRETS_API_URL = "https://data.explore.star.fr/api/explore/v2.1/catalog/datasets/tco-bus-topologie-\
    dessertes-td/records?select=nomcourtligne%2C%20nomarret%2C%20idparcours&where=idparcours%3D%27{\
        parcours}%27&order_by=ordre&limit=100&offset=0&timezone=UTC&include_links=false&include_app\
            _metas=false"
HORAIRE_API_URL = "https://data.explore.star.fr/api/explore/v2.1/catalog/datasets/tco-bus-circulati\
    on-passages-tr/records?select=depart%2Cidbus&where=nomcourtligne%3D%27{bus_number}%27%20AND%20n\
        omarret%3D%27{stop}%27%20AND%20precision%3D%27Temps%20r%C3%A9el%27%20AND%20destination%3D%2\
            7{direction}%27&order_by=depart&limit=2&offset=0&timezone=Europe%2FParis&include_links=\
                false&include_app_metas=false&apikey={api_key}"
COORDINATES_BUS_API_URL = "https://data.explore.star.fr/api/explore/v2.1/catalog/datasets/tco-bus-v\
    ehicules-position-tr/records?select=coordonnees&where=idbus%3D%27{idbus}%27&limit=10&offset=0&t\
        imezone=UTC&include_links=false&include_app_metas=false&apikey={api_key}"