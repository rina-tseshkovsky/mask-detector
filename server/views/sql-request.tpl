<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')

        <form action="/sql-request" method="post">
            SQL Query: <input name="sql-query" type="text" /><br>
            <input value="Run SQL Query" type="submit" />
            <input type="submit" name="bt1" value="Back" />

        </form>  

        <p>AVAIBLE TABLES</p>
        <table style="width:100%">
        <tr>
            <th>Name</th>
            <th>Features</th> 
        </tr>
        <tr>
            <td>raw_data</td>
            <td>id(TEXT), date(TEXT), status(TEXT)</td>
        </tr>
        <tr>
            <td>users</td>
            <td>id(TEXT), name(TEXT), password(TEXT)</td>
        </tr>
        <tr>
            <td>sensors</td>
            <td>UUID(TEXT), password(TEXT)</td>
        </tr>
        </table>


        <p>SQL SYNTAXSES</p>
        <table style="width:100%">
        <tr>
            <th>SQL Statement</th>
            <th>Description</th> 
        </tr>
        <tr>
            <td>SELECT * FROM XXXX</td>
            <td>selects all the records in the "XXXX" table</td>
        </tr>
        <tr>
            <td>SELECT * FROM XXXX WHERE YY=Z</td>
            <td>selects all the records in the "XXXX" table where feature "YY" equals"Z"</td>
        </tr>
        </table>

    </body>    
</html>