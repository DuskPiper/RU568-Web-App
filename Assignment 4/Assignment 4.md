# <center>Web Application Assignment 4</center>

<center>Ruiyu Zhang || rz213</center>

<center>2019.03.08</center>



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

### 1)

Modified XSL code

```xml
<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/TR/WD-xsl"
 result-ns="http://www.w3.org/TR/REC-html">
<xsl:template match="/">
 <html>
 <head>
 <title>Bibliography</title>
 </head>
 <body background="antiquewhite">
 <center><h2>Bibliography</h2><hr width="90%"/></center>
 <ul>
 <xsl:for-each select="bib/book">
 <p/><li>
 <xsl:value-of select="author/lastname"/>, <!-- MODIFIED -->
 <xsl:value-of select="author/firstname"/>. <!-- MODIFIED -->
<b><xsl:value-of select="title"/></b>,
<xsl:value-of select="publisher"/>
<xsl:text> </xsl:text> <!-- MODIFIED TO ADD SPACE -->
<xsl:value-of select="address"/>
<xsl:text> </xsl:text> <!-- MODIFIED TO ADD SPACE -->
 <xsl:value-of select="year"/>.
 </li>
 </xsl:for-each>
 <xsl:for-each select="bib/article">
 <p/><li>
 <xsl:value-of select="author"/>,
<b><xsl:value-of select="title"/></b>,
 <b> <!-- MODIFIED -->
  <xsl:value-of select="journal"/>, <!-- MODIFIED -->
  <xsl:value-of select="volume"/>, <!-- MODIFIED -->
 </b>, <!-- MODIFIED -->
 pp.<xsl:apply-templates select="page"/> <!-- MODIFIED TEXT -->
<xsl:value-of select="year"/>.
 </li>
 </xsl:for-each>
 </ul>
 </body>
 </html>
</xsl:template>
<xsl:template match="page">
 <xsl:value-of select="from"/>-<xsl:value-of select="to"/>,
</xsl:template>
</xsl:stylesheet>
```



Modified XML

```xml
<?xml version="1.0" encoding="ISO-8859-1" ?>
<?xml-stylesheet type="text/xsl" href="bib.xsl"?>
<!DOCTYPE bib SYSTEM "bib.dtd">
<bib>
<book>
 <author> <!-- MODIFIED TO SEPERATE FIRST & LAST NAME -->
  <firstname>Leslie</firstname> <!-- MODIFIED -->
  <lastname>Lamport</lastname> <!-- MODIFIED -->
 </author> <!-- MODIFIED -->
 <title>Latex: A Document Preparation System </title>
 <year>1986</year>
 <publisher>Addison-Wesley</publisher>
</book>
<article>
 <author> <!-- MODIFIED TO SEPERATE FIRST & LAST NAME -->
  <firstname>David</firstname> <!-- MODIFIED -->
  <lastname>Marr</lastname> <!-- MODIFIED -->
 </author> <!-- MODIFIED -->
 <title>Visual information processing</title>
 <year>1980</year>
 <volume>290</volume>
 <page>
 <from>199</from>
 <to>218</to>
 </page>
 <journal>Phil. Trans. Roy. Soc. B</journal>
</article>
<article>
 <author> <!-- MODIFIED TO SEPERATE FIRST & LAST NAME -->
  <firstname>R. K.</firstname> <!-- MODIFIED -->
  <lastname>Clifton</lastname> <!-- MODIFIED -->
 </author> <!-- MODIFIED -->
 <title>Breakdown of echo suppression in the precedence
effect</title>
 <year>1987</year>
 <volume>82</volume> 
 <page>
 <from>1834</from>
 <to>1835</to>
 </page>
 <journal>J. Acoust. Soc. Am. </journal>
 </article>
 <book>
 <author> <!-- MODIFIED TO SEPERATE FIRST & LAST NAME -->
  <firstname>David</firstname> <!-- MODIFIED -->
  <lastname>Marr</lastname> <!-- MODIFIED -->
 </author> <!-- MODIFIED -->
 <title>Vision</title>
 <year>1982</year>
 <address> NY </address>
 <publisher>Freeman</publisher>
 </book>
<article>
 <author>David Marr</author>
 <title>Visual information processing</title>
 <year>1980</year>
 <volume>290</volume>
 <page>
 <from>199</from>
 <to>218</to>
 </page>
 <journal> Phil. Trans. Roy. Soc. B</journal>
</article>
</bib>
```



Modified DTD

```dtd
<?xml version="1.0" ?>
<!ELEMENT bib ( (book | article)+)>
<!ELEMENT book ( author, title, year, (address)?, publisher )>
<!ELEMENT article ( author, title, year, volume, page, journal)>
<!ELEMENT page (from, to)>
<!ELEMENT author (firstname, lastname)>
<!ELEMENT firstname (#PCDATA)>
<!ELEMENT lastname (#PCDATA)>
<!ELEMENT title (#PCDATA)>
<!ELEMENT year (#PCDATA)>
<!ELEMENT address (#PCDATA)>
<!ELEMENT publisher (#PCDATA)>
<!ELEMENT from (#PCDATA)>
<!ELEMENT to (#PCDATA)>
<!ELEMENT journal (#PCDATA)>
<!ELEMENT volume (#PCDATA)> 
```



### 2)

Additional content in XML

```xml
<bib>
	<book>
    	<author>
        	<firstname>Hua</firstname>
            <lastname>Yu</lastname>
        </author>
        <title>To Live</title>
        <year>1992</year>
        <address>CHN</address>
        <publisher>Hachette</publisher>
    </book>
    
    <book>
    	<author>
        	<firstname>Robert Lawrence</firstname>
            <lastname>Kuhn</lastname>
        </author>
        <title>The Man Who Changed China: The Life and Legacy of Jiang Zemin</title>
        <year>2004</year>
        <address>NY</address>
        <!-- MISSING PUBLISHER -->
    </book>
    
    <article>
    	<author>
        	<firstname>Xinyu</firstname>
            <lastname>Li</lastname>
        </author>
        <title>
            Process Progress Estimation and Phase Detection
        </title>
        <year>2016</year>
        <volume>16</volume>
        <!-- MISSING PAGE -->
        <Journal>UbiComp</Journal>
    </article>
    
    <article>
    	<author>
        	<firstname>Yingwei</firstname>
            <lastname>Li</lastname>
        </author>
        <title>
        	VLAD: Encoding Dynamics of Deep Features For Action Recognition
        </title>
        <year>2016</year>
        <volume>10</volume>
        <page>
        	<from>1951</from>
            <to>1960</to>
        </page>
        <journal>CVPR</journal>
    </article>
</bib>
```



### 3)

Additional content in XSL

```xml
<xsl:for-each select="bib/phd_thesis">
	<li>
    	<xsl:value-of select="author/firstname"/>
        <xsl:value-of select="author/lastname"/>
        <b><xsl:value-of select="title"/></b>
        <xsl:value-of select="year"/>
        <em><xsl:value-of select="university"/></em>
    </li>
</xsl:for-each>
```



Additional content in XML

```xml
<bib>
	<phd_thesis>
        <author>
            <firstname>Yue</firstname>
            <lastname>Gu</lastname>
        </author>
        <title>Speech intention classification with multimodal deep learning</title>
        <year>2017</year>
        <university>Rutgers University New Brunswick</university>
    </phd_thesis>
    
    <phd_thesis>
        <author>
            <firstname>Xinyu</firstname>
            <lastname>Li</lastname>
        </author>
        <title>Deep Learning for RFID-Based Activity Recognition</title>
        <year>2016</year>
        <university>Rutgers University New Brunswick</university>
    </phd_thesis>
</bib>
```



Modified DTD

```dtd
<?xml version="1.0" ?>
<!ELEMENT bib ( (book | article | phd_thesis)+)>
<!ELEMENT book ( author, title, year, (address)?, publisher )> <!-- MODIFIED -->
<!ELEMENT article ( author, title, year, volume, page, journal)>
<!ELEMENT phd_thesis (author, title, year, university)> <!-- ADDED -->
<!ELEMENT page (from, to)>
<!ELEMENT author (firstname, lastname)>
<!ELEMENT firstname (#PCDATA)>
<!ELEMENT lastname (#PCDATA)>
<!ELEMENT title (#PCDATA)>
<!ELEMENT year (#PCDATA)>
<!ELEMENT address (#PCDATA)>
<!ELEMENT publisher (#PCDATA)>
<!ELEMENT from (#PCDATA)>
<!ELEMENT to (#PCDATA)>
<!ELEMENT journal (#PCDATA)>
<!ELEMENT volume (#PCDATA)> 
<!ELEMENT university (#PCDATA)>  <!-- ADDED -->
```

