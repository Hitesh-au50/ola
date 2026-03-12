-- Display all records from the dataset
SELECT * 
FROM ola.ola_ride;

-- Insight:This query displays the entire OLA ride dataset, helping analysts understand the data structure and verify that all ride records are correctly stored in the database.

-- Count the total number of rows in the dataset
SELECT COUNT(*) 
FROM ola.ola_ride;

-- Insight:This query calculates the total number of ride records in the dataset, helping measure the overall volume of OLA bookings available for analysis.

-- 1. Retrieve all successful bookings
-- This query filters rides where the booking status is marked as 'Success'
SELECT *
FROM ola.ola_ride
WHERE Booking_Status = 'Success';

-- Insight: This query retrieves all rides that were successfully completed, helping analyze completed bookings and overall service performance.

-- 2. Find the average ride distance for each vehicle type
-- GROUP BY is used to calculate the average ride distance for each vehicle category
SELECT Vehicle_Type,
       AVG(Ride_Distance) AS avg_ride_distance
FROM ola.ola_ride
GROUP BY Vehicle_Type;

-- Insight: This query calculates the average ride distance for each vehicle type, helping identify which vehicle categories are typically used for longer trips.

-- 3. Get the total number of rides cancelled by customers
-- Counts all rides where the booking status indicates customer cancellation
SELECT COUNT(*) AS total_customer_cancellations
FROM ola.ola_ride
WHERE Booking_Status = 'Canceled by Customer';

-- Insight: This query counts the total number of rides cancelled by customers, helping identify customer-driven cancellation trends in the OLA platform.

-- 4. List the top 5 customers who booked the highest number of rides
-- GROUP BY counts rides per customer and ORDER BY sorts them in descending order
SELECT Customer_ID,
       COUNT(*) AS total_rides
FROM ola.ola_ride
GROUP BY Customer_ID
ORDER BY total_rides DESC
LIMIT 5;

-- Insight: This query identifies the top 5 customers with the highest number of rides, helping recognize frequent users who contribute most to bookings.

-- 5. Get the number of rides cancelled by drivers due to personal or car-related issues
-- Filters rows where driver cancellation reason is personal or vehicle related
SELECT COUNT(*) AS driver_cancelled_rides
FROM ola.ola_ride
WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue';

-- Insight: This query counts the number of rides cancelled by drivers due to personal or car-related issues, helping identify operational problems affecting ride completion.

-- 6. Find the maximum and minimum driver ratings for Prime Sedan bookings
-- Aggregation functions are used to find highest and lowest ratings
SELECT MAX(Driver_Ratings) AS max_rating,
       MIN(Driver_Ratings) AS min_rating
FROM ola.ola_ride
WHERE Vehicle_Type = 'Prime Sedan';

-- Insight: This query finds the highest and lowest driver ratings for Prime Sedan rides, helping evaluate service quality within this premium vehicle category.

-- 7. Retrieve all rides where payment was made using UPI
-- Filters rides based on payment method
SELECT *
FROM ola.ola_ride
WHERE Payment_Method = 'UPI';

-- Insight: This query retrieves all rides where the payment was made using UPI, helping analyze the usage of digital payment methods among customers.

-- 8. Find the average customer rating for each vehicle type
-- Calculates mean customer rating grouped by vehicle category
SELECT Vehicle_Type,
       AVG(Customer_Rating) AS avg_customer_rating
FROM ola.ola_ride
GROUP BY Vehicle_Type;

-- Insight: This query calculates the average customer rating for each vehicle type, helping evaluate customer satisfaction across different ride categories.

-- 9. Calculate the total booking value of rides completed successfully
-- SUM function calculates total revenue generated from successful rides
SELECT SUM(Booking_Value) AS total_successful_revenue
FROM ola.ola_ride
WHERE Booking_Status = 'Success';

-- Insight: This query calculates the total revenue generated from all successfully completed rides, helping measure the platform’s overall earnings from completed bookings.

-- 10. List all incomplete rides along with the reason
-- Retrieves booking ID and reason where the ride was marked incomplete
SELECT Booking_ID,
       Incomplete_Rides_Reason
FROM ola.ola_ride
WHERE Incomplete_Rides = 'Yes';

--Insight: This query retrieves all incomplete rides along with their reasons, helping identify operational issues that prevent rides from being successfully completed.