<html>
  % include('head.tpl')
  <body>
    % include('header.tpl')

    <h2>Users Table</h2>
    
    <form action="/delete-user" method="post">
        <input type="submit" name="bt1" value="Back" />
      </form> 

    <table id="mytable" style="width:100%">
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
  </body>
</html>
