<html>
<head>

<style>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
</style>

</head>

<body>
<h2>Users Table</h2>
<table style="width:100%">
  <tr>
    <th>ID</th>
    <th>NAME</th> 
    <th>STATUS</th>
  </tr>

    % for row in tpl_rows:
        <tr>
            <td>{{row[0]}}</td>
            <td>{{row[1]}}</td>
            <td>{{row[2]}}</td>
        </tr>
    % end 
</table>

<form action="/show-all-users" method="post">
            <input type="submit" name="bt1" value="Back" />
</form> 

</body>
</html>
