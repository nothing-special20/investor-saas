drop sequence investorhistory_sequence
CREATE SEQUENCE investorhistory_sequence
  start 1
  increment 1;

insert INTO find_investors_investorhistory
select nextval('investorhistory_sequence') as id, sale_data."PIN", "PURCHASE_DATE", "SALE_DATE", 
		"SALE_AMOUNT"::decimal, "PURCHASE_AMOUNT"::decimal, sale_data."GRANTOR", sale_data."GRANTEE", 
		"SALE_AMOUNT"::decimal - "PURCHASE_AMOUNT"::decimal as "PROFIT"

from 
(SELECT "PIN", "SALE_AMOUNT", TO_DATE("SALE_DATE", 'YYYY-MM-DD') AS "SALE_DATE", "GRANTOR", "GRANTEE", "rank"
	FROM public.find_investors_proc_sales where "GRANTOR" like '%LLC%') sale_data
	
left join

(SELECT "PIN", "SALE_AMOUNT" as "PURCHASE_AMOUNT", TO_DATE("SALE_DATE", 'YYYY-MM-DD') as "PURCHASE_DATE", "GRANTOR", "GRANTEE", "rank"
	FROM public.find_investors_proc_sales) purchase_data

on (sale_data."rank" + 1) = purchase_data."rank"
and sale_data."PIN" = purchase_data."PIN"
;
