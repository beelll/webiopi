<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>フォームからPOSTで送信されたデータを表示 - サンプル2 - PHP入門 - Webkaru</title>
</head>
<body>
post
<?php
  echo $_POST["onamae"] ."さんのメールアドレスは". $_POST["mail"] ."です。";
?>
</form>
</body>
</html>

