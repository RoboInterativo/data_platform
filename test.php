<?php
$link = mysqli_connect("localhost", "test", "secret","employees");

if ($link == false){
    print("Ошибка: Невозможно подключиться к MySQL " . mysqli_connect_error());
}
else {
    print("Соединение установлено успешно");
}

/* ysql> select * from departments;
+---------+--------------------+
| dept_no | dept_name
*/
// make foo the current db

/*
$db_selected = mysqli_select_db('employees', $link);
if (!$db_selected) {
    die ('Can\'t use foo : ' . mysql_error());
}
*/



$sql = 'SELECT * FROM departments';

$result = mysqli_query($link, $sql);

while ($row = mysqli_fetch_array($result)) {
    print("Номер " . $row['dept_no'] . "; Название: . " . $row['dept_name'] . "<br>");
}

?>
