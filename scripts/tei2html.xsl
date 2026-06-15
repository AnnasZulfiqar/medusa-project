<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" exclude-result-prefixes="tei">
  <xsl:output method="html" encoding="UTF-8" indent="yes"/>
  <xsl:key name="entity" match="tei:*[@xml:id]" use="@xml:id"/>
  <xsl:template match="/">
    <html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1.0"/><title>Medusa TEI Reading View</title><link rel="stylesheet" href="../assets/css/style.css"/></head>
      <body><header class="subhero"><a href="../index.html">← Project home</a><p class="eyebrow">TEI P5 transformed with XSLT</p><h1><xsl:value-of select="//tei:titleStmt/tei:title"/></h1><p><xsl:value-of select="//tei:abstract/tei:p"/></p></header>
      <main class="reading"><section class="legend"><strong>Annotations:</strong> <span class="tag person">person</span> <span class="tag place">place</span> <span class="tag org">organization</span> <span class="tag work">work / concept / event</span></section><xsl:apply-templates select="//tei:body/tei:div"/></main>
      <footer>Generated from <a href="../xml/medusa.xml">medusa.xml</a> using <a href="../scripts/tei2html.xsl">tei2html.xsl</a>.</footer></body></html>
  </xsl:template>
  <xsl:template match="tei:div"><article><h2><xsl:value-of select="tei:head"/></h2><xsl:apply-templates select="node()[not(self::tei:head)]"/></article></xsl:template>
  <xsl:template match="tei:p"><p><xsl:apply-templates/></p></xsl:template>
  <xsl:template match="tei:quote"><blockquote><xsl:apply-templates/><cite>Ovid, <em>Metamorphoses</em>, Book IV</cite></blockquote></xsl:template>
  <xsl:template match="tei:persName|tei:placeName|tei:orgName|tei:rs|tei:bibl">
    <xsl:variable name="id" select="substring-after(@ref,'#')"/><xsl:variable name="target" select="key('entity',$id)/@sameAs"/>
    <a><xsl:attribute name="class">entity <xsl:choose><xsl:when test="self::tei:persName">person</xsl:when><xsl:when test="self::tei:placeName">place</xsl:when><xsl:when test="self::tei:orgName">org</xsl:when><xsl:otherwise>work</xsl:otherwise></xsl:choose></xsl:attribute><xsl:if test="$target"><xsl:attribute name="href"><xsl:value-of select="$target"/></xsl:attribute><xsl:attribute name="target">_blank</xsl:attribute></xsl:if><xsl:attribute name="title"><xsl:value-of select="$id"/></xsl:attribute><xsl:apply-templates/></a>
  </xsl:template>
  <xsl:template match="tei:title"><em><xsl:apply-templates/></em></xsl:template>
</xsl:stylesheet>
