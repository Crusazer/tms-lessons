""" SELECT COUNT(*) FROM user WHERE age > 116; """

""" SELECT SUM(age) FROM user; """

""" SELECT SUM(age) FROM user; """

""" SELECT AVG(age) FROM user;  """

""" SELECT SUM(age)/count(*) FROM user; """

""" SELECT MIN(age) FROM user; """

""" SELECT MAX(age) FROM user; """

""" SELECT MAX(age) - MIN(age) FROM user; """

""" SELECT ROUND(age / 100.0, 1) FROM user; """

""" SELECT LENGTH(first_name) FROM user; """

""" SELECT LENGTH(last_name) FROM user; """

""" SELECT LENGTH(first_name || last_name) FROM user; """

""" SELECT SUBSTR(first_name, 1,1)||'.'||SUBSTR(last_name,1 ,1)||'.' FROM user; """

""" SELECT * FROM user ORDER BY age DESC; """

""" SELECT * FROM user ORDER BY last_name, first_name; """

""" SELECT * FROM user ORDER BY country, age DESC; """

""" SELECT * FROM user ORDER BY LENGTH(first_name||last_name); """

""" SELECT *, (SUBSTR(first_name,1,1)||'.'||SUBSTR(last_name,1,1)||'.') AS init FROM user ORDER BY init; """

""" SELECT country, COUNT() FROM user GROUP BY country; """

""" SELECT *, COUNT() FROM user GROUP BY first_name; """

""" SELECT country, SUM(age) FROM user GROUP BY country; """

""" SELECT country, AVG(age) FROM user GROUP BY country; """

""" SELECT country, MAX(age) FROM user GROUP BY country; """

""" SELECT country, COUNT() FROM user GROUP BY country HAVING COUNT() >= 5; """

""" SELECT COUNT() FROM(SELECT * FROM user GROUP BY last_name HAVING COUNT() > 1); """

""" SELECT country FROM(SELECT country, MAX(age) FROM user); """

""" SELECT country, MAX(age) FROM user; """

""" SELECT * FROM user WHERE country = (SELECT country FROM user WHERE age = (SELECT MAX(age) FROM user)); """

""" SELECT * FROM user WHERE last_name IN (SELECT last_name FROM user GROUP BY last_name HAVING COUNT() > 1); """

""" SELECT * FROM product p INNER JOIN vendor v ON p.vendor_id = v.id; """

""" SELECT * FROM product p LEFT JOIN vendor v ON p.vendor_id = v.id; """

""" SELECT * FROM product p RIGHT JOIN vendor v ON p.vendor_id = v.id; """

""" SELECT * FROM product p FULL JOIN vendor v ON p.vendor_id = v.id;"""

""" SELECT v.name, COUNT() AS count FROM product p JOIN vendor v ON p.vendor_id = v.id GROUP BY v.name; """

""" SELECT v.name, AVG(p.price) AS avg_price FROM product p JOIN vendor v ON p.vendor_id = v.id GROUP BY v.name; """

""" SELECT vendor.name FROM vendor LEFT JOIN product ON vendor.id = product.vendor_id GROUP BY vendor.name HAVING COUNT(product.id) = 0; """
