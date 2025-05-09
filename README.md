
# E-commerce Store API
This project is an e-commerce API that allows users to add items to their cart, checkout, and apply discount codes. It also includes admin functionality to generate discount codes and retrieve purchase statistics. The project is built with Django REST Framework (DRF).

## Features
- Add items to the cart
- Checkout and apply discount codes
- Admin API for generating discount codes and retrieving purchase statistics
- Simple in-memory storage (No database required)

## Technology Stack
- Python 3.x
- Django
- Django REST Framework (DRF)
- In-memory storage (No database)

## Project Setup
### Prerequisites

Make sure you have the following installed:

- [Python 3.7+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/) (Python's package installer)
- [git](https://git-scm.com/downloads) (for cloning the repository)
- [Postman](https://www.postman.com/downloads/) (Optional, for testing the API)

### Installation Steps

Follow the steps below to set up and run the project:

#### Step 1: Clone the repository

Start by cloning the repository to your local machine:

```bash
git  clone  https://github.com/upendra-is-dev/ecommerce-api-assignment.git
cd  ecommerce-store-api
```  
  
## Set up the virtual environment

python  version  =  3.9

1.  **Create  virtual-environment**
	-  If  virtualenv  is  installed
	-  virtualenv  -p  python(your  python  version) environment-name
	-  If  virtualenv  is  not  installed,  install  this  using  `pip install virtualenv`

2.  **Activate  Virtualenv**
	-  source  environment-name/bin/activate

3.  **Install  requirements.txt**
	-  pip3  install  -r  requirements.txt

4.  **Run  Test  Cases**  -  `python manage.py test`
5.  **Run  Project  Using**  -  `python manage.py runserver`

## Postman Collection

This  repository  includes  a  Postman  collection  to  help  you  test  the  API  endpoints  easily.

### Import the Collection

	1.  Open  Postman.
	2.  Click  on  Import in the top-left corner.
	3.  Choose  the File tab.
	4.  Upload  the  `your-collection-name.json`  file  located  in  this  repository (`./path/to/your-collection.json`).
	5.  Click Import to  add  it  to  your  Postman  workspace.