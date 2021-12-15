# Capstone_1

Project Proposal-App for restaurateurs to track inventory and food cost levels

Overall Goals of Website-Allow restaurant operators the ability to easily track inventory levels of their product as well as have an inventory count (based in a perfect world)

Target User-Small-level restaurant owners/operators that are looking for an interactive tool to help keep track of food cost and inventory levels.

Data I Plan to Use-	Product Pricing-Local pricing of products used in restaurants. Users will be able to input purchases that interact with current inventory and a pre-set budget 
			Food Cost Calculation-After a day of sales, users will be able to input sales/pmix information into the app in order to see what food cost they ran for the day as well as their current inventory levels.
			Decreasing Budget-Users will be able to set a weekly budget for an “ideal” food cost that they wish to achieve. As they enter in purchases, their budget will reflect what they spent and give a breakdown of daily spending
			Sales forecasting-Users will be able to create a forecast for the week that will be used to create the ideal budget and food cost expectations. 



Database Schema - 
User Table - List of all users with user ID, username, password, restaurant name
Product Table - Lists all base ingredients used in a restaurant with their purchase price and current inventory levels. This table will also display case size of product and how much each individual food item costs (ex: 1 case of hotdog buns has 8 buns in a pack and sells for $2.99. Each individual bun costs $.37) - connected to the user table by User ID.
Menu Table - List of all menu items and their menu price connected to product table and lists all ingredients that go into making the menu item
Weekly Sales Forecast Table - Each day of the week is going to have a forecasted sales amount and an actual sales amount

API issues - Fluctuating pricing/out of stock ingredients. Having to find replacement items and still be able to account for the product correctly.

Sensitive Information - This app will have basic login information so there can be multiple different restaurants using the app at the same time

Functionality and user flow - When a new user signs up their restaurant for the app, they will have to set up their profile by inputting all of their raw ingredients and their menu. Each ingredient input into their profile will make a GET request to the API which will return price and pack size. 
After the ingredients table is complete, the user will have to create their menu on the app. This will pull data from the Product Table and generate how much each product will be to make.
Once their restaurant is set up, the user will be able to create a sales forecast for each day of the week and input an ideal food cost that they would like to achieve. The app will then produce a budget for the week.
As the week progresses, the user will input their sales and pmix data into the app, which will start to deplete the inventory and generate a food cost for the day. This will also deplete the budget that was generated by the app. The user will be able to see each day how they are doing at obtaining their goals. 
When the week is over, the app will generate a weekly food cost and budget information. 


Stretch goals -
 Create a continuous account of data - Restaurants keep data for years and rely on that data in order to accurately predict business.
Create app for real time applications -Create realistic days connected to an actual calendar so the app is more realistic
Account for waste- All of the numbers are based in a “perfect world”. This is considered a “theoretical food cost”. So I would like to find a way to account for a waste goal. Restaurant operators conduct physical inventory weekly or monthly in order to get an accurate grasp on how the business is running. So the reality of the results of the  inventory count will be different than what the app is saying. So I would like to allow for some waste allowance (2%-5%)

Api that I will be using is the Kroger API

Link to my database Schema design https://docs.google.com/spreadsheets/d/1mtUNDS5T0X6ZQ9L5My7RtincxkdQGabZ0YL7P_JuZkw/edit#gid=0
