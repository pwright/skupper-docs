<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="generator" content="Asciidoctor 2.0.15">
<title>Creating a service network with OpenShift</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Open+Sans:300,300italic,400,400italic,600,600italic%7CNoto+Serif:400,400italic,700,700italic%7CDroid+Sans+Mono:400,700">
<style>
/* Asciidoctor default stylesheet | MIT License | https://asciidoctor.org */
/* Uncomment @import statement to use as custom stylesheet */
/*@import "https://fonts.googleapis.com/css?family=Open+Sans:300,300italic,400,400italic,600,600italic%7CNoto+Serif:400,400italic,700,700italic%7CDroid+Sans+Mono:400,700";*/
article,aside,details,figcaption,figure,footer,header,hgroup,main,nav,section{display:block}
audio,video{display:inline-block}
audio:not([controls]){display:none;height:0}
html{font-family:sans-serif;-ms-text-size-adjust:100%;-webkit-text-size-adjust:100%}
a{background:none}
a:focus{outline:thin dotted}
a:active,a:hover{outline:0}
h1{font-size:2em;margin:.67em 0}
abbr[title]{border-bottom:1px dotted}
b,strong{font-weight:bold}
dfn{font-style:italic}
hr{-moz-box-sizing:content-box;box-sizing:content-box;height:0}
mark{background:#ff0;color:#000}
code,kbd,pre,samp{font-family:monospace;font-size:1em}
pre{white-space:pre-wrap}
q{quotes:"\201C" "\201D" "\2018" "\2019"}
small{font-size:80%}
sub,sup{font-size:75%;line-height:0;position:relative;vertical-align:baseline}
sup{top:-.5em}
sub{bottom:-.25em}
img{border:0}
svg:not(:root){overflow:hidden}
figure{margin:0}
fieldset{border:1px solid silver;margin:0 2px;padding:.35em .625em .75em}
legend{border:0;padding:0}
button,input,select,textarea{font-family:inherit;font-size:100%;margin:0}
button,input{line-height:normal}
button,select{text-transform:none}
button,html input[type="button"],input[type="reset"],input[type="submit"]{-webkit-appearance:button;cursor:pointer}
button[disabled],html input[disabled]{cursor:default}
input[type="checkbox"],input[type="radio"]{box-sizing:border-box;padding:0}
button::-moz-focus-inner,input::-moz-focus-inner{border:0;padding:0}
textarea{overflow:auto;vertical-align:top}
table{border-collapse:collapse;border-spacing:0}
*,*::before,*::after{-moz-box-sizing:border-box;-webkit-box-sizing:border-box;box-sizing:border-box}
html,body{font-size:100%}
body{background:#fff;color:rgba(0,0,0,.8);padding:0;margin:0;font-family:"Noto Serif","DejaVu Serif",serif;font-weight:400;font-style:normal;line-height:1;position:relative;cursor:auto;tab-size:4;word-wrap:anywhere;-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased}
a:hover{cursor:pointer}
img,object,embed{max-width:100%;height:auto}
object,embed{height:100%}
img{-ms-interpolation-mode:bicubic}
.left{float:left!important}
.right{float:right!important}
.text-left{text-align:left!important}
.text-right{text-align:right!important}
.text-center{text-align:center!important}
.text-justify{text-align:justify!important}
.hide{display:none}
img,object,svg{display:inline-block;vertical-align:middle}
textarea{height:auto;min-height:50px}
select{width:100%}
.subheader,.admonitionblock td.content>.title,.audioblock>.title,.exampleblock>.title,.imageblock>.title,.listingblock>.title,.literalblock>.title,.stemblock>.title,.openblock>.title,.paragraph>.title,.quoteblock>.title,table.tableblock>.title,.verseblock>.title,.videoblock>.title,.dlist>.title,.olist>.title,.ulist>.title,.qlist>.title,.hdlist>.title{line-height:1.45;color:#7a2518;font-weight:400;margin-top:0;margin-bottom:.25em}
div,dl,dt,dd,ul,ol,li,h1,h2,h3,#toctitle,.sidebarblock>.content>.title,h4,h5,h6,pre,form,p,blockquote,th,td{margin:0;padding:0}
a{color:#2156a5;text-decoration:underline;line-height:inherit}
a:hover,a:focus{color:#1d4b8f}
a img{border:0}
p{font-family:inherit;font-weight:400;font-size:1em;line-height:1.6;margin-bottom:1.25em;text-rendering:optimizeLegibility}
p aside{font-size:.875em;line-height:1.35;font-style:italic}
h1,h2,h3,#toctitle,.sidebarblock>.content>.title,h4,h5,h6{font-family:"Open Sans","DejaVu Sans",sans-serif;font-weight:300;font-style:normal;color:#ba3925;text-rendering:optimizeLegibility;margin-top:1em;margin-bottom:.5em;line-height:1.0125em}
h1 small,h2 small,h3 small,#toctitle small,.sidebarblock>.content>.title small,h4 small,h5 small,h6 small{font-size:60%;color:#e99b8f;line-height:0}
h1{font-size:2.125em}
h2{font-size:1.6875em}
h3,#toctitle,.sidebarblock>.content>.title{font-size:1.375em}
h4,h5{font-size:1.125em}
h6{font-size:1em}
hr{border:solid #dddddf;border-width:1px 0 0;clear:both;margin:1.25em 0 1.1875em;height:0}
em,i{font-style:italic;line-height:inherit}
strong,b{font-weight:bold;line-height:inherit}
small{font-size:60%;line-height:inherit}
code{font-family:"Droid Sans Mono","DejaVu Sans Mono",monospace;font-weight:400;color:rgba(0,0,0,.9)}
ul,ol,dl{font-size:1em;line-height:1.6;margin-bottom:1.25em;list-style-position:outside;font-family:inherit}
ul,ol{margin-left:1.5em}
ul li ul,ul li ol{margin-left:1.25em;margin-bottom:0;font-size:1em}
ul.square li ul,ul.circle li ul,ul.disc li ul{list-style:inherit}
ul.square{list-style-type:square}
ul.circle{list-style-type:circle}
ul.disc{list-style-type:disc}
ol li ul,ol li ol{margin-left:1.25em;margin-bottom:0}
dl dt{margin-bottom:.3125em;font-weight:bold}
dl dd{margin-bottom:1.25em}
abbr,acronym{text-transform:uppercase;font-size:90%;color:rgba(0,0,0,.8);border-bottom:1px dotted #ddd;cursor:help}
abbr{text-transform:none}
blockquote{margin:0 0 1.25em;padding:.5625em 1.25em 0 1.1875em;border-left:1px solid #ddd}
blockquote,blockquote p{line-height:1.6;color:rgba(0,0,0,.85)}
@media screen and (min-width:768px){h1,h2,h3,#toctitle,.sidebarblock>.content>.title,h4,h5,h6{line-height:1.2}
h1{font-size:2.75em}
h2{font-size:2.3125em}
h3,#toctitle,.sidebarblock>.content>.title{font-size:1.6875em}
h4{font-size:1.4375em}}
table{background:#fff;margin-bottom:1.25em;border:solid 1px #dedede;word-wrap:normal}
table thead,table tfoot{background:#f7f8f7}
table thead tr th,table thead tr td,table tfoot tr th,table tfoot tr td{padding:.5em .625em .625em;font-size:inherit;color:rgba(0,0,0,.8);text-align:left}
table tr th,table tr td{padding:.5625em .625em;font-size:inherit;color:rgba(0,0,0,.8)}
table tr.even,table tr.alt{background:#f8f8f7}
table thead tr th,table tfoot tr th,table tbody tr td,table tr td,table tfoot tr td{line-height:1.6}
h1,h2,h3,#toctitle,.sidebarblock>.content>.title,h4,h5,h6{line-height:1.2;word-spacing:-.05em}
h1 strong,h2 strong,h3 strong,#toctitle strong,.sidebarblock>.content>.title strong,h4 strong,h5 strong,h6 strong{font-weight:400}
.center{margin-left:auto;margin-right:auto}
.stretch{width:100%}
.clearfix::before,.clearfix::after,.float-group::before,.float-group::after{content:" ";display:table}
.clearfix::after,.float-group::after{clear:both}
:not(pre).nobreak{word-wrap:normal}
:not(pre).nowrap{white-space:nowrap}
:not(pre).pre-wrap{white-space:pre-wrap}
:not(pre):not([class^=L])>code{font-size:.9375em;font-style:normal!important;letter-spacing:0;padding:.1em .5ex;word-spacing:-.15em;background:#f7f7f8;-webkit-border-radius:4px;border-radius:4px;line-height:1.45;text-rendering:optimizeSpeed}
pre{color:rgba(0,0,0,.9);font-family:"Droid Sans Mono","DejaVu Sans Mono",monospace;line-height:1.45;text-rendering:optimizeSpeed}
pre code,pre pre{color:inherit;font-size:inherit;line-height:inherit}
pre>code{display:block}
pre.nowrap,pre.nowrap pre{white-space:pre;word-wrap:normal}
em em{font-style:normal}
strong strong{font-weight:400}
.keyseq{color:rgba(51,51,51,.8)}
kbd{font-family:"Droid Sans Mono","DejaVu Sans Mono",monospace;display:inline-block;color:rgba(0,0,0,.8);font-size:.65em;line-height:1.45;background:#f7f7f7;border:1px solid #ccc;-webkit-border-radius:3px;border-radius:3px;-webkit-box-shadow:0 1px 0 rgba(0,0,0,.2),0 0 0 .1em white inset;box-shadow:0 1px 0 rgba(0,0,0,.2),0 0 0 .1em #fff inset;margin:0 .15em;padding:.2em .5em;vertical-align:middle;position:relative;top:-.1em;white-space:nowrap}
.keyseq kbd:first-child{margin-left:0}
.keyseq kbd:last-child{margin-right:0}
.menuseq,.menuref{color:#000}
.menuseq b:not(.caret),.menuref{font-weight:inherit}
.menuseq{word-spacing:-.02em}
.menuseq b.caret{font-size:1.25em;line-height:.8}
.menuseq i.caret{font-weight:bold;text-align:center;width:.45em}
b.button::before,b.button::after{position:relative;top:-1px;font-weight:400}
b.button::before{content:"[";padding:0 3px 0 2px}
b.button::after{content:"]";padding:0 2px 0 3px}
p a>code:hover{color:rgba(0,0,0,.9)}
#header,#content,#footnotes,#footer{width:100%;margin-left:auto;margin-right:auto;margin-top:0;margin-bottom:0;max-width:62.5em;*zoom:1;position:relative;padding-left:.9375em;padding-right:.9375em}
#header::before,#header::after,#content::before,#content::after,#footnotes::before,#footnotes::after,#footer::before,#footer::after{content:" ";display:table}
#header::after,#content::after,#footnotes::after,#footer::after{clear:both}
#content{margin-top:1.25em}
#content::before{content:none}
#header>h1:first-child{color:rgba(0,0,0,.85);margin-top:2.25rem;margin-bottom:0}
#header>h1:first-child+#toc{margin-top:8px;border-top:1px solid #dddddf}
#header>h1:only-child,body.toc2 #header>h1:nth-last-child(2){border-bottom:1px solid #dddddf;padding-bottom:8px}
#header .details{border-bottom:1px solid #dddddf;line-height:1.45;padding-top:.25em;padding-bottom:.25em;padding-left:.25em;color:rgba(0,0,0,.6);display:-ms-flexbox;display:-webkit-flex;display:flex;-ms-flex-flow:row wrap;-webkit-flex-flow:row wrap;flex-flow:row wrap}
#header .details span:first-child{margin-left:-.125em}
#header .details span.email a{color:rgba(0,0,0,.85)}
#header .details br{display:none}
#header .details br+span::before{content:"\00a0\2013\00a0"}
#header .details br+span.author::before{content:"\00a0\22c5\00a0";color:rgba(0,0,0,.85)}
#header .details br+span#revremark::before{content:"\00a0|\00a0"}
#header #revnumber{text-transform:capitalize}
#header #revnumber::after{content:"\00a0"}
#content>h1:first-child:not([class]){color:rgba(0,0,0,.85);border-bottom:1px solid #dddddf;padding-bottom:8px;margin-top:0;padding-top:1rem;margin-bottom:1.25rem}
#toc{border-bottom:1px solid #e7e7e9;padding-bottom:.5em}
#toc>ul{margin-left:.125em}
#toc ul.sectlevel0>li>a{font-style:italic}
#toc ul.sectlevel0 ul.sectlevel1{margin:.5em 0}
#toc ul{font-family:"Open Sans","DejaVu Sans",sans-serif;list-style-type:none}
#toc li{line-height:1.3334;margin-top:.3334em}
#toc a{text-decoration:none}
#toc a:active{text-decoration:underline}
#toctitle{color:#7a2518;font-size:1.2em}
@media screen and (min-width:768px){#toctitle{font-size:1.375em}
body.toc2{padding-left:15em;padding-right:0}
#toc.toc2{margin-top:0!important;background:#f8f8f7;position:fixed;width:15em;left:0;top:0;border-right:1px solid #e7e7e9;border-top-width:0!important;border-bottom-width:0!important;z-index:1000;padding:1.25em 1em;height:100%;overflow:auto}
#toc.toc2 #toctitle{margin-top:0;margin-bottom:.8rem;font-size:1.2em}
#toc.toc2>ul{font-size:.9em;margin-bottom:0}
#toc.toc2 ul ul{margin-left:0;padding-left:1em}
#toc.toc2 ul.sectlevel0 ul.sectlevel1{padding-left:0;margin-top:.5em;margin-bottom:.5em}
body.toc2.toc-right{padding-left:0;padding-right:15em}
body.toc2.toc-right #toc.toc2{border-right-width:0;border-left:1px solid #e7e7e9;left:auto;right:0}}
@media screen and (min-width:1280px){body.toc2{padding-left:20em;padding-right:0}
#toc.toc2{width:20em}
#toc.toc2 #toctitle{font-size:1.375em}
#toc.toc2>ul{font-size:.95em}
#toc.toc2 ul ul{padding-left:1.25em}
body.toc2.toc-right{padding-left:0;padding-right:20em}}
#content #toc{border-style:solid;border-width:1px;border-color:#e0e0dc;margin-bottom:1.25em;padding:1.25em;background:#f8f8f7;-webkit-border-radius:4px;border-radius:4px}
#content #toc>:first-child{margin-top:0}
#content #toc>:last-child{margin-bottom:0}
#footer{max-width:none;background:rgba(0,0,0,.8);padding:1.25em}
#footer-text{color:rgba(255,255,255,.8);line-height:1.44}
#content{margin-bottom:.625em}
.sect1{padding-bottom:.625em}
@media screen and (min-width:768px){#content{margin-bottom:1.25em}
.sect1{padding-bottom:1.25em}}
.sect1:last-child{padding-bottom:0}
.sect1+.sect1{border-top:1px solid #e7e7e9}
#content h1>a.anchor,h2>a.anchor,h3>a.anchor,#toctitle>a.anchor,.sidebarblock>.content>.title>a.anchor,h4>a.anchor,h5>a.anchor,h6>a.anchor{position:absolute;z-index:1001;width:1.5ex;margin-left:-1.5ex;display:block;text-decoration:none!important;visibility:hidden;text-align:center;font-weight:400}
#content h1>a.anchor::before,h2>a.anchor::before,h3>a.anchor::before,#toctitle>a.anchor::before,.sidebarblock>.content>.title>a.anchor::before,h4>a.anchor::before,h5>a.anchor::before,h6>a.anchor::before{content:"\00A7";font-size:.85em;display:block;padding-top:.1em}
#content h1:hover>a.anchor,#content h1>a.anchor:hover,h2:hover>a.anchor,h2>a.anchor:hover,h3:hover>a.anchor,#toctitle:hover>a.anchor,.sidebarblock>.content>.title:hover>a.anchor,h3>a.anchor:hover,#toctitle>a.anchor:hover,.sidebarblock>.content>.title>a.anchor:hover,h4:hover>a.anchor,h4>a.anchor:hover,h5:hover>a.anchor,h5>a.anchor:hover,h6:hover>a.anchor,h6>a.anchor:hover{visibility:visible}
#content h1>a.link,h2>a.link,h3>a.link,#toctitle>a.link,.sidebarblock>.content>.title>a.link,h4>a.link,h5>a.link,h6>a.link{color:#ba3925;text-decoration:none}
#content h1>a.link:hover,h2>a.link:hover,h3>a.link:hover,#toctitle>a.link:hover,.sidebarblock>.content>.title>a.link:hover,h4>a.link:hover,h5>a.link:hover,h6>a.link:hover{color:#a53221}
details,.audioblock,.imageblock,.literalblock,.listingblock,.stemblock,.videoblock{margin-bottom:1.25em}
details>summary:first-of-type{cursor:pointer;display:list-item;outline:none;margin-bottom:.75em}
.admonitionblock td.content>.title,.audioblock>.title,.exampleblock>.title,.imageblock>.title,.listingblock>.title,.literalblock>.title,.stemblock>.title,.openblock>.title,.paragraph>.title,.quoteblock>.title,table.tableblock>.title,.verseblock>.title,.videoblock>.title,.dlist>.title,.olist>.title,.ulist>.title,.qlist>.title,.hdlist>.title{text-rendering:optimizeLegibility;text-align:left;font-family:"Noto Serif","DejaVu Serif",serif;font-size:1rem;font-style:italic}
table.tableblock.fit-content>caption.title{white-space:nowrap;width:0}
.paragraph.lead>p,#preamble>.sectionbody>[class="paragraph"]:first-of-type p{font-size:1.21875em;line-height:1.6;color:rgba(0,0,0,.85)}
table.tableblock #preamble>.sectionbody>[class="paragraph"]:first-of-type p{font-size:inherit}
.admonitionblock>table{border-collapse:separate;border:0;background:none;width:100%}
.admonitionblock>table td.icon{text-align:center;width:80px}
.admonitionblock>table td.icon img{max-width:none}
.admonitionblock>table td.icon .title{font-weight:bold;font-family:"Open Sans","DejaVu Sans",sans-serif;text-transform:uppercase}
.admonitionblock>table td.content{padding-left:1.125em;padding-right:1.25em;border-left:1px solid #dddddf;color:rgba(0,0,0,.6);word-wrap:anywhere}
.admonitionblock>table td.content>:last-child>:last-child{margin-bottom:0}
.exampleblock>.content{border-style:solid;border-width:1px;border-color:#e6e6e6;margin-bottom:1.25em;padding:1.25em;background:#fff;-webkit-border-radius:4px;border-radius:4px}
.exampleblock>.content>:first-child{margin-top:0}
.exampleblock>.content>:last-child{margin-bottom:0}
.sidebarblock{border-style:solid;border-width:1px;border-color:#dbdbd6;margin-bottom:1.25em;padding:1.25em;background:#f3f3f2;-webkit-border-radius:4px;border-radius:4px}
.sidebarblock>:first-child{margin-top:0}
.sidebarblock>:last-child{margin-bottom:0}
.sidebarblock>.content>.title{color:#7a2518;margin-top:0;text-align:center}
.exampleblock>.content>:last-child>:last-child,.exampleblock>.content .olist>ol>li:last-child>:last-child,.exampleblock>.content .ulist>ul>li:last-child>:last-child,.exampleblock>.content .qlist>ol>li:last-child>:last-child,.sidebarblock>.content>:last-child>:last-child,.sidebarblock>.content .olist>ol>li:last-child>:last-child,.sidebarblock>.content .ulist>ul>li:last-child>:last-child,.sidebarblock>.content .qlist>ol>li:last-child>:last-child{margin-bottom:0}
.literalblock pre,.listingblock>.content>pre{-webkit-border-radius:4px;border-radius:4px;overflow-x:auto;padding:1em;font-size:.8125em}
@media screen and (min-width:768px){.literalblock pre,.listingblock>.content>pre{font-size:.90625em}}
@media screen and (min-width:1280px){.literalblock pre,.listingblock>.content>pre{font-size:1em}}
.literalblock pre,.listingblock>.content>pre:not(.highlight),.listingblock>.content>pre[class="highlight"],.listingblock>.content>pre[class^="highlight "]{background:#f7f7f8}
.literalblock.output pre{color:#f7f7f8;background:rgba(0,0,0,.9)}
.listingblock>.content{position:relative}
.listingblock code[data-lang]::before{display:none;content:attr(data-lang);position:absolute;font-size:.75em;top:.425rem;right:.5rem;line-height:1;text-transform:uppercase;color:inherit;opacity:.5}
.listingblock:hover code[data-lang]::before{display:block}
.listingblock.terminal pre .command::before{content:attr(data-prompt);padding-right:.5em;color:inherit;opacity:.5}
.listingblock.terminal pre .command:not([data-prompt])::before{content:"$"}
.listingblock pre.highlightjs{padding:0}
.listingblock pre.highlightjs>code{padding:1em;-webkit-border-radius:4px;border-radius:4px}
.listingblock pre.prettyprint{border-width:0}
.prettyprint{background:#f7f7f8}
pre.prettyprint .linenums{line-height:1.45;margin-left:2em}
pre.prettyprint li{background:none;list-style-type:inherit;padding-left:0}
pre.prettyprint li code[data-lang]::before{opacity:1}
pre.prettyprint li:not(:first-child) code[data-lang]::before{display:none}
table.linenotable{border-collapse:separate;border:0;margin-bottom:0;background:none}
table.linenotable td[class]{color:inherit;vertical-align:top;padding:0;line-height:inherit;white-space:normal}
table.linenotable td.code{padding-left:.75em}
table.linenotable td.linenos{border-right:1px solid currentColor;opacity:.35;padding-right:.5em}
pre.pygments .lineno{border-right:1px solid currentColor;opacity:.35;display:inline-block;margin-right:.75em}
pre.pygments .lineno::before{content:"";margin-right:-.125em}
.quoteblock{margin:0 1em 1.25em 1.5em;display:table}
.quoteblock:not(.excerpt)>.title{margin-left:-1.5em;margin-bottom:.75em}
.quoteblock blockquote,.quoteblock p{color:rgba(0,0,0,.85);font-size:1.15rem;line-height:1.75;word-spacing:.1em;letter-spacing:0;font-style:italic;text-align:justify}
.quoteblock blockquote{margin:0;padding:0;border:0}
.quoteblock blockquote::before{content:"\201c";float:left;font-size:2.75em;font-weight:bold;line-height:.6em;margin-left:-.6em;color:#7a2518;text-shadow:0 1px 2px rgba(0,0,0,.1)}
.quoteblock blockquote>.paragraph:last-child p{margin-bottom:0}
.quoteblock .attribution{margin-top:.75em;margin-right:.5ex;text-align:right}
.verseblock{margin:0 1em 1.25em}
.verseblock pre{font-family:"Open Sans","DejaVu Sans",sans;font-size:1.15rem;color:rgba(0,0,0,.85);font-weight:300;text-rendering:optimizeLegibility}
.verseblock pre strong{font-weight:400}
.verseblock .attribution{margin-top:1.25rem;margin-left:.5ex}
.quoteblock .attribution,.verseblock .attribution{font-size:.9375em;line-height:1.45;font-style:italic}
.quoteblock .attribution br,.verseblock .attribution br{display:none}
.quoteblock .attribution cite,.verseblock .attribution cite{display:block;letter-spacing:-.025em;color:rgba(0,0,0,.6)}
.quoteblock.abstract blockquote::before,.quoteblock.excerpt blockquote::before,.quoteblock .quoteblock blockquote::before{display:none}
.quoteblock.abstract blockquote,.quoteblock.abstract p,.quoteblock.excerpt blockquote,.quoteblock.excerpt p,.quoteblock .quoteblock blockquote,.quoteblock .quoteblock p{line-height:1.6;word-spacing:0}
.quoteblock.abstract{margin:0 1em 1.25em;display:block}
.quoteblock.abstract>.title{margin:0 0 .375em;font-size:1.15em;text-align:center}
.quoteblock.excerpt>blockquote,.quoteblock .quoteblock{padding:0 0 .25em 1em;border-left:.25em solid #dddddf}
.quoteblock.excerpt,.quoteblock .quoteblock{margin-left:0}
.quoteblock.excerpt blockquote,.quoteblock.excerpt p,.quoteblock .quoteblock blockquote,.quoteblock .quoteblock p{color:inherit;font-size:1.0625rem}
.quoteblock.excerpt .attribution,.quoteblock .quoteblock .attribution{color:inherit;font-size:.85rem;text-align:left;margin-right:0}
p.tableblock:last-child{margin-bottom:0}
td.tableblock>.content{margin-bottom:1.25em;word-wrap:anywhere}
td.tableblock>.content>:last-child{margin-bottom:-1.25em}
table.tableblock,th.tableblock,td.tableblock{border:0 solid #dedede}
table.grid-all>*>tr>*{border-width:1px}
table.grid-cols>*>tr>*{border-width:0 1px}
table.grid-rows>*>tr>*{border-width:1px 0}
table.frame-all{border-width:1px}
table.frame-ends{border-width:1px 0}
table.frame-sides{border-width:0 1px}
table.frame-none>colgroup+*>:first-child>*,table.frame-sides>colgroup+*>:first-child>*{border-top-width:0}
table.frame-none>:last-child>:last-child>*,table.frame-sides>:last-child>:last-child>*{border-bottom-width:0}
table.frame-none>*>tr>:first-child,table.frame-ends>*>tr>:first-child{border-left-width:0}
table.frame-none>*>tr>:last-child,table.frame-ends>*>tr>:last-child{border-right-width:0}
table.stripes-all tr,table.stripes-odd tr:nth-of-type(odd),table.stripes-even tr:nth-of-type(even),table.stripes-hover tr:hover{background:#f8f8f7}
th.halign-left,td.halign-left{text-align:left}
th.halign-right,td.halign-right{text-align:right}
th.halign-center,td.halign-center{text-align:center}
th.valign-top,td.valign-top{vertical-align:top}
th.valign-bottom,td.valign-bottom{vertical-align:bottom}
th.valign-middle,td.valign-middle{vertical-align:middle}
table thead th,table tfoot th{font-weight:bold}
tbody tr th{background:#f7f8f7}
tbody tr th,tbody tr th p,tfoot tr th,tfoot tr th p{color:rgba(0,0,0,.8);font-weight:bold}
p.tableblock>code:only-child{background:none;padding:0}
p.tableblock{font-size:1em}
ol{margin-left:1.75em}
ul li ol{margin-left:1.5em}
dl dd{margin-left:1.125em}
dl dd:last-child,dl dd:last-child>:last-child{margin-bottom:0}
ol>li p,ul>li p,ul dd,ol dd,.olist .olist,.ulist .ulist,.ulist .olist,.olist .ulist{margin-bottom:.625em}
ul.checklist,ul.none,ol.none,ul.no-bullet,ol.no-bullet,ol.unnumbered,ul.unstyled,ol.unstyled{list-style-type:none}
ul.no-bullet,ol.no-bullet,ol.unnumbered{margin-left:.625em}
ul.unstyled,ol.unstyled{margin-left:0}
ul.checklist{margin-left:.625em}
ul.checklist li>p:first-child>.fa-square-o:first-child,ul.checklist li>p:first-child>.fa-check-square-o:first-child{width:1.25em;font-size:.8em;position:relative;bottom:.125em}
ul.checklist li>p:first-child>input[type="checkbox"]:first-child{margin-right:.25em}
ul.inline{display:-ms-flexbox;display:-webkit-box;display:flex;-ms-flex-flow:row wrap;-webkit-flex-flow:row wrap;flex-flow:row wrap;list-style:none;margin:0 0 .625em -1.25em}
ul.inline>li{margin-left:1.25em}
.unstyled dl dt{font-weight:400;font-style:normal}
ol.arabic{list-style-type:decimal}
ol.decimal{list-style-type:decimal-leading-zero}
ol.loweralpha{list-style-type:lower-alpha}
ol.upperalpha{list-style-type:upper-alpha}
ol.lowerroman{list-style-type:lower-roman}
ol.upperroman{list-style-type:upper-roman}
ol.lowergreek{list-style-type:lower-greek}
.hdlist>table,.colist>table{border:0;background:none}
.hdlist>table>tbody>tr,.colist>table>tbody>tr{background:none}
td.hdlist1,td.hdlist2{vertical-align:top;padding:0 .625em}
td.hdlist1{font-weight:bold;padding-bottom:1.25em}
td.hdlist2{word-wrap:anywhere}
.literalblock+.colist,.listingblock+.colist{margin-top:-.5em}
.colist td:not([class]):first-child{padding:.4em .75em 0;line-height:1;vertical-align:top}
.colist td:not([class]):first-child img{max-width:none}
.colist td:not([class]):last-child{padding:.25em 0}
.thumb,.th{line-height:0;display:inline-block;border:solid 4px #fff;-webkit-box-shadow:0 0 0 1px #ddd;box-shadow:0 0 0 1px #ddd}
.imageblock.left{margin:.25em .625em 1.25em 0}
.imageblock.right{margin:.25em 0 1.25em .625em}
.imageblock>.title{margin-bottom:0}
.imageblock.thumb,.imageblock.th{border-width:6px}
.imageblock.thumb>.title,.imageblock.th>.title{padding:0 .125em}
.image.left,.image.right{margin-top:.25em;margin-bottom:.25em;display:inline-block;line-height:0}
.image.left{margin-right:.625em}
.image.right{margin-left:.625em}
a.image{text-decoration:none;display:inline-block}
a.image object{pointer-events:none}
sup.footnote,sup.footnoteref{font-size:.875em;position:static;vertical-align:super}
sup.footnote a,sup.footnoteref a{text-decoration:none}
sup.footnote a:active,sup.footnoteref a:active{text-decoration:underline}
#footnotes{padding-top:.75em;padding-bottom:.75em;margin-bottom:.625em}
#footnotes hr{width:20%;min-width:6.25em;margin:-.25em 0 .75em;border-width:1px 0 0}
#footnotes .footnote{padding:0 .375em 0 .225em;line-height:1.3334;font-size:.875em;margin-left:1.2em;margin-bottom:.2em}
#footnotes .footnote a:first-of-type{font-weight:bold;text-decoration:none;margin-left:-1.05em}
#footnotes .footnote:last-of-type{margin-bottom:0}
#content #footnotes{margin-top:-.625em;margin-bottom:0;padding:.75em 0}
.gist .file-data>table{border:0;background:#fff;width:100%;margin-bottom:0}
.gist .file-data>table td.line-data{width:99%}
div.unbreakable{page-break-inside:avoid}
.big{font-size:larger}
.small{font-size:smaller}
.underline{text-decoration:underline}
.overline{text-decoration:overline}
.line-through{text-decoration:line-through}
.aqua{color:#00bfbf}
.aqua-background{background:#00fafa}
.black{color:#000}
.black-background{background:#000}
.blue{color:#0000bf}
.blue-background{background:#0000fa}
.fuchsia{color:#bf00bf}
.fuchsia-background{background:#fa00fa}
.gray{color:#606060}
.gray-background{background:#7d7d7d}
.green{color:#006000}
.green-background{background:#007d00}
.lime{color:#00bf00}
.lime-background{background:#00fa00}
.maroon{color:#600000}
.maroon-background{background:#7d0000}
.navy{color:#000060}
.navy-background{background:#00007d}
.olive{color:#606000}
.olive-background{background:#7d7d00}
.purple{color:#600060}
.purple-background{background:#7d007d}
.red{color:#bf0000}
.red-background{background:#fa0000}
.silver{color:#909090}
.silver-background{background:#bcbcbc}
.teal{color:#006060}
.teal-background{background:#007d7d}
.white{color:#bfbfbf}
.white-background{background:#fafafa}
.yellow{color:#bfbf00}
.yellow-background{background:#fafa00}
span.icon>.fa{cursor:default}
a span.icon>.fa{cursor:inherit}
.admonitionblock td.icon [class^="fa icon-"]{font-size:2.5em;text-shadow:1px 1px 2px rgba(0,0,0,.5);cursor:default}
.admonitionblock td.icon .icon-note::before{content:"\f05a";color:#19407c}
.admonitionblock td.icon .icon-tip::before{content:"\f0eb";text-shadow:1px 1px 2px rgba(155,155,0,.8);color:#111}
.admonitionblock td.icon .icon-warning::before{content:"\f071";color:#bf6900}
.admonitionblock td.icon .icon-caution::before{content:"\f06d";color:#bf3400}
.admonitionblock td.icon .icon-important::before{content:"\f06a";color:#bf0000}
.conum[data-value]{display:inline-block;color:#fff!important;background:rgba(0,0,0,.8);-webkit-border-radius:50%;border-radius:50%;text-align:center;font-size:.75em;width:1.67em;height:1.67em;line-height:1.67em;font-family:"Open Sans","DejaVu Sans",sans-serif;font-style:normal;font-weight:bold}
.conum[data-value] *{color:#fff!important}
.conum[data-value]+b{display:none}
.conum[data-value]::after{content:attr(data-value)}
pre .conum[data-value]{position:relative;top:-.125em}
b.conum *{color:inherit!important}
.conum:not([data-value]):empty{display:none}
dt,th.tableblock,td.content,div.footnote{text-rendering:optimizeLegibility}
h1,h2,p,td.content,span.alt{letter-spacing:-.01em}
p strong,td.content strong,div.footnote strong{letter-spacing:-.005em}
p,blockquote,dt,td.content,span.alt{font-size:1.0625rem}
p{margin-bottom:1.25rem}
.sidebarblock p,.sidebarblock dt,.sidebarblock td.content,p.tableblock{font-size:1em}
.exampleblock>.content{background:#fffef7;border-color:#e0e0dc;-webkit-box-shadow:0 1px 4px #e0e0dc;box-shadow:0 1px 4px #e0e0dc}
.print-only{display:none!important}
@page{margin:1.25cm .75cm}
@media print{*{-webkit-box-shadow:none!important;box-shadow:none!important;text-shadow:none!important}
html{font-size:80%}
a{color:inherit!important;text-decoration:underline!important}
a.bare,a[href^="#"],a[href^="mailto:"]{text-decoration:none!important}
a[href^="http:"]:not(.bare)::after,a[href^="https:"]:not(.bare)::after{content:"(" attr(href) ")";display:inline-block;font-size:.875em;padding-left:.25em}
abbr[title]::after{content:" (" attr(title) ")"}
pre,blockquote,tr,img,object,svg{page-break-inside:avoid}
thead{display:table-header-group}
svg{max-width:100%}
p,blockquote,dt,td.content{font-size:1em;orphans:3;widows:3}
h2,h3,#toctitle,.sidebarblock>.content>.title{page-break-after:avoid}
#header,#content,#footnotes,#footer{max-width:none}
#toc,.sidebarblock,.exampleblock>.content{background:none!important}
#toc{border-bottom:1px solid #dddddf!important;padding-bottom:0!important}
body.book #header{text-align:center}
body.book #header>h1:first-child{border:0!important;margin:2.5em 0 1em}
body.book #header .details{border:0!important;display:block;padding:0!important}
body.book #header .details span:first-child{margin-left:0!important}
body.book #header .details br{display:block}
body.book #header .details br+span::before{content:none!important}
body.book #toc{border:0!important;text-align:left!important;padding:0!important;margin:0!important}
body.book #toc,body.book #preamble,body.book h1.sect0,body.book .sect1>h2{page-break-before:always}
.listingblock code[data-lang]::before{display:block}
#footer{padding:0 .9375em}
.hide-on-print{display:none!important}
.print-only{display:block!important}
.hide-for-print{display:none!important}
.show-for-print{display:inherit!important}}
@media print,amzn-kf8{#header>h1:first-child{margin-top:1.25rem}
.sect1{padding:0!important}
.sect1+.sect1{border:0}
#footer{background:none}
#footer-text{color:rgba(0,0,0,.6);font-size:.9em}}
@media amzn-kf8{#header,#content,#footnotes,#footer{padding:0}}
</style>
</head>
<body id="openshift-tutorial" class="article">
<div id="header">
<h1>Creating a service network with OpenShift</h1>
</div>
<div id="content">
<div id="preamble">
<div class="sectionbody">
<div class="paragraph system:abstract">
<p>This tutorial demonstrates how to connect a frontend service on a OpenShift cluster with a backend service on a OpenShift cluster using the <code>skupper</code> command-line interface (CLI).</p>
</div>
<div class="ulist">
<div class="title">Prerequisites</div>
<ul>
<li>
<p>Access to projects in two OpenShift clusters, <code>cluster-admin</code> access is not required.</p>
</li>
<li>
<p>One of the OpenShift clusters must be addressable from the other cluster.</p>
</li>
</ul>
</div>
<div class="paragraph">
<p>This tutorial shows how to connect the following namespaces:</p>
</div>
<div class="ulist">
<ul>
<li>
<p><code>west</code> - runs the frontend service and is typically a public cluster.</p>
</li>
<li>
<p><code>east</code> - runs the backend service.</p>
</li>
</ul>
</div>
</div>
</div>
<div class="sect1">
<h2 id="introduction-to-skupper">1. Introduction to Skupper </h2>
<div class="sectionbody">
<div class="paragraph">
<p>A service network enables communication between services running in different network locations.
It allows geographically distributed services to connect as if they were all running in the same site.</p>
</div>
<div class="imageblock">
<div class="content">
<img src="data:image/svg+xml;base64,PHN2ZyBpZD0iYmY4NzkwZGYtNDNlYS00NjNhLWI1ZGEtNDAxYmIyYThiNDAyIiBkYXRhLW5hbWU9ImFydHdvcmsiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgd2lkdGg9Ijc2MCIgaGVpZ2h0PSIzNjMuODY0Ij48ZGVmcz48c3R5bGU+LmE2YjRlYWU1LTJiZTMtNGFjYi05OThmLWMwNDA4OTc5YWI3YXtmaWxsOiNlOGU4ZTh9LmE3ZjNkNDg5LTFjNzMtNDI0ZC05MmZlLWFlNmE2MGQ5YjZhOCwuYWEwNTZlYTctOTllYS00NDY0LWJmYTAtM2Q3ZTkwNTdiYjBhLC5hYzUwYjZiYy0yMjdlLTQ0YWQtOWViMC00Y2FjOGI1OGNlYjEsLmFlMTFiYzRlLTNhNTktNDMwMS05OWUwLWJhNDM5OWU5ODM0MSwuYjhhMDEwYmMtMTdjMi00NDYxLTlhOWQtMjk3MWRjNDUyZDI5LC5mNjNmMmVkNS0xY2NhLTRmYWUtYmU1Mi05OGI3NWFlYzhmZDl7ZmlsbDpub25lfS5hN2YzZDQ4OS0xYzczLTQyNGQtOTJmZS1hZTZhNjBkOWI2YTgsLmI4YTAxMGJjLTE3YzItNDQ2MS05YTlkLTI5NzFkYzQ1MmQyOSwuZjYzZjJlZDUtMWNjYS00ZmFlLWJlNTItOThiNzVhZWM4ZmQ5e3N0cm9rZTojYWRhZGFkfS5hN2YzZDQ4OS0xYzczLTQyNGQtOTJmZS1hZTZhNjBkOWI2YTgsLmFhMDU2ZWE3LTk5ZWEtNDQ2NC1iZmEwLTNkN2U5MDU3YmIwYSwuYWM1MGI2YmMtMjI3ZS00NGFkLTllYjAtNGNhYzhiNThjZWIxLC5hZTExYmM0ZS0zYTU5LTQzMDEtOTllMC1iYTQzOTllOTgzNDEsLmI4YTAxMGJjLTE3YzItNDQ2MS05YTlkLTI5NzFkYzQ1MmQyOSwuZjYzZjJlZDUtMWNjYS00ZmFlLWJlNTItOThiNzVhZWM4ZmQ5e3N0cm9rZS1saW5lY2FwOnJvdW5kO3N0cm9rZS1saW5lam9pbjpyb3VuZH0uYjhhMDEwYmMtMTdjMi00NDYxLTlhOWQtMjk3MWRjNDUyZDI5e3N0cm9rZS1kYXNoYXJyYXk6MyAzfS5hN2YzZDQ4OS0xYzczLTQyNGQtOTJmZS1hZTZhNjBkOWI2YTh7c3Ryb2tlLWRhc2hhcnJheToyLjk5OCAyLjk5OH0uZWRmOWI3OGQtZmE4NC00YWY2LTgyNWMtNDgxMWIxM2MxMDZhe2ZvbnQtc2l6ZToxNHB4fS5iM2Y0ZDUwNy1mZWRiLTRiOTUtOGZhOC0yN2EyN2YzZDRmOWEsLmI1MjcxYzI3LTNjZTEtNDgyNS1hZmQzLWIyMjE3YjVhZDc2NSwuZWQ5ODQyYmEtMWU3Mi00YWY4LWI1ZmMtMzRmMzk4N2QxNjYzLC5lZGY5Yjc4ZC1mYTg0LTRhZjYtODI1Yy00ODExYjEzYzEwNmEsLmVmZDYzYTE1LTQ3NzItNDE4MC05ZDZhLWEzZmJjY2U4ZmEwY3tmaWxsOiMxNTE1MTV9LmVkZjliNzhkLWZhODQtNGFmNi04MjVjLTQ4MTFiMTNjMTA2YSwuZWZkNjNhMTUtNDc3Mi00MTgwLTlkNmEtYTNmYmNjZThmYTBje2ZvbnQtZmFtaWx5OlJlZEhhdFRleHQsJnF1b3Q7UmVkIEhhdCBUZXh0JnF1b3Q7LE92ZXJwYXNzLCZxdW90O0hlbHZldGljYSBOZXVlJnF1b3Q7LEFyaWFsLHNhbnMtc2VyaWY7Zm9udC13ZWlnaHQ6NzAwfS5iY2RmYjc2Yi1lOTUwLTRmNTAtYmUyNS1iODRhOTEyOTM0ZTd7ZmlsbDojZmZmfS5iNTI3MWMyNy0zY2UxLTQ4MjUtYWZkMy1iMjIxN2I1YWQ3NjUsLmVmZDYzYTE1LTQ3NzItNDE4MC05ZDZhLWEzZmJjY2U4ZmEwY3tmb250LXNpemU6MTJweH0uYjNmNGQ1MDctZmVkYi00Yjk1LThmYTgtMjdhMjdmM2Q0Zjlhe2ZvbnQtc2l6ZToxMXB4fS5iM2Y0ZDUwNy1mZWRiLTRiOTUtOGZhOC0yN2EyN2YzZDRmOWEsLmI1MjcxYzI3LTNjZTEtNDgyNS1hZmQzLWIyMjE3YjVhZDc2NXtmb250LWZhbWlseTpSZWRIYXRUZXh0LCZxdW90O1JlZCBIYXQgVGV4dCZxdW90OyxPdmVycGFzcywmcXVvdDtIZWx2ZXRpY2EgTmV1ZSZxdW90OyxBcmlhbCxzYW5zLXNlcmlmO2ZvbnQtd2VpZ2h0OjUwMH0uYWM1MGI2YmMtMjI3ZS00NGFkLTllYjAtNGNhYzhiNThjZWIxe3N0cm9rZTojMTUxNTE1fS5lNWQ3MzU5MC1kMjUwLTQxMTEtYTFiOC0xZjA3NTU0ODBiMzV7ZmlsbDojMDZjfS5hYTA1NmVhNy05OWVhLTQ0NjQtYmZhMC0zZDdlOTA1N2JiMGEsLmFlMTFiYzRlLTNhNTktNDMwMS05OWUwLWJhNDM5OWU5ODM0MXtzdHJva2U6Izk5YzJlYn0uYWEwNTZlYTctOTllYS00NDY0LWJmYTAtM2Q3ZTkwNTdiYjBhe3N0cm9rZS1kYXNoYXJyYXk6My4yIDMuMn08L3N0eWxlPjwvZGVmcz48cGF0aCBjbGFzcz0iYTZiNGVhZTUtMmJlMy00YWNiLTk5OGYtYzA0MDg5NzlhYjdhIiBkPSJNMCAxNmgzMTB2MzA3Ljg2NEgweiIvPjxwYXRoIGNsYXNzPSJmNjNmMmVkNS0xY2NhLTRmYWUtYmU1Mi05OGI3NWFlYzhmZDkiIGQ9Ik0yMCAyNjIuMzY0djEuNWgxLjUiLz48cGF0aCBjbGFzcz0iYjhhMDEwYmMtMTdjMi00NDYxLTlhOWQtMjk3MWRjNDUyZDI5IiBkPSJNMjQuNSAyNjMuODY0SDI4NyIvPjxwYXRoIGNsYXNzPSJmNjNmMmVkNS0xY2NhLTRmYWUtYmU1Mi05OGI3NWFlYzhmZDkiIGQ9Ik0yODguNSAyNjMuODY0aDEuNXYtMS41Ii8+PHBhdGggY2xhc3M9ImE3ZjNkNDg5LTFjNzMtNDI0ZC05MmZlLWFlNmE2MGQ5YjZhOCIgZD0iTTI5MCAyNTkuMzY2VjM4Ljk5OSIvPjxwYXRoIGNsYXNzPSJmNjNmMmVkNS0xY2NhLTRmYWUtYmU1Mi05OGI3NWFlYzhmZDkiIGQ9Ik0yOTAgMzcuNVYzNmgtMS41Ii8+PHBhdGggY2xhc3M9ImI4YTAxMGJjLTE3YzItNDQ2MS05YTlkLTI5NzFkYzQ1MmQyOSIgZD0iTTI4NS41IDM2SDIzIi8+PHBhdGggY2xhc3M9ImY2M2YyZWQ1LTFjY2EtNGZhZS1iZTUyLTk4Yjc1YWVjOGZkOSIgZD0iTTIxLjUgMzZIMjB2MS41Ii8+PHBhdGggY2xhc3M9ImE3ZjNkNDg5LTFjNzMtNDI0ZC05MmZlLWFlNmE2MGQ5YjZhOCIgZD0iTTIwIDQwLjQ5OHYyMjAuMzY3Ii8+PHRleHQgY2xhc3M9ImVkZjliNzhkLWZhODQtNGFmNi04MjVjLTQ4MTFiMTNjMTA2YSIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMjAgMzAzLjk4NCkiPkt1YmVybmV0ZXMgQ2x1c3RlciBBPC90ZXh0PjxwYXRoIGNsYXNzPSJiY2RmYjc2Yi1lOTUwLTRmNTAtYmUyNS1iODRhOTEyOTM0ZTciIHRyYW5zZm9ybT0icm90YXRlKDE4MCAxNTUgMTQ3LjYxNCkiIGQ9Ik0zMCA0Ni4zNjRoMjUwdjIwMi41SDMweiIvPjx0ZXh0IGNsYXNzPSJlZmQ2M2ExNS00NzcyLTQxODAtOWQ2YS1hM2ZiY2NlOGZhMGMiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDQ1IDIzMy43MDQpIj5TaXRlIEE8L3RleHQ+PHBhdGggY2xhc3M9ImE2YjRlYWU1LTJiZTMtNGFjYi05OThmLWMwNDA4OTc5YWI3YSIgZD0iTTQ1IDE1OC44NjRoMjIwdjUwSDQ1eiIvPjx0ZXh0IGNsYXNzPSJiM2Y0ZDUwNy1mZWRiLTRiOTUtOGZhOC0yN2EyN2YzZDRmOWEiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDEyMy4zMzIgMTg2LjkxMSkiPkRlcGxveW1lbnQ8L3RleHQ+PHBhdGggY2xhc3M9ImE2YjRlYWU1LTJiZTMtNGFjYi05OThmLWMwNDA4OTc5YWI3YSIgZD0iTTM0Ni41IDE2SDc2MHYzMDcuODY0SDM0Ni41eiIvPjxwYXRoIGNsYXNzPSJmNjNmMmVkNS0xY2NhLTRmYWUtYmU1Mi05OGI3NWFlYzhmZDkiIGQ9Ik0zNjYuNSAyNjIuMzY0djEuNWgxLjUiLz48cGF0aCBjbGFzcz0iYjhhMDEwYmMtMTdjMi00NDYxLTlhOWQtMjk3MWRjNDUyZDI5IiBkPSJNMzcxIDI2My44NjRoMTcyLjUiLz48cGF0aCBjbGFzcz0iZjYzZjJlZDUtMWNjYS00ZmFlLWJlNTItOThiNzVhZWM4ZmQ5IiBkPSJNNTQ1IDI2My44NjRoMS41di0xLjUiLz48cGF0aCBjbGFzcz0iYTdmM2Q0ODktMWM3My00MjRkLTkyZmUtYWU2YTYwZDliNmE4IiBkPSJNNTQ2LjUgMjU5LjM2NlYzOC45OTkiLz48cGF0aCBjbGFzcz0iZjYzZjJlZDUtMWNjYS00ZmFlLWJlNTItOThiNzVhZWM4ZmQ5IiBkPSJNNTQ2LjUgMzcuNVYzNkg1NDUiLz48cGF0aCBjbGFzcz0iYjhhMDEwYmMtMTdjMi00NDYxLTlhOWQtMjk3MWRjNDUyZDI5IiBkPSJNNTQyIDM2SDM2OS41Ii8+PHBhdGggY2xhc3M9ImY2M2YyZWQ1LTFjY2EtNGZhZS1iZTUyLTk4Yjc1YWVjOGZkOSIgZD0iTTM2OCAzNmgtMS41djEuNSIvPjxwYXRoIGNsYXNzPSJhN2YzZDQ4OS0xYzczLTQyNGQtOTJmZS1hZTZhNjBkOWI2YTgiIGQ9Ik0zNjYuNSA0MC40OTh2MjIwLjM2NyIvPjx0ZXh0IGNsYXNzPSJlZGY5Yjc4ZC1mYTg0LTRhZjYtODI1Yy00ODExYjEzYzEwNmEiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDM2Ni41IDMwMy45ODQpIj5LdWJlcm5ldGVzIENsdXN0ZXIgQjwvdGV4dD48cGF0aCBjbGFzcz0iYmNkZmI3NmItZTk1MC00ZjUwLWJlMjUtYjg0YTkxMjkzNGU3IiB0cmFuc2Zvcm09InJvdGF0ZSgxODAgNDU2LjUgMTQ3LjYxNCkiIGQ9Ik0zNzYuNSA0Ni4zNjRoMTYwdjIwMi41aC0xNjB6Ii8+PHRleHQgY2xhc3M9ImVmZDYzYTE1LTQ3NzItNDE4MC05ZDZhLWEzZmJjY2U4ZmEwYyIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMzkxLjUgMjMzLjcwNCkiPlNpdGUgQjwvdGV4dD48cGF0aCBjbGFzcz0iYTZiNGVhZTUtMmJlMy00YWNiLTk5OGYtYzA0MDg5NzlhYjdhIiBkPSJNMzkxLjUgMTU4Ljg2NGgxMzB2NTBoLTEzMHoiLz48dGV4dCBjbGFzcz0iYjNmNGQ1MDctZmVkYi00Yjk1LThmYTgtMjdhMjdmM2Q0ZjlhIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSg0MzcuMjg5IDE4Ni45MTEpIj5TZXJ2aWNlPC90ZXh0PjxwYXRoIGNsYXNzPSJhYzUwYjZiYy0yMjdlLTQ0YWQtOWViMC00Y2FjOGI1OGNlYjEiIGQ9Ik00NTYuNSAxNDkuMTg4VjEyMy41NCIvPjxwYXRoIGNsYXNzPSJlZDk4NDJiYS0xZTcyLTRhZjgtYjVmYy0zNGYzOTg3ZDE2NjMiIGQ9Ik00NjEuNDg2IDE0Ny43MjlsLTQuOTg2IDguNjM1LTQuOTg2LTguNjM1aDkuOTcyek00NjEuNDg2IDEyNC45OTlsLTQuOTg2LTguNjM1LTQuOTg2IDguNjM1aDkuOTcyeiIvPjxwYXRoIGNsYXNzPSJiY2RmYjc2Yi1lOTUwLTRmNTAtYmUyNS1iODRhOTEyOTM0ZTciIHRyYW5zZm9ybT0icm90YXRlKDE4MCA2NTAgMTQ3LjYxNCkiIGQ9Ik01NzAgNDYuMzY0aDE2MHYyMDIuNUg1NzB6Ii8+PHRleHQgY2xhc3M9ImVmZDYzYTE1LTQ3NzItNDE4MC05ZDZhLWEzZmJjY2U4ZmEwYyIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNTg1IDIzMy43MDQpIj5TaXRlIEM8L3RleHQ+PHBhdGggY2xhc3M9ImE2YjRlYWU1LTJiZTMtNGFjYi05OThmLWMwNDA4OTc5YWI3YSIgZD0iTTU4NSAxNTguODY0aDEzMHY1MEg1ODV6Ii8+PHRleHQgY2xhc3M9ImIzZjRkNTA3LWZlZGItNGI5NS04ZmE4LTI3YTI3ZjNkNGY5YSIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNjMwLjc4OSAxODYuOTExKSI+U2VydmljZTwvdGV4dD48cGF0aCBjbGFzcz0iYWM1MGI2YmMtMjI3ZS00NGFkLTllYjAtNGNhYzhiNThjZWIxIiBkPSJNNjUwIDE0OS4xODhWMTIzLjU0Ii8+PHBhdGggY2xhc3M9ImVkOTg0MmJhLTFlNzItNGFmOC1iNWZjLTM0ZjM5ODdkMTY2MyIgZD0iTTY1NC45ODYgMTQ3LjcyOUw2NTAgMTU2LjM2NGwtNC45ODYtOC42MzVoOS45NzJ6TTY1NC45ODYgMTI0Ljk5OUw2NTAgMTE2LjM2NGwtNC45ODYgOC42MzVoOS45NzJ6Ii8+PGc+PHBhdGggY2xhc3M9ImY2M2YyZWQ1LTFjY2EtNGZhZS1iZTUyLTk4Yjc1YWVjOGZkOSIgZD0iTTU2MCAyNjIuMzY0djEuNWgxLjUiLz48cGF0aCBjbGFzcz0iYjhhMDEwYmMtMTdjMi00NDYxLTlhOWQtMjk3MWRjNDUyZDI5IiBkPSJNNTY0LjUgMjYzLjg2NEg3MzciLz48cGF0aCBjbGFzcz0iZjYzZjJlZDUtMWNjYS00ZmFlLWJlNTItOThiNzVhZWM4ZmQ5IiBkPSJNNzM4LjUgMjYzLjg2NGgxLjV2LTEuNSIvPjxwYXRoIGNsYXNzPSJhN2YzZDQ4OS0xYzczLTQyNGQtOTJmZS1hZTZhNjBkOWI2YTgiIGQ9Ik03NDAgMjU5LjM2NlYzOC45OTkiLz48cGF0aCBjbGFzcz0iZjYzZjJlZDUtMWNjYS00ZmFlLWJlNTItOThiNzVhZWM4ZmQ5IiBkPSJNNzQwIDM3LjVWMzZoLTEuNSIvPjxwYXRoIGNsYXNzPSJiOGEwMTBiYy0xN2MyLTQ0NjEtOWE5ZC0yOTcxZGM0NTJkMjkiIGQ9Ik03MzUuNSAzNkg1NjMiLz48cGF0aCBjbGFzcz0iZjYzZjJlZDUtMWNjYS00ZmFlLWJlNTItOThiNzVhZWM4ZmQ5IiBkPSJNNTYxLjUgMzZINTYwdjEuNSIvPjxwYXRoIGNsYXNzPSJhN2YzZDQ4OS0xYzczLTQyNGQtOTJmZS1hZTZhNjBkOWI2YTgiIGQ9Ik01NjAgNDAuNDk4djIyMC4zNjciLz48L2c+PHBhdGggY2xhc3M9ImU1ZDczNTkwLWQyNTAtNDExMS1hMWI4LTFmMDc1NTQ4MGIzNSIgZD0iTTQ1IDYxLjM2NGg2NjkuNXY1Mi41SDQ1eiIvPjxwYXRoIGNsYXNzPSJhNmI0ZWFlNS0yYmUzLTRhY2ItOTk4Zi1jMDQwODk3OWFiN2EiIGQ9Ik0xMTMuNDYzIDI1OC44MTdoODMuMDczdjE1LjA5NGgtODMuMDczeiIvPjx0ZXh0IGNsYXNzPSJiNTI3MWMyNy0zY2UxLTQ4MjUtYWZkMy1iMjIxN2I1YWQ3NjUiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDExNi40OTIgMjY3LjQ5NikiPk5hbWVzcGFjZSBBPC90ZXh0PjxwYXRoIGNsYXNzPSJhNmI0ZWFlNS0yYmUzLTRhY2ItOTk4Zi1jMDQwODk3OWFiN2EiIGQ9Ik00MTEuODg5IDI1OC44MTdoODkuMjIzdjE1LjA5NGgtODkuMjIzeiIvPjx0ZXh0IGNsYXNzPSJiNTI3MWMyNy0zY2UxLTQ4MjUtYWZkMy1iMjIxN2I1YWQ3NjUiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDQxNy45OTggMjY3LjQ5NikiPk5hbWVzcGFjZSBCPC90ZXh0PjxwYXRoIGNsYXNzPSJhNmI0ZWFlNS0yYmUzLTRhY2ItOTk4Zi1jMDQwODk3OWFiN2EiIGQ9Ik02MDUuMzUyIDI1OC44MTdoODkuMjk3djE1LjA5NGgtODkuMjk3eiIvPjx0ZXh0IGNsYXNzPSJiNTI3MWMyNy0zY2UxLTQ4MjUtYWZkMy1iMjIxN2I1YWQ3NjUiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDYxMS4zMzcgMjY3LjQ5NikiPk5hbWVzcGFjZSBDPC90ZXh0PjxwYXRoIGNsYXNzPSJiY2RmYjc2Yi1lOTUwLTRmNTAtYmUyNS1iODRhOTEyOTM0ZTciIGQ9Ik0xMzAuMDAxIDEyOC45ODJ2LTIxLjQyOGwyNS03LjE0MyAyNSA3LjE0M3YyMS40MjhoLTUweiIvPjx0ZXh0IGNsYXNzPSJiM2Y0ZDUwNy1mZWRiLTRiOTUtOGZhOC0yN2EyN2YzZDRmOWEiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDE0My43NzggMTE4LjgzMSkiPlRDUDwvdGV4dD48Zz48cGF0aCBjbGFzcz0iYWUxMWJjNGUtM2E1OS00MzAxLTk5ZTAtYmE0Mzk5ZTk4MzQxIiBkPSJNMTU1IDk5LjQxMXYtMS41Ii8+PHBhdGggc3Ryb2tlLWRhc2hhcnJheT0iMy40OTQgMy40OTQiIHN0cm9rZT0iIzk5YzJlYiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBmaWxsPSJub25lIiBkPSJNMTU1IDk0LjQxN3YtNS4yNCIvPjxwYXRoIGNsYXNzPSJhZTExYmM0ZS0zYTU5LTQzMDEtOTllMC1iYTQzOTllOTgzNDEiIGQ9Ik0xNTUgODcuNDN2LTEuNWgxLjUiLz48cGF0aCBzdHJva2UtZGFzaGFycmF5PSIzLjAxNSAzLjAxNSIgc3Ryb2tlPSIjOTljMmViIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGZpbGw9Im5vbmUiIGQ9Ik0xNTkuNTE1IDg1LjkzaDI5My45NzgiLz48cGF0aCBjbGFzcz0iYWUxMWJjNGUtM2E1OS00MzAxLTk5ZTAtYmE0Mzk5ZTk4MzQxIiBkPSJNNDU1LjAwMSA4NS45M2gxLjV2MS41Ii8+PHBhdGggY2xhc3M9ImFhMDU2ZWE3LTk5ZWEtNDQ2NC1iZmEwLTNkN2U5MDU3YmIwYSIgZD0iTTQ1Ni41MDEgOTAuNjN2MTcuNjAxIi8+PHBhdGggY2xhc3M9ImFlMTFiYzRlLTNhNTktNDMwMS05OWUwLWJhNDM5OWU5ODM0MSIgZD0iTTQ1Ni41MDEgMTA5LjgzMXYxLjUiLz48L2c+PGc+PHBhdGggY2xhc3M9ImFlMTFiYzRlLTNhNTktNDMwMS05OWUwLWJhNDM5OWU5ODM0MSIgZD0iTTQ1Ni41MDEgODUuOTNoMS41Ii8+PHBhdGggc3Ryb2tlLWRhc2hhcnJheT0iMy4wMjQgMy4wMjQiIHN0cm9rZT0iIzk5YzJlYiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBmaWxsPSJub25lIiBkPSJNNDYxLjAyNSA4NS45M2gxODUuOTYzIi8+PHBhdGggY2xhc3M9ImFlMTFiYzRlLTNhNTktNDMwMS05OWUwLWJhNDM5OWU5ODM0MSIgZD0iTTY0OC41IDg1LjkzaDEuNXYxLjUiLz48cGF0aCBjbGFzcz0iYWEwNTZlYTctOTllYS00NDY0LWJmYTAtM2Q3ZTkwNTdiYjBhIiBkPSJNNjUwIDkwLjYzdjE3LjYwMSIvPjxwYXRoIGNsYXNzPSJhZTExYmM0ZS0zYTU5LTQzMDEtOTllMC1iYTQzOTllOTgzNDEiIGQ9Ik02NTAgMTA5LjgzMXYxLjUiLz48L2c+PGc+PHBhdGggY2xhc3M9ImFjNTBiNmJjLTIyN2UtNDRhZC05ZWIwLTRjYWM4YjU4Y2ViMSIgZD0iTTE1NSAxNDkuMTg4VjEzMy41NCIvPjxwYXRoIGNsYXNzPSJlZDk4NDJiYS0xZTcyLTRhZjgtYjVmYy0zNGYzOTg3ZDE2NjMiIGQ9Ik0xNTkuOTg2IDE0Ny43MjlMMTU1IDE1Ni4zNjRsLTQuOTg2LTguNjM1aDkuOTcyek0xNTkuOTg2IDEzNC45OTlMMTU1IDEyNi4zNjRsLTQuOTg2IDguNjM1aDkuOTcyeiIvPjwvZz48cGF0aCBjbGFzcz0iZTVkNzM1OTAtZDI1MC00MTExLWExYjgtMWYwNzU1NDgwYjM1IiBkPSJNMjYxLjA0NiA3Mi4wMDhoMTE5Ljk1djI1LjIxMWgtMTE5Ljk1eiIvPjx0ZXh0IHRyYW5zZm9ybT0idHJhbnNsYXRlKDI2NC4zOTQgODguNzM1KSIgZm9udC1zaXplPSIxMSIgZmlsbD0iI2ZmZiIgZm9udC1mYW1pbHk9IlJlZEhhdFRleHQsJnF1b3Q7UmVkIEhhdCBUZXh0JnF1b3Q7LE92ZXJwYXNzLCZxdW90O0hlbHZldGljYSBOZXVlJnF1b3Q7LEFyaWFsLHNhbnMtc2VyaWYiIGZvbnQtd2VpZ2h0PSI3MDAiPlNlcnZpY2UgbmV0d29yazwvdGV4dD48Zz48dGV4dCB0cmFuc2Zvcm09InRyYW5zbGF0ZSg2OTMuNTYyIDM0Ni44ODEpIiBmb250LXNpemU9IjEwIiBmaWxsPSIjZjNmM2YzIiBmb250LWZhbWlseT0iUmVkSGF0VGV4dCwmcXVvdDtSZWQgSGF0IFRleHQmcXVvdDssT3ZlcnBhc3MsJnF1b3Q7SGVsdmV0aWNhIE5ldWUmcXVvdDssQXJpYWwsc2Fucy1zZXJpZiI+MTMwX0FNUV8wMTIxPC90ZXh0PjxwYXRoIGZpbGw9Im5vbmUiIGQ9Ik0tLjI1IDMyMy44NjRoNzYwdjQwaC03NjB6Ii8+PC9nPjwvc3ZnPg==" alt="Overview of a service network">
</div>
</div>
<div class="paragraph">
<p>For example, you can deploy your frontend in a public OpenShift cluster and deploy your backend in a private OpenShift cluster, then connect them into a service network.</p>
</div>
<div class="paragraph">
<p>A service network provides the following features:</p>
</div>
<div class="ulist">
<ul>
<li>
<p>Security by default. All inter-site traffic is protected by mutual TLS using a private, dedicated certificate authority (CA).</p>
</li>
<li>
<p>Easy connections between OpenShift clusters, even private clusters.</p>
</li>
<li>
<p>A service network supports existing TCP-based applications without requiring modification.</p>
</li>
<li>
<p>Monitor your application traffic spread across multiple OpenShift clusters using the service network console.</p>
</li>
</ul>
</div>
<div class="paragraph">
<p>You deploy and manage a service network using the <code>skupper</code> CLI.</p>
</div>
</div>
</div>
<div class="sect1">
<h2 id="installing-cli">2. Installing the <code>skupper</code> CLI</h2>
<div class="sectionbody">
<div class="paragraph system:abstract">
<p>Installing the <code>skupper</code> command-line interface (CLI) provides a simple method to get started with Skupper.</p>
</div>
<div class="olist arabic">
<div class="title">Procedure</div>
<ol class="arabic">
<li>
<p>Verify the installation.</p>
<div class="listingblock">
<div class="content">
<pre>$ skupper version
client version 0.5.2</pre>
</div>
</div>
</li>
</ol>
</div>
</div>
</div>
<div class="sect1">
<h2 id="configuring-consoles">3. Configuring terminal sessions</h2>
<div class="sectionbody">
<div class="paragraph system:abstract">
<p>This procedure describes how to configure your terminal sessions to use configurations to avoid problems as you configure Skupper on different clusters.</p>
</div>
<div class="paragraph">
<p>The following table shows how you might set up your terminal sessions.</p>
</div>
<table class="tableblock frame-all grid-all stretch">
<caption class="title">Table 1. Terminal sessions</caption>
<colgroup>
<col style="width: 50%;">
<col style="width: 50%;">
</colgroup>
<thead>
<tr>
<th class="tableblock halign-left valign-top">west terminal session</th>
<th class="tableblock halign-left valign-top">east terminal session</th>
</tr>
</thead>
<tbody>
<tr>
<td class="tableblock halign-left valign-top"><div class="content"><div class="listingblock">
<div class="content">
<pre class="highlight"><code class="language-bash" data-lang="bash"> $ oc project
 west</code></pre>
</div>
</div></div></td>
<td class="tableblock halign-left valign-top"><div class="content"><div class="listingblock">
<div class="content">
<pre class="highlight"><code class="language-bash" data-lang="bash"> $ oc project
 east</code></pre>
</div>
</div></div></td>
</tr>
</tbody>
</table>
<div class="ulist">
<div class="title">Prerequisites</div>
<ul>
<li>
<p>The OpenShift CLI is installed.
See the <a href="https://access.redhat.com/documentation/en-us/openshift_container_platform/4.6/html-single/cli_tools/index#installing-openshift-cli">OpenShift CLI</a> documentation for more instructions on how to install <code>oc</code>.</p>
</li>
</ul>
</div>
<div class="admonitionblock note">
<table>
<tr>
<td class="icon">
<div class="title">Note</div>
</td>
<td class="content">
In OpenShift 4.6 and later, you can use the web terminal to perform the following procedure, as described in the <a href="https://docs.openshift.com/container-platform/4.5/web_console/odc-about-web-terminal.html">web terminal</a> documentation.
</td>
</tr>
</table>
</div>
<div class="olist arabic">
<div class="title">Procedure</div>
<ol class="arabic">
<li>
<p>Start a terminal session to work on the <code>west</code> namespace and set the <code>KUBECONFIG</code> environment variable:</p>
<div class="paragraph">
<p><pre>$ <a href=didact://?commandId=vscode.didact.sendNamedTerminalAString&text=west$$export%20KUBECONFIG%3D%24HOME%2F.kube%2Fconfig-west style="text-decoration:none">export KUBECONFIG=$HOME/.kube/config-west</a></pre></p>
</div>
<div class="paragraph">
<p>This session is referred to later as the <em>west</em> terminal session.</p>
</div>
</li>
</ol>
</div>
<div class="paragraph">
<p><span class="icon">[cogs]</span> <a href="didact://?commandId=workbench.action.terminal.split">Split terminal</a></p>
</div>
<div class="paragraph">
<p><span class="icon">[cogs]</span> <a href="didact://?commandId=workbench.action.terminal.renameWithArg&amp;json={&#34;name&#34;:&#34;east&#34;}">Rename terminal</a></p>
</div>
<div class="olist arabic">
<ol class="arabic" start="2">
<li>
<p>Start a terminal session to work on the <code>east</code> namespace and set the <code>KUBECONFIG</code> environment variable:</p>
<div class="paragraph">
<p><pre>$ <a href=didact://?commandId=vscode.didact.sendNamedTerminalAString&text=east$$export%20KUBECONFIG%3D%24HOME%2F.kube%2Fconfig-east style="text-decoration:none">export KUBECONFIG=$HOME/.kube/config-east</a></pre></p>
</div>
<div class="paragraph">
<p>This session is referred to later as the <em>east</em> terminal session.</p>
</div>
</li>
<li>
<p>In each terminal session, log into the OpenShift cluster, for example:</p>
<div class="listingblock">
<div class="content">
<pre> $ oc login</pre>
</div>
</div>
</li>
</ol>
</div>
</div>
</div>
<div class="sect1">
<h2 id="installing-skupper">4. Installing the service network router in both clusters</h2>
<div class="sectionbody">
<div class="olist arabic">
<ol class="arabic">
<li>
<p>In the west terminal session:</p>
<div class="olist loweralpha">
<ol class="loweralpha" type="a">
<li>
<p>Create the <code>west</code> project (namespace):</p>
<div class="paragraph">
<p><pre>$ <a href=didact://?commandId=vscode.didact.sendNamedTerminalAString&text=west$$oc%20new-project%20west%20 style="text-decoration:none">oc new-project west </a></pre></p>
</div>
</li>
<li>
<p>Create the service network router:</p>
<div class="paragraph">
<p><pre>$ <a href=didact://?commandId=vscode.didact.sendNamedTerminalAString&text=west$$skupper%20init style="text-decoration:none">skupper init</a></pre></p>
</div>
</li>
<li>
<p>Check the site status:</p>
<div class="openblock">
<div class="content">
<div class="paragraph">
<p><pre>$ <a href=didact://?commandId=vscode.didact.sendNamedTerminalAString&text=west$$skupper%20status style="text-decoration:none">skupper status</a></pre></p>
</div>
<div class="paragraph">
<p>The output should be similar to the following:</p>
</div>
<div class="listingblock">
<div class="content">
<pre>Skupper enabled for namespace 'west'. It is not connected to any other sites.</pre>
</div>
</div>
</div>
</div>
</li>
</ol>
</div>
</li>
<li>
<p>In the east terminal session:</p>
<div class="olist loweralpha">
<ol class="loweralpha" type="a">
<li>
<p>Create the <code>east</code> project (namespace):</p>
<div class="paragraph">
<p><pre>$ <a href=didact://?commandId=vscode.didact.sendNamedTerminalAString&text=east$$oc%20new-project%20east%20 style="text-decoration:none">oc new-project east </a></pre></p>
</div>
</li>
<li>
<p>Create the service network router:</p>
<div class="paragraph">
<p><pre>$ <a href=didact://?commandId=vscode.didact.sendNamedTerminalAString&text=east$$skupper%20init style="text-decoration:none">skupper init</a></pre></p>
</div>
</li>
<li>
<p>Check the site status:</p>
<div class="openblock">
<div class="content">
<div class="paragraph">
<p><pre>$ <a href=didact://?commandId=vscode.didact.sendNamedTerminalAString&text=east$$skupper%20status style="text-decoration:none">skupper status</a></pre></p>
</div>
<div class="paragraph">
<p>The output should be similar to the following:</p>
</div>
<div class="listingblock">
<div class="content">
<pre>Skupper enabled for namespace 'east'. It is not connected to any other sites.</pre>
</div>
</div>
</div>
</div>
</li>
</ol>
</div>
</li>
</ol>
</div>
</div>
</div>
<div class="sect1">
<h2 id="connecting-namespaces">5. Connecting namespaces to create a service network</h2>
<div class="sectionbody">
<div class="paragraph">
<p>With the service network routers installed, you can connect them together securely and allow service sharing across the service network.</p>
</div>
<div class="olist arabic">
<div class="title">Procedure</div>
<ol class="arabic">
<li>
<p>In the west terminal session, create a connection token to allow connection to the west namespace:</p>
<div class="paragraph">
<p><pre>$ <a href=didact://?commandId=vscode.didact.sendNamedTerminalAString&text=west$$skupper%20token%20create%20%24HOME%2Fsecret.yaml style="text-decoration:none">skupper token create $HOME/secret.yaml</a></pre></p>
</div>
<div class="paragraph">
<p>This command creates the <code>secret.yaml</code> file in your home directory, which you can use to create the secure connection.</p>
</div>
</li>
<li>
<p>In the east terminal session, use the token to create a connection to the west namespace:</p>
<div class="paragraph">
<p><pre>$ <a href=didact://?commandId=vscode.didact.sendNamedTerminalAString&text=east$$skupper%20link%20create%20%24HOME%2Fsecret.yaml style="text-decoration:none">skupper link create $HOME/secret.yaml</a></pre></p>
</div>
</li>
<li>
<p>Check the site status from the west terminal session:</p>
<div class="openblock">
<div class="content">
<div class="paragraph">
<p><pre>$ <a href=didact://?commandId=vscode.didact.sendNamedTerminalAString&text=west$$skupper%20status style="text-decoration:none">skupper status</a></pre></p>
</div>
<div class="paragraph">
<p>The output should be similar to the following:</p>
</div>
<div class="listingblock">
<div class="content">
<pre>Skupper is enabled for namespace "west" in interior mode. It is connected to 1 other site. It has no exposed services.
The site console url is:  https://&lt;skupper-url&gt;
The credentials for internal console-auth mode are held in secret: 'skupper-console-users'</pre>
</div>
</div>
</div>
</div>
</li>
</ol>
</div>
</div>
</div>
<div class="sect1">
<h2 id="frontend">6. Creating the frontend service</h2>
<div class="sectionbody">
<div class="paragraph">
<p>The frontend service is a simple Python application that displays a message from the backend application.</p>
</div>
<div class="paragraph">
<div class="title">Procedure</div>
<p>Perform all tasks in the west terminal session:</p>
</div>
<div class="olist arabic">
<ol class="arabic">
<li>
<p>Deploy the frontend service:</p>
<div class="paragraph">
<p><pre>$ <a href=didact://?commandId=vscode.didact.sendNamedTerminalAString&text=west$$oc%20create%20deployment%20hello-world-frontend%20--image%20quay.io%2Fskupper%2Fhello-world-frontend style="text-decoration:none">oc create deployment hello-world-frontend --image quay.io/skupper/hello-world-frontend</a></pre></p>
</div>
</li>
<li>
<p>Expose the frontend deployment as a cluster service:</p>
<div class="paragraph">
<p><pre>$ <a href=didact://?commandId=vscode.didact.sendNamedTerminalAString&text=west$$oc%20expose%20deployment%20hello-world-frontend%20--port%208080%20--type%20LoadBalancer style="text-decoration:none">oc expose deployment hello-world-frontend --port 8080 --type LoadBalancer</a></pre></p>
</div>
</li>
<li>
<p>Create a route for the frontend:</p>
<div class="paragraph">
<p><pre>$ <a href=didact://?commandId=vscode.didact.sendNamedTerminalAString&text=west$$oc%20expose%20svc%2Fhello-world-frontend style="text-decoration:none">oc expose svc/hello-world-frontend</a></pre></p>
</div>
</li>
<li>
<p>Check the frontend route:</p>
<div class="olist loweralpha">
<ol class="loweralpha" type="a">
<li>
<p>Get the route details:</p>
<div class="openblock">
<div class="content">
<div class="paragraph">
<p><pre>$ <a href=didact://?commandId=vscode.didact.sendNamedTerminalAString&text=west$$%20oc%20get%20routes style="text-decoration:none"> oc get routes</a></pre></p>
</div>
<div class="paragraph">
<p>The output should be similar to the following:</p>
</div>
<div class="listingblock">
<div class="content">
<pre>NAME                   HOST/PORT
hello-world-frontend   &lt;frontend-url&gt;</pre>
</div>
</div>
</div>
</div>
</li>
<li>
<p>Navigate to the <code>&lt;frontend-url&gt;</code> value in your browser, you see a message similar to the following because the frontend cannot communicate with the backend yet:</p>
<div class="listingblock">
<div class="content">
<pre>Trouble! HTTPConnectionPool(host='hello-world-backend', port=8080): Max retries exceeded with url: /api/hello (Caused by NewConnectionError('&lt;urllib3.connection.HTTPConnection object at 0x7fbfcdf0d1d0&gt;: Failed to establish a new connection: [Errno -2] Name or service not known'))</pre>
</div>
</div>
<div class="paragraph">
<p>To resolve this situation, you must create the backend service and make it available on the service network.</p>
</div>
</li>
</ol>
</div>
</li>
</ol>
</div>
</div>
</div>
<div class="sect1">
<h2 id="backend">7. Creating the backend service and making it available on the service network</h2>
<div class="sectionbody">
<div class="paragraph">
<p>The backend service runs in the <code>east</code> namespace and is not available on the service network by default.
You use the <code>skupper</code> command to expose the service to all namespaces on the service network.
The backend app is a simple Python application that passes a message to the frontend application.</p>
</div>
<div class="olist arabic">
<div class="title">Procedure</div>
<ol class="arabic">
<li>
<p>Deploy the backend service in the east terminal session:</p>
<div class="paragraph">
<p><pre>$ <a href=didact://?commandId=vscode.didact.sendNamedTerminalAString&text=east$$oc%20create%20deployment%20hello-world-backend%20--image%20quay.io%2Fskupper%2Fhello-world-backend style="text-decoration:none">oc create deployment hello-world-backend --image quay.io/skupper/hello-world-backend</a></pre></p>
</div>
</li>
<li>
<p>Expose the backend service on the service network from the east terminal session:</p>
<div class="paragraph">
<p><pre>$ <a href=didact://?commandId=vscode.didact.sendNamedTerminalAString&text=east$$skupper%20expose%20deployment%20hello-world-backend%20--port%208080%20--protocol%20tcp style="text-decoration:none">skupper expose deployment hello-world-backend --port 8080 --protocol tcp</a></pre></p>
</div>
</li>
<li>
<p>Check the site status from the west terminal session:</p>
<div class="openblock">
<div class="content">
<div class="paragraph">
<p><pre>$ <a href=didact://?commandId=vscode.didact.sendNamedTerminalAString&text=west$$skupper%20status style="text-decoration:none">skupper status</a></pre></p>
</div>
<div class="paragraph">
<p>The output should be similar to the following:</p>
</div>
<div class="listingblock">
<div class="content">
<pre>Skupper is enabled for namespace "west" in interior mode. It is connected to 1 other site. It has 1 exposed service.</pre>
</div>
</div>
<div class="paragraph">
<p>The service is exposed from the <code>east</code> namespace.</p>
</div>
</div>
</div>
</li>
<li>
<p>Check the frontend route in the west terminal session:</p>
<div class="olist loweralpha">
<ol class="loweralpha" type="a">
<li>
<p>Get the route details:</p>
<div class="openblock">
<div class="content">
<div class="paragraph">
<p><pre>$ <a href=didact://?commandId=vscode.didact.sendNamedTerminalAString&text=west$$%20oc%20get%20routes style="text-decoration:none"> oc get routes</a></pre></p>
</div>
<div class="paragraph">
<p>The output should be similar to the following:</p>
</div>
<div class="listingblock">
<div class="content">
<pre>NAME                   HOST/PORT
hello-world-frontend   &lt;frontend-url&gt;</pre>
</div>
</div>
</div>
</div>
</li>
<li>
<p>Navigate to the <code>&lt;frontend-url&gt;</code> value in your browser, you see a message similar to the following:</p>
<div class="listingblock">
<div class="content">
<pre>I am the frontend.  The backend says 'Hello from hello-world-backend-78cd4d7d8c-plrr9 (1)'.</pre>
</div>
</div>
</li>
</ol>
</div>
</li>
</ol>
</div>
<div class="paragraph">
<p>This shows how the frontend calls the backend service over the service network from a different OpenShift cluster.</p>
</div>
<div class="ulist">
<div class="title">Additional resources</div>
<ul>
<li>
<p><a href="{linkroot}console/index.html">Monitoring Skupper sites using the console</a></p>
</li>
<li>
<p><a href="{linkroot}cli/index.html">Configuring Skupper sites using the CLI</a></p>
</li>
</ul>
</div>
</div>
</div>
<div class="sect1">
<h2 id="tearing-down">8. Tearing down the service network</h2>
<div class="sectionbody">
<div class="paragraph">
<p>This procedure describes how to remove the service network you created.</p>
</div>
<div class="olist arabic">
<ol class="arabic">
<li>
<p>Delete the <code>west</code> namespace from the west terminal session:</p>
<div class="paragraph">
<p><pre>$ <a href=didact://?commandId=vscode.didact.sendNamedTerminalAString&text=west$$%20oc%20delete%20project%20west style="text-decoration:none"> oc delete project west</a></pre></p>
</div>
</li>
<li>
<p>Delete the <code>east</code> namespace from the east terminal session:</p>
<div class="paragraph">
<p><pre>$ <a href=didact://?commandId=vscode.didact.sendNamedTerminalAString&text=east$$%20oc%20delete%20project%20east style="text-decoration:none"> oc delete project east</a></pre></p>
</div>
</li>
</ol>
</div>
</div>
</div>
</div>
<div id="footer">
<div id="footer-text">
Last updated 2021-05-23 20:01:06 +0100
</div>
</div>
</body>
</html>