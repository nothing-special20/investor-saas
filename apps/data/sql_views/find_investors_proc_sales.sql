insert INTO find_investors_proc_sales
SELECT llc_pins."PIN", "FOLIO", "SALE_AMOUNT", "SALE_DATE", "GRANTOR", "GRANTEE", "COUNTY",
		rank () over (PARTITION BY llc_pins."PIN" order by "SALE_DATE" desc)
FROM public.find_investors_sales
right join ( select distinct "PIN" from public.find_investors_sales where "GRANTOR" like '%LLC%') llc_pins
on find_investors_sales."PIN" = llc_pins."PIN"
where "GRANTOR" != "GRANTEE"
and "SALE_AMOUNT"::decimal > 100
and TO_DATE("SALE_DATE", 'YYYY-MM-DD') > TO_DATE('2005-12-31', 'YYYY-MM-DD')
;