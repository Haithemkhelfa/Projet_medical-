
/*  Première partie du test */

SELECT date, SUM(prod_price*prod_qty*1000) as ventes 
FROM TRANSACTION_table 
WHERE date BETWEEN 01/01/2019 AND 31/12/2019
GROUP BY date;

/* Seconde partie du test */

SELECT t.client_id, (SELECT   SUM(t1.prod_price * t1.prod_qty) FROM TRANSACTION_table t1, PRODUCT_NOMENCLATURE_table p1
                    WHERE t1.prod_id = p1.product_id AND  p1.product_type LIKE 'MEUBLE' AND t.client_id=t1.client_id) AS ventes_meuble
                    ,
                    (SELECT   SUM(t1.prod_price * t1.prod_qty) FROM TRANSACTION_table t1, PRODUCT_NOMENCLATURE_table p1
                    WHERE t1.prod_id = p1.product_id AND  p1.product_type LIKE 'DECO' AND t.client_id=t1.client_id) AS ventes_deco
 
FROM
TRANSACTION_table t , PRODUCT_NOMENCLATURE_table p 
WHERE date BETWEEN 01/01/2020 AND 31/12/2020
GROUP BY t.client_id;









