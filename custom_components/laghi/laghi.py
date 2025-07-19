import datetime
from requests_html import HTMLSession


class Laghi:
    def __init__(self):
        """ Initializes the Laghi class to fetch lake data from laghi.net."""
        self._SESSION_URL = "https://laghi.net/Page/laghi"
        self._DATA_URL = "https://laghi.net/MappaConSegnaposti/BootWidgetData"
        self._POST_DATA = {"config": "370"}
        self._ID_LEVEL = 3  # "Livello" 
        self._ID_INFLOW = 4  # "Afflusso"
        self._ID_OUTFLOW = 5  # "Deflusso"
        self._ID_FILL = 6  # "Riempimento"

        self._session = HTMLSession()

    def _fetch_laghi_data(self):
        """Fetches data from the laghi.net REST API.
        Returns:
            dict: The data from the API.
            """

        self._session.get(self._SESSION_URL)
        response = self._session.post(self._DATA_URL, data=self._POST_DATA)

        try:
            data = response.json()
        except ValueError:
            data = None

        if data is None:
            return None

        if data["success"] == False:
            return None

        return data

    def _extract_lake_data(self, data):
        """ Extracts lake data from the fetched data.
        Args:
            data (dict): The data from the API.
        Returns:
            list: A list of dictionaries containing lake data.
        """

        data_list = data["data"]
        lakes = []

        for lake_object in data_list:
            lake_data = {
                "name": "",
                "fill":
                {
                    "value": 50,
                    "unit": "%",
                },
                "inflow": {
                    "value": 50,
                    "unit": "m³/s",
                },
                "outflow": {
                    "value": 50,
                    "unit": "m³/s",
                },
                "level": {
                    "value": 50,
                    "unit": "m",
                },
                "timestamp": 0
            }

            lake_data["name"] = lake_object["tooltip_config"]['titolo']
            serie_counter = 0
            for serie_data in lake_object["tooltip_config"]["series"]:

                if serie_data["id"] == self._ID_FILL:
                    unit = lake_object["tooltip_data"][serie_counter]["anagrafica_serie"]["UnMis"]
                    value = lake_object["tooltip_data"][serie_counter]["data_serie"][0]["val"]
                    datetime_str = lake_object["tooltip_data"][serie_counter]["data_serie"][0]["data"]
                    timestamp = int(datetime.datetime.strptime(
                        datetime_str, "%Y-%m-%d %H:%M").timestamp())
                    lake_data["fill"]["value"] = value
                    lake_data["fill"]["unit"] = unit
                    lake_data["timestamp"] = timestamp

                elif serie_data["id"] == self._ID_INFLOW:
                    unit = lake_object["tooltip_data"][serie_counter]["anagrafica_serie"]["UnMis"]
                    value = lake_object["tooltip_data"][serie_counter]["data_serie"][0]["val"]
                    lake_data["inflow"]["value"] = value
                    lake_data["inflow"]["unit"] = unit

                elif serie_data["id"] == self._ID_OUTFLOW:
                    unit = lake_object["tooltip_data"][serie_counter]["anagrafica_serie"]["UnMis"]
                    value = lake_object["tooltip_data"][serie_counter]["data_serie"][0]["val"]
                    lake_data["outflow"]["value"] = value
                    lake_data["outflow"]["unit"] = unit

                elif serie_data["id"] == self._ID_LEVEL:
                    unit = lake_object["tooltip_data"][serie_counter]["anagrafica_serie"]["UnMis"]
                    value = lake_object["tooltip_data"][serie_counter]["data_serie"][0]["val"]
                    lake_data["level"]["value"] = value
                    lake_data["level"]["unit"] = unit

                serie_counter += 1

            lakes.append(lake_data)

        return lakes

    def get_data(self)->list:
        """Fetches and extracts lake data.
        Returns:
            list: A list of dictionaries containing lake data.
        """
        data = self._fetch_laghi_data()
        if data is None:
            return []
        return self._extract_lake_data(data)

if __name__ == "__main__":
    laghi = Laghi()
    laghi_data = laghi.get_data()    
    print(laghi_data)
