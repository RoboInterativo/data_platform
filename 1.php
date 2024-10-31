root@test:~# cd /var/www
root@test:/var/www# ls
html
root@test:/var/www# cd html/
root@test:/var/www/html# cat
index.nginx-debian.html  index.php                test.php
root@test:/var/www/html# cat index.php
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
  </head>
  <body>

    <?php
    $link = mysqli_connect("localhost", "test", "secret","employees");

    if ($link == false){
        print("Ошибка: Невозможно подключиться к MySQL " . mysqli_connect_error());
    }
    else {
        // print("Соединение установлено успешно");
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
?>
<nav class="navbar bg-primary navbar-expand-lg ">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">Navbar</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="#">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Link</a>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Dropdown
          </a>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#">Action</a></li>
            <li><a class="dropdown-item" href="#">Another action</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#">Something else here</a></li>
          </ul>
        </li>
        <li class="nav-item">
          <a class="nav-link disabled" aria-disabled="true">Disabled</a>
        </li>
      </ul>
      <form class="d-flex" role="search">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
        <button class="btn btn-outline-success" type="submit">Search</button>
      </form>
    </div>
  </div>
</nav>
<div class="container text-center">
  <div class="row">
    <div class="col-1">

    </div>
    <div class="col-10">


    <table class="table">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Название</th>

        </tr>
      </thead>
      <tbody>
<?php
        while ($row = mysqli_fetch_array($result)) {
            print("<tr>   <td>" . $row['dept_no']  . "</td>");
            print(" <td>" . $row['dept_name']  . "</td></tr>");


        }
?>


          <td>Mark</td>

        </tr>

      </tbody>
    </table>
  </div>
  <div class="col-1">

  </div>
</div>
</div>

<?php


    ?>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
  </body>
</html>
