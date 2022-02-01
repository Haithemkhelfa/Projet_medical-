SELECT date, sum(prod_price*prod_qty*1000) as ventes 
FROM my_table7 
WHERE YEAR(date)=2019  
GROUP BY date;

