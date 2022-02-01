SELECT date, sum(prod_price*prod_qty*1000) as ventes 
FROM TRANSACTION_table 
WHERE YEAR(date)=2019  
GROUP BY date;

