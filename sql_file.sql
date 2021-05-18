







/* Create tables */
create table customer (
	customer_id integer primary key,
	first_name text,
	last_name text,
	address text,
	email text
);

create table product (
	product_id integer primary key,
	product_name text,
	category text,
	prod_year text,
	quantity int,
	price float
);


/* Insert data to the tables */

/*
(name, surname, address, email)
*/

insert into customer (first_name, last_name, address, email) values (
	'Trond', 'Haug', 'Bergen', 'trond@email.com');
insert into customer (first_name, last_name, address, email) values (
	'Karl', 'Hagen', 'Oslo', 'karl@email.com');
insert into customer (first_name, last_name, address, email) values (
	'Tonje', 'Ulvang', 'Oslo', 'tonje@email.com');
insert into customer (first_name, last_name, address, email) values (
	'Jarle', 'Vaag', 'Trondheim', 'jarle@email.com');


/*
(product_name, category, prod_year, quantity, price)
*/

insert into product (product_name, category, prod_year, quantity, price) values (
'Comedy 1', 'Comedy', '1995', '5', '100');
insert into product (product_name, category, prod_year, quantity, price) values (
'Comedy 2', 'Comedy', '2000', '10', '110');
insert into product (product_name, category, prod_year, quantity, price) values (
'Comedy 3', 'Comedy', '2010', '15', '120');
insert into product (product_name, category, prod_year, quantity, price) values (
'Comedy 4', 'Comedy', '2018', '20', '130');

insert into product (product_name, category, prod_year, quantity, price) values (
'Action 1', 'Action', '1997', '10', '100');
insert into product (product_name, category, prod_year, quantity, price) values (
'Action 2', 'Action', '2002', '15', '110');
insert into product (product_name, category, prod_year, quantity, price) values (
'Action 3', 'Action', '2011', '20', '120');
insert into product (product_name, category, prod_year, quantity, price) values (
'Action 4', 'Action', '2019', '25', '140');

insert into product (product_name, category, prod_year, quantity, price) values (
'SciFi 1', 'SciFi', '1999', '15', '100');
insert into product (product_name, category, prod_year, quantity, price) values (
'SciFi 2', 'SciFi', '2004', '20', '100');
insert into product (product_name, category, prod_year, quantity, price) values (
'SciFi 3', 'SciFi', '2014', '25', '120');
insert into product (product_name, category, prod_year, quantity, price) values (
'SciFi 4', 'SciFi', '2020', '30', '150');

insert into product (product_name, category, prod_year, quantity, price) values (
'Drama 1', 'Drama', '1996', '20', '100');
insert into product (product_name, category, prod_year, quantity, price) values (
'Drama 2', 'Drama', '2006', '25', '110');
insert into product (product_name, category, prod_year, quantity, price) values (
'Drama 3', 'Drama', '2017', '30', '120');
insert into product (product_name, category, prod_year, quantity, price) values (
'Drama 4', 'Drama', '2021', '35', '150');





