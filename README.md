# Project2: Commerce

### E-commerce Auction WebSite 

This project is an e-commerce auction website similar to eBay, developed using Django, a Python web framework.

#### Description

The website allows users to create auction listings, place bids on existing listings, add listings to a watchlist, and comment on listings. Additionally, users can browse active listings, filter listings by categories, and manage their own listings and activities through an intuitive interface.

#### Key Features

- **Listing Creation**: Users can create new auction listings with details such as title, description, initial bid, optional image, and category.
  
- **Active Listing Exploration**: Users can view all active auction listings on the website's homepage, enabling them to discover new buying opportunities.
  
- **Listing Details**: Upon clicking on a specific listing, users can view detailed information about the listing, including the current price and the ability to place bids, add to watchlist, and comment.

- **Watchlist**: Users can keep track of listings they're interested in by adding them to their watchlist. They can also easily access these listings from their profile.

- **Listing Categorization**: Users can browse listings by categories, making it easier to find specific products of interest.

- **Admin Interface**: Site administrators have access to a Django admin interface to manage all listings, comments, and bids on the site.


## Developed using:

- Django
- Python
- HTML
- CSS
- Jinja
- SQL
- Bootstrap

## Run Locally

### Clone the project

```bash
git clone https://github.com/Alex000127/cs50w-project2.git
```

### Set up the virtual environment (optional)

```bash
pip install virtualenv
```

```bash
python -m venv env
```
or
```bash
virtualenv env
```

```bash
.\env\Scripts\activate
```

### Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Navigate to the project directory

```bash
cd cs50w-project2
```

### Apply migrations

```bash
python manage.py migrate
```

### Start the server

```bash
python manage.py runserver
```

## Author

- [Alexandra Salazar](https://github.com/Alex000127)
