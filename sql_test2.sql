
/* inner join of 2 tables: TRANSACTION_table  & PRODUCT_NOMENCLATURE_table  */

SELECT client_id, prod_id, prod_price, prod_qty, product_type 
FROM TRANSACTION_table 
INNER JOIN PRODUCT_NOMENCLATURE_table ON PRODUCT_NOMENCLATURE_table.product_id = TRANSACTION_table.prod_id;

/* By use a subquery  */

SELECT client_id, sum(prod_qty*prod_price) AS ventes_deco, sum(prod_qty*prod_price) AS ventes_meuble 
WHERE 
client_id IN (
    SELECT 
        client_id
    FROM 
        PRODUCT_NOMENCLATURE_table
    WHERE      
        product_type= 'MEUBLE'
    FROM 
        PRODUCT_NOMENCLATURE_table  
    WHERE     
        product_type= 'DECO'
            )
WHERE YEAR(date)=2019  
GROUP BY date;  





