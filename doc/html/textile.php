#!/usr/bin/php
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <title>John Novak / blog</title>
    <meta name="description" content="This is the personal website of John Novak.">

    <link rel="stylesheet" href="/css/main.css">

    <link href="http://fonts.googleapis.com/css?family=Source+Sans+Pro:200,300,400,600" rel="stylesheet" type="text/css">
  </head>

  <body id="blog">
    <div id="header">
      <h1 id="logo">
        <img src="/img/jn.png" alt="JN" />
        <span class="jn">John Novak </span>
        <span class="sub">blog</span>
      </h1>

      <ul id="mainmenu">
        <li><a href="/photo">Photo</a></li>
        <li><a href="/music">Music</a></li>
        <li><a href="/code">Code</a></li>
        <li class="sel"><a href="/blog">Blog</a></li>
        <li><a href="/about">About</a></li>
      </ul>
    </div>
<?php

require('classTextile.php');

$infile = $argv[1];
$outfile = $argv[2];

$str = file_get_contents($infile);

$textile = new Textile();
$html = $textile->TextileThis($str);

file_put_contents($outfile, $html);

?>
