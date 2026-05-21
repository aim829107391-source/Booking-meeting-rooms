# 1. NovaMeet

## 2. Description
NovaMeet is a premium dark-themed web platform for smart meeting room and studio booking. The system allows users to view available rooms with their capacity, select specific dates and times, and securely books reservations via an integrated database, preventing double bookings (overbooking).

## 3. Technologies Used
* **Backend:** Python, Flask framework
* **Database:** SQLite3
* **Frontend:** HTML5, CSS3 (Custom Premium Loft Design)
* **Fonts:** Playfair Display, Montserrat

## 4. Installation
Follow these steps to set up the project locally:

1. Clone or download the project folder.
2. Open the project folder in Visual Studio Code.
3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   ```
4. Activate the virtual environment:
   * **Windows:** `.venv\Scripts\activate`
   * **macOS/Linux:** `source .venv/bin/activate`
5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 5. How to Run
To start the local web server, run the following command in your terminal:
```bash
python app.py
```
After running, open your browser and navigate to: `http://127.0.0`

## 6. Project Features & Examples
* **Dynamic Room List:** Displays 5 premium rooms directly fetched from the SQLite database.
* **Smart Booking System:** Automatically pre-selects the room when clicking "Book Now" from the main page.
* **Overbooking Protection:** If a user tries to book an already reserved room for the exact same date and time, the system blocks the request and displays a security notice.

## 7. Screenshots
*(To display your screenshots, save your images into the `static` folder and link them here)*

### Main Page:
![Main Page Layout](static/main_page_screenshot.png)

### Booking Page:
![Booking Form Layout](static/booking_page_screenshot.png)

