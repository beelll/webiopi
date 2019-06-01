<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>フォームから GET で送信されたデータを表示 - サンプル2 - PHP入門 - Webkaru</title>
</head>
<body>
get
<?php
  echo "<p>年齢：" . $_GET["age"] ."</p>";
  echo "<p>性別：" . $_GET["seibetsu"] ."</p>";
?>
</form>
</body>
</html>

