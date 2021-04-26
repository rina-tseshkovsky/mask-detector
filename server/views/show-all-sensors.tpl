<html>
  % include('head.tpl')
  <body>
    % include('header.tpl')
    
    <h2>Sensors Table</h2>

    <form action="/show-all-sensors" method="post">
       <input type="submit" name="bt1" value="Back" />
    </form> 

    <table id="mytable1" style="width:100%">
      <tr>
        <th>UUID</th>
        <th>PASSWPRD</th> 
      </tr>

        % for row in tpl_rows:
            <tr>
                <td>{{row[0]}}</td>
                <td>{{row[1]}}</td>
            </tr>
        % end 
    </table>
  </body>
</html>
