# Market-Point E-commerce store using Django

MarketPoint is an e-commerce website built with Django.

<h3>Features</h3><br>
<li>Browse and search products</li>
<li>Add/remove products to cart</li>
<li>Checkout and make payments</li>
<li>User authentication</li>
<li>Admin portal to manage products, orders, etc</li>
<br>

<b>Installation</b><br>
<br>
Clone the repo
```
git clone https://github.com/<your_username>/marketpoint.git
```
Install requirements
```
pip install -r requirements.txt
```
Run migrations
```
python manage.py migrate
```
Create superuser
```
python manage.py createsuperuser
```
Run development server
```
python manage.py runserver
```
The app should now be running at http://localhost:8000

<b>Usage</b>
<li>Browse products and add them to cart<br>
<li>Create an account or login to checkout<br>
<li>Use Razorpay to make payments<br>
<li>Access admin site at http://localhost:8000/admin to manage products, orders, etc</li>  <br>

<b>Customization</b>
<li>Set Razorpay keys in settings.py</li>
<li>Modify models in apps/products and apps/orders</li>
<li>Add new apps for coupons, user profile etc.</li><br>

<h2>Demo Images</h2>

<h3>Front Page</h3>

![image](https://github.com/Abhishekservi/MarketPoint-Ecommerce-Store-using-Django/assets/90319592/bd786f27-6373-48a8-806e-ae5c8306a911)


<h3>Shop Page</h3>

![image](https://github.com/Abhishekservi/MarketPoint-Ecommerce-Store-using-Django/assets/90319592/cd0eadb5-f989-4077-96f5-0f028710de1a)


<b>License</b>

The source code is released under an MIT License.

<b>Credits</b>

MarketPoint was created by Abhishek Choudhary
