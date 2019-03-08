# <center>Web App Assignment 4</center>

<center>Ruiyu Zhang || rz213</center>



## Q1

### a)

```xml-dtd
<?xml version="1.0">
<!ELEMENT products (product*)>
<!ELEMENT product (name, price, description, store*)>
<!ELEMENT store (name, phones, markup)>

<!ELEMENT name (#PCDATA)>
<!ELEMENT price (#PCDATA)>
<!ELEMENT description (#PCDATA)>
<!ELEMENT phones (#PCDATA)>
<!ELEMENT markup (#PCDATA)>

<!ATTLIST product pid CDATA #REQUIRED>
<!ATTLIST store sid CDATA #REQUIRED>
```



### b)

```xquery
<products>
    {
	for $product in doc("q1b.xml")/db/products/row
    return
    	<product pid="{$product/pid}">
    		{$product/name}{$product/price}{$product/description}
            {
            	for $store in doc("q1b.xml")/db/stores/row
            	for $sell in doc("q1b.xml")/db/sells/row
            	where $product/pid = $sell/pid and $store/pid = $sell/sid
            	return
            	<store sid="{$store/sid}">
            		{$store/name}{$store/phones}{$sell/markup}
            	</store>
            }
    	</product>
    }
</products>
```



### c)

```xquery
<products>
	{
        for $product in doc("q1a.xml")/products/product
        where $product/store/markup = "25%"
        return 
        	<product>
        		{$product/name}{$product/price}
        	</product>
	}
</products>
```



### d)

```sql
SELECT P.name, P.price
FROM product P, sell S
WHERE P.pid = S.pid AND S.markup = "25%"
GROUP BY P.name
```



## Q2

### a)

```xquery
for $title in doc("q2.xml")/broadway/title
return <result>{$title}</result>
```



### b)

```xquery
for $theater in $doc("q2.xml")/broadway/theater[date="11/9/2008"]
where some $t in $theater/price satisfies data($t) lt 35
return <theater>{$theater/title}</theater>
```



### c)

```xquery
for $concert in doc("q2.xml")/broadway/concert[type="chamber orchestra"]
where avg(data($concert/price)) >= 50
return <result>{$concert/title}</result>
```



### d)

```xquery
for $date in distinct-values(doc("q2.xml")//date)
for $x in //theater[date=$date] | //concert[date=$date] | //opera[date=$date]
return
	<groupByDate>
		<day>
			{$date}
			<show>{$x/title}{$x/price}</show>
		</day>
	</groupByDate>
```



## Q3

