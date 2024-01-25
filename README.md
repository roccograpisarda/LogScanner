# LogScanner
<p align="center">
  <img src="src/imgs/LogScanner_icon.png" alt="LogScanner Icon" width="100" height="100">
</p>

##

LogScanner is a tool designed for extracting and analyzing intents and entities from Botium execution log files. 

## How to Use It

### Extracting Covered Intents
To extract the covered intents from your log files, execute the `get_intents_infos.py` script. The results will be stored in the `/results/intents` directory.
```bash
python get_intents_infos.py
```

### Extracting Covered Entities

To extract the covered entities from your log files, execute the `get_entities_infos.py` script. The results will be stored in the `/results/entities` directory.
```bash
python get_entities_infos.py
```
## Installation

```bash
# Clone the repository
git clone https://github.com/roccograpisarda/LogScanner.git
# Navigate to the repository directory
cd LogScanner
```

## Tested Chatbots

LogScanner has been tested with the following chatbots.

| Chatbot Name | Description | Source |
|--------------|-------------|--------|
| [E-Commerce](https://github.com/roccograpisarda/modified-chatbot-source-files/tree/main/Kommunicate/ecommerce-dialogflow) |provides support for the products of an e-commerce.| Kommunicate |
| [RoomReservation](https://github.com/roccograpisarda/modified-chatbot-source-files/tree/main/Dialogflow/Charm/room-reservation-dialogflow) |room management and reservation.| Charm Repository |
| [Weather Forecast](https://github.com/roccograpisarda/modified-chatbot-source-files/tree/main/Dialogflow/weather-forecast-dialogflow) | provides weather forecasts for the specified location. | Dialogflow |
| [Currency-converter](https://github.com/roccograpisarda/modified-chatbot-source-files/tree/main/Dialogflow/currency-converter-dialogflow) | provides the value from one currency to another at the current exchange rate. | Dialogflow |
| [Temperature-converter](https://github.com/roccograpisarda/modified-chatbot-source-files/tree/main/Dialogflow/temperature-converter-dialogflow) |gives the temperature from Celsius to Fahrenheit and vice versa. | Dialogflow |
| [G-Calendar appointment scheduler](https://github.com/roccograpisarda/modified-chatbot-source-files/tree/main/Dialogflow/gcalendar-scheduler-dialogflow) |allows one to make an appointment and mark it in Google Calendar. | Dialogflow |
| [News](https://github.com/roccograpisarda/modified-chatbot-source-files/tree/main/Dialogflow/news-dialogflow) | provides news of the specified gender and country. | Dialogflow |


## Contributing

If you wish to contribute to this repository, follow these steps:
1. Fork this repository.
2. Make your changes to the desired script.
3. Submit a pull request with a detailed description of your modifications.

## Issue Reporting

If you encounter issues or want to report bugs related to the modified chatbots in this repository, open a new issue in the source repository of the respective chatbot.
